import datetime

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


def convert_to_datetime(time: str):
    return datetime.datetime.strptime(time[:9], "%Y %m ").date()


def clean_EIA_series(data: pd.DataFrame, column_label: str):
    data.replace("-", np.nan, regex=True, inplace=True)
    data.fillna(method="bfill", inplace=True)
    data.index = data.index.map(convert_to_datetime)
    data.index = pd.to_datetime(data.index)
    data.columns = [column_label]
    return None  # best-practice to denote the function is void.


def plot_time_series(
    data: pd.DataFrame,
    x_label: str,
    x_unit: str,
    y_label: str,
    y_unit: str,
    column_name: str = "price",
    scatter: bool = False,
):

    plt.figure(figsize=(12, 6), dpi=100)
    if not scatter:
        plt.plot(data.index, data[column_name])
    if scatter:
        plt.scatter(data.index, data[column_name])
    plt.xlabel(x_label + " : " + x_unit)
    plt.ylabel(y_label + " : " + y_unit)
    plt.grid()
    plt.show()


def store_df_local(df, fpath):
    df.to_pickle(fpath)  # where to save it, usually as a .pkl


def load_df_pickled(fpath):
    return pd.read_pickle(fpath)


def split_df(df, train_set_ratio: float = 0.8, test_set_ratio: float=0.1,
             valid_set_ratio: float=0.1):
    assert train_set_ratio + test_set_ratio + valid_set_ratio == 1, \
        "the sum of train/valid/test ratio shall be 1."

    train_end_idx = int(df.shape[0]*train_set_ratio)
    valid_end_idx = int(df.shape[0]*(train_set_ratio+valid_set_ratio))
    test_end_idx = int(df.shape[0])

    train_data = df[:train_end_idx]
    valid_data = df[train_end_idx: valid_end_idx]
    test_data = df[valid_end_idx:test_end_idx]

    return train_data, valid_data, test_data
