from __future__ import annotations

import os
from itertools import chain
from typing import Callable, Dict, List, Optional, TYPE_CHECKING

from squirrel.driver import IterDriver
from squirrel.iterstream import FilePathGenerator, IterableSource

from squirrel_datasets_core.io import load_image

if TYPE_CHECKING:
    from squirrel.iterstream import Composable


class RawKaggleCastingQualityDriver(IterDriver):
    name = "raw_kaggle_casting_quality"

    def __init__(self, url: str, **kwargs) -> None:
        """Initializes the RawKaggleCastingQualityDriver.

        Args:
            url (str): Path to the directory containing the dataset.
            **kwargs: Other keyword arguments passes to super class initializer.
        """
        super().__init__(**kwargs)
        self.url = url

    @staticmethod
    def load_sample(sample: Dict) -> Dict:
        """Load sample from dict containing url to sample."""
        sample["image"] = load_image(sample["url"])
        return sample

    def get_iter(self, split: str, hooks: Optional[List[Callable]] = None, parse: bool = True, **kwargs) -> Composable:
        """Create iterstream based on dataset split (train, test). Applies hooks before loading samples."""
        assert split in ["train", "test"]  # kaggle casting quality datasets only have train and test split.
        if hooks is None:
            hooks = []

        samples_def = FilePathGenerator(os.path.join(self.url, split, "def_front")).map(
            lambda x: {"url": x, "label": 0}
        )
        samples_ok = FilePathGenerator(os.path.join(self.url, split, "ok_front")).map(lambda x: {"url": x, "label": 1})
        it = IterableSource(chain(samples_ok, samples_def)).shuffle(size=1_000_000, initial=1_000_000)
        for h in hooks:
            it = it.to(h)
        if not parse:
            return it
        return it.map(RawKaggleCastingQualityDriver.load_sample)
