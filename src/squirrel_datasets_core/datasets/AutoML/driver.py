from __future__ import annotations
from typing import TYPE_CHECKING
import io
import zipfile
import requests
import numpy as np

from squirrel.driver import IterDriver
from squirrel.iterstream import IterableSource

if TYPE_CHECKING:
    from squirrel.iterstream import Composable

URLS = {
    'helena': "https://competitions.codalab.org/my/datasets/download/09ada795-4052-4fac-957a-87f02229b201",
    'jannis': "http://www.causality.inf.ethz.ch/AutoML/jannis.zip"
}


class AutoML(IterDriver):

    name = "automl"

    def __init__(self, dataset_name: str, split:str = 'train', **kwargs) -> None:
        """Initialze the Helena dataset driver."""
        super().__init__(**kwargs)
        self.dataset_name=dataset_name
        self.split = split
        self.zipfile = zipfile.ZipFile(io.BytesIO(requests.get(URLS[self.dataset_name]).content))
        if self.split == 'train':
            self._data = self._get_train_split()
        else:
            self._data = self._get_test_or_valid_split()
    
    def _get_train_split(self):
        """Create train split"""
        records = []
        for feat, lbl in zip(self.zipfile.read(f'{self.dataset_name}_train.data').decode('utf-8').split('\n'),
                             self.zipfile.read(f'{self.dataset_name}_train.solution').decode('utf-8').split('\n')):
            try:
                records.append({
                    'features': [float(x) for x in feat.strip().split(" ")],
                    'class': int(np.argwhere(np.asarray([int(x) for x in lbl.strip().split(" ")]) == 1))
                })
            except ValueError as e:
                pass
        return records

    def _get_test_or_valid_split(self):
        """
        Create test or validation split
        """

        records = []
        for feat in self.zipfile.read(f'{self.dataset_name}_{self.split}.data').decode('utf-8').split('\n'):
            try:
                records.append({
                    'features': [float(x) for x in feat.strip().split(" ")],
                    'class': None
                })
            except ValueError as e:
                pass
        return records


    def get_iter(self, shuffle_item_buffer: int = 100, **kwargs) -> Composable:
        """
        Get an iterator over samples.

        Args:
            shuffle_item_buffer (int): the size of the buffer used to shuffle samples after being fetched. Please note the memory footprint of samples
        """
        return IterableSource(self._data).shuffle(size=shuffle_item_buffer)
