import os
from itertools import chain
from typing import Callable, Dict, List, Optional

from squirrel.driver import RecordIteratorDriver
from squirrel.iterstream import Composable, FilePathGenerator, IterableSource

from squirrel_datasets_core.driver.fsspec import TwoDImageFileDriver


class RawKaggleCastingQualityDriver(RecordIteratorDriver, TwoDImageFileDriver):
    name = "raw_kaggle_casting_quality"

    def __init__(self, url: str, **kwargs) -> None:
        """Init driver."""
        self.path = url

    @staticmethod
    def load_sample(sample: Dict) -> Dict:
        """Load sample from dict containing url to sample."""
        sample["image"] = RawKaggleCastingQualityDriver.load_image(sample["url"])
        return sample

    def get_iter(self, split: str, hooks: Optional[List[Callable]] = None, parse: bool = True, **kwargs) -> Composable:
        """Create iterstream based on dataset split (train, test). Applies hooks before loading samples."""
        assert split in ["train", "test"]  # kaggle casting quality datasets only have train and test split.
        if hooks is None:
            hooks = []

        samples_def = FilePathGenerator(os.path.join(self.path, split, "def_front")).map(
            lambda x: {"url": x, "label": 0}
        )
        samples_ok = FilePathGenerator(os.path.join(self.path, split, "ok_front")).map(lambda x: {"url": x, "label": 1})
        it = IterableSource(chain(samples_ok, samples_def)).shuffle(size=1_000_000, initial=1_000_000)
        for h in hooks:
            it = it.to(h)
        if not parse:
            return it
        return it.map(RawKaggleCastingQualityDriver.load_sample)
