import inspect
import logging
from tempfile import gettempdir
from typing import Any, Optional, Type

import torchvision
from squirrel.driver import IterDriver
from squirrel.iterstream import IterableSource

logger = logging.getLogger(__name__)

TORCH_DATASET_NAMES_AND_CLASSES = {x[0]: x[1] for x in inspect.getmembers(torchvision.datasets, inspect.isclass)}

TORCH_DATASET_DOC = "https://pytorch.org/vision/stable/datasets.html"

__all__ = ["TorchvisionDriver"]


class TorchvisionDriver(IterDriver):
    name = "torchvision"

    def __init__(self, name: str, url: Optional[str] = None, download: Optional[bool] = None, **open_kwargs) -> None:
        """Initialize TorchVisionLoader.

        Args:
            url (str): Path to the directory containing the dataset (or the directory where the dataset will be
                downloaded, which applies when `download` is set to be `True`).
                If not given, will use a temp dir created from tempfile package instead.
            name (str): The name of the `torch.utils.dataset.Dataset` class to be used to load the dataset.
                Upper case and lower case ambiguity is allowed.
            download (str): If not None, will pass to subclasses of `torchvision.datasets.DatasetFolder` which are
                listed under https://pytorch.org/vision/stable/datasets.html. If True, will assert if self.url
                already has the dataset, if not, will start downloading. If False, torch will assume the dataset
                is already saved under `self.url`. The `None` option applies to torch classes that do not have the
                download argument implemented (mostly because not all datasets can be downloaded by anonymous callers.)
            **kwargs: Additional keyword arguments passed to the super class initializer.
        """
        super().__init__(**open_kwargs)
        self.url = (
            url if url is not None else f"{gettempdir()}/{name}"
        )  # gettempdir returns a constant result throughout a session. Add a suffix to differentiate diff datasets.
        self.name = name
        self.download = download

    def get_iter(self, **open_kwargs) -> IterableSource:
        """Load a torchvision dataset and pass them into iterstream. For a full list of arguments for each
        torchvision.datasets class, see https://pytorch.org/vision/stable/datasets.html.

        Returns:
            An instance of :py:class:`IterableSource`. Notice each raw sample from torchvision follows such
            format: Tuple[img, Any] where the img is a PIL opened image object and Any could be class_id, annotations
            or other types of metadata for a dataset. Please refer to
            https://pytorch.org/vision/stable/datasets.html for a detailed description of what sample format you will
            get.
        """
        ds = self.get_torchvision_dataset(**open_kwargs)
        return IterableSource(ds)

    def get_torchvision_dataset(self, **open_kwargs) -> Any:
        """Return a handler for the dataset."""
        if open_kwargs is None:
            open_kwargs = {}

        dataset = self._find_torchvision_dataset_class(self.name)
        if self.download is not None:
            return dataset(root=self.url, download=self.download, **open_kwargs)
        else:
            return dataset(root=self.url, **open_kwargs)

    @staticmethod
    def _find_torchvision_dataset_class(name: str) -> Type[torchvision.datasets.VisionDataset]:
        """Try to find the `torchvision.dataset` class given the input name. Allow upper and lower case ambiguity.
        Raise an value error if the name could not be found in the implemented list of `torchvision.dataset` classes.
        """
        for key in TORCH_DATASET_NAMES_AND_CLASSES:
            if key.lower() == name.lower():
                return TORCH_DATASET_NAMES_AND_CLASSES[key]
        raise ValueError(f"Dataset {name} could not be found in torchvision. See {TORCH_DATASET_DOC} for a full list.")
