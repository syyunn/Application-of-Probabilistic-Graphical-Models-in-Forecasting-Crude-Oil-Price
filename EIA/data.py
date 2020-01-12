import pandas as pd
import numpy as np

import eia

import utils
import api_keys

if __name__ == "__main__":
    eia_api = eia.API(api_keys.eia)
    time_series_label = 'TOTAL.COEXPUS.M'  # (C)rude (O)il (E)xport - (M)onthly
    eia_data = pd.DataFrame(eia_api.data_by_series(
        series=time_series_label))

    indices_datetime = eia_data.index.map(utils.convert_to_datetime)
    pd_df_indices_datetime = pd.to_datetime(indices_datetime)
    eia_data.index = pd.to_datetime(pd_df_indices_datetime)  # index re-write
    eia_data.columns = [time_series_label]  # feature-label re-write

    eia_data.replace('-', np.nan, regex=True, inplace=True)
    eia_data.fillna(method='bfill', inplace=True)  # Backward fill of na
    pass
