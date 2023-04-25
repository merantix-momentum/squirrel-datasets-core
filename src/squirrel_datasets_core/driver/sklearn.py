import inspect
import logging
from tempfile import gettempdir
from typing import Optional, List

from sklearn import datasets
from pandas import DataFrame
from squirrel.driver import DataFrameDriver
from squirrel.iterstream import IterableSource

logger = logging.getLogger(__name__)

__all__ = ["SklearnDriver"]


class SklearnDriver(DataFrameDriver):
    name = "sklearn"

    def __init__(self, name: str, data_home: Optional[str] = None) -> None:
        super().__init__()
        self.name = name 
        self._data_home = data_home
        
    def get_df(self) -> DataFrame:
        """Return a pandas dataframe with input and target."""
        try: 
            load_ds = getattr(datasets, f"load_{self.name}")
        except AttributeError:
             raise ValueError(f"Dataset {self.name} does not exist, please choose one from {self.get_availabel_datasets()}")
         
        args =  inspect.getargspec(load_ds)[0]
        if "data_home" in args:
            # Toy datasets wont allow you to specify a home folder for your data
            return load_ds(return_X_y=True,
                            as_frame=True)
        else:
            return load_ds(return_X_y=True,
                           as_frame=True,
                           data_home=self._data_home)
    
    @staticmethod
    def get_availabel_datasets() -> List[str]:
        """Returns a list of available datasets."""
        return [name.split('_')[0] 
                for name, _ in inspect.getmembers(datasets) if name.startswith("load_")]
        
    def get_iter(self) -> IterableSource:
        """Returns a iterstream over the dataframe"""
        return IterableSource(self.get_df().iterrows())


