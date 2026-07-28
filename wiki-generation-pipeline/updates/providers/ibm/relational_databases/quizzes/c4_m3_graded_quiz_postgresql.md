<mark style="background-color: rgba(200, 230, 201, 0.4);">NEW</mark>

> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 3:** MySQL and PostgreSQL
> **Quiz:** Graded Quiz — PostgreSQL

# Graded Quiz: PostgreSQL

**Due:** Jul 20, 11:59 PM EEST  
**Attempts:** 3 (every 8 hours)  
**Pass required:** Yes

---

## Question 1

**Which pgAdmin feature can you use to design an ERD and generate SQL to create the database objects?**

- psql
- ERD Tool
- Query Tool
- pgAdmin

**Correct answer: ERD Tool**

[ENRICHED: explanation — The pgAdmin **ERD Tool** (shortcut: Tools → ERD Tool) provides a visual canvas for designing Entity-Relationship Diagrams. You can create tables, define columns and data types, set primary/foreign keys, establish relationships, and add notations. Once the design is complete, the ERD Tool can **generate SQL** (DDL statements) to create the corresponding database objects. This is distinct from the **Query Tool** (which is for running ad-hoc SQL queries) and **psql** (the command-line interface). pgAdmin is the overall application, not a specific feature. See `module_3_mysql_and_postgresql/c4_m3_getting_started_with_postgresql.md` for the full pgAdmin tool breakdown including the ERD Tool's ability to reverse-engineer ERDs from existing databases, auto-layout tables, and export to SQL/image/PDF.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **psql** | The PostgreSQL CLI — text-based, no visual ERD design capability |
| **ERD Tool** (correct) | pgAdmin's visual ERD designer with SQL generation — the only option that combines both ERD design and DDL generation |
| **Query Tool** | Runs SQL queries and displays results — no ERD design or code generation |
| **pgAdmin** | The overall database administration platform — not a specific feature for ERD design |

---

## Question 2

**When using the pgAdmin Restore command, which of the following items can you regenerate in the database? (Select three)**

- Tables
- Passwords
- Data
- Data types

**Correct answers: Tables, Data, Data types**

[ENRICHED: explanation — The pgAdmin **Restore** command (backed by `pg_restore`) can regenerate **Tables** (the schema structure), **Data** (the row content), and **Data types** (custom or extension-defined types). These are the three components captured in a pg_dump backup file. **Passwords** are NOT stored in database dumps — PostgreSQL passwords are stored in the `pg_authid` system catalog (hashed), which is part of the cluster-wide global objects. To back up passwords (roles/users), you need `pg_dumpall --globals-only` or manual extraction from `pg_shadow`/`pg_authid`. See `module_3_mysql_and_postgresql/c4_m3_creating_databases_loading_data_postgresql.md` for the full pg_dump/pg_restore workflow with format options (plain SQL, custom, directory, tar) and the Restore dialog's Data Options and Structure tabs.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Tables** (correct) | Table schemas (columns, constraints, indexes) are restored — they are the primary structure objects in a dump |
| **Passwords** | Not included in database-level dumps — role passwords are cluster-wide objects backed up separately via pg_dumpall |
| **Data** (correct) | Row data from tables is restored when the Data toggle is enabled in the Restore dialog |
| **Data types** (correct) | Custom data types (CREATE TYPE), enums, domains, and extension-provided types are restored as schema objects |

---

## Question 3

**What is the main difference between regular views and materialized views?**

- You can save regular views for future use
- Regular views can improve performance
- Regular views don't store data; materialized views store query results.
- You can store regular views in memory

**Correct answer: Regular views don't store data; materialized views store query results.**

[ENRICHED: explanation — The fundamental distinction between regular (standard) views and materialized views in PostgreSQL is **data persistence**. A **regular view** is a virtual table defined by a stored SQL query — every time you query it, the database re-executes the underlying query against the base tables. No data is stored; it is always current but can be slow for expensive queries. A **materialized view** physically stores the query result on disk on the first execution, acting like a snapshot table. It must be refreshed (`REFRESH MATERIALIZED VIEW`) to reflect changes in underlying data. This makes materialized views faster to read (no re-execution) but potentially stale. See `module_3_mysql_and_postgresql/c4_m3_views_postgresql.md` for the 8-dimension comparison (storage, freshness, refresh mechanism, indexing, performance, concurrency, use cases, DML support) and REFRESH MATERIALIZED VIEW CONCURRENTLY for non-blocking refreshes.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **You can save regular views for future use** | True of both types — both are persisted as schema objects |
| **Regular views can improve performance** | Regular views cannot improve performance — they re-run the query each time (though predicate pushdown can reduce scanned data). Materialized views improve read performance by caching results |
| **Regular views don't store data; materialized views store query results** (correct) | The defining difference — virtual vs. physical storage |
| **You can store regular views in memory** | Views are stored as query definitions in the system catalog (disk), not in memory |

---

## Question 4

**When initiating the creation of a new table in a database through pgAdmin, which tab in the Create Table dialog box helps to define data types?**

- Columns
- General
- Parameters
- Constraints

**Correct answer: Columns**

[ENRICHED: explanation — In pgAdmin's **Create-Table** dialog (right-click Tables → Create → Table), the **Columns** tab is where you define each column's name, data type, length/precision, and NOT NULL constraint. Each row in the Columns tab grid represents one column; the **Data type** dropdown is in this grid's third column (after Name and before Length/Precision). The other tabs serve different purposes: **General** (table name, owner, schema, comments), **Parameters** (table-level parameters like fillfactor, autovacuum settings, tablespace), **Constraints** (primary keys, foreign keys, unique constraints, check constraints, and indexes). See `module_3_mysql_and_postgresql/c4_m3_creating_databases_loading_data_postgresql.md` for the full pgAdmin table creation workflow covering all five tabs (General, Definition, Security, Parameters, Columns).]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Columns** (correct) | The tab where data types are selected for each column in the column definition grid |
| **General** | Table-level metadata (name, owner, schema) — no column/type definitions |
| **Parameters** | Table storage parameters (fillfactor, autovacuum, toast_tuple_target) — not for column types |
| **Constraints** | PK, FK, UNIQUE, CHECK, and EXCLUDE constraints — data types are defined before constraints are applied |

---

## Question 5

**Which of the following SQL statement defines a view in PostgreSQL?**

- CREATE VIEW
- JOIN
- SELECT
- VIEW

**Correct answer: CREATE VIEW**

[ENRICHED: explanation — `CREATE VIEW` (not just `VIEW`) is the standard SQL DDL statement for defining a view. The full syntax is: `CREATE VIEW view_name AS select_query;`. For example: `CREATE VIEW employee_contacts AS SELECT first_name, last_name, email FROM employees WHERE active = true;`. Neither `JOIN` nor `SELECT` alone define a view — they are parts of the query that a view encapsulates. `VIEW` alone is not a valid SQL statement — it must be preceded by `CREATE` (or `CREATE OR REPLACE`, `ALTER`, `DROP`). PostgreSQL also supports `CREATE MATERIALIZED VIEW` for materialized views and `CREATE OR REPLACE VIEW` for idempotent view creation. See `module_3_mysql_and_postgresql/c4_m3_views_postgresql.md` for the complete view creation workflow in pgAdmin (Views → Create → View, General tab for naming, Code tab for the defining SQL).]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **CREATE VIEW** (correct) | The full DDL statement that creates a view object in the database |
| **JOIN** | A SQL clause used within queries to combine tables — not a DDL statement and does not define a view |
| **SELECT** | A DML statement for reading data — not a DDL statement. A SELECT query can appear inside a CREATE VIEW, but SELECT alone does not define a view |
| **VIEW** | Not a valid SQL statement — must be combined with CREATE (CREATE VIEW), ALTER (ALTER VIEW), or DROP (DROP VIEW) |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Explanation | pgAdmin ERD Tool can design ERDs and generate SQL DDL; distinguished from psql, Query Tool, and pgAdmin as a whole | HIGH |
| 2 | Q2 | Explanation | pgAdmin Restore (pg_restore) regenerates Tables, Data, and Data types; Passwords require pg_dumpall --globals-only | HIGH |
| 3 | Q3 | Explanation | Regular views are virtual (re-execute query each time); materialized views store results (snapshot, need REFRESH) | HIGH |
| 4 | Q4 | Explanation | Columns tab in pgAdmin Create-Table dialog defines data types; distinguished from General, Parameters, Constraints tabs | HIGH |
| 5 | Q5 | Explanation | CREATE VIEW is the full DDL; JOIN/SELECT are subcomponents; VIEW alone is invalid | HIGH |
