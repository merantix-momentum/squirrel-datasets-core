from squirrel.catalog import Source, CatalogKey
from squirrel_datasets_core.datasets.california_housing.driver import CaliforniaHousing

__all__ = ["SOURCES", "DRIVERS"]

DRIVERS = [CaliforniaHousing]
SOURCES = [
    (
        CatalogKey("california_housing", 1),
        Source(
            driver_name="california_housing",
            metadata={
                "uri": "https://ndownloader.figshare.com/files/5976036/cal_housing.tgz",
                "src": "https://github.com/scikit-learn/scikit-learn/blob/"
                + "36958fb24/sklearn/datasets/_california_housing.py",
            },
        ),
    )
]
