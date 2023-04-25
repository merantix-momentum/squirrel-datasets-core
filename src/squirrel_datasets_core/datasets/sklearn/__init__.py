# Exemplary sources for the torchvision driver

from squirrel.catalog import Source, CatalogKey

from squirrel_datasets_core.driver.sklearn import TOY_DATASETS, REAL_DATASETS

__all__ = ["SOURCES"]

SKLEARN_DATASETS = TOY_DATASETS + REAL_DATASETS

SOURCES = [(CatalogKey(f"{name}_sklearn", 1), Source(driver_name="sklearn", driver_kwargs={"name": name}))
             for name in SKLEARN_DATASETS]
