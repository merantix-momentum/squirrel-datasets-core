from __future__ import annotations
from typing import TYPE_CHECKING
import os
import pandas as pd

from squirrel.driver import IterDriver
from squirrel.iterstream import IterableSource

if TYPE_CHECKING:
    from squirrel.iterstream import Composable

META_DATA = dict(
    filename="cal_housing.tgz",
    url="https://ndownloader.figshare.com/files/5976036",
)

_FEATURE_NAMES = [
    "longitude",
    "latitude",
    "housingMedianAge",
    "totalRooms",
    "totalBedrooms",
    "population",
    "households",
    "medianIncome",
    "medianHouseValue",
]


class CaliforniaHousing(IterDriver):

    name = "california_housing"

    def __init__(self, **kwargs) -> None:
        """Initialze the California housing dataset driver."""
        super().__init__(**kwargs)
        self._data = pd.read_csv(
            os.path.join(META_DATA["url"], META_DATA["filename"]),
            compression="gzip",
            index_col=None,
            header=None,
            names=_FEATURE_NAMES,
        ).to_dict(orient="records")

    def get_iter(self, shuffle_item_buffer: int = 100, **kwargs) -> Composable:
        """
        Get an iterator over samples.

        Args:
            shuffle_item_buffer (int): the size of the buffer used to shuffle samples after being fetched. Please note
                the memory footprint of samples
        """
        return IterableSource(self._data).shuffle(size=shuffle_item_buffer)
