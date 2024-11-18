-- Drop all tables if they already exist
DROP TABLE IF EXISTS GraphData;

-- Create all tables
CREATE TABLE GraphData (
    ticker TEXT,
    actual TEXT,
    date DATE,
    value REAL NOT NULL,
    days INTEGER NOT NULL,
    PRIMARY KEY (ticker, actual, date)
);