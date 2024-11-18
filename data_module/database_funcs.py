import sqlite3

def get_predictor_db():
    conn = sqlite3.connect('data/predictor_database.db')
    conn.row_factory = sqlite3.Row
    return conn