-- Drop all tables if they already exist
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Portfolio;
DROP TABLE IF EXISTS Transactions;

DROP TRIGGER IF EXISTS Create_Portfolio;

-- Create all tables

-- Stores all users
CREATE TABLE Users (
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    balance REAL DEFAULT 1000.00
);

-- Stores assets owned by each user
CREATE TABLE Portfolio (
    username TEXT,
    stock_symbol TEXT,
    quantity_owned INTEGER,
    PRIMARY KEY (username, stock_symbol),
    FOREIGN KEY (username) REFERENCES Users(username)
);

-- Stores 10 most recent transactions for each user
CREATE TABLE Transactions (
    username TEXT,
    stock_symbol TEXT,
    action TEXT,
    quantity INTEGER,
    price REAL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username, time),
    FOREIGN KEY (username) REFERENCES Users(username)
);

-- Create trigger
CREATE TRIGGER Create_Portfolio AFTER INSERT
ON Users
BEGIN
    INSERT INTO Portfolio (username, stock_symbol, quantity_owned) 
    VALUES (NEW.username, 'AAPL', 0),
           (NEW.username, 'AMZN', 0),
           (NEW.username, 'GOOGL', 0),
           (NEW.username, 'MSFT', 0),
           (NEW.username, 'NVDA', 0);
END;