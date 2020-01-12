import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import eia

import utils
import api_keys

if __name__ == "__main__":
    eia_api = eia.API(api_keys.eia)
    time_series_label = 'TOTAL.COEXPUS.M'  # (C)rude (O)il (E)xport - (M)onthly
    eia_data = pd.DataFrame(eia_api.data_by_series(
        series=time_series_label))
    utils.clean_EIA_series(eia_data, column_label=time_series_label)
    utils.plot_time_series(eia_data, column_name=time_series_label)

    pass
