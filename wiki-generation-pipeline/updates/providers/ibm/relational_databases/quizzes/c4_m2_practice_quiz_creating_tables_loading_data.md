> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 2:** Creating Tables and Loading Data & Designing Keys, Indexes, and Constraints
> **Quiz:** Practice Quiz — Creating Tables and Loading Data

# Practice Quiz: Creating Tables and Loading Data

**Due:** Jul 13, 11:59 PM EEST  
**Attempts:** Unlimited (not scored)

---

## Question 1

**True or False:** Utilizing INSERT statements for large data volumes is inefficient.

- True
- False

**Correct answer: True**

[ENRICHED: explanation — INSERT statements are row-by-row DML operations that log each row to the transaction log, fire any per-row triggers, and incur network round-trips per statement (or per batch). For large data volumes (hundreds of thousands of rows or more), bulk load utilities (Db2 LOAD, PostgreSQL COPY, MySQL LOAD DATA INFILE) are far more efficient because they operate at the page level, bypass the SQL engine, and minimize logging. See `lessons/c4_m2_loading_data.md` for the detailed INSERT vs. bulk load comparison.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **False** (incorrect) | INSERT is a reasonable choice for a few rows during development/testing, but the question specifies "large data volumes," where INSERT becomes impractical due to per-row overhead, logging, and network latency. The course explicitly states: "it's often not practical to use this method to load hundreds or thousands of rows of data." |

---

## Question 2

**Which information is essential to gather before creating a table?**

- Whether to permit duplicate values in each column
- Whether to allow null values in each column
- The table's name
- All of the above

**Correct answer: All of the above**

[ENRICHED: explanation — Before creating a table, you need to define the table name, column names, data types, nullability (whether NULL values are allowed), and uniqueness constraints (whether duplicate values are permitted). These decisions affect data integrity, storage, and indexing from the moment the first row is inserted. See `lessons/c4_m2_creating_tables.md` for the full list of key considerations.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Whether to permit duplicate values** (incomplete) | This is part of the consideration (choosing PRIMARY KEY, UNIQUE constraints), but it is not the only essential information needed. |
| **Whether to allow null values** (incomplete) | Nullability is important for mandatory vs. optional fields, but it is not the only requirement. |
| **The table's name** (incomplete) | A table name is required syntax for CREATE TABLE, but you also need column definitions. |
| **All of the above** (correct) | The course lists choosing the location (schema), table name, column names, data types, nullability, and duplicate-value considerations as essential pre-creation information. |

---

## Question 3

**Which of the following data movement scenarios is beneficial for disaster recovery purposes?**

- Generate a snapshot of the current database state
- Add or append data
- Create a working copy of the database
- Initial populating of the entire database

**Correct answer: Generate a snapshot of the current database state**

[ENRICHED: explanation — For disaster recovery (DR), you need a point-in-time copy (snapshot or backup) of the database that can be restored if the primary database fails or data is corrupted. A snapshot preserves the database state at a specific moment, enabling recovery to that point. See `lessons/c4_m2_data_movement_utilities.md` for backup/restore strategies including RPO (Recovery Point Objective) and RTO (Recovery Time Objective).]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Generate a snapshot** (correct) | A snapshot/backup captures the database state for recovery. This is the primary DR mechanism. |
| **Add or append data** (incorrect) | Appending data is a routine data-loading operation, not a DR scenario. |
| **Create a working copy** (incorrect) | A working copy is for development/testing, not recovery from disaster. |
| **Initial populating** (incorrect) | Initial population loads data into a new database, which is unrelated to disaster recovery. |

---

## Question 4

**What must appear immediately after the keywords CREATE TABLE in a SQL statement?**

- Table name
- Primary key
- Datatypes
- Entities

**Correct answer: Table name**

[ENRICHED: explanation — The syntax is `CREATE TABLE table_name (...);` The table name is the **required** element immediately after `CREATE TABLE`. Column definitions (including data types, primary keys, and constraints) follow inside parentheses after the table name. See `lessons/c4_m2_create_table_statement.md` for the full syntax grammar.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Table name** (correct) | Required syntax: `CREATE TABLE <table_name> (<column_definitions>);` |
| **Primary key** (incorrect) | Primary key is part of the column/table constraint definitions inside the parentheses, not immediately after CREATE TABLE. |
| **Datatypes** (incorrect) | Data types are specified per column inside the parentheses, after the column names. |
| **Entities** (incorrect) | "Entities" is an ERD concept, not a SQL keyword. Entities become table names in the relational model. |

---

## Question 5

**Which of the following commonly used DDL statements helps alter data types?**

- TRUNCATE
- CREATE
- DROP
- ALTER

**Correct answer: ALTER**

[ENRICHED: explanation — The `ALTER TABLE` statement with the `ALTER COLUMN` clause (or `MODIFY COLUMN` in MySQL) is used to change a column's data type. For example: `ALTER TABLE author ALTER COLUMN telephone_number SET DATA TYPE CHAR(20);` See `lessons/c4_m2_alter_drop_truncate_tables.md` for type modification syntax across Db2, PostgreSQL, and MySQL.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **TRUNCATE** (incorrect) | TRUNCATE removes all rows from a table but does not alter the table structure or data types. |
| **CREATE** (incorrect) | CREATE defines new objects (tables, views, indexes). It cannot alter existing columns. |
| **DROP** (incorrect) | DROP removes entire objects (tables, views). It does not modify columns. |
| **ALTER** (correct) | ALTER TABLE is the DDL statement specifically designed for modifying existing table structures, including column data types, adding/dropping columns, and managing constraints. |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Explanation | Connected INSERT inefficiency to bulk load comparison from Loading Data lesson | HIGH |
| 2 | Q2 | Explanation | Connected table creation considerations to Creating Tables lesson | HIGH |
| 3 | Q3 | Explanation | Connected snapshot/DR scenario to backup/restore strategies and RPO/RTO | HIGH |
| 4 | Q4 | Explanation | Connected CREATE TABLE syntax to CREATE TABLE Statement lesson with grammar reference | HIGH |
| 5 | Q5 | Explanation | Connected ALTER COLUMN type modification to ALTER/DROP/TRUNCATE lesson with cross-database syntax | HIGH |
