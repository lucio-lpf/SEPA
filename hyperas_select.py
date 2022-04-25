
import pandas as pd
import numpy as np

from hyperopt import Trials, STATUS_OK, tpe
from hyperas import optim
from hyperas.distributions import choice, uniform

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

location_dir = ''


def data():
    dataset_path = './data/washington_dc/join/summer_data.csv'

    raw_data = pd.read_csv(dataset_path)
    dataset = raw_data.loc[:, (raw_data != raw_data.iloc[0]).any(axis=0)]

    stats = dataset.describe()
    stats.pop("Efficiency")
    stats = stats.transpose()
    train_labels = dataset.pop('Efficiency')

    normed_train_data = (dataset-stats['mean'])/stats['std']

    return normed_train_data, train_labels, normed_train_data, train_labels


def train(normed_train_data, train_labels, normed_test_data, test_labels):

    len_ds = len(normed_train_data.keys())

    model_layers = []
    model_layers.append(layers.Dense({{choice([512, 1024])}},
                                     activation={{choice(['relu',
                                                          'sigmoid',
                                                          'linear',
                                                          'tanh'])}},
                                     input_shape=[len_ds]))
    model_layers.append(layers.Dropout({{uniform(0, 0.5)}}))

    model_layers.append(layers.Dense({{choice([128, 256, 512, 1024])}},
                                     activation={{choice(['relu',
                                                          'sigmoid',
                                                          'linear',
                                                          'tanh'])}}))
    model_layers.append(layers.Dropout({{uniform(0, 0.5)}}))

    model_layers.append(layers.Dense({{choice([128, 256, 512, 1024])}},
                                     activation={{choice(['relu',
                                                          'sigmoid',
                                                          'linear',
                                                          'tanh'])}}))
    model_layers.append(layers.Dropout({{uniform(0, 0.5)}}))

    model_layers.append(layers.Dense(1, activation='linear'))

    model = keras.Sequential(model_layers)

    model.compile(loss='mse',
                  optimizer={{choice(['RMSprop', 'adam', 'sgd'])}},
                  metrics=['mae',
                           'mse', 'mape',
                           tf.keras.metrics.RootMeanSquaredError()])

    EPOCHS = 20

    history = model.fit(
      normed_train_data, train_labels,
      batch_size={{choice([8, 16, 32, 64])}},
      epochs=EPOCHS, validation_split=0.2, verbose=2, use_multiprocessing=True)

    validation_mse = np.amin(history.history['val_mse'])

    return {'loss': validation_mse, 'status': STATUS_OK, 'model': model}


if __name__ == '__main__':

    best_run, best_model = optim.minimize(model=train,
                                          data=data,
                                          algo=tpe.suggest,
                                          max_evals=50,
                                          trials=Trials())

    print("Best performing model chosen hyper-parameters:")
    print(best_run)
