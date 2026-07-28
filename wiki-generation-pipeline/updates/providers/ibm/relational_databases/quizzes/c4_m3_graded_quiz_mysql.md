<mark style="background-color: rgba(200, 230, 201, 0.4);">NEW</mark>

> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 3:** MySQL and PostgreSQL
> **Quiz:** Graded Quiz — MySQL

# Graded Quiz: MySQL

**Due:** Jul 17, 11:59 PM EEST  
**Attempts:** 3 (every 8 hours)  
**Pass required:** Yes

---

## Question 1

**In MySQL Workbench, what is the name of the left-side panel used to view database objects (tables, views, etc.)?**

- Object Browser
- Schemas
- Visual Data Editor
- Administration

**Correct answer: Schemas**

[ENRICHED: explanation — In MySQL Workbench, the left-side Navigator panel has two tabs: **Management** (server admin functions) and **Schemas** (lists all databases, tables, views, stored procedures, etc.). The Schemas tab shows each database as a collapsible tree node. Expanding a database reveals Tables, Views, Stored Procedures, and Functions. "Object Browser" is the name used in SQL Server Management Studio (SSMS) and Oracle SQL Developer, not MySQL Workbench. See `c4_m3_getting_started_with_mysql.md` for the full MySQL Workbench interface breakdown.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Object Browser** | Common distractor — this is the equivalent panel in SQL Server Management Studio and Oracle SQL Developer |
| **Schemas** (correct) | The Navigator panel's Schemas tab in MySQL Workbench lists all database objects |
| **Visual Data Editor** | Not a panel name — MySQL Workbench has a Result Grid for viewing/editing data, but it's not the left panel |
| **Administration** | The Management tab in the Navigator panel shows server administration (users, logs, status), not database objects |

---

## Question 2

**When setting up a MySQL database using phpMyAdmin, at what stage do you choose the encoding method for the data?**

- When you add tables to the database
- When you name the new database
- When you define the columns in the table
- When you see a summary of the new table's structure

**Correct answer: When you name the new database**

[ENRICHED: explanation — In phpMyAdmin's **Create database** dialog, there are two fields: the database name and a **collation** dropdown (e.g., `utf8mb4_general_ci`, `latin1_swedish_ci`). Collation determines how characters are sorted and compared — it is the encoding method for the database. This is chosen at database creation time, before any tables are defined. Column-level encoding can override it later, but the database-level default is set here. See `c4_m3_creating_databases_tables_mysql.md` for the full phpMyAdmin workflow with utf8mb4 guidance.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **When you name the new database** (correct) | The encoding/collation is set in the Create database dialog alongside the database name |
| **When you add tables** | Table-level collation can be set here, but the database-level default encoding is already set |
| **When you define columns** | Column-level collation overrides exist but are optional; the database default applies if unset |
| **When you see a summary** | The summary just displays what was already configured |

---

## Question 3

**Which of the following approaches help fill MySQL database tables with small amounts of data? [Select two]**

- Entering the rows using the phpMyAdmin interface manually
- Running SQL INSERT statements to enter the rows
- Insert the rows from a data file
- Restore the rows from a backup

**Correct answers: Entering the rows using the phpMyAdmin interface manually, Running SQL INSERT statements to enter the rows**

[ENRICHED: explanation — **Manual entry** (phpMyAdmin GUI) and **INSERT statements** are appropriate for small amounts of data because they insert one row at a time (or a few rows per statement). Loading from a data file and restoring from a backup are bulk operations designed for large datasets — they use MySQL's high-performance load infrastructure (LOAD DATA INFILE can insert millions of rows per minute). See `c4_m3_populating_mysql_databases_tables.md` for the spectrum of data loading methods from manual to bulk.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **phpMyAdmin manual entry** (correct) | Point-and-click row-by-row entry — fine for a handful of rows |
| **INSERT statements** (correct) | `INSERT INTO table VALUES (...)` adds one row at a time, suitable for small data |
| **Insert from a data file** | LOAD DATA INFILE is a bulk loader designed for large files (thousands to millions of rows) |
| **Restore from a backup** | mysqldump restore recreates entire tables/databases — overkill and impractical for small additions |

---

## Question 4

**When contrasting foreign keys with primary keys, which statement exclusively pertains to foreign keys?**

- Must relate to a unique primary key
- Are always indexed
- Cannot contain nulls
- Are unique within the table

**Correct answer: Must relate to a unique primary key**

[ENRICHED: explanation — A foreign key constraint **references** a primary key (or unique constraint) in another table. This is the defining characteristic of FKs that does not apply to PKs. PKs are defined on their own table and don't relate outward. The other options either apply to both or apply only to PKs: (1) Index — PKs are always auto-indexed (clustered in InnoDB); FKs are not auto-indexed but should be for join performance. (2) Nulls — PKs cannot contain NULLs (entity integrity); FKs can contain NULLs (optional relationship). (3) Uniqueness — PKs must be unique within the table; FKs can have duplicate values. See `lessons/c4_m2_primary_keys_foreign_keys.md` for the complete PK vs. FK comparison.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Must relate to a unique PK** (correct) | An FK column references a PK or unique constraint in another table — this is exclusive to FKs |
| **Are always indexed** | PKs are always auto-indexed; FKs are NOT auto-indexed (though indexing FKs is a best practice for join performance) |
| **Cannot contain nulls** | PKs cannot be null; FKs CAN be null (representing an optional relationship) |
| **Are unique within the table** | PKs are unique; FKs can have duplicate values (many-to-one relationship) |

---

## Question 5

**Which of the following tools administers MySQL from a graphical web interface?**

- MySQL
- mysqladmin
- phpMyAdmin
- MySQL Workbench

**Correct answer: phpMyAdmin**

[ENRICHED: explanation — **phpMyAdmin** is a free, open-source web-based GUI written in PHP for MySQL/MariaDB administration. It runs in a browser, requires a web server (Apache/Nginx) with PHP, and provides database management through a point-and-click interface. **MySQL Workbench** is a desktop application (not web-based). **mysqladmin** is a command-line administration tool. **MySQL** is the database server itself, not an admin tool. See `c4_m3_getting_started_with_mysql.md` for the full tool comparison table (MySQL CLI, Workbench, phpMyAdmin) with deployment models and features.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **MySQL** | The database server, not an administration tool |
| **mysqladmin** | Command-line tool for server administration tasks (shutdown, status, process list) — not GUI, not web |
| **phpMyAdmin** (correct) | The only fully web-based graphical MySQL admin tool |
| **MySQL Workbench** | Desktop GUI application — powerful but not web-based |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Explanation | Distinguished MySQL Workbench Schemas tab from SSMS/Oracle Object Browser terminology | HIGH |
| 2 | Q2 | Explanation | Documented phpMyAdmin Create database dialog with collation dropdown and utf8mb4 guidance | HIGH |
| 3 | Q3 | Explanation | Spectrum of data loading methods from manual entry to bulk load with performance context | HIGH |
| 4 | Q4 | Explanation | Comprehensive PK vs. FK comparison across 4 dimensions: referencing, indexing, nullability, uniqueness | HIGH |
| 5 | Q5 | Explanation | Tool comparison: phpMyAdmin (web GUI), MySQL Workbench (desktop), mysqladmin (CLI) | HIGH |
