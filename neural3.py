from __future__ import absolute_import, division, unicode_literals

import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sb
import sys
import os


import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers


def norm(x, ts):
    return (x - ts['mean']) / ts['std']


def plot_history(history, dataset_path):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [Efficiency]')
    plt.plot(hist['epoch'], hist['mae'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mae'],
             label='Val Error')
    plt.ylim([0, 1.5])
    plt.legend()
    plt.savefig(dataset_path+'/images/mae_learning_rate.png')

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$Efficiency^2$]')
    plt.plot(hist['epoch'], hist['mse'],
             label='Train Error')
    plt.plot(hist['epoch'], hist['val_mse'],
             label='Val Error')
    plt.ylim([0, 1.5])
    plt.legend()
    plt.savefig(dataset_path+'/images/mse_learning_rate.png')


def plot_accuracy_graph(test_predictions, test_labels, dataset_path):
    plt.figure()
    plt.scatter(test_labels, test_predictions)
    plt.xlabel('True Values [Efficiency]')
    plt.ylabel('Predictions [Efficiency]')
    plt.axis('equal')
    plt.axis('square')
    plt.xlim([0, 12])
    plt.ylim([0, 12])
    _ = plt.plot([-100, 100], [-100, 100])
    plt.savefig(dataset_path+'/images/result.png')


def plot_error_count(test_predictions, test_labels, dataset_path):
    plt.figure()
    error = test_predictions - test_labels
    plt.hist(error, bins=25)
    plt.xlabel("Prediction Error [MPG]")
    _ = plt.ylabel("Count")
    plt.savefig(dataset_path+'/images/result2.png')


def build_model(len_ds):
    model_layers = []

    # INPUT LAYER
    model_layers.append(layers.Dense(1024, activation='relu',
                                     input_shape=[len_ds]))
    model_layers.append(layers.Dropout(0.1544360343627376))

    # HIDDEN LAYERS
    model_layers.append(layers.Dense(256, activation='sigmoid'))
    model_layers.append(layers.Dropout(0.1162917162162163))

    model_layers.append(layers.Dense(512, activation='relu'))
    model_layers.append(layers.Dropout(0.1262714506018493))

    # OUPUT LAYERS
    model_layers.append(layers.Dense(1, activation='linear'))

    model = keras.Sequential(model_layers)

    opt = tf.keras.optimizers.Adam(learning_rate=0.0005)
    model.compile(loss='mse',
                  optimizer=opt,
                  metrics=['mae', 'mse',
                           'mape', tf.keras.metrics.RootMeanSquaredError()])
    return model


def train(dataset_path, season):

    dataset_path_file = './data/' + dataset_path + '/join/'
    raw_data = pd.read_csv(dataset_path_file+season+'_data.csv')

    # REMOVES COLUMNS WITH ONLY CONSTANT
    dataset = raw_data.loc[:, (raw_data != raw_data.iloc[0]).any(axis=0)]

    # SHUFFLES DATASET AND DIVIDES IT INTO TRAIN AND TEST
    dataset = dataset.sample(frac=1).reset_index(drop=True)
    train_dataset = dataset.sample(frac=0.9, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    print(test_dataset.mean(axis=0))

    # GET DATASET METRICS (MEAN ,STD)
    train_stats = train_dataset.describe()
    train_stats.pop("Efficiency")
    train_stats = train_stats.transpose()

    # REMOVES LABEL FROM DATASET PREVIOUS NORMALIZATION
    train_labels = train_dataset.pop('Efficiency')
    test_labels = test_dataset.pop('Efficiency')

    # C_mat = train_dataset.corr()
    # fig = plt.figure(figsize=(50, 25))
    # sb.set(font_scale=4)
    # ax = sb.heatmap(C_mat, vmax=1, vmin=-1, square=True, linewidths=.5,
    #            cmap="mako_r", annot_kws={'size': 28})
    #
    # ax.figure.savefig('./images/heat_graph.png', bbox_inches='tight')

    # NORMALIZES DATASET
    normed_train_data = norm(train_dataset, train_stats)
    normed_test_data = norm(test_dataset, train_stats)

    model = build_model(len(train_dataset.keys()))

    EPOCHS = 200
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss',
                                               patience=20)

    history = model.fit(
      normed_train_data, train_labels, batch_size=2,
      epochs=EPOCHS, validation_split=0.2,
      verbose=2, use_multiprocessing=True, callbacks=[early_stop],
      shuffle=1)

    loss, mae, mse, mape, rmse = model.evaluate(normed_test_data,
                                                test_labels,
                                                verbose=2)

    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    print("\n")
    print(hist.tail())

    print("Testing set Mean Abs Error: {:5.2f} Efficiency".format(mae))
    print("Testing set Mean Square Error: {:5.2f} Efficiency".format(mse))
    print("Testing set RMSE: {:5.2f} Efficiency".format(rmse))
    print("Testing set MAPE: {:5.2f} Efficiency".format(mape))

    test_predictions = model.predict(normed_test_data).flatten()

    plot_history(history, dataset_path + '/' + season)
    plot_accuracy_graph(test_predictions, test_labels,
                        dataset_path + '/' + season)
    plot_error_count(test_predictions, test_labels,
                     dataset_path + '/' + season)

    model.save(dataset_path+'/'+season+'/')


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Please, inform the data path and the season. EX: san_francisco")
        exit()

    if not os.path.exists(sys.argv[1]):
        os.mkdir(sys.argv[1])

    if not os.path.exists(sys.argv[1]+'/'+sys.argv[2]):
        os.mkdir(sys.argv[1]+'/'+sys.argv[2])
        os.mkdir(sys.argv[1]+'/'+sys.argv[2]+'/images')

    train(sys.argv[1], sys.argv[2])
