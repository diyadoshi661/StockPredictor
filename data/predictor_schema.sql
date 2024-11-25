-- Drop all tables if they already exist
DROP TABLE IF EXISTS GraphData;
DROP TABLE IF EXISTS GraphPrediction;

-- Create all tables
CREATE TABLE GraphData (
    ticker TEXT,
    date DATE,
    value REAL NOT NULL,
    days INTEGER NOT NULL,
    PRIMARY KEY (ticker, date)
);

CREATE TABLE GraphPrediction (
    ticker TEXT PRIMARY KEY,
    value REAL NOT NULL
);