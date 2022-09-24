from squirrel.catalog import Source, CatalogKey
from squirrel_datasets_core.datasets.helena.driver import AutoML

__all__ = ["SOURCES", "DRIVERS"]

DRIVERS = [AutoML]
SOURCES = [
    (
        CatalogKey("helena", 1),
        Source(
            driver_name="automl",
            metadata={
                "src": "https://automl.chalearn.org/data"
            },
            driver_kwargs={"dataset_name": "helena"},
            
        ),
    ),
    (
        CatalogKey("jannis", 1),
        Source(
            driver_name="automl",
            metadata={
                "src": "https://automl.chalearn.org/data"
            },
            driver_kwargs={"dataset_name": "jannis"},
        ),
    )
]