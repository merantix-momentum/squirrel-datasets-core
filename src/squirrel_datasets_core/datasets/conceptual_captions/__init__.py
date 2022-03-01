from squirrel.catalog import Source, CatalogKey
from squirrel_datasets_core.datasets.conceptual_captions.driver import CC12MDriver

__all__ = ["SOURCES", "DRIVERS"]

DRIVERS = [CC12MDriver]
SOURCES = [
    (
        CatalogKey("conceptual-captions-12m", 1),
        Source(
            driver_name="conceptual-captions-12m",
            driver_kwargs={"index_url": "https://storage.googleapis.com/conceptual_12m/cc12m.tsv"},
        ),
    ),
]
