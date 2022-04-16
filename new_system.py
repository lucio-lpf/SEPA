from __future__ import absolute_import, division, unicode_literals

import matplotlib.pyplot as plt
import pandas as pd

import tensorflow as tf

from tensorflow import keras

print(tf.__version__)


def norm(x, ts):
    return (x - ts['mean']) / ts['std']


model = keras.models.load_model('./sidney/join')

# for filename in os.listdir(forecasting_dir):
#     sys_id = filename.split("_")[1].split('.')[0]
#     print(sys_id)

raw_data = pd.read_csv('./data/new_system/join/join_data.csv')

train_dataset = pd.read_csv('./data/sidney/join/join_data.csv')


train_stats = train_dataset.describe()
train_stats.pop("Efficiency")
train_stats = train_stats.transpose()

test_labels = raw_data.pop("Efficiency")
normed_test_data = norm(raw_data, train_stats)

test_predictions = model.predict(normed_test_data).flatten()

test_predictions = test_predictions[::-1]
test_labels = test_labels[::-1]

plot_data = pd.DataFrame({'time': range(1, 366),
                          'predicted': test_predictions,
                          'actual': test_labels})

plt.rcParams.update({'font.size': 70})
plt.figure(figsize=(80, 20))
plt.ylabel('Efficiency')
plt.xlabel('Days')
plt.xlim([1, 365])
plt.ylim([0, 8])
plt.plot('time', 'predicted', data=plot_data, marker='o', markersize=10,
         color='tab:blue', linewidth=4)
plt.legend()
plt.savefig('./images/new_system_example.png')

# plt.plot('time', 'actual', data=plot_data, marker='o', markersize=10,
#          color='tab:red', linewidth=5)
# plt.legend()
#
# plt.savefig('./images/new_system_eval.png')
