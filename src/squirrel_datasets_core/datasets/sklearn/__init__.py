# Exemplary sources for the torchvision driver

from squirrel.catalog import Source, CatalogKey

from squirrel_datasets_core.driver.sklearn import SklearnDriver

__all__ = ["SOURCES"]

SKLEARN_DATASETS = SklearnDriver.get_availabel_datasets()

SOURCES = [(CatalogKey(name, 1), Source(driver_name="sklearn", driver_kwargs={"name": name}))
             for name in SKLEARN_DATASETS]
