import sqlite3
import yfinance as yf

# Connect to database for predictor
connection = sqlite3.connect('data/predictor_database.db')
cur = connection.cursor()

# Remove all data
cur.execute('DELETE FROM GraphData')

# Apple dataframe
apple_data = yf.download('AAPL', start='2010-01-01')
apple_df = apple_data.reset_index()
apple_df['Days'] = (apple_df['Date'] - apple_df['Date'].min()).dt.days # Convert date to days
# Convert to list of tuples to be inserted
apple_tuples = [tuple([('APPL'), 't', row['Date'].iloc[0].strftime('%Y-%m-%d'), row['Close'].iloc[0], row['Days'].iloc[0]]) for index, row in apple_df.iterrows()]
cur.executemany('INSERT INTO GraphData VALUES (?, ?, ?, ?, ?)', apple_tuples)

connection.commit()
connection.close()

# # Connect to database for simulator
# connection = sqlite3.connect('data/simulator_database.db')
# cur = connection.cursor()

# # Execute statements here

# connection.commit()
# connection.close()