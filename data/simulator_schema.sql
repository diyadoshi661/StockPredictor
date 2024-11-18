-- Drop all tables if they already exist
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Portfolio;
DROP TABLE IF EXISTS Transactions;

-- Create all tables

-- Stores all users
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    balance REAL DEFAULT 1000.00
);

-- Stores assets owned by each user
CREATE TABLE Portfolio (
    user_id INTEGER,
    stock_symbol TEXT,
    quantity_owned INTEGER,
    PRIMARY KEY (user_id, stock_symbol),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Stores 5 most recent transactions for each user
CREATE TABLE Transactions (
    user_id INTEGER,
    stock_symbol TEXT,
    action TEXT,
    quantity INTEGER,
    price REAL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, time),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);