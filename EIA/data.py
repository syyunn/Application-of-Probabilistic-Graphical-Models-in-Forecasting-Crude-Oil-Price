import pandas as pd
import numpy as np

import eia

import api_keys

if __name__ == "__main__":
    eia_api = eia.API(api_keys.eia)
    time_series_label = 'TOTAL.COEXPUS.M'  # (C)rude (O)il (E)xport - (M)onthly
    eia_data = pd.DataFrame(eia_api.data_by_series(
        series=time_series_label))
    pass
