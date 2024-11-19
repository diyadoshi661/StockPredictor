import sqlite3

def get_predictor_db():
    """Returns a connection to the database containing all 
        actual and predicted values for each company"""
    conn = sqlite3.connect('data/predictor_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_simulator_db():
    """Returns a connection to the database containing all
        information about each user and their individual simulations"""
    conn = sqlite3.connect('data/simulator_database.db')
    conn.row_factory = sqlite3.Row
    return conn