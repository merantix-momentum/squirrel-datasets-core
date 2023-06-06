from __future__ import annotations
from typing import TYPE_CHECKING
import os
import pandas as pd
import tarfile
import urllib.request
from pathlib import Path

from squirrel.driver import IterDriver
from squirrel.iterstream import IterableSource

if TYPE_CHECKING:
    from squirrel.iterstream import Composable

META_DATA = dict(
    filename="cal_housing.tgz",
    url="https://ndownloader.figshare.com/files/5976036"
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

        data_home = os.path.join(str(Path.home()), ".squirrel_data")
        if not os.path.exists(data_home):
            os.makedirs(data_home)

        local_filepath = os.path.join(data_home, "cal_housing.csv")
        if not os.path.exists(local_filepath):
            download_url = META_DATA["url"] + "/" + META_DATA["filename"]
            archive_filepath = os.path.join(data_home, "CaliforniaHousing.tgz")
            print("Downloading Cal. housing from {} to {}".format(download_url, data_home))
            urllib.request.urlretrieve(download_url, archive_filepath)

            with tarfile.open(mode="r:gz", name=archive_filepath) as f:
                calif_housing = pd.read_csv(
                    f.extractfile("CaliforniaHousing/cal_housing.data"), 
                    index_col=None,
                    header=None,
                    names=_FEATURE_NAMES,
                )
                calif_housing.to_csv(local_filepath, index=False)
                self._data = calif_housing.to_dict(orient="records")
            os.remove(archive_filepath)
        else:
            self._data = pd.read_csv(local_filepath).to_dict(orient="records")

    def get_iter(self, shuffle_item_buffer: int = 100, **kwargs) -> Composable:
        """
        Get an iterator over samples.

        Args:
            shuffle_item_buffer (int): the size of the buffer used to shuffle samples after being fetched. Please note
                the memory footprint of samples
        """
        return IterableSource(self._data).shuffle(size=shuffle_item_buffer)



if __name__ == "__main__":
    CaliforniaHousing()