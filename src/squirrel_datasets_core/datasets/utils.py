from typing import Optional, Tuple

import pandas as pd


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
