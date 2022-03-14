"""
This driver can be used to parse the Zenodo Monthly German Tweet dataset obtainable at
    https://zenodo.org/record/3633935#.YcMujb1Khqt
"""
from __future__ import annotations

import json
from typing import Iterable, Iterator, List, TYPE_CHECKING

from squirrel.driver import MapDriver
from squirrel.fsspec.fs import get_fs_from_url
from squirrel.iterstream import FilePathGenerator

if TYPE_CHECKING:
    from squirrel.iterstream import Composable


class MonthlyGermanTweetsDriver(MapDriver):
    name = "raw_monthly_german_tweets"

    def __init__(self, folder: str, **kwargs) -> None:
        """Init the MonthlyGermanTweets driver.

        Args:
            folder: Path to the unzipped data dump
        """
        self.folder = folder
        self.compression = "gzip"
        self.parse_error_count = 0

    def parse_archive(self, url: str) -> List[str]:
        """Parse a single archive. Note the custom parsing function due to the special file layout."""

        fs = get_fs_from_url(url)
        with fs.open(url, "rb", compression=self.compression) as f:
            json_bytes = list(f)

        dec = "".join([b.decode("utf-8").strip() for b in json_bytes])[1:-1]
        samples = ["{" + elem for elem in dec.split(",{") if not elem.startswith("{")]
        return samples

    def get(self, url: str) -> Iterator:
        """Yields all samples in a single archive."""

        samples = self.parse_archive(url)

        for s in samples:
            try:
                sample = json.loads(s)
                yield sample
            except json.JSONDecodeError:
                self.parse_error_count += 1

    def get_iter(self, flatten: bool = True, **kwargs) -> Composable:
        """Returns a composable that iterates over the raw data in a full unzipped shard of the Monthly German Tweets
        dataset.

        Args:
            flatten (bool): Whether to flatten the returned iterable. Defaults to False.
            **kwargs: Other keyword arguments passed to :py:meth:`MapDriver.get_iter`.
        """

        return super().get_iter(flatten=flatten, **kwargs)

    def keys(self, **kwargs) -> Iterable:
        """Returns the paths of the files in the root directory relative to root."""
        return FilePathGenerator(self.folder)
