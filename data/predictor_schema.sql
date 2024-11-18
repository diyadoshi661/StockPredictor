-- Drop all tables if they already exist
DROP TABLE IF EXISTS Predictions;

-- Create all tables
CREATE TABLE Predictions (
    date TIMESTAMP PRIMARY KEY,
    value REAL NOT NULL
);