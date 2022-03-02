from squirrel.catalog import CatalogKey, Source
from squirrel_datasets_core.datasets.allenai_c4.allenai_c4_multilingual import C4DatasetDriver
from squirrel_datasets_core.datasets.allenai_c4.constants import C4_MULTILINGUAL_CONFIG

__all__ = ["SOURCES", "DRIVERS"]

DRIVERS = [C4DatasetDriver]
SOURCES = [
    (
        CatalogKey("c4", 1),
        Source(driver_name="c4", driver_kwargs={"subsets": dict(C4_MULTILINGUAL_CONFIG)}),
    ),
]
