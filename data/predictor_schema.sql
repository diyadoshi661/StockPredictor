-- Drop all tables if they already exist
DROP TABLE IF EXISTS PredictionData;
DROP TABLE IF EXISTS StockData;

-- Create all tables
CREATE TABLE PredictionData (
    date TIMESTAMP PRIMARY KEY,
    value REAL NOT NULL
);

CREATE TABLE StockData (
    date TIMESTAMP PRIMARY KEY,
    value REAL NOT NULL
);