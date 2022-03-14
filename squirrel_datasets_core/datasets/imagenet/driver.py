from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, List, Optional, Set, TYPE_CHECKING, Tuple

from squirrel.driver import FileDriver, IterDriver
from squirrel.iterstream import FilePathGenerator

from squirrel_datasets_core.io import load_image

if TYPE_CHECKING:
    from squirrel.iterstream import Composable


class RawImageNetDriver(IterDriver):
    name = "raw_imagenet"

    def __init__(
        self,
        url: str,
        cls_mapping_url: Optional[str] = None,
        loc_train_mapping_url: Optional[str] = None,
        loc_val_mapping_url: Optional[str] = None,
        cls_val_mapping_url: Optional[str] = None,
        val_blacklist_url: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Init RawImageNetDriver.

        Args:
            url (str): Path to the root directory of the dataset.
            cls_mapping_url (str, optional): Path to the text file that contains the class mapping. Each line of this
                file should be formatted as "{class_id} {class_idx} {class_name}". If not provided, samples will not
                have label information. Defaults to None.
            loc_train_mapping_url (str, optional): Path to the text file that contains the bounding boxes for the train
                set. If not provided, train samples will not have bounding box information. Defaults to None.
            loc_val_mapping_url (str, optional): Path to the text file that contains the bounding boxes for the
                validation set. If not provided, train samples will not have bounding box information. Defaults to None.
            cls_val_mapping_url (str, optional): Path to the text file that contains the groundtruth class indices for
                the validation set. Line i (0-indexed) of this file corresponds to the i-th validation sample. If not
                provided, validation samples will not have class label information. Defaults to None.
            val_blacklist_url (str, optional): Path to the text file that contains the blacklisted validation samples
                Each line of this file should contain a sample index. If not provided, validation samples will not be
                filtered. Defaults to None.
        """
        self.path = url
        self.cls_mapping_path = cls_mapping_url
        self.loc_train_mapping_path = loc_train_mapping_url
        self.loc_val_mapping_path = loc_val_mapping_url
        self.cls_val_mapping_path = cls_val_mapping_url
        self.val_blacklist_path = val_blacklist_url

    @staticmethod
    def parse_gt_train(
        samples: Iterable[Dict[str, Any]], cls_map: Dict[str, Tuple[int, str]]
    ) -> Generator[Dict[str, Any], None, None]:
        """Add class id, class index, and class label to training set samples.
        The class id, index, and label are stored under the keys "class_id", "classification_label",
        "classification_label_name", respectively.
        """
        for sample in samples:
            class_id = sample["url"].split("/")[-2]
            label, label_name = cls_map[class_id]
            sample["classification_label"] = label
            sample["classification_label_name"] = label_name
            sample["class_id"] = class_id
            yield sample

    @staticmethod
    def parse_bbox(
        samples: Iterable[Dict[str, Any]], cls_map: Dict[str, Tuple[int, str]], loc_map: Dict[str, List[Dict[str, Any]]]
    ) -> Generator[Dict[str, Any], None, None]:
        """Add bounding boxes to samples.
        The list of bounding box dictionaries are stored under the key "bboxes".
        """
        for sample in samples:
            # split after last / and before last .
            filename = Path(sample["url"]).stem
            sample["bboxes"] = []
            if filename in loc_map:
                a_bboxes = loc_map[filename]
                for bbox in a_bboxes:
                    label, label_name = cls_map[bbox["class_id"]]
                    bbox["classification_label"] = label
                    bbox["classification_label_name"] = label_name
                    sample["bboxes"].append(bbox)
            yield sample

    @staticmethod
    def parse_gt_val(
        samples: Iterable[Dict[str, Any]], clsidx_map: Dict[int, Tuple[str, str]], clsidx_val_list: List[int]
    ) -> Generator[Dict[str, Any], None, None]:
        """Add class id, class index, and class label to validation set samples.
        The class id, index, and label are stored under the keys "class_id", "classification_label",
        "classification_label_name", respectively.
        """
        for sample in samples:
            # split after last / and before last .
            filename = Path(sample["url"]).stem
            # extract label id from filename
            a_id = int(filename.split("_")[-1]) - 1
            label = clsidx_val_list[a_id]
            class_id, label_name = clsidx_map[label]
            sample["class_id"] = class_id
            sample["classification_label_name"] = label_name
            sample["classification_label"] = label
            yield sample

    @staticmethod
    def filter_val_samples_by_idx(
        samples: Iterable[Dict[str, Any]], idx_blacklist: Set[int]
    ) -> Generator[Dict[str, Any], None, None]:
        """Yield samples that are not in the blacklist."""
        for sample in samples:
            a_id = int(Path(sample["url"]).stem.split("_")[-1]) - 1
            if a_id not in idx_blacklist:
                yield sample

    def get_loc_mapper(self, url: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get dict that maps from an imagenet filename to a list of bbox dicts."""
        loc_map = dict()
        with FileDriver(url).open(mode="rt") as f:
            f.readline()  # skip the header
            for row in f.readlines():
                file_name, bboxes_raw = row.strip().split(",")
                bboxes = []
                for bbox_raw in bboxes_raw.split("n")[1:]:
                    class_id, *x = bbox_raw.strip().split(" ")
                    assert len(x) == 4
                    class_id = f"n{class_id}"
                    bboxes.append({"class_id": class_id, "loc": [int(ax) for ax in x]})
                loc_map[file_name] = bboxes
        return loc_map

    def get_val_clsidx_list(self) -> List[int]:
        """Get list of class indices for validation samples."""
        with FileDriver(self.cls_val_mapping_path).open(mode="rt") as f:
            val_clsidx = [int(row.strip()) - 1 for row in f.readlines()]
        return val_clsidx

    def get_val_blacklist_indices(self) -> Set[int]:
        """Get a set of blacklisted validation sample indices."""
        with FileDriver(self.val_blacklist_path).open(mode="rt") as f:
            blacklist_idx = {int(row.strip()) - 1 for row in f.readlines()}
        return blacklist_idx

    def get_id_to_idx_and_name_mapper(self) -> Dict[str, Tuple[int, str]]:
        """Get dict that maps from an imagenet foldername (i.e. class id) to a (class index, class name) tuple.
        WARNING: Imagenet idx start from 1. Here we start from 0.
        """
        gt_map = dict()
        with FileDriver(self.cls_mapping_path).open(mode="rt") as f:
            for row in f.readlines():
                row = row.strip()
                class_id, class_idx, class_name = row.split(" ")
                gt_map[class_id] = (int(class_idx) - 1, class_name)
        return gt_map

    def get_idx_to_id_and_name_mapper(self) -> Dict[int, Tuple[str, str]]:
        """Get dict that maps from an imagenet class index to a (class id, class name) tuple.
        WARNING: Imagenet idx start from 1. Here we start from 0.
        """
        cls_map = self.get_id_to_idx_and_name_mapper()
        return {class_idx: (class_id, class_name) for class_id, (class_idx, class_name) in cls_map.items()}

    @staticmethod
    def load_sample(sample: Dict[str, Any]) -> Dict[str, Any]:
        """Load sample from dict containing url to sample."""
        sample["image"] = load_image(sample["url"])
        return sample

    def get_iter(
        self,
        split: str,
        hooks: Optional[List[Iterable]] = None,
        parse: bool = True,
        shuffle: bool = True,
        buffer_size: int = 100_000,
        **kwargs,
    ) -> Composable:
        """Create iterstream for the given split.

        Args:
            split (str): Split name. Must be one of ("train", "val", "test").
            hooks (List[Iterable], optional): Hooks to apply. Hooks are applied before parsing the samples. Defaults to
                None.
            parse (bool, optional): Whether to load the image into sample dictionary. Image will be stored under the
                key "image". Defaults to True.
            shuffle (bool, optional): Whether to shuffle the samples. Defaults to True.
            buffer_size (int, optional): Buffer size used for shuffling. Defaults to 100_000.

        Returns:
            Composable: Composable containing the samples.
        """
        assert split in ["train", "val", "test"]
        url = os.path.join(self.path, split)
        if hooks is None:
            hooks = []

        it = FilePathGenerator(url, nested=True)

        if shuffle:
            it = it.shuffle(size=buffer_size, initial=buffer_size)

        it = it.map(lambda x: {"url": x})
        if self.cls_mapping_path is not None and split != "test":
            cls_map = self.get_id_to_idx_and_name_mapper()

            if split == "train":
                it = it.to(RawImageNetDriver.parse_gt_train, cls_map=cls_map)

                if self.loc_train_mapping_path is not None:
                    loc_map = self.get_loc_mapper(self.loc_train_mapping_path)
                    it = it.to(RawImageNetDriver.parse_bbox, cls_map=cls_map, loc_map=loc_map)

            elif split == "val":
                if self.val_blacklist_path is not None:
                    val_blacklist = self.get_val_blacklist_indices()
                    it = it.to(RawImageNetDriver.filter_val_samples_by_idx, idx_blacklist=val_blacklist)

                if self.cls_val_mapping_path is not None:
                    val_clsidx_map = self.get_val_clsidx_list()
                    clsidx_map = self.get_idx_to_id_and_name_mapper()
                    it = it.to(RawImageNetDriver.parse_gt_val, clsidx_map=clsidx_map, clsidx_val_list=val_clsidx_map)

                if self.loc_val_mapping_path is not None:
                    loc_map = self.get_loc_mapper(self.loc_val_mapping_path)
                    it = it.to(RawImageNetDriver.parse_bbox, cls_map=cls_map, loc_map=loc_map)

        for h in hooks:
            it = it.to(h)

        if not parse:
            return it
        return it.map(RawImageNetDriver.load_sample)
