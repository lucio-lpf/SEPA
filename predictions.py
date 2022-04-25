from __future__ import absolute_import, division, unicode_literals

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys


import tensorflow as tf

from tensorflow import keras

print(tf.__version__)


def norm(x, ts):
    return (x - ts['mean']) / ts['std']


model = keras.models.load_model('./san_francisco/summer')


raw_data = pd.read_csv('./data/san_francisco/join_f/all_forecasting.csv')


train_dataset = pd.read_csv('./data/san_francisco/join/summer_data.csv')
train_dataset = train_dataset.loc[:, (train_dataset != train_dataset.iloc[0]).any(axis=0)]
raw_data = raw_data[train_dataset.columns]

train_stats = train_dataset.describe()
train_stats.pop("Efficiency")
train_stats = train_stats.transpose()
test_labels = raw_data.pop("Efficiency")


normed_test_data = norm(raw_data, train_stats)

test_predictions = model.predict(normed_test_data).flatten()


print(test_labels.values)
print(test_predictions)
exit()
plot_data = pd.DataFrame({'time': range(1, 6),
                          'actual': test_labels,
                          'predicted': test_predictions})

plt.ylabel('Efficiency')
plt.xlabel('Days')
plt.xlim([0, 6])
plt.ylim([0, 5])
plt.plot('time', 'actual', data=plot_data, marker='o', markersize=5,
         color='skyblue', linewidth=2)
plt.plot('time', 'predicted', data=plot_data, marker='o', markersize=5,
         color='olive', linewidth=2)
plt.legend()
plt.savefig('./san_franciscoimages/predictions.png')
