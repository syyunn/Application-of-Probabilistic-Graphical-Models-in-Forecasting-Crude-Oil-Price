import pandas as pd

from fredapi import Fred

import utils
import api_keys

if __name__ == "__main__":
    fred = Fred(api_key=api_keys.fred)
    time_series_label = 'WTISPLC'  # Spot Crude Oil Price: WTI grade
    fred_data = pd.DataFrame(fred.get_series(time_series_label),
                             columns=[time_series_label])
    utils.plot_time_series(fred_data,
                           x_label="Date",
                           x_unit="Year",
                           y_label="Spot WTI Crude Oil Price",
                           y_unit='USD',
                           column_name=time_series_label)

    pass
