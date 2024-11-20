-- Drop all tables if they already exist
DROP TABLE IF EXISTS GraphData;
DROP TABLE IF EXISTS GraphLink;

-- Create all tables
CREATE TABLE GraphData (
    ticker TEXT,
    actual TEXT,
    date DATE,
    value REAL NOT NULL,
    days INTEGER NOT NULL,
    PRIMARY KEY (ticker, actual, date)
);

CREATE TABLE GraphLink (
    ticker TEXT PRIMARY KEY,
    link TEXT
)