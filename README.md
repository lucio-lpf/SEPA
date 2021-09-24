# SEPA: Solar Energy Prediction Application

This project uses Deep Neural Networks (DNN) to predict solar energy generation. We use open data from solar panel community owners and historical weather information to train our machine learning model. Instead of analyzing a single PV System, our approach uses multiple data sources, combining several PV systems to compose our dataset.

Our project can be used for:

    i) creating a neural network to analyze PV energy generation;
    ii) analyzing the impact that a new system will have in that region;
    iii) predicting the regional next-day energy generation by using weather forecasting;


## Installation:

  You will need to download this repository and install the following libs to run our project:

    Python (3.6.9)
    TensorFlow (2.7.0)
    seaborn (0.11.1)
    Hyperas (0.4.1)
    hypeorpt (0.2.5)
    Pandas (1.1.5)
    Numpy (1.19.5)

## Using it:

### Running the Neural Network:
Simply run the neural_network.py script informing the path to your dataset. E.g.

    python3 neural_network.py ./data/join/summer_data.csv

Successful execution will save a model of the created neural network.

### Running hyperas hyper-parameters analysis:

Run hypera_select.py script informing the path to your dataset. E.g.

    python3 hypera_select.py ./data/join/summer_data.csv

The program will output a set of values. E.g:

    {'Dense': 2, 'Dense_1': 0, 'Dense_2': 2, 'Dropout': 0.002306486013380127, 'Dropout_1': 0.129745456686155, 'Dropout_2': 0.4482920922182265, 'Dropout_3': 0, 'Dropout_4': 0.5384236484916557, 'activation': 0, 'activation_1': 1, 'activation_2': 2, 'activation_3': 1, 'batch_size': 0, 'optimizer': 0}

You can update the neural_network.py file with this new hyper-parameters values.
More about how it works on: https://github.com/maxpumperla/hypera

### Running a new system prediction:

After running the neural network step, a model will be saved for future analises.

You can use this model for evaluating how a configuration of a new PV System. Just run the script new_system_prediction.py passing as param the dataset location. E.g.

    python3 new_system_prediction.py ./data/join/new_system.csv

 This dataset needs to have the same features as the ones used for training the model. You can create a configuration and combine it with the weather information of a PV system used previously. Check the data folder.

 The script will output a graph depicting how the created system would behave along the time. E.g.

![new_system](https://user-images.githubusercontent.com/8583169/134723268-2d47b534-f622-4bfb-9eec-38457a3b4d87.png)
