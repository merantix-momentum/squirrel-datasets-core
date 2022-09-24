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

URL = "https://competitions.codalab.org/my/datasets/download/09ada795-4052-4fac-957a-87f02229b201"


class Helena(IterDriver):

    name = "helena"

    def __init__(self, split:str = 'train', **kwargs) -> None:
        """Initialze the Helena dataset driver."""
        super().__init__(**kwargs)
        self.zipfile = zipfile.ZipFile(io.BytesIO(requests.get(URL).content))
        self.split = split
        if self.split == 'train':
            self._data = self._get_train_split()
        else:
            self._data = self._get_test_or_valid_split(self.split)
    
    def _get_train_split(self):
        """Create train split"""
        records = []
        for feat, lbl in zip(self.zipfile.read('helena_train.data').decode('utf-8').split('\n'),
                             self.zipfile.read('helena_train.solution').decode('utf-8').split('\n')):
            try:
                records.append({
                    'features': [float(x) for x in feat.strip().split(" ")],
                    'class': int(np.argwhere(np.asarray([int(x) for x in lbl.strip().split(" ")]) == 1))
                })
            except ValueError as e:
                pass
        return records

    def _get_test_or_valid_split(self, split: str):
        """
        Create test or validation split
        
        Args:
            split (str): can be `valid` or `test`.
        """

        records = []
        for feat in self.zipfile.read(f'helena_{split}.data').decode('utf-8').split('\n'):
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
