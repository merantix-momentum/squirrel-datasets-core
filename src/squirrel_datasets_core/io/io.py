from typing import Dict, Optional

import fsspec
import numpy as np
from PIL import Image


def load_image(
    path: str, fs: Optional[fsspec.AbstractFileSystem] = None, open_kwargs: Optional[Dict] = None
) -> np.ndarray:
    """Load an image.

    File is opened from an arbitrary path using fsspec and image is loaded using PIL and converted to a numpy array.

    Args:
        path (str): Image path.
        fs (fsspec.AbstractFileSystem, optional): Filesystem object to use for opening the file. If not provided,
            :py:func:`fsspec.open` will be used. Defaults to None.
        open_kwargs (Dict, optional): Keyword arguments passed to `fs.open()`. By default, only mode="rb" is set.

    Returns:
        np.ndarray: Image as a numpy array.
    """
    if open_kwargs is None:
        open_kwargs = {}
    open_kwargs["mode"] = open_kwargs.get("mode", "rb")

    if fs is None:
        fs = fsspec

    with fs.open(path, **open_kwargs) as fh:
        return np.array(Image.open(fh))
