from squirrel.catalog import Source, CatalogKey
from squirrel_datasets_core.datasets.helena.driver import Helena

__all__ = ["SOURCES", "DRIVERS"]

DRIVERS = [Helena]
SOURCES = [
    (
        CatalogKey("helena", 1),
        Source(
            driver_name="helena",
            metadata={
                "src": "https://automl.chalearn.org/data"
            },
        ),
    )
]