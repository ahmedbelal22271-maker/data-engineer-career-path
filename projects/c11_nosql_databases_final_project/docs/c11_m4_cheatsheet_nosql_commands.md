# Quick Reference Cheatsheet: NoSQL Commands & Workflows

**Estimated Study Time:** 8 mins (Deep Comprehension @ 2.5x) | Base Reading: 3 mins

## Overview
This quick-reference cheatsheet aggregates the primary CLI commands, aggregation operators, and syntax patterns used across MongoDB, Apache Cassandra, and IBM Cloudant for the final project and hands-on labs.

---

## 1. Environment & Shell Setup

### Python Virtual Environment:
```bash
# Activate existing virtual environment
source final_project_venv/bin/activate

# Create the environment
python3.11 -m venv final_project_venv
```

---

## 2. IBM Cloudant CLI Utilities

### Installation:
```bash
sudo npm install -g couchimport@1.4.0
```

### Export Data:
```bash
# Export to CSV
couchexport --url $CLOUDANTURL --db <database_name> --delimiter "," > output.csv

# Export to JSONL (Newline-delimited JSON)
couchexport --url $CLOUDANTURL --db <database_name> --type jsonl > output.json
```

---

## 3. MongoDB Commands & Aggregations

### Connecting to MongoDB:
```bash
# WSL Local (Default / No Auth)
mongosh

# WSL Local with Authentication
mongosh -u <user> -p <password> --authenticationDatabase admin
```

### CLI Data Ingestion & Export (WSL Local):
```bash
# Standard Local WSL (Default):
mongoimport --db <db_name> --collection <coll_name> --file <file.json>
mongoexport --db <db_name> --collection <coll_name> --out <file.json>
mongoexport --db <db_name> --collection <coll_name> --out <file.csv> --type=csv --fields field1,field2,field3

# Local WSL with Auth / Host flag:
mongoimport -u <user> -p <password> --authenticationDatabase admin --db <db_name> --collection <coll_name> --file <file.json> --host localhost
mongoexport -u <user> -p <password> --authenticationDatabase admin --db <db_name> --collection <coll_name> --out <file.json> --host localhost
mongoexport -u <user> -p <password> --authenticationDatabase admin --db <db_name> --collection <coll_name> --out <file.csv> --type=csv --fields field1,field2,field3 --host localhost
```

### Interactive Mongosh Queries:
```javascript
// Switch database
use entertainment;

// Create collection
db.createCollection("movies");

// Filter and count documents
db.movies.countDocuments({ year: { $gt: 1999 } });

// Group, count, sort, and limit (Top year by release count)
db.movies.aggregate([
  { $group: { _id: "$year", movieCount: { $sum: 1 } } },
  { $sort: { movieCount: -1 } },
  { $limit: 1 }
]);

// Match criteria and compute average
db.movies.aggregate([
  { $match: { year: 2007 } },
  { $group: { _id: "$year", averageVotes: { $avg: "$Votes" } } }
]);

db.dropDatabase()

use entertainment

show collections

```

---

## 4. Apache Cassandra & CQL Commands

### Connecting via CQLSH:
```bash
cqlsh --username <user> --password <password>
```

### Keyspace & Table DDL:
```sql
-- Create Keyspace
CREATE KEYSPACE IF NOT EXISTS entertainment
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE entertainment;

-- Create Table Schema
CREATE TABLE IF NOT EXISTS movies (
    _id text PRIMARY KEY,
    title text,
    year text,
    rating text,
    director text
);
```

### Bulk Import & Export via `COPY`:
```sql
-- Ingest CSV dataset
COPY entertainment.movies(_id, title, year, rating, director)
FROM 'partial_data.csv'
WITH DELIMITER=',' AND HEADER=TRUE;

-- Export table to CSV
COPY movies TO 'cassandra-movies.csv';
```

### Querying & Secondary Indexing:
```sql
-- Count total rows
SELECT COUNT(*) FROM movies;

-- Create Secondary Index on non-partition column
CREATE INDEX IF NOT EXISTS movies_rating_idx ON entertainment.movies (rating);

-- Filtered query on indexed column
SELECT COUNT(*) FROM movies WHERE rating = 'G';
```
