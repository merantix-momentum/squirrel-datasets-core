"""
This driver can be used to parse the Zenodo Monthly German Tweet dataset obtainable at
    https://zenodo.org/record/3633935#.YcMujb1Khqt
"""
import json
from typing import Callable, Generator, List, Optional

from squirrel.driver import RecordIteratorDriver
from squirrel.fsspec.fs import get_fs_from_url
from squirrel.iterstream import Composable, FilePathGenerator


class MonthlyGermanTweetsDriver(RecordIteratorDriver):
    name = "raw_monthly_german_tweets"

    def __init__(self, folder: str, **kwargs) -> None:
        """
        Init the iterator.

        Args:
            folder: Path to the unzipped data dump
        """
        self.folder = folder
        self.compression = "gzip"
        self.parse_error_count = 0

    def parse_archive(self, url: str) -> List[str]:
        """Parse a single archive. Note the custom parsing function due to the
        special file layout.
        """

        fs = get_fs_from_url(url)
        with fs.open(url, "rb", compression=self.compression) as f:
            json_bytes = list(f)

        dec = "".join([b.decode("utf-8").strip() for b in json_bytes])[1:-1]
        samples = ["{" + elem for elem in dec.split(",{") if not elem.startswith("{")]
        return samples

    def iterate_single_archive(self, url: str) -> Generator:
        """Iterate over all samples in a single archive"""

        samples = self.parse_archive(url)

        for s in samples:
            try:
                sample = json.loads(s)
                yield sample
            except json.JSONDecodeError:
                self.parse_error_count += 1

    def get_iter(
        self,
        key_hooks: Optional[List[Callable]] = None,
        prefetch_buffer: int = 1_000,
        max_workers: Optional[int] = None,
        **kwargs,
    ) -> Composable:
        """
        Returns a composable that iterates over the raw data in a full unzipped shard of the
        Monthly German Tweets dataset.

        Args:
            key_hooks: List of Callables to modify the iteration over the archives in the shard
            prefetch_buffer: buffer size of the samples buffer
            max_workers: number of workers to use in the async_map loading.
        """

        it = FilePathGenerator(self.folder)

        if key_hooks:
            for hook in key_hooks:
                it = it.to(hook)

        _map = (
            it.map(self.iterate_single_archive)
            if max_workers == 0
            else it.async_map(self.iterate_single_archive, prefetch_buffer, max_workers)
        )

        return _map.flatten()
