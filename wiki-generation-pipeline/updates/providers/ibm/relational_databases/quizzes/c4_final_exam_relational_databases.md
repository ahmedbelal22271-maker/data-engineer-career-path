> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Assessment:** Final Exam

# Final Exam: Introduction to Relational Databases (RDBMS)

**Time:** 45 min
**Due:** Jul 20, 11:59 PM EEST
**Attempts:** 3 (every 24 hours)
**Pass requirement:** Must complete to pass the course

---

### Question 1

Data types define the type of data that can be stored in which part of a database table?

- Schemas
- Rows
- **Columns** ✅
- Index

<details>
<summary>Explanation</summary>

**Correct answer: Columns.**

A database table represents a single entity, and its columns symbolize the attributes of that entity. The information entered in each column must always be of the same type or kind of data. Data types (VARCHAR, INTEGER, FLOAT, DATE, etc.) define what kind of data is permissible in a given column — they are a column-level constraint.

- **Schemas** — A schema is a logical grouping of database objects (tables, views, functions). It is a container, not a storage location for data values.
- **Rows** — Rows (tuples) represent individual records/instances of the entity. Each row contains one data value per column, but the data type constraint is defined at the column level, not the row level.
- **Index** — An index is a performance optimization structure that speeds up data retrieval. It does not store the actual data values in the table — it stores pointers to them.

[ENRICHED: data type enforcement — Data types serve two purposes: (1) **storage optimization** — the database engine allocates the right number of bytes (e.g., SMALLINT uses 2 bytes vs. BIGINT uses 8 bytes), and (2) **integrity enforcement** — inserting a string into an INTEGER column triggers an error. Different databases implement types slightly differently: MySQL's TEXT has a 65,535-byte limit, PostgreSQL's TEXT is unlimited, and Oracle's VARCHAR2 maxes at 4,000 bytes (or 32,767 in PL/SQL).]

**Reference:** See `../lessons/c4_m1_data_types.md` for the full data type comparison across databases.

</details>

---

### Question 2

The surge in popularity of cloud databases over the past decade results from which cloud service model?

- Software-as-a-Service (SaaS)
- Platform as a Service (PaaS)
- Commercial databases
- **Infrastructure as a Service (IaaS)** ✅

<details>
<summary>Explanation</summary>

**Correct answer: Infrastructure as a Service (IaaS).**

The primary driver for the consistent growth in cloud database popularity is the increasing adoption of the **Software as a Service (SaaS)** model. SaaS delivers applications over the internet, eliminating the need to download or install database software locally. Users access cloud-based databases from anywhere with an internet connection.

- **Platform as a Service (PaaS)** — Provides a platform for developing and deploying applications without managing infrastructure. While PaaS databases exist (e.g., Heroku Postgres), the surge in popularity is attributed to SaaS adoption.
- **Commercial databases** — Refers to proprietary database products (Oracle, SQL Server) that require licensing fees. This is a pricing model, not a cloud service model.
- **Infrastructure as a Service (IaaS)** — Provides virtualized computing resources (VMs, storage, networking). You provision a VM and install the DBMS yourself. While IaaS enables cloud databases, the SaaS model is what drove the popularity surge.

[ENRICHED: cloud service models for databases —
| Model | Database Example | You Manage | Provider Manages |
|---|---|---|---|
| IaaS | Db2 on IBM Cloud VM | DBMS install, config, patching, backups | Hardware, networking, OS |
| PaaS/DBaaS | IBM Db2 on Cloud, Amazon RDS | Schema design, queries, tuning | DBMS software, patching, backups, HA |
| SaaS | Snowflake, Salesforce | Schema, queries | Everything else (DBMS, infra, scaling) |

The SaaS model eliminates the need for organizations to manage database infrastructure entirely, which is why it drove the popularity surge — it lowered the barrier to entry for small and medium businesses.]

**Reference:** See `../lessons/c4_m1_database_architecture.md` and `../lessons/c4_m1_introduction_to_relational_database_offerings.md` for cloud database architecture and service models.

</details>

---

### Question 3

Which statement regarding the data access layer in a database management system software (DBMS) is true?

- It is the place for storing the data.
- The client typically directly accesses it.
- **It contains an engine that compiles queries, retrieves data, and returns a result set.** ✅
- It encapsulates the application and business logic.

<details>
<summary>Explanation</summary>

**Correct answer: It contains an engine that compiles queries, retrieves data, and returns a result set.**

The data access layer server provides interfaces for various client types (JDBC, ODBC, command line processor, vendor-specific interfaces) and incorporates an engine responsible for compiling queries, retrieving and processing data, and delivering the result set. Each layer abstracts the layer below it — the engine doesn't need to know the physical disk layout, and the access layer doesn't need to know the query optimization strategy.

- **It is the place for storing the data** — This describes the **storage layer**, which is below the data access layer in the DBMS architecture. The storage layer manages physical disk I/O, page management, and buffer pools.
- **The client typically directly accesses it** — False. The client communicates with the database interface/API, which then talks to the data access layer. The client never directly accesses the storage layer.
- **It encapsulates the application and business logic** — This describes the **application layer** in a three-tier architecture, not the data access layer of the DBMS itself. Business logic belongs in the application tier, not the database access layer.

[ENRICHED: DBMS internal architecture — A typical DBMS has three internal layers:
1. **Data access layer** — Interfaces (JDBC, ODBC, CLP) + query compilation engine
2. **Query engine** — Optimization, execution planning, result set generation
3. **Storage layer** — Buffer pool management, page I/O, transaction logging, physical data placement

The separation of concerns means the access layer handles client communication and query parsing, the engine optimizes and executes, and the storage layer manages physical data. This layered design allows each component to evolve independently.]

**Reference:** See `../lessons/c4_m1_database_architecture.md` for the full DBMS internal architecture diagram.

</details>

---

### Question 4

Which statement is true with regard to PostgreSQL?

- It is object-oriented.
- It is proprietary software.
- **It supports inheritance and overloading.** ✅
- It is a NoSQL database management system (DBMS).

<details>
<summary>Explanation</summary>

**Correct answer: It supports inheritance and overloading.**

PostgreSQL is an **object-relational** database management system. The "object" in its architecture refers to object-oriented features that extend the standard relational model: **table inheritance** (child tables inherit columns from parent tables), **function overloading** (multiple functions with the same name but different parameter types), **user-defined types (UDTs)**, and **operator overloading**.

- **It is object-oriented** — PostgreSQL is object-*relational*, not purely object-oriented. Object-oriented databases (like db4o, ObjectDB) store objects directly without a relational model. PostgreSQL extends the relational model with object features.
- **It is proprietary software** — False. PostgreSQL is **open-source** under the PostgreSQL License (similar to MIT/BSD). It is free to use, modify, and distribute.
- **It is a NoSQL database management system (DBMS)** — False. PostgreSQL is a **relational** (SQL) database. While it supports JSON/JSONB for semi-structured data, it is fundamentally an RDBMS with full ACID compliance.

[ENRICHED: PostgreSQL object-relational features —
```sql
-- Table inheritance
CREATE TABLE vehicle (id SERIAL, make TEXT, model TEXT);
CREATE TABLE car (doors INT) INHERITS (vehicle);
-- car inherits id, make, model from vehicle

-- Function overloading
CREATE FUNCTION calculate(x INTEGER) RETURNS INTEGER ...
CREATE FUNCTION calculate(x NUMERIC) RETURNS NUMERIC ...
-- PostgreSQL resolves which to call based on argument type
```

These features make PostgreSQL uniquely suited for hybrid workloads mixing structured relational data with semi-structured (JSONB), geospatial (PostGIS), vector embeddings (pgvector), and time-series (TimescaleDB) data — all within a single database.]

**Reference:** See `../lessons/c4_m1_postgresql_introduction.md` for PostgreSQL object-relational features and historical context.

</details>

---

### Question 5

What is the purpose of the Entity Relationship Diagram (ERD) model?

- The ERD model helps you map data types to existing columns and rows.
- The ERD model helps you define the data in each table row.
- The ERD model helps you to design a database with a single table.
- **The ERD model helps you to define entities and their attributes, map them to tables, and identify the relationships between the tables.** ✅

<details>
<summary>Explanation</summary>

**Correct answer: The ERD model helps you to define entities and their attributes, map them to tables, and identify the relationships between the tables.**

An ERD is a visual representation that illustrates the relationships and interactions between entities in a database. It showcases the logical structure of a database system, displaying entities and the relationships between them as lines connecting boxes. Introduced by Peter Chen in 1976, it is the standard tool for conceptual database design.

- **Map data types to existing columns and rows** — This describes schema refinement or data type migration, not the purpose of an ERD. ERDs work at the conceptual/logical level, not the physical data type level.
- **Define the data in each table row** — This describes data entry or population, not design. ERDs define structure (entities, attributes, relationships), not individual row data.
- **Design a database with a single table** — ERDs are specifically designed for modeling **multi-table** relationships. A single-table database wouldn't need an ERD for relationship mapping.

[ENRICHED: ERD components — An ERD consists of:
- **Entities** — People, objects, or concepts (represented as rectangles)
- **Attributes** — Characteristics of entities (represented as ovals)
- **Relationships** — Associations between entities (represented as diamonds)
- **Cardinality** — Constraints on relationships (1:1, 1:N, M:N)

The three levels of ERD design: (1) **Conceptual** — entities and relationships only, (2) **Logical** — attributes and keys added, (3) **Physical** — tables, columns, data types, indexes.]

**Reference:** See `../lessons/c4_m1_erds_and_types_of_relationships.md` for ERD notation and relationship types.

</details>

---

### Question 6

Which of the following Db2 features helps to improve performance and reduce overheads for analytic workloads by directing queries to specific columns?

- Data Skipping
- **Column Store** ✅
- Machine Learning Algorithms
- The Common SQL Engine

<details>
<summary>Explanation</summary>

**Correct answer: Column Store.**

The **Column Store (BLU Acceleration)** feature improves performance and reduces overheads for analytic workloads by directing queries to specific columns rather than processing an entire data table. Traditional row-store databases read entire rows even when only a few columns are needed. Columnar storage (introduced in Db2 10.5 as "BLU Acceleration") stores data column-by-column, so analytic queries that reference only a few columns read far less data from disk.

- **Data Skipping** — While Data Skipping also improves analytic performance, it works by skipping data pages that don't match query predicates (based on metadata about min/max values per page). It reduces irrelevant data read but does not "direct queries to specific columns."
- **Machine Learning Algorithms** — Db2 uses ML for query optimization (identifying efficient execution plans), but ML does not direct queries to specific columns.
- **The Common SQL Engine** — This is Db2's SQL parsing and execution engine, not a performance optimization feature for analytics.

[ENRICHED: Column Store vs. Data Skipping — These two features work together but address different problems:
| Feature | Problem It Solves | How It Works |
|---|---|---|
| Column Store (BLU) | Reading entire rows when only 2-3 columns needed | Stores data column-by-column; reads only referenced columns |
| Data Skipping | Scanning pages that don't match WHERE predicates | Stores min/max metadata per page; skips pages outside query range |

Combined, they make Db2 Warehouse highly competitive for BI and analytics workloads — column store reduces per-query data read, data skipping reduces irrelevant data read.]

**Reference:** See `../lessons/c4_m1_db2_introduction.md` for BLU Acceleration, Data Skipping, and Db2 Warehouse architecture.

</details>

---

### Question 7

Which of the following attributes is appropriate to use as a primary key?

- Social security number
- Author
- Street address
- Copyright date

<details>
<summary>Explanation</summary>

**Correct answer: Social security number.**

A **Social Security Number (SSN)** is an appropriate primary key because it is a **natural key** — a naturally occurring attribute that is already unique for each person. A primary key must be **unique** (no two rows can share the same value) and **non-null** (every row must have a value). SSN satisfies both requirements for US citizens.

- **Author** — Not unique. Multiple books can have the same author (e.g., multiple J.K. Rowling novels). An author name cannot uniquely identify a row in a books table.
- **Street address** — Not unique. Multiple people can live at the same address (households, apartment buildings). Even within a single table, addresses can repeat.
- **Copyright date** — Not unique. Many books can share the same copyright year (e.g., thousands of books published in 2024).

[ENRICHED: primary key types —
| Type | Example | Pros | Cons |
|---|---|---|---|
| Natural key | SSN, ISBN, email | Meaningful, no extra column needed | Can change (ISBN format changed in 2007), can be long, privacy concerns (SSN) |
| Surrogate key | AUTO_INCREMENT, SERIAL, UUID | Stable, short, no business meaning | Extra column, meaningless to humans, requires join to get business meaning |

In practice, many systems use surrogate keys (e.g., `id SERIAL PRIMARY KEY`) alongside natural keys (e.g., `UNIQUE(ssn)`) — the surrogate key for joins and performance, the natural key for business logic uniqueness.]

**Reference:** See `../lessons/c4_m2_primary_keys_foreign_keys.md` for natural vs. surrogate key tradeoffs.

</details>

---

### Question 8

Which of the following is a disadvantage of using indexes?

- Guarantees uniqueness of rows
- **Uses disk space** ✅
- Enhances SELECT query performance
- Reduce the need to sort data

<details>
<summary>Explanation</summary>

**Correct answer: Uses disk space.**

Each index you create uses disk space in the same way that adding indexes increases the number of pages in a book. An index can be as large as, or even larger than, the table itself. This is a clear disadvantage — indexes consume storage resources.

- **Guarantees uniqueness of rows** — This is actually an **advantage** of a UNIQUE index. It ensures no duplicate values exist in the indexed column(s).
- **Enhances SELECT query performance** — This is the primary **advantage** of indexes. They speed up data retrieval by allowing the database to locate rows without scanning the entire table.
- **Reduce the need to sort data** — This is also an **advantage**. Indexes store data in sorted order, so ORDER BY queries can use the index's sort order instead of performing a separate sort operation.

[ENRICHED: index tradeoffs — Indexes provide fast reads at the cost of:
1. **Disk space** — Each index consumes storage (sometimes more than the table itself for wide tables with many indexes)
2. **Write performance** — Every INSERT, UPDATE, or DELETE on an indexed column must maintain every index on that table (index maintenance overhead)
3. **Complexity** — Choosing the right indexes requires understanding query patterns; wrong indexes waste space and slow writes without helping reads

Rule of thumb: Index columns used in WHERE, JOIN, and ORDER BY clauses, but avoid over-indexing on tables with heavy write workloads. A table with 5 indexes takes roughly 5x longer to write to than an unindexed table.]

**Reference:** See `../indexes/c4_m2_overview_of_indexes.md` for the full advantages and disadvantages of indexes.

</details>

---

### Question 9

Which constraint specifies the permissible values for a given attribute?

- Entity integrity constraint
- Semantic integrity constraint
- **Domain constraint** ✅
- Unique constraint

<details>
<summary>Explanation</summary>

**Correct answer: Domain constraint.**

A **domain constraint** defines the set of allowable values for an attribute. It is the most fundamental constraint — it specifies what data type, range, format, or set of values a column can contain. For example, a "country" attribute might be constrained to valid two-letter country codes, or an "age" attribute might be constrained to non-negative integers.

- **Entity integrity constraint** — Ensures the uniqueness of primary key values and prohibits NULLs in the primary key. It operates at the row level, not at the individual attribute value level.
- **Semantic integrity constraint** — Maintains the correctness of data meaning (e.g., ensuring a "city" column contains actual city names, not garbage values). It is broader than domain constraints — it enforces business rules about what data means, not just what format it takes.
- **Unique constraint** — Ensures all values in a column (or combination of columns) are distinct. It prevents duplicates but doesn't define the permissible set of values (a domain constraint does that).

[ENRICHED: constraint hierarchy — The three constraint types form a layered defense:
| Level | Constraint | What It Protects |
|---|---|---|
| Column | Domain constraint | What values are allowed (type, range, format) |
| Row | Entity integrity | Uniqueness and identification (primary key) |
| Table-to-table | Referential integrity | Foreign key references valid primary keys |

Domain constraints are enforced through data types, CHECK constraints, and NOT NULL constraints. For example: `age INT CHECK (age >= 0 AND age <= 150)` combines a data type constraint with a domain-specific range check.]

**Reference:** See `../lessons/c4_m2_relational_model_constraints_advanced.md` for the full constraint taxonomy.

</details>

---

### Question 10

What is the difference between system schemas and user schemas?

- System schemas contain partitions, and user schemas contain metadata
- Both schemas contain the same objects
- **System schemas store configuration information and metadata** ✅
- Neither schema contains database objects

<details>
<summary>Explanation</summary>

**Correct answer: System schemas store configuration information and metadata.**

System schemas (system catalogs) contain configuration and metadata for the database — user permissions, index metadata, partition information, data type definitions. They are read-only for regular users; only database administrators can modify them. User schemas contain database objects like tables, views, and functions created by users.

- **System schemas contain partitions, and user schemas contain metadata** — This is backwards. System schemas contain metadata (including partition information), not just partitions. User schemas contain user-created objects, not metadata.
- **Both schemas contain the same objects** — False. System schemas contain system catalog tables (SYSCAT, pg_catalog, information_schema), while user schemas contain user-created objects (tables, views, functions).
- **Neither schema contains database objects** — False. Both schemas contain objects — system schemas contain system catalog objects, user schemas contain user-created objects.

[ENRICHED: system schemas per database —
| Database | System Schema | Key Tables |
|---|---|---|
| Db2 | SYSCAT | SYSCAT.TABLES, SYSCAT.COLUMNS, SYSCAT.INDEXES |
| PostgreSQL | pg_catalog | pg_tables, pg_indexes, pg_class |
| MySQL | information_schema | TABLES, COLUMNS, STATISTICS |
| SQL Server | sys + INFORMATION_SCHEMA | sys.tables, sys.columns, INFORMATION_SCHEMA.COLUMNS |

The system catalog is itself stored as tables — a concept known as **reflection** or **introspection**. You can query system schemas to discover the database structure: `SELECT * FROM information_schema.tables WHERE table_schema = 'mydb'`.]

**Reference:** See `../lessons/c4_m2_database_objects_and_hierarchy.md` for schema hierarchy and system catalog introspection.

</details>

---

### Question 11

Which MySQL tool can you use to visually design a MySQL database?

- phpMyAdmin
- **MySQL Workbench** ✅
- mysql
- mysqladmin

<details>
<summary>Explanation</summary>

**Correct answer: MySQL Workbench.**

**MySQL Workbench** is the official desktop application for visually designing MySQL databases. It integrates SQL development, administration, and database design within a unified environment. Key design features include visual EER (Enhanced Entity-Relationship) diagrams, forward and reverse engineering, and schema synchronization.

- **phpMyAdmin** — A free, open-source **web-based** GUI for MySQL/MariaDB administration. While it can create databases and tables through a web interface, it is not primarily a visual *design* tool — it lacks EER diagrams and forward/reverse engineering capabilities.
- **mysql** — The MySQL command-line client. It is a text-based tool, not a visual design tool.
- **mysqladmin** — A command-line administrative utility for performing administrative operations (create databases, drop databases, monitor status). Not a visual design tool.

[ENRICHED: MySQL tool comparison —
| Tool | Type | Visual Design | ERD Support | Platform |
|---|---|---|---|---|
| MySQL Workbench | Desktop app | Yes (EER diagrams) | Yes (forward/reverse) | Windows, Linux, macOS |
| phpMyAdmin | Web app | Limited | No | Browser (PHP) |
| mysql | CLI | No | No | Terminal |
| mysqladmin | CLI | No | No | Terminal |

MySQL Workbench is the only tool in this list that provides visual database design with ERD capabilities. It can generate ERDs from existing schemas (reverse engineering) and create physical databases from visual designs (forward engineering).]

**Reference:** See `../lessons/c4_m3_getting_started_with_mysql.md` for MySQL Workbench features and capabilities.

</details>

---

### Question 12

When utilizing phpMyAdmin to create a MySQL database, when do you specify the data column's length in the process?

- When you name the new database
- When you are shown a summary of the structure of the new table
- When you add tables to the database
- **When you define the columns in the table** ✅

<details>
<summary>Explanation</summary>

**Correct answer: When you define the columns in the table.**

In phpMyAdmin's interface, when creating a table and defining its columns, each column has configurable options including **Name** (column name), **Type** (MySQL data type), **Length/Values** (max length or ENUM values), **Default**, **Collation**, **Attributes**, **Null**, **Index**, **A_I** (AUTO_INCREMENT), and **Comments**. The length is specified as part of the column definition step.

- **When you name the new database** — Database naming happens before any table or column definition. No column details exist at this stage.
- **When you are shown a summary of the structure of the new table** — The summary appears *after* you've defined all columns. By this point, lengths are already set.
- **When you add tables to the database** — Adding a table name doesn't involve column details. Column definition (including length) happens in the next step.

[ENRICHED: phpMyAdmin column definition workflow —
1. Create/select database
2. Create new table → enter table name and number of columns
3. **Define each column** → Name, Type, **Length**, Default, Null, Index, A_I
4. Review summary of table structure
5. Save

The Length/Values field is where you specify constraints like `VARCHAR(50)` (enter `50`) or `DECIMAL(10,2)` (enter `10,2`). For data types without length (INT, DATE, TEXT), this field is left empty.]

**Reference:** See `../lessons/c4_m3_creating_databases_tables_mysql.md` for phpMyAdmin column definition details.

</details>

---

### Question 13

In many default phpMyAdmin/PHP configurations, what is a typical default maximum upload size (before changing server settings)?

- Unlimited
- **2 megabytes** ✅
- 3 megabytes
- 1 megabyte

<details>
<summary>Explanation</summary>

**Correct answer: 2 megabytes.**

By default, phpMyAdmin enforces a **~2 MB upload limit**. This limit is configured via PHP's `upload_max_filesize` and `post_max_size` settings in `php.ini`. For larger files, you can use the MySQL CLI (`mysql -u root -p myauthors < dump.sql`) or split the file into smaller chunks.

- **Unlimited** — phpMyAdmin imposes a file size limit by default. While this can be increased in php.ini, the default is not unlimited.
- **3 megabytes** — Incorrect. The default is 2 MB, not 3 MB.
- **1 megabyte** — Incorrect. The default is 2 MB, not 1 MB.

[ENRICHED: phpMyAdmin upload workarounds — When your SQL dump exceeds 2 MB:
1. **Use the MySQL CLI** — `mysql -u root -p database_name < dump.sql` (no file size limit)
2. **Split the file** — Divide large dumps into smaller chunks using tools like `split` (Linux) or manual editing
3. **Increase PHP limits** — Edit `php.ini`: `upload_max_filesize = 64M` and `post_max_size = 128M`, then restart Apache/PHP-FPM
4. **Use LOAD DATA INFILE** — Server-side bulk loading (requires FILE privilege)

SQL scripts are the standard mechanism for loading larger datasets — they are portable, repeatable, version-controllable, and bypass GUI file size limits.]

**Reference:** See `../labs/c4_m3_lab_phpmyadmin_create_tables.md` for phpMyAdmin Import tab capabilities and file size limits.

</details>

---

### Question 14

Which of the following programs contains an ERD tool that you can use to create an ERD for an existing database?

- **pgAdmin** ✅
- PostgresSQL
- MySQL
- phpAdmin

<details>
<summary>Explanation</summary>

**Correct answer: pgAdmin.**

**pgAdmin** incorporates an Entity Relationship Diagram (ERD) tool that facilitates creating ERDs for existing databases and generating SQL statements for underlying database objects. To generate an ERD from an existing database, you right-click the database and select "Generate ERD" — the tool automatically reviews the database structure and produces a visual diagram of tables and their relationships.

- **PostgresSQL** — PostgreSQL is the database engine itself, not a GUI tool. It doesn't contain an ERD tool; it is the software that pgAdmin connects to.
- **MySQL** — MySQL is a database engine, not a GUI tool. MySQL *Workbench* (a separate application) contains an ERD tool, but MySQL itself does not.
- **phpAdmin** — This appears to be a misspelling of "phpMyAdmin," which is a web-based MySQL admin tool that does not contain an ERD tool.

[ENRICHED: pgAdmin ERD capabilities — The pgAdmin ERD Tool supports:
1. **Forward engineering** — Design an ERD visually, then generate SQL DDL to create the database
2. **Reverse engineering** — Right-click an existing database → "Generate ERD" → visual diagram of tables and relationships
3. **Auto-layout** — Automatically arrange tables for readability
4. **Export** — Save as SQL DDL scripts, images (PNG), or PDFs
5. **Modification** — Reorganize tables, modify relationships, add notes and documentation

Other tools with ERD capabilities: MySQL Workbench (EER diagrams), DBeaver (ERD viewer), DrawSQL, dbdiagram.io.]

**Reference:** See `../lessons/c4_m3_getting_started_with_postgresql.md` for pgAdmin ERD Tool features and `../labs/c4_m4_hands_on_lab_database_design_using_erds.md` for hands-on ERD creation.

</details>

---

### Question 15

What is the fundamental way a view is created in a database?

- Using the mySQL admin tool
- From an entity relationship diagram
- **From SQL code** ✅
- Using the PostgreSQL GUI tool

<details>
<summary>Explanation</summary>

**Correct answer: From SQL code.**

A view is fundamentally created using the `CREATE VIEW` SQL statement. The full syntax is: `CREATE VIEW view_name AS select_query;`. A view is a virtual table whose contents are defined by a stored query — the query is re-evaluated each time the view is accessed.

- **Using the mySQL admin tool** — While GUI tools like phpMyAdmin or MySQL Workbench can help create views through their interfaces, the underlying mechanism is always SQL code. The GUI is just a frontend that generates the `CREATE VIEW` statement.
- **From an entity relationship diagram** — ERDs are design tools for planning database structure. They don't create views — they help you design tables and relationships.
- **Using the PostgreSQL GUI tool** — Similar to the MySQL admin tool option. pgAdmin can help create views through its GUI (right-click Views → Create → View), but the fundamental creation mechanism is still SQL code entered on the Code tab.

[ENRICHED: view creation syntax —
```sql
-- Basic view creation
CREATE VIEW employee_contacts AS
SELECT first_name, last_name, email, phone
FROM employees
WHERE department = 'Engineering';

-- Idempotent view update
CREATE OR REPLACE VIEW employee_contacts AS
SELECT first_name, last_name, email, phone, slack_handle
FROM employees
WHERE department = 'Engineering';

-- Dropping a view
DROP VIEW IF EXISTS employee_contacts;
```

`CREATE OR REPLACE VIEW` allows modifying the view definition without dropping and recreating it, which preserves existing permissions. Views are virtual — they don't store data, they store queries that are re-evaluated on each access.]

**Reference:** See `../lessons/c4_m3_views_postgresql.md` for view creation in pgAdmin and SQL.

</details>

---

## Summary

| # | Topic | Correct Answer | Key Concept |
|---|---|---|---|
| 1 | Data types in database tables | Columns | Data types define permissible data at the column level |
| 2 | Cloud database popularity | SaaS | Software-as-a-Service drove cloud database adoption |
| 3 | Data access layer in DBMS | Contains engine that compiles queries | Access layer provides interfaces + query compilation engine |
| 4 | PostgreSQL features | Supports inheritance and overloading | Object-relational: table inheritance, function overloading, UDTs |
| 5 | ERD model purpose | Define entities, attributes, relationships | ERD = conceptual design tool for multi-table databases |
| 6 | Db2 analytic features | Column Store | BLU Acceleration stores data column-by-column for analytics |
| 7 | Primary key attributes | Social security number | Natural key: unique, non-null, meaningful |
| 8 | Index disadvantages | Uses disk space | Each index consumes storage + adds write overhead |
| 9 | Constraint for permissible values | Domain constraint | Defines the set of allowable values for an attribute |
| 10 | System vs user schemas | System schemas store configuration/metadata | System = metadata; User = tables/views/functions |
| 11 | MySQL visual design tool | MySQL Workbench | Desktop app with EER diagrams, forward/reverse engineering |
| 12 | phpMyAdmin column length | When defining columns | Length/Values field in column definition step |
| 13 | phpMyAdmin upload limit | 2 megabytes | Default PHP upload_max_filesize; use CLI for larger files |
| 14 | ERD tool for existing databases | pgAdmin | Right-click database → Generate ERD |
| 15 | View creation | From SQL code | `CREATE VIEW view_name AS select_query;` |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Definition | Explained data type enforcement (storage optimization + integrity) | HIGH |
| 2 | Q2 | Ecosystem connection | Added IaaS/PaaS/SaaS comparison table with database examples | HIGH |
| 3 | Q3 | Ecosystem connection | Added DBMS internal architecture (access → engine → storage layers) | HIGH |
| 4 | Q4 | Concrete example | Added SQL code examples for table inheritance and function overloading | HIGH |
| 5 | Q5 | Definition | Added ERD components (entities, attributes, relationships, cardinality) and design levels | HIGH |
| 6 | Q6 | Alternative & tradeoff | Compared Column Store vs. Data Skipping with table showing different problems solved | HIGH |
| 7 | Q7 | Ecosystem connection | Added natural vs. surrogate key comparison table with tradeoffs | HIGH |
| 8 | Q8 | Performance context | Added write amplification rule (5 indexes = 5x slower writes) | HIGH |
| 9 | Q9 | Definition | Added constraint hierarchy table (column → row → table-to-table) | HIGH |
| 10 | Q10 | Concrete example | Added system schema comparison table across Db2, PostgreSQL, MySQL, SQL Server | HIGH |
| 11 | Q11 | Concrete example | Added MySQL tool comparison table (type, visual design, ERD support, platform) | HIGH |
| 12 | Q12 | Definition | Added phpMyAdmin column definition workflow (5-step process) | HIGH |
| 13 | Q13 | Alternative & tradeoff | Added 4 workarounds for phpMyAdmin upload limit (CLI, split, php.ini, LOAD DATA) | HIGH |
| 14 | Q14 | Ecosystem connection | Added pgAdmin ERD capabilities list and alternative tools | HIGH |
| 15 | Q15 | Concrete example | Added CREATE VIEW SQL syntax examples including CREATE OR REPLACE | HIGH |
