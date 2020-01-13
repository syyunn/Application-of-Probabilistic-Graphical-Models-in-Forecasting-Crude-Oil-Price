import pandas as pd

import eia
from fredapi import Fred

import utils
import api_keys
from data.datasets import datasets_eia, datasets_fred

# Instantiate the API streams for EIA and FRED
eia_api = eia.API(api_keys.eia)
fred = Fred(api_key=api_keys.fred)

# Append dataFrames from each API streams into data_merge list
data_merge = []

for series_id in datasets_eia:
    df = pd.DataFrame(eia_api.data_by_series(series=series_id))
    utils.clean_EIA_series(df, column_label=series_id)
    df.columns = [series_id]
    data_merge.append(df)

for series_id in datasets_fred:
    df = pd.DataFrame(fred.get_series(series_id), columns=[series_id])
    data_merge.append(df)

data = pd.concat(data_merge, axis=1, join='inner')

utils.store_df_local(data, './data.pkl')

if __name__ == "__main__":
    pass
