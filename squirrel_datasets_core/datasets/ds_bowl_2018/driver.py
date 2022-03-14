"""Driver that can parse the Data Science Bowl 2018 dataset."""
from __future__ import annotations

import os
from functools import partial
from typing import Callable, Dict, List, Optional, TYPE_CHECKING

from squirrel.driver import IterDriver
from squirrel.iterstream import FilePathGenerator, IterableSource

from squirrel_datasets_core.io import load_image

if TYPE_CHECKING:
    from squirrel.iterstream import Composable


class DataScienceBowl2018Driver(IterDriver):
    """Driver that can iterate over the samples of the `2018 Data Science Bowl
    <https://www.kaggle.com/c/data-science-bowl-2018>`_ dataset.

    The driver expects the image and label formats, directory structure and the data split used in the competition.
    Drivers allows three dataset splits: stage1_train, stage1_test, stage2_test_final.
    """

    name = "ds_bowl_18"

    def __init__(self, url: str, **kwargs) -> None:
        """Initializes the DataScienceBowl2018Driver.

        Args:
            url (str): Path to the directory containing the dataset.
            **kwargs: Other keyword arguments passes to super class initializer.
        """
        super().__init__(**kwargs)
        self.url = url

    @staticmethod
    def load_sample(sample: Dict, parse_image: bool = True, parse_mask: bool = True) -> Dict:
        """Parse and load image and/or groundtruth mask into the sample dictionary.
        Image and masks are stored under the keys "image" and "masks", respectively.
        """
        # labels are list of arrays (masks) and list of bbox coordinates
        sample_url = sample["sample_url"]
        if parse_image:
            stem = os.path.splitext(os.path.basename(sample_url))[0]
            url = os.path.join(sample_url, "images", f"{stem}.png")
            sample["image"] = load_image(url)

        if sample["split"] == "stage1_train" and parse_mask:
            gen = FilePathGenerator(os.path.join(sample_url, "masks"))
            sample["masks"] = [load_image(url).astype("bool") for url in gen]

        return sample

    def get_iter(
        self,
        split: str,
        hooks: Optional[List[Callable]] = None,
        parse_image: bool = True,
        parse_mask: bool = True,
        shuffle_size: int = 800,
        shuffle_initial: int = 800,
    ) -> Composable:
        """Create iterstream for the given split.

        Args:
            split (str): Split name. Must be one of ("stage1_train", "stage1_test", "stage2_test_final").
            hooks (List[Iterable], optional): Hooks to apply. Hooks are applied before parsing the samples. Defaults to
                None.
            parse_image (bool, optional): Whether to load the image into sample dictionary. Image will be stored under
                the key "image". Defaults to True.
            parse_mask (bool, optional): Whether to load the instance masks into sample dictionary. Masks will be
                stored under the key "masks". Only in effect for split="stage1_train". Defaults to True.
            shuffle_size (int, optional): Buffer size used for shuffling. Defaults to 800.
            shuffle_initial (int, optional): Initial buffer size before starting to iterate. Defaults to 800.

        Returns:
            Composable: Composable containing the samples.
        """
        assert split in {"stage1_train", "stage1_test", "stage2_test_final"}
        if hooks is None:
            hooks = []

        gen = FilePathGenerator(os.path.join(self.url, split)).map(lambda x: dict(sample_url=x, split=split))
        it = IterableSource(gen).shuffle(size=shuffle_size, initial=shuffle_initial)

        for h in hooks:
            it = it.to(h)

        load = partial(self.load_sample, parse_image=parse_image, parse_mask=parse_mask)
        return it.map(load)
