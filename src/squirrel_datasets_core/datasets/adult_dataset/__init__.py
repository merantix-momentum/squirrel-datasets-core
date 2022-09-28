from squirrel.catalog import Source, CatalogKey
from squirrel_datasets_core.datasets.adult_dataset.driver import AdultIncome

__all__ = ["SOURCES", "DRIVERS"]

DRIVERS = [AdultIncome]
SOURCES = [
    (
        CatalogKey("adult_income", 1),
        Source(
            driver_name="adult_income",
            metadata={"src": "http://www.cs.toronto.edu/~delve/data/adult/adultDetail.html"},
        ),
    )
]
