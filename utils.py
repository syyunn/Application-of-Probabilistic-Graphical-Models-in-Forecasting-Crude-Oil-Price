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
