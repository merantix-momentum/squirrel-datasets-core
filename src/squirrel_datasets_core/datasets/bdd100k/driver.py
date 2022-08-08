"""Driver that can parse the Berkeley Deep Drive Semantic Segmentation (BDD100K) dataset."""

from __future__ import annotations

import os
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Dict, List, Optional

from squirrel.driver import IterDriver
from squirrel.iterstream import FilePathGenerator, IterableSource

if TYPE_CHECKING:
    from squirrel.iterstream import Composable

from squirrel_datasets_core.io.io import load_image


class BDD100KDriver(IterDriver):
    """Driver that can iterate over the samples of the `Berkeley Deep Drive Semantic Segmentation (BDD100K) dataset
    <https://www.bdd100k.com/>`_ dataset.

    The dataset contains the following classes for semantic segmentation:
    0:  road
    1:  sidewalk
    2:  building
    3:  wall
    4:  fence
    5:  pole
    6:  traffic light
    7:  traffic sign
    8:  vegetation
    9:  terrain
    10: sky
    11: person
    12: rider
    13: car
    14: truck
    15: bus
    16: train
    17: motorcycle
    18: bicycle
    255: “unknown” category, and will not be evaluated
    """

    name = "bdd100k"

    def __init__(self, url: str, **kwargs) -> None:
        """Initializes the BDD100kDriver.

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
        if parse_label and "label_url" in sample:
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

        imgs_dir = os.path.join(self.url, "images/10k", split)

        if split == "test":
            gen = FilePathGenerator(imgs_dir).map(lambda x: dict(image_url=x, split=split))
        else:
            labels_dir = os.path.join(self.url, "labels/sem_seg/masks", split)
            gen = FilePathGenerator(imgs_dir).map(
                lambda x: dict(image_url=x, label_url=os.path.join(labels_dir, Path(x).stem + ".png"), split=split)
            )

        it = IterableSource(gen).shuffle(size=shuffle_size, initial=shuffle_initial)

        for h in hooks:
            it = it.to(h)

        load = partial(self.load_sample, parse_image=parse_image, parse_label=parse_label)
        return it.map(load)
