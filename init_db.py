import sqlite3

# Create database for predictor
connection = sqlite3.connect('data/predictor_database.db')

with open('data/predictor_schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()

# Create database for simulator
connection = sqlite3.connect('data/simulator_database.db')

with open('data/simulator_schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()