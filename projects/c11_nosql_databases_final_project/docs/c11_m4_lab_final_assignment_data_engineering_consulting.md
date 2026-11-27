# Hands-on Lab: Final Assignment — Data Engineering for a Consulting Firm

**Estimated Study Time:** 113 mins (Deep Comprehension @ 2.5x) | Hands-on Capstone Base: 45 mins

## Scenario & Objectives

You are a **Data Engineer at a data analytics consulting company**. Analysts in your office rely on you to ingest raw data from external sources, perform schema design and transformations across multiple NoSQL database engines (MongoDB and Apache Cassandra), export filtered subsets, and run optimized queries.

In this capstone assignment, you will:
1. Start and authenticate against **MongoDB** and **Apache Cassandra** services in the Cloud IDE or local WSL.
2. Ingest `movies.json` into MongoDB (`entertainment.movies`).
3. Construct MongoDB aggregation pipelines and filtering queries.
4. Export designated movie fields into CSV (`partial_data.csv`).
5. Create the `entertainment` keyspace and `movies` table in Apache Cassandra.
6. Ingest `partial_data.csv` into Cassandra via `cqlsh` `COPY`.
7. Create secondary indexes in Cassandra and execute filtered queries.

---

## Required Screenshot Submission Checklist

| Task | Deliverable Description | Mandatory Screenshot Evidence |
|---|---|---|
| **Task 1** | MongoDB Ingestion | Screenshot showing `mongoimport` command and terminal output confirming document ingestion into `entertainment.movies`. |
| **Task 5** | MongoDB CSV Export | Screenshot showing `mongoexport` command and terminal output exporting 5 designated fields into `partial_data.csv`. |
| **Task 6** | Cassandra Keyspace Creation | Screenshot showing `CREATE KEYSPACE entertainment` and `DESCRIBE KEYSPACE entertainment` output. |
| **Task 7** | Cassandra Table Schema & Ingestion | Screenshot showing `CREATE TABLE movies` and `COPY FROM` command with terminal output. |
| **Task 9** | Cassandra Secondary Index | Screenshot showing `CREATE INDEX` on `rating` and `DESCRIBE TABLE movies` showing the index listed in schema metadata. |

---

## Environment Setup & Service Initialization

### 1. Start MongoDB Service
- **WSL / Local Environment:**
  ```bash
  sudo service mongodb start
  # or with systemd:
  sudo systemctl start mongod
  ```
- **Coursera Cloud IDE:** Navigate to **Skills Network Toolbox**, select **MongoDB**, click **Start**, note password, and connect:
  ```bash
  mongosh -u root -p <PASSWORD> --authenticationDatabase admin local
  ```
- Initialize context:
  ```javascript
  use entertainment;
  db.createCollection("movies");
  ```

### 2. Start Apache Cassandra Service
- **WSL / Local Environment:**
  ```bash
  sudo service cassandra start
  cqlsh
  ```
- **Coursera Cloud IDE:** Select **Cassandra** in Toolbox, click **Start**, note password, and connect:
  ```bash
  cqlsh --username cassandra --password <PASSWORD>
  ```

---

## Exercise 1: Working with MongoDB

### Download Sample Dataset
Download `movies.json` into your working project directory:

```bash
curl -O https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DB0151EN-edX/labs/FinalProject/movies.json
```

#### Sample Movie Document Structure:
```json
{
  "_id": "9",
  "title": "The Lost City of Z",
  "genre": "Action,Adventure,Biography",
  "Description": "A true-life drama, centering on British explorer Col. Percival Fawcett...",
  "Director": "James Gray",
  "Actors": "Charlie Hunnam, Robert Pattinson, Sienna Miller, Tom Holland",
  "year": 2016,
  "Runtime (Minutes)": 141,
  "rating": "unrated",
  "Votes": 7188,
  "Revenue (Millions)": 8.01,
  "Metascore": 78
}
```

---

### Task 1: Ingest `movies.json` into MongoDB

> [!IMPORTANT]
> **Mandatory Screenshot Requirement:**  
> Take a clear screenshot of the command you used and its output showing successful ingestion into the `entertainment` database and `movies` collection.

**Local WSL Command (No Auth):**
```bash
mongoimport --db entertainment --collection movies --file movies.json
```

**Coursera Cloud IDE / Authenticated Command:**
```bash
mongoimport -u root -p <PASSWORD> --authenticationDatabase admin --db entertainment --collection movies --file movies.json --host mongo
```

---

### Task 2: Find the Year with the Highest Number of Movies Released
Execute an aggregation pipeline to group movies by release year, calculate total movie counts per year, sort descending, and return the top year:

```javascript
use entertainment;

db.movies.aggregate([
  {
    $group: {
      _id: "$year",
      movieCount: { $sum: 1 }
    }
  },
  {
    $sort: { movieCount: -1 }
  },
  {
    $limit: 1
  }
]);
```

---

### Task 3: Count Movies Released After 1999
Count all movie documents where the `year` field is strictly greater than 1999:

```javascript
use entertainment;

db.movies.countDocuments({ year: { $gt: 1999 } });
// Or via find query:
db.movies.find({ year: { $gt: 1999 } }).count();
```
*Expected Output:* `99`

---

### Task 4: Calculate Average Votes for Movies Released in 2007
Filter for movies released in 2007 and compute the mean vote count using `$avg`:

```javascript
use entertainment;

db.movies.aggregate([
  {
    $match: { year: 2007 }
  },
  {
    $group: {
      _id: "$year",
      averageVotes: { $avg: "$Votes" }
    }
  }
]);
```
*Expected Output:* Average votes of `192.5`

---

### Task 5: Export Filtered Movie Fields to CSV

> [!IMPORTANT]
> **Mandatory Screenshot Requirement:**  
> Take a clear screenshot of the command you used and its output displaying the export of fields `_id`, `title`, `year`, `rating`, and `Director` into `partial_data.csv`.

**Local WSL Command:**
```bash
mongoexport --db entertainment --collection movies --out partial_data.csv --type=csv --fields _id,title,year,rating,Director
```

**Coursera Cloud IDE / Authenticated Command:**
```bash
mongoexport -u root -p <PASSWORD> --authenticationDatabase admin --db entertainment --collection movies --out partial_data.csv --type=csv --fields _id,title,year,rating,Director --host mongo
```

---

## Exercise 2: Working with Apache Cassandra

### Download Backup Dataset (If Needed)
If you need the pre-generated CSV file, download it via `curl`:

```bash
curl -O https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DB0151EN-edX/labs/FinalProject/partial_data.csv
```

---

### Task 6: Create the `entertainment` Keyspace

> [!IMPORTANT]
> **Mandatory Screenshot Requirement:**  
> Take a clear screenshot of the `CREATE KEYSPACE` command along with `DESCRIBE KEYSPACE entertainment;` output.

Connect to `cqlsh` and instantiate the `entertainment` keyspace:

```sql
CREATE KEYSPACE IF NOT EXISTS entertainment
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

DESCRIBE KEYSPACE entertainment;
```

---

### Task 7: Create Table and Ingest `partial_data.csv`

> [!IMPORTANT]
> **Mandatory Screenshot Requirement:**  
> Take a clear screenshot of the `CREATE TABLE` command and the `COPY FROM` execution output confirming imported rows.

#### Step 1: Define Table Schema
Create the `movies` table with all text/varchar columns:

```sql
USE entertainment;

CREATE TABLE IF NOT EXISTS movies (
    "_id" text PRIMARY KEY,
    title text,
    year text,
    rating text,
    director text
);
```

#### Step 2: Import CSV Data via `COPY FROM`
Ingest the exported CSV into Cassandra:

```sql
USE entertainment;

COPY entertainment.movies(_id, title, year, rating, director)
FROM 'partial_data.csv'
WITH DELIMITER=',' AND HEADER=TRUE;
```

---

### Task 8: Count Total Rows in `movies` Table
Query the total row count across all partitions:

```sql
USE entertainment;

SELECT COUNT(*) FROM movies;
```

---

### Task 9: Create Secondary Index on `rating` Column

> [!IMPORTANT]
> **Mandatory Screenshot Requirement:**  
> Take a clear screenshot of the `CREATE INDEX` command and the subsequent `DESCRIBE TABLE movies;` output displaying `CREATE INDEX` in the schema metadata.

Create a secondary index to enable equality filtering on the non-primary key column `rating`:

```sql
USE entertainment;

CREATE INDEX IF NOT EXISTS movies_rating_idx
ON entertainment.movies (rating);

DESCRIBE TABLE movies;
```

---

### Task 10: Count Movies with 'G' Rating
Execute a filtered count query utilizing the secondary index on `rating`:

```sql
USE entertainment;

SELECT COUNT(*) FROM movies WHERE rating = 'G';
```

---

## Authors & Acknowledgements
- **Author:** [Muhammad Yahya](https://www.linkedin.com/in/1muhammadyahya/)
- *© IBM Corporation. All rights reserved.*