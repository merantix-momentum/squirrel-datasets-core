"""Driver that can parse the Cambridge-driving Labeled Video Database (CamVid) dataset."""
from __future__ import annotations

import os
from functools import partial
from typing import Callable, Dict, List, Optional, TYPE_CHECKING

from squirrel.driver import IterDriver
from squirrel.iterstream import FilePathGenerator, IterableSource

from squirrel_datasets_core.io.io import load_image

if TYPE_CHECKING:
    from squirrel.iterstream import Composable

_CLASSES = [
    "sky",
    "building",
    "pole",
    "road",
    "pavement",
    "tree",
    "sign_symbol",
    "fence",
    "car",
    "pedestrian",
    "bicyclist",
    "unlabelled",
]
CAMVID_NAME_TO_LABEL_ID = dict(zip(_CLASSES, range(12)))
CAMVID_LABEL_ID_TO_NAME = {idx: cls for cls, idx in CAMVID_NAME_TO_LABEL_ID.items()}


class CamvidDriver(IterDriver):
    """Driver that can iterate over the samples of the `Cambridge-driving Labeled Video Database (CamVid)
    <http://web4.cs.ucl.ac.uk/staff/g.brostow/MotionSegRecData/>`_ dataset.

    The driver expects the image and label formats, directory structure and the data split used by Alex Kendall's
    `SegNet tutorial https://github.com/alexgkendall/SegNet-Tutorial/tree/master/CamVid>`_.

    The dataset contains the following classes: sky (0), building (1), pole (2), road (3), pavement (4), tree (5),
    sign/symbol (6), fence (7), car (8), pedestrian (9), bicyclist (10), unlabelled (11).
    """

    name = "camvid"

    def __init__(self, url: str, **kwargs) -> None:
        """Initializes the CamvidDriver.

        Args:
            url (str): Path to the directory containing the dataset.
            **kwargs: Other keyword arguments passes to super class initializer.
        """
        super().__init__(**kwargs)
        self.url = url

    @staticmethod
    def load_sample(sample: Dict, parse_image: bool = True, parse_label: bool = True) -> Dict:
        """Parse and load image and/or label into the sample dictionary.
        Image and label are stored under the keys "image" and "label", respectively.
        """
        if parse_image:
            sample["image"] = load_image(sample["image_url"])
        if parse_label:
            sample["label"] = load_image(sample["label_url"])
        return sample

    def get_iter(
        self,
        split: str,
        hooks: Optional[List[Callable]] = None,
        parse_image: bool = True,
        parse_label: bool = True,
        shuffle_size: int = 800,
        shuffle_initial: int = 800,
    ) -> Composable:
        """Create iterstream for the given split.

        Args:
            split (str): Split name. Must be one of ("train", "val", "test").
            hooks (List[Iterable], optional): Hooks to apply. Hooks are applied before parsing the samples. Defaults to
                None.
            parse_image (bool, optional): Whether to load the image into sample dictionary. Image will be stored under
                the key "image". Defaults to True.
            parse_label (bool, optional): Whether to load the label into sample dictionary. Label will be stored under
                the key "label". Defaults to True.
            shuffle_size (int, optional): Buffer size used for shuffling. Defaults to 800.
            shuffle_initial (int, optional): Initial buffer size before starting to iterate. Defaults to 800.

        Returns:
            Composable: Composable containing the samples.
        """
        assert split in {"train", "val", "test"}
        if hooks is None:
            hooks = []

        imgs_dir = os.path.join(self.url, split)
        labels_dir = os.path.join(self.url, f"{split}annot")
        gen = FilePathGenerator(imgs_dir).map(
            lambda x: dict(image_url=x, label_url=os.path.join(labels_dir, os.path.basename(x)), split=split)
        )
        it = IterableSource(gen).shuffle(size=shuffle_size, initial=shuffle_initial)

        for h in hooks:
            it = it.to(h)

        load = partial(self.load_sample, parse_image=parse_image, parse_label=parse_label)
        return it.map(load)
