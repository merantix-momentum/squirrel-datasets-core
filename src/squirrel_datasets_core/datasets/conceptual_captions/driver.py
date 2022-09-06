from __future__ import annotations

import logging
import sys
import typing as t
import urllib
from typing import TYPE_CHECKING
from urllib.request import Request

import numpy as np
import requests
from PIL import Image, UnidentifiedImageError
from squirrel.driver import IterDriver
from squirrel.iterstream.source import IterableSource

if TYPE_CHECKING:
    from squirrel.catalog import Catalog
    from squirrel.iterstream import Composable


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class CC12MDriver(IterDriver):

    name = "conceptual-captions-12m"

    def __init__(self, index_url: str, catalog: t.Optional[Catalog] = None, **kwargs) -> None:
        """
        Initialize the ConceptualCaptions driver:
        Args:
            index_url: url to the index file containing the captions and URLs to the image file locations.
            catalog: a `squirrel.catalog.Catalog` that contains configuration for custom dataset locations.
        """

        super().__init__(catalog, **kwargs)
        self._index_url = index_url

    @property
    def _index_iterator(self) -> t.Iterable:
        """Reads the index file as a stream and returns individual elements"""
        with requests.get(self._index_url, stream=True) as req:
            for line in req.iter_lines():
                url, caption = line.decode("utf-8").split("\t")
                yield {"caption": caption, "url": url}

    @staticmethod
    def _download_image(url: str) -> np.ndarray:
        """
        Download an individual image from the given URL.

        Args:
            url: location of the image
        """
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=1)
        return np.array(Image.open(resp))

    @staticmethod
    def _map_fn(record: t.Dict[str, str]) -> t.Dict[str, t.Union[str, np.ndarray]]:
        """
        Map function over all index elements.

        Args:
            record: dict containing the url under the key `url`
        """
        url = record["url"]
        record["error"] = False
        try:
            record["image"] = CC12MDriver._download_image(url)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logger.info(f"Cannot access url {url} due to Error {e}")
            record["error"] = True
        except UnidentifiedImageError as e:
            logger.info(f"Cannot open image at {url} due to Error {e}")
            record["error"] = True

        return record

    @staticmethod
    def _has_no_error(record: t.Dict[str, t.Union[str, np.ndarray]]) -> bool:
        """Filter to remove erroneous downloads."""
        return not record["error"]

    def get_iter(
        self,
        shuffle_key_buffer: int = 1000,
        shuffle_item_buffer: int = 100,
        prefetch_buffer: int = 2,
        max_workers: t.Optional[int] = None,
        **kwargs,
    ) -> Composable:
        """
        Get an iterator over samples.

        Args:
            shuffle_key_buffer (int): the size of the buffer used to shuffle keys.
            prefetch_buffer (int): the size of the buffer that defines how many shards are pre-fetched. Please note the
                memory footprint when setting this parameter
            shuffle_item_buffer (int): the size of the buffer used to shuffle samples after being fetched. Please note
                the memory footprint of samples
            max_workers: number of workers in the ThreadPoolExecutor. If set to 0 runs a sequential map.

        Returns:
            (squirrel.iterstream.Composable)
        """
        it = IterableSource(self._index_iterator).shuffle(size=shuffle_key_buffer)

        map_fn = CC12MDriver._map_fn
        _map = it.map(map_fn) if max_workers == 0 else it.async_map(map_fn, prefetch_buffer, max_workers)
        return _map.filter(CC12MDriver._has_no_error).shuffle(size=shuffle_item_buffer)
