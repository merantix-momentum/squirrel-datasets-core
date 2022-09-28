from squirrel_datasets_core.datasets.AutoML.driver import AutoML

from squirrel.catalog import CatalogKey, Source

__all__ = ["SOURCES", "DRIVERS"]

DRIVERS = [AutoML]
SOURCES = [
    (
        CatalogKey("helena", 1),
        Source(
            driver_name="automl",
            metadata={"src": "https://automl.chalearn.org/data"},
            driver_kwargs={"dataset_name": "helena"},
        ),
    ),
    (
        CatalogKey("jannis", 1),
        Source(
            driver_name="automl",
            metadata={"src": "https://automl.chalearn.org/data"},
            driver_kwargs={"dataset_name": "jannis"},
        ),
    ),
]
