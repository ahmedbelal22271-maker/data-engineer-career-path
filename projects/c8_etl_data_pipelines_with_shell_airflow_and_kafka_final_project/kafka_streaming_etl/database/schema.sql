-- Database Schema Definition for Toll Traffic Data
-- Course 8 Final Project: Streaming ETL Pipeline using Kafka & MySQL

CREATE DATABASE IF NOT EXISTS tolldata;
USE tolldata;

DROP TABLE IF EXISTS livetolldata;

CREATE TABLE livetolldata (
    timestamp DATETIME,
    vehicle_id INT,
    vehicle_type VARCHAR(15),
    toll_plaza_id INT
);

-- Index for timestamp query performance
CREATE INDEX idx_livetolldata_timestamp ON livetolldata (timestamp);
