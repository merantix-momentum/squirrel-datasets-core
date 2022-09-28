from __future__ import annotations

import io
import zipfile
from typing import TYPE_CHECKING, Any, Dict, List

import numpy as np
import requests

from squirrel.driver import IterDriver
from squirrel.iterstream import IterableSource

if TYPE_CHECKING:
    from squirrel.iterstream import Composable

URLS = {
    "helena": "https://competitions.codalab.org/my/datasets/download/09ada795-4052-4fac-957a-87f02229b201",
    "jannis": "http://www.causality.inf.ethz.ch/AutoML/jannis.zip",
}


class AutoML(IterDriver):

    name = "automl"

    def __init__(self, dataset_name: str, **kwargs) -> None:
        """Initialize the Helena dataset driver."""
        super().__init__(**kwargs)
        self.dataset_name = dataset_name
        self.zipfile = zipfile.ZipFile(io.BytesIO(requests.get(URLS[self.dataset_name]).content))

    def _get_train_split(self) -> List[Dict[str, Any]]:
        """Create train split"""
        records = []
        for feat, lbl in zip(
            self.zipfile.read(f"{self.dataset_name}_train.data").decode("utf-8").split("\n"),
            self.zipfile.read(f"{self.dataset_name}_train.solution").decode("utf-8").split("\n"),
        ):
            try:
                records.append(
                    {
                        "features": [float(x) for x in feat.strip().split(" ")],
                        "class": int(np.argwhere(np.asarray([int(x) for x in lbl.strip().split(" ")]) == 1)),
                    }
                )
            except ValueError:
                pass
        return records

    def _get_test_or_valid_split(self, split: str = "train") -> List[Dict[str, Any]]:
        """Create test or validation split"""
        records = []
        for feat in self.zipfile.read(f"{self.dataset_name}_{split}.data").decode("utf-8").split("\n"):
            try:
                records.append({"features": [float(x) for x in feat.strip().split(" ")], "class": None})
            except ValueError:
                pass
        return records

    def get_iter(self, split: str = "train", shuffle_item_buffer: int = 100, **kwargs) -> Composable:
        """
        Get an iterator over samples.

        Args:
            split (str): can be "train" or "test"
            shuffle_item_buffer (int): the size of the buffer used to shuffle samples after being fetched.
                Please note the memory footprint of samples
        """
        assert split in ["train", "test"]
        if split == "train":
            return IterableSource(self._get_train_split()).shuffle(size=shuffle_item_buffer)
        else:
            return IterableSource(self._get_test_or_valid_split(split)).shuffle(size=shuffle_item_buffer)
