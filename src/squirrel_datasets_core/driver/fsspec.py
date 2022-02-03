"""Base driver class that utilizes fsspec to access files."""
import os
from typing import Any, Dict, Optional

import numpy as np
from PIL import Image
from squirrel.driver.driver import FileDriver
from squirrel.fsspec.fs import get_fs_from_url


class FsspecDriver(FileDriver):
    """Generic driver that uses an fsspec filesystem object to load its samples."""

    def __init__(self, url: str, **kwargs) -> None:
        """Initialize FsspecDriver.

        Args:
            url (str): Path to the directory containing the dataset.
            **kwargs: Additional keyword arguments passed to the super class initializer.
        """
        super().__init__(**kwargs)
        self.url = url

    @staticmethod
    def _get_store_helper(path: str, storage_options: Optional[Dict] = None, open_kwargs: Optional[Dict] = None) -> Any:
        """Return a handler for a file."""
        if storage_options is None:
            storage_options = {}
        if open_kwargs is None:
            open_kwargs = {}

        fs = get_fs_from_url(path, **storage_options)
        return fs.open(path, **open_kwargs)

    def get_store(self, path: str, storage_options: Optional[Dict] = None, open_kwargs: Optional[Dict] = None) -> Any:
        """Return a handler for a file in the dataset.

        Args:
            path (str): File path relative to `self.url`.
            storage_options (Dict, optional): Storage options passed to :py:meth:`squirrel.fsspec.fs.get_fs_from_url`.
            open_kwargs (Dict, optional): Keyword arguments passed to `fs.open()`. By default, only mode="r" is set.

        Returns:
            File handler corresponding to the given file.
        """
        if open_kwargs is None:
            open_kwargs = {}
        open_kwargs["mode"] = open_kwargs.get("mode", "r")

        fp = os.path.join(self.url, path)
        return self._get_store_helper(path=fp, storage_options=storage_options, open_kwargs=open_kwargs)


class TwoDImageFileDriver(FsspecDriver):
    @staticmethod
    def load_image(path: str, storage_options: Optional[Dict] = None, open_kwargs: Optional[Dict] = None) -> np.ndarray:
        """Load a 2D RGB image.

        Args:
            path (str): Image path.
            storage_options (Dict, optional): Storage options passed to :py:meth:`squirrel.fsspec.fs.get_fs_from_url`.
                Defaults to None.
            open_kwargs (Dict, optional): Keyword arguments passed to `fs.open()`. By default, only mode="rb" is set.

        Returns:
            np.ndarray: Image as a numpy array.
        """
        if open_kwargs is None:
            open_kwargs = {}
        open_kwargs["mode"] = open_kwargs.get("mode", "rb")

        with FsspecDriver._get_store_helper(path, storage_options=storage_options, open_kwargs=open_kwargs) as fh:
            return np.array(Image.open(fh))
