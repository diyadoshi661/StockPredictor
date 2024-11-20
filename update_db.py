import sqlite3
import yfinance as yf

# Imports for machine learning and graphing
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf

# Import custom modules
from data_module import *

def upload_data(ticker):
    """Uploads actual values in database for given ticker
        to be current"""
    # Load dataframe
    data = yf.download(ticker, start='2010-01-01')
    df = data.reset_index()
    # Convert date to days
    df['Days'] = (df['Date'] - df['Date'].min()).dt.days
    # Convert to list of tuples to be inserted
    tuples = [tuple([ticker, 't', row['Date'].iloc[0].strftime('%Y-%m-%d'), row['Close'].iloc[0], row['Days'].iloc[0]]) for index, row in df.iterrows()]
    cur.executemany('INSERT INTO GraphData VALUES (?, ?, ?, ?, ?)', tuples)

def upload_graph_link(ticker):
    """Uploads link to prediction graph to be displayed"""
    link = prediction_graph(ticker)
    cur.execute('INSERT INTO GraphLink VALUES (?, ?)', (ticker, link))

# TODO: Update ML algorithm to Random Forest
def predict_trend(ticker):
    """Predicts stock trends using LSTM"""
    start_date = '2010-01-01'
    stock_data = yf.download(tickers = ticker, start = start_date)
    # Remove secondary column header
    stock_data.columns = stock_data.columns.droplevel(1)
    # We don't want date as index
    stock_data = stock_data.reset_index()
    # Convert date to days
    stock_data['Days'] = (stock_data['Date'] - stock_data['Date'].min()).dt.days
    # Adjust Date to exclude time
    stock_data['Date'] = stock_data['Date'].dt.date
    # Reset name of columns
    stock_data.columns.name = ""
    
    # Create moving averages
    stock_data['moving_avg100'] = stock_data.Close.rolling(window=100).mean()
    stock_data['moving_avg200'] = stock_data.Close.rolling(window=200).mean()

    # Split into training, validation, and testing
    data_training = pd.DataFrame(stock_data['Close'][0:int(len(stock_data)*0.80)])
    data_validation = pd.DataFrame(stock_data['Close'][int(len(stock_data)*0.80):int(len(stock_data)*0.90)])
    data_testing = pd.DataFrame(stock_data['Close'][int(len(stock_data)*0.90):int(len(stock_data))])

    data_training_arr = np.array(data_training['Close'] / stock_data['Close'].max())
    data_validation_arr = np.array(data_validation['Close'] / stock_data['Close'].max())
    data_testing_arr = np.array(data_validation['Close'] / stock_data['Close'].max())

    # Prepare training data
    x_train = [] #100 val
    y_train = [] #101 val
    for i in range(100, data_training_arr.shape[0]):
        x_train.append(data_training_arr[i-100:i])
        y_train.append(data_training_arr[i])
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Prepare validation data
    x_validation = []
    y_validation = []
    for i in range(100, data_validation_arr.shape[0]):
        x_validation.append(data_validation_arr[i-100:i])
        y_validation.append(data_validation_arr[i])
    x_validation, y_validation = np.array(x_validation), np.array(y_validation)

    # Prepare testing data
    x_test = []
    y_test = []
    for i in range(100, data_testing_arr.shape[0]):
        x_test.append(data_testing_arr[i-100:i])
        y_test.append(data_testing_arr[i])
    x_test, y_test = np.array(x_test), np.array(y_test)

    # Train model
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(units=50, activation='tanh', return_sequences=True, input_shape=(x_train.shape[1], 1)),
        tf.keras.layers.LSTM(units=60, activation='tanh', return_sequences=True),
        tf.keras.layers.LSTM(units=80, activation='tanh', return_sequences=True),
        tf.keras.layers.LSTM(units=80, activation='tanh'),
        tf.keras.layers.Dense(units=1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    NUM_EPOCHS = 10
    history = model.fit(
        x_train, y_train,
        epochs=NUM_EPOCHS,
        validation_data=(x_validation, y_validation),
        batch_size=32,  # Adjust batch size if needed
        verbose=1,  # Controls the output display (1 for progress bar)
        callbacks=[early_stopping]  # Optional early stopping
    )

    y_predicted = model.predict(x_test)

    y_predicted = y_predicted * stock_data['Close'].max()

    return y_predicted

def upload_prediction(ticker):
    """Loads predicted values into database to be graphed later"""
    data = predict_trend(ticker)
    tuples = [tuple([ticker, 'f', float(data[index].item()), index]) for index in range(len(data))]
    cur.executemany('INSERT INTO GraphData (ticker, actual, value, days) VALUES (?, ?, ?, ?)', tuples)

# Connect to database for predictor
connection = sqlite3.connect('data/predictor_database.db')
cur = connection.cursor()

# Remove all data
cur.execute('DELETE FROM GraphData')
cur.execute('DELETE FROM GraphLink')

# Updates actual values in database for all tickers
upload_data('AAPL')
upload_data('AMZN')
upload_data('GOOGL')
upload_data('MSFT')
upload_data('NVDA')

# Updates predicted values in database for all tickers
# upload_prediction('AAPL')
# upload_prediction('AMZN')
# upload_prediction('GOOGL')
# upload_prediction('MSFT')
# upload_prediction('NVDA')

# Update links to graphs for all tickers
upload_graph_link('AAPL')
upload_graph_link('AMZN')
upload_graph_link('GOOGL')
upload_graph_link('MSFT')
upload_graph_link('NVDA')

connection.commit()
connection.close()

# # Connect to database for simulator
# connection = sqlite3.connect('data/simulator_database.db')
# cur = connection.cursor()

# # Execute statements here

# connection.commit()
# connection.close()