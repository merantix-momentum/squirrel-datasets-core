from __future__ import annotations

import io
import zipfile
from typing import TYPE_CHECKING, Any, Dict, List

import numpy as np
import pandas as pd
import requests

from squirrel.driver import IterDriver
from squirrel.iterstream import IterableSource
from squirrel_datasets_core.datasets.utils import proportionate_sample_df


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

    def _get_train_test_split(self, split: str = "train") -> List[Dict[str, Any]]:
        """Create train split"""
        records = []
        for feat, lbl in zip(
            self.zipfile.read(f"{self.dataset_name}_train.data").decode("utf-8").split("\n"),
            self.zipfile.read(f"{self.dataset_name}_train.solution").decode("utf-8").split("\n"),
        ):
            try:
                record = {
                    f"features_{idx:03d}": val for idx, val in enumerate([float(x) for x in feat.strip().split(" ")])
                }
                record["class"] = int(np.argwhere(np.asarray([int(x) for x in lbl.strip().split(" ")]) == 1))
                records.append(record)
            except ValueError:
                pass

        df = pd.DataFrame.from_records(records)
        train_df, test_df = proportionate_sample_df(df, "class", 0.2, seed=42)
        if split == "train":
            return train_df.to_dict(orient="records")
        else:
            return test_df.to_dict(orient="records")

    def _get_test_or_valid_split(self, split: str = "orig_train") -> List[Dict[str, Any]]:
        """Create test or validation split"""
        split = split.split("_")[-1]
        records = []
        for feat in self.zipfile.read(f"{self.dataset_name}_{split}.data").decode("utf-8").split("\n"):
            try:
                record = {
                    f"features_{idx:03d}": val for idx, val in enumerate([float(x) for x in feat.strip().split(" ")])
                }
                record["class"] = None
                records.append(record)
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
        assert split in ["train", "test", "orig_test", "orig_valid"]
        if split == "train":
            return IterableSource(self._get_train_test_split(split="train")).shuffle(size=shuffle_item_buffer)
        elif split == "test":
            return IterableSource(self._get_train_test_split(split="test")).shuffle(size=shuffle_item_buffer)
        elif split in ["orig_train", "orig_valid"]:
            return IterableSource(self._get_test_or_valid_split(split)).shuffle(size=shuffle_item_buffer)
