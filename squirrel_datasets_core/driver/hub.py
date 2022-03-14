"""Driver for hub datasets."""
from typing import Optional

import hub
from squirrel.driver import IterDriver
from squirrel.iterstream import Composable, IterableSource


class HubDriver(IterDriver):
    """Driver to access hub datasets."""

    name = "hub"

    def __init__(self, url: str, **kwargs) -> None:
        """Initialize HubDriver.

        Args:
            url (str): Path to the directory containing the dataset.
            **kwargs: Additional keyword arguments passed to the super class initializer.
        """
        super().__init__(**kwargs)
        self.url = url

    def get_iter(self, subset: Optional[str] = None, **dataset_kwargs) -> Composable:
        """Return an iterstream on top of a hub dataset.

        Args:
            subset (str): Subset to open. If not provided, all subsets will be used.
            **dataset_kwargs: Keyword arguments passed to :py:func:`hub.dataset`.

        Returns:
            Composable
        """
        with self.get_hub(**dataset_kwargs) as ds:
            it = IterableSource(ds) if subset is None else IterableSource(ds[subset])
            return it.map(lambda x: x.tensors)

    def get_hub(self, **dataset_kwargs) -> hub.Dataset:
        """Return a handler for the dataset.

        Args:
            **dataset_kwargs: Keyword arguments passed to :py:func:`hub.dataset`.

        Returns:
            Hub dataset.
        """
        return hub.dataset(path=self.url, **dataset_kwargs)
