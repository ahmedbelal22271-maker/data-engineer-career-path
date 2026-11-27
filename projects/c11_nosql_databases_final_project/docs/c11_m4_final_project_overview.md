# Final Project Overview

**Estimated Study Time:** 13 mins (Deep Comprehension @ 2.5x) | Base Reading: 5 mins

## Overview & Scenario

Welcome to the capstone final project for **NoSQL Databases with MongoDB and Apache Cassandra**.

In this project, you apply the practical database administration and querying skills acquired throughout the course to a realistic consulting scenario. You assume the role of a **Data Engineer at a data analytics consulting firm**, supporting data analysts by managing, transforming, denormalizing, and querying datasets across heterogeneous NoSQL platforms.

---

## Project Structure & Exercises

The project takes approximately 60 minutes to execute and is divided into **two primary exercises** encompassing 10 technical tasks:

### Exercise 1: Semi-Structured Data Management with MongoDB
- **Task 1:** Ingest `movies.json` into the `entertainment` database within the `movies` collection.
- **Task 2:** Construct an aggregation pipeline to find the year in which the highest number of movies were released.
- **Task 3:** Write a query to count the total number of movies released after 1999.
- **Task 4:** Calculate the average vote count for movies released in the year 2007.
- **Task 5:** Export designated fields (`_id`, `title`, `year`, `rating`, `Director`) into `partial_data.csv`.

### Exercise 2: Distributed Data Management with Apache Cassandra
- **Task 6:** Create the `entertainment` keyspace with appropriate replication parameters.
- **Task 7:** Ingest `partial_data.csv` into Cassandra within the `movies` table.
- **Task 8:** Construct a CQL query to count total rows in the `movies` table.
- **Task 9:** Create a secondary index on the `rating` column in the `movies` table.
- **Task 10:** Execute a filtered query to count all movies rated `G`.

---

## Deliverables & Evidence Collection
While performing the tasks, document each executed command and its corresponding output or screenshot for project submission and evaluation.

---

## Authors & Acknowledgements
- **Author:** Niveditha Pandith TS (IBM Skills Network)
- *© IBM Corporation. All rights reserved.*