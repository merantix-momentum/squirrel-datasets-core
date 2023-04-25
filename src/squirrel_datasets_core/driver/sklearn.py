import inspect
import logging
from tempfile import gettempdir
from typing import Optional, List, Dict

from sklearn import datasets
from pandas import DataFrame
from squirrel.driver import IterDriver
from squirrel.iterstream import IterableSource
from squirrel.catalog.catalog import Catalog
    
logger = logging.getLogger(__name__)

__all__ = ["SklearnDriver"]

TOY_DATASETS = ["_".join(name.split('_')[1:])
                for name, _ in inspect.getmembers(datasets) if name.startswith("load_")]  

REAL_DATASETS = ["_".join(name.split('_')[1:]) 
                for name, _ in inspect.getmembers(datasets) if name.startswith("fetch_")]

class SklearnDriver(IterDriver):
    name = "sklearn"

    def __init__(self, name: str,
                 data_home: Optional[str] = None,
                 download_if_missing: Optional[bool] = True,
                 catalog: Optional[Catalog] = None) -> None:
        """A driver for sklearn datasets. There toy datasets, which are internal to the package
        and real-world datasets which needs to be downloaded

        Args:
            name (str): name of the dataset. Visit https://scikit-learn.org/stable/modules/classes.html#module-sklearn.datasets or 
            call get_dataset_names() method
            data_home (Optional[str], optional): location where the dataset is downloaded. Defaults to ‘~/scikit_learn_data’
            download_if_missing (Optional[bool], optional): Only download if this is true, otherwise throw an  IOError. Defaults to True.
            catalog (Optional[Catalog], optional): default argument for catalog registration. Defaults to None.
        """
        super().__init__(catalog)
        self.name = name 
        self._data = self._get_data(data_home, download_if_missing)
        self._data_home = data_home
        
    def _get_data(self,
                  data_home: Optional[str] = None,
                  download_if_missing: Optional[bool] = True) -> DataFrame:
        """Return a pandas dataframe with input and target."""
        if self.name in TOY_DATASETS:
            load_ds = getattr(datasets, f"load_{self.name}")
            return load_ds()
        elif self.name in REAL_DATASETS:
            load_ds = getattr(datasets, f"fetch_{self.name}")
            return load_ds(data_home=data_home, download_if_missing=download_if_missing)
        else:
            raise ValueError(f"Dataset {self.name} is not available. Use one of these {TOY_DATASETS + REAL_DATASETS}")
    
    def get_iter(self) -> IterableSource:
        """Returns a iterstream over the dataframe"""
        return IterableSource(zip(self._data["data"], self._data["target"]))
    
    def get_info(self) -> Dict[str, str]:
        info = {"description": self._data.get("DESCR", "No description available"),
                "feature_names": self._data.get("feature_names", "no feature names available"),
                "target_names": self._data.get("target_names", "no target names available")}
        return info
            
    @staticmethod
    def get_dataset_names() -> Dict[str, List[str]]:
        """Returns a list of available datasets"""
        return {"toy": TOY_DATASETS, "real": REAL_DATASETS}
    