import sqlite3
import yfinance as yf

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

# Connect to database for predictor
connection = sqlite3.connect('data/predictor_database.db')
cur = connection.cursor()

# Remove all data
cur.execute('DELETE FROM GraphData')

# Updates values in database for all tickers
upload_data('AAPL')
upload_data('AMZN')
upload_data('GOOGL')
upload_data('MSFT')
upload_data('NVDA')

connection.commit()
connection.close()

# # Connect to database for simulator
# connection = sqlite3.connect('data/simulator_database.db')
# cur = connection.cursor()

# # Execute statements here

# connection.commit()
# connection.close()