from tensorflow.keras import Sequential
from tensorflow.keras.layers import *
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping
import streamlit as st
import warnings
warnings.filterwarnings("ignore")


def create_dataset(data_input, data_output, size):
    dataset_input = data_input.loc[:, ["GG Compr Press",
                                       "GG Speed Actual",
                                       "GG Inlet Vibr",
                                       "GG Center Vib",
                                       "T1 Avg",
                                       "T2 Avg",
                                       "T3 Avg",
                                       "T4 Avg",
                                       "T5 Avg",
                                       "T6 Avg",
                                       "T7 Avg",
                                       "T8 Avg"]]

    dataset_output = data_output

    scaler = MinMaxScaler(feature_range=(0, 1))

    dataset_input = scaler.fit_transform(dataset_input)
    dataset_output = scaler.fit_transform(dataset_output.reshape(-1, 1))

    train_size = int(len(dataset_input) * size)

    X_train = dataset_input[0:train_size]
    X_test = dataset_input[train_size:len(dataset_input)]
    Y_train = dataset_output[0:train_size]
    Y_test = dataset_output[train_size:len(dataset_input)]

    return X_train, X_test, Y_train, Y_test


def model_lstm(data_input, data_output, size):
    X_train, X_test, Y_train, Y_test = create_dataset(data_input, data_output, size)

    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])

    model = Sequential()
    model.add(LSTM(32, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(LSTM(16, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(8))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error',
                  optimizer='adam',
                  metrics=['accuracy'])
    history = model.fit(X_train,
                        Y_train,
                        validation_data=(X_test, Y_test),
                        epochs=10,
                        batch_size=10,
                        verbose=1,
                        shuffle=False,
                        callbacks=[EarlyStopping(monitor='val_loss', patience=10)])

    return model, history
