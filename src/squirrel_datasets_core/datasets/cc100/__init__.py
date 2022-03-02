from squirrel.catalog import CatalogKey, Source

from squirrel_datasets_core.datasets.cc100.cc100 import CC100Driver
from squirrel_datasets_core.datasets.cc100.constants import CC_100_CONFIG

__all__ = ["SOURCES", "DRIVERS"]

DRIVERS = [CC100Driver]
SOURCES = [
    (
        CatalogKey("cc100", 1),
        Source(driver_name="cc100", driver_kwargs={"subsets": dict(CC_100_CONFIG)}),
    ),
]
