import datetime

import numpy as np
import pandas as pd


def convert_to_datetime(time: str):
    return datetime.datetime.strptime(time[:9], "%Y %m ").date()


def clean_EIA_series(data: pd.DataFrame):
    data.replace('-', np.nan, regex=True, inplace=True)
    data.fillna(method='bfill', inplace=True)
    data.index = data.index.map(convert_to_datetime)
    data.index = pd.to_datetime(data.index)
