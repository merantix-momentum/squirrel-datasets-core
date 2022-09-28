from __future__ import annotations

import os
from typing import TYPE_CHECKING, Optional, Tuple

import pandas as pd

from squirrel.driver import IterDriver
from squirrel.iterstream import IterableSource

if TYPE_CHECKING:
    from squirrel.iterstream import Composable

META_DATA = dict(
    filename="adult.csv",
    url="https://datahub.io/machine-learning/adult/r",
)

_FEATURE_NAMES = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education-num",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capitalgain",
    "capitalloss",
    "hoursperweek",
    "native-country",
    "class",
]


def stratified_sample_df(
    df: pd.DataFrame, col: str, n_samples: int, seed: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Creates a stratified split of a pd.Dataframe across the given column with n_samples in each class

    Args:
        df (pd.Dataframe): Dataframe containing the tabular data.
        col (str): The column across which to sample the folds
        n_samples (int): Number of samples in each fold.
        seed (int): [Optional] The random seed for the sampler.
    """
    n = min(n_samples, df[col].value_counts().min())
    test_df_ = df.groupby(col).apply(lambda x: x.sample(n, random_state=seed))
    test_df_.index = test_df_.index.droplevel(0)
    train_df_ = df.drop(test_df_.index)
    return train_df_, test_df_


def proportionate_sample_df(
    df: pd.DataFrame, col: str, fraction: float = 0.2, seed: Optional[int] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Creates a proportional split of a pd.Dataframe across the given column.

    Args:
        df (pd.Dataframe): Dataframe containing the tabular data.
        col (str): The column across which to sample the folds
        fraction (float): Percentage of samples in each class. Defaults to 0.2.
        seed (int): [Optional] The random seed for the sampler.
    """
    test_df_ = df.groupby(col, group_keys=False).apply(lambda x: x.sample(frac=fraction, random_state=seed))
    train_df_ = df.drop(test_df_.index)
    return train_df_, test_df_


class AdultIncome(IterDriver):

    name = "adult_income"

    def __init__(self, **kwargs) -> None:
        """Initialze the California housing dataset driver."""
        super().__init__(**kwargs)
        self._train_df, self._test_df = self._init()
        self._train_df = self._train_df.to_dict(orient="records")
        self._test_df = self._test_df.to_dict(orient="records")

    def _init(self) -> pd.DataFrame:
        """Uses a proportionate sampling strategy to split the dataset into train and test folds."""
        df = pd.read_csv(
            os.path.join(META_DATA["url"], META_DATA["filename"]),
            index_col=None,
        )
        df = df.fillna("NAN")
        train_df, test_df = proportionate_sample_df(df, "class", 0.2, seed=42)
        return train_df, test_df

    def get_iter(self, split: str = "train", shuffle_item_buffer: int = 100, **kwargs) -> Composable:
        """
        Get an iterator over samples.

        Args:
            split (str): can be `train` or `test`.
            shuffle_item_buffer (int): the size of the buffer used to shuffle samples after being fetched. Please note
                the memory footprint of samples
        """
        assert split in ["train", "test"]
        if split == "train":
            return IterableSource(self._train_df).shuffle(size=shuffle_item_buffer)
        else:
            return IterableSource(self._test_df).shuffle(size=shuffle_item_buffer)
