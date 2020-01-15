"""Regime Detection"""
import hmms
import numpy as np
import pandas as pd

import utils
import matplotlib.pyplot as plt


df_pickled_path = "./data/data.pkl"
data = utils.load_df_pickled(df_pickled_path)

train_data, valid_data, test_data = utils.split_df(
    data, train_set_ratio=0.8, test_set_ratio=0.1, valid_set_ratio=0.1
)

column_label = 'WTISPLC'  # Spot Crude Oil Price: West Texas Intermediate
price = train_data[column_label]

price_diff = price.diff()[1:]
e_seq = np.array(price_diff.apply(lambda x: 1 if x > 0 else 0).values)  #
# emission sequence

dhmm_r = hmms.DtHMM.random(3, 2)

e_seq_split = np.array_split(e_seq, 32)  # hmms.DtHMM takes a list of arrays
# no greater than length 32

dhmm_r.baum_welch(e_seq_split, 100)

hmms.print_parameters(dhmm_r)

(log_prob, s_seq) = dhmm_r.viterbi(np.concatenate(e_seq_split).ravel())  #
# assign one of 3 states to each sequence.

price_plot = pd.DataFrame(price[1:], index=price[1:].index)
price_plot['Regime'] = s_seq
price_plot['diff'] = price_diff
means = price_plot.groupby(['Regime'])['diff'].mean()
lst_1 = means.index.tolist()
lst_2 = means.sort_values().index.tolist()
map_regimes = dict(zip(lst_2, lst_1))
price_plot['Regime'] = price_plot['Regime'].map(map_regimes)

import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
from matplotlib.colors import Colormap, ListedColormap, BoundaryNorm

fig, _ = plt.subplots(figsize=(20, 8))
# Make 0 (Bear) - red, 1 (Stagnant) - blue, 2 (Bull) - green
cmap = ListedColormap(['r', 'b', 'g'], 'indexed')
norm = BoundaryNorm(range(3 + 1), cmap.N)
inxval = mdates.date2num(price_plot['WTISPLC'].index.to_pydatetime())
points = np.array([inxval, price_plot['WTISPLC']]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = LineCollection(segments, cmap=cmap, norm=norm)
lc.set_array(price_plot['Regime'])
plt.gca().add_collection(lc)
plt.xlim(price_plot['WTISPLC'].index.min(), price_plot['WTISPLC'].index.max())
plt.ylim(price_plot['WTISPLC'].min(), price_plot['WTISPLC'].max())
r_patch = mpatches.Patch(color='red', label='Bear')
b_patch = mpatches.Patch(color='blue', label='Stagnant')
g_patch = mpatches.Patch(color='green', label='Bull')
plt.legend(handles=[r_patch, g_patch, b_patch])
plt.show()

if __name__ == "__main__":
    pass
