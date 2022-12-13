"""Driver for deeplake datasets."""
from typing import Optional

import deeplake
from squirrel.driver import IterDriver
from squirrel.iterstream import Composable, IterableSource


class DeeplakeDriver(IterDriver):
    """Driver to access deeplake datasets."""

    name = "deeplake"

    def __init__(self, url: str, **kwargs) -> None:
        """Initialize DeeplakeDriver.

        Args:
            url (str): Path to the directory containing the dataset.
            **kwargs: Additional keyword arguments passed to the super class initializer.
        """
        super().__init__(**kwargs)
        self.url = url

    def get_iter(self, subset: Optional[str] = None, **dataset_kwargs) -> Composable:
        """Return an iterstream on top of a deeplake dataset.

        Args:
            subset (str): Subset to open. If not provided, all subsets will be used.
            **dataset_kwargs: Keyword arguments passed to :py:func:`deeplake.load`.

        Returns:
            Composable
        """
        with self.get_deeplake(**dataset_kwargs) as ds:
            it = IterableSource(ds) if subset is None else IterableSource(ds[subset])
            return it.map(lambda x: x.tensors)

    def get_deeplake(self, **dataset_kwargs) -> deeplake.Dataset:
        """Return a handler for the dataset.

        Args:
            **dataset_kwargs: Keyword arguments passed to :py:func:`deeplake.load`.

        Returns:
            deeplake.Dataset: The deeplake dataset.
        """
        return deeplake.load(path=self.url, **dataset_kwargs)
