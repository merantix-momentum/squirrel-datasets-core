import importlib
import pkgutil
from typing import List, Tuple, Type

from squirrel.catalog import CatalogKey, Source
from squirrel.driver import Driver
from squirrel.framework.plugins.hookimpl import hookimpl


def get_hub_driver() -> Driver:
    """Imports and returns the hub driver class"""
    from squirrel_datasets_core.driver.hub import HubDriver

    return HubDriver


def get_huggingface_driver() -> Driver:
    """Imports and returns the huggingface driver class"""
    from squirrel_datasets_core.driver.huggingface import HuggingfaceDriver

    return HuggingfaceDriver


def get_torchvision_driver() -> Driver:
    """Imports and returns the torchvision driver class"""
    from squirrel_datasets_core.driver.torchvision import TorchvisionDriver

    return TorchvisionDriver


@hookimpl
def squirrel_drivers() -> List[Type[Driver]]:
    """Custom drivers added by this package."""
    import squirrel_datasets_core.datasets as ds

    drivers = []
    add_drivers = {
        "hub": get_hub_driver,
        "huggingface": get_huggingface_driver,
        "torchvision": get_torchvision_driver,
    }

    for d in add_drivers:
        try:
            drivers.append(add_drivers[d]())
        except ImportError as e:
            print(f"Failed to import {d} driver with error: {e}")

    for m in pkgutil.iter_modules(ds.__path__):
        try:
            d = importlib.import_module(f"{ds.__package__}.{m.name}").DRIVERS
            drivers += d
        except AttributeError:
            pass
        except ImportError as e:
            print(f"Failed to import module {m.name} with error: {e}")

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
