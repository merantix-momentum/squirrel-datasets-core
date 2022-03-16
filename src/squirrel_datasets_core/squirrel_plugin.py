import importlib
import pkgutil
from typing import List, Tuple, Type

from squirrel.catalog import CatalogKey, Source
from squirrel.driver import Driver
from squirrel.framework.plugins.hookimpl import hookimpl


@hookimpl
def squirrel_drivers() -> List[Type[Driver]]:
    """Custom drivers added by this package."""
    import squirrel_datasets_core.datasets as ds
    from squirrel_datasets_core.driver.huggingface import HuggingfaceDriver
    from squirrel_datasets_core.driver.torchvision import TorchvisionDriver
    from squirrel_datasets_core.driver.hub import HubDriver

    drivers = [TorchvisionDriver, HuggingfaceDriver, HubDriver]
    for m in pkgutil.iter_modules(ds.__path__):
        try:
            d = importlib.import_module(f"{ds.__package__}.{m.name}").DRIVERS
            drivers += d
        except AttributeError:
            pass

    return drivers


@hookimpl
def squirrel_sources() -> List[Tuple[CatalogKey, Source]]:
    """Custom sources added by this package.

    Returns:
        List of (CatalogKey, Source) tuples.
    """
    datasets = []

    import squirrel_datasets_core.datasets as ds

    for m in pkgutil.iter_modules(ds.__path__):
        try:
            d = importlib.import_module(f"{ds.__package__}.{m.name}").SOURCES
            datasets += d
        except AttributeError:
            pass

    return datasets
