# MySQL and PostgreSQL Hands-On

> **Source:** IBM Introduction to Relational Databases — Module 3 (MySQL and PostgreSQL)

## Overview

MySQL and PostgreSQL are the two most widely deployed open-source relational databases. MySQL, known for speed and ease of use, powers large-scale web applications (Facebook, YouTube, Twitter). PostgreSQL, known for standards compliance and extensibility, is favored for complex queries, geospatial data, and analytical workloads. This topic covers hands-on operations in both databases and compares their philosophies.

[Cross-ref: topics/c4_sql_data_types_and_schema_design.md — SQL types, DDL, constraints primer]
[Cross-ref: topics/c4_keys_indexes_and_constraints.md — keys, indexes, constraints in depth]

---

## MySQL

### Starting MySQL

**Command-line client:**
```bash
mysql -h hostname -u username -p
```

**Common admin commands:**
```sql
SHOW DATABASES;
USE database_name;
SHOW TABLES;
DESCRIBE table_name;
SHOW PROCESSLIST;
SHOW STATUS;
```

**Batch mode (script execution):**
```bash
mysql -u root -p < setup_database.sql > output.log
```

### Creating Databases and Tables

```sql
CREATE DATABASE company;

USE company;

CREATE TABLE employee_details (
    employee_id INT NOT NULL AUTO_INCREMENT,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    email       VARCHAR(100) UNIQUE,
    hire_date   DATE,
    salary      DECIMAL(10,2),
    department_id INT,
    PRIMARY KEY (employee_id)
);
```

**DESCRIBE output:**

| Field | Type | Null | Key | Default | Extra |
|---|---|---|---|---|---|
| employee_id | int | NO | PRI | NULL | auto_increment |
| first_name | varchar(50) | NO | | NULL | |
| last_name | varchar(50) | NO | | NULL | |
| email | varchar(100) | YES | UNI | NULL | |
| hire_date | date | YES | | NULL | |
| salary | decimal(10,2) | YES | | NULL | |
| department_id | int | YES | | NULL | |

**MySQL data type categories:**

| Category | Types |
|---|---|
| Numeric | `INT`, `TINYINT`, `SMALLINT`, `BIGINT`, `DECIMAL(p,s)`, `FLOAT`, `DOUBLE` |
| String | `VARCHAR(n)`, `CHAR(n)`, `TEXT`, `ENUM`, `SET` |
| Date/Time | `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`, `YEAR` |
| Binary | `BLOB`, `VARBINARY(n)` |

Use `VARCHAR` for variable-length strings, `CHAR` for fixed-length codes, `DECIMAL` for monetary values (exact precision), `FLOAT`/`DOUBLE` for scientific calculations.

**Schema management:**

```sql
SHOW CREATE TABLE employee_details;
ALTER TABLE employee_details ADD COLUMN phone VARCHAR(20) AFTER email;
ALTER TABLE employee_details MODIFY COLUMN salary DECIMAL(12,2) NOT NULL;
ALTER TABLE employee_details DROP COLUMN phone;
```

### Populating Data

**Backup and restore with mysqldump:**
```bash
# Backup entire database
mysqldump -u root -p employees > employeesbackup.sql

# Restore
mysql -u root -p employees < employeesbackup.sql

# Production-quality backup (InnoDB consistent, no locking)
mysqldump -u root -p --single-transaction --routines --triggers employees > backup.sql
```

**Key mysqldump options:**

| Option | Purpose |
|---|---|
| `--single-transaction` | Consistent InnoDB backup without locking (use for production) |
| `--routines` | Include stored procedures and functions |
| `--triggers` | Include triggers |
| `--no-data` | Schema only (no rows) |
| `--where="condition"` | Backup only matching rows |

**LOAD DATA INFILE (bulk CSV load):**
```sql
LOAD DATA INFILE '/path/to/employees.csv'
INTO TABLE employee_details
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

`LOAD DATA INFILE` is the fastest way to bulk load into MySQL — 1M+ rows per minute. Indexes slow down loading; consider dropping non-PK indexes before bulk loads and rebuilding afterward.

**mysqlimport (CLI wrapper around LOAD DATA INFILE):**
```bash
mysqlimport -u root -p --local employees /path/to/employee_details.csv
```

The table name is inferred from the CSV filename — it must match exactly.

**phpMyAdmin:** GUI tool for visual database operations. The Import tab supports SQL and CSV files (default limit: 2 MB). For larger files, use CLI methods.

### Keys and Constraints in MySQL

**Creating primary keys:**
```sql
-- During table creation
CREATE TABLE employee_details (
    empid INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (empid)
) AUTO_INCREMENT = 1000;

-- Added later
ALTER TABLE employee_details ADD PRIMARY KEY (empid);
```

**AUTO_INCREMENT behavior:**
- Default start: 1. Override: `ALTER TABLE t AUTO_INCREMENT = 1000;`
- Gaps occur on transaction rollback and failed INSERTs — values are not guaranteed to be sequential
- Retrieve last inserted ID: `SELECT LAST_INSERT_ID();`

**Foreign keys (InnoDB only — MyISAM parses but ignores FK constraints):**
```sql
ALTER TABLE employee_contact_info
ADD CONSTRAINT fk_employee_contact
FOREIGN KEY (empid)
REFERENCES employee_details(empid)
ON DELETE CASCADE
ON UPDATE CASCADE;
```

**Requirements for MySQL FK creation:**
1. Both tables must use the **InnoDB** storage engine
2. FK and referenced PK columns must have the same data type
3. The referenced column must have an index (PRIMARY KEY or UNIQUE)
4. FK columns should be indexed (MySQL does not auto-index FKs)

**Unique constraints:**
```sql
ALTER TABLE employee_details ADD UNIQUE KEY (email);
ALTER TABLE employee_details ADD CONSTRAINT unique_email UNIQUE (email);
```

In MySQL, `UNIQUE` constraint and `UNIQUE` index are the same thing at the implementation level. MySQL allows multiple NULLs in a UNIQUE column (unlike SQL Server which allows only one).

**NULL handling:**
- phpMyAdmin default: NOT NULL (unchecked = required)
- CLI default: NULL allowed if `NOT NULL` is not explicitly specified

---

## PostgreSQL

### Starting PostgreSQL

**Command-line client (psql):**
```bash
psql -h localhost -U postgres -d mydb
```

**Common psql meta-commands:**
```sql
\l                    -- List databases
\c database_name      -- Connect to database
\dt                   -- List tables
\d table_name         -- Describe table
\di                   -- List indexes
\du                   -- List users
\q                    -- Quit
```

**Batch mode:**
```bash
psql -U postgres -d mydb -f setup.sql
```

### Creating Databases and Tables

```sql
CREATE DATABASE company;

\c company

CREATE TABLE employee_details (
    employee_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    email       VARCHAR(100) UNIQUE,
    hire_date   DATE DEFAULT CURRENT_DATE,
    salary      NUMERIC(10,2) CHECK (salary > 0),
    department_id INTEGER REFERENCES department(department_id)
);
```

**PostgreSQL-specific features:**
- `GENERATED ALWAYS AS IDENTITY` — SQL-standard identity column (preferred over `SERIAL`)
- `SERIAL` / `BIGSERIAL` — auto-incrementing integers (legacy style, still widely used)
- `NUMERIC(p,s)` — exact decimal arithmetic (synonymous with `DECIMAL`)
- `TEXT` — unlimited variable-length string (no length limit, unlike VARCHAR(n))
- `JSONB` — binary JSON with indexing support (GIN indexes)
- `UUID` — native UUID type with `gen_random_uuid()` function
- `ARRAY` — native array type for storing lists in a single column
- `CREATE DOMAIN` — reusable domain constraints

### Loading Data

**pg_dump (backup):**
```bash
# Plain SQL dump (portable)
pg_dump -U postgres company > company.sql

# Custom format (compressed, parallel restore)
pg_dump -U postgres -Fc company > company.dump

# Schema only (no data)
pg_dump -U postgres --schema-only company > company_schema.sql

# Restore
psql -U postgres -d company < company.sql
pg_restore -U postgres -d company company.dump   # For custom format
```

**COPY command (bulk load/export):**
```sql
-- Export to CSV
COPY employee_details TO '/tmp/employees.csv'
WITH (FORMAT CSV, HEADER true, DELIMITER ',');

-- Import from CSV
COPY employee_details (first_name, last_name, email, hire_date, salary)
FROM '/tmp/employees.csv'
WITH (FORMAT CSV, HEADER true, DELIMITER ',');
```

`COPY` is PostgreSQL's high-speed bulk load utility, analogous to MySQL's `LOAD DATA INFILE`. For client-side files, use `psql \copy`:

```bash
\copy employee_details FROM 'employees.csv' WITH (FORMAT CSV, HEADER)
```

### Views in PostgreSQL

```sql
-- Simple view (updatable under certain conditions)
CREATE VIEW active_employees AS
SELECT employee_id, first_name, last_name, email
FROM employee_details
WHERE termination_date IS NULL;

-- Materialized view (physically stored snapshot, must be refreshed)
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT DATE_TRUNC('month', sale_date) AS month,
       SUM(amount) AS total_sales
FROM sales
GROUP BY month
WITH DATA;

REFRESH MATERIALIZED VIEW monthly_sales;
```

### Keys and Constraints in PostgreSQL

PostgreSQL supports all six constraint types with SQL-standard syntax:

```sql
-- Primary key
ALTER TABLE employee ADD PRIMARY KEY (employee_id);

-- Foreign key with named constraint
ALTER TABLE employee
ADD CONSTRAINT fk_department
FOREIGN KEY (department_id) REFERENCES department(department_id)
ON DELETE SET NULL;

-- Check constraint (cross-column validation)
ALTER TABLE employee
ADD CONSTRAINT chk_dates
CHECK (termination_date IS NULL OR termination_date > hire_date);

-- Exclusion constraint (generalized uniqueness beyond equality)
CREATE TABLE booking (
    room_id INTEGER,
    during TSRANGE,
    EXCLUDE USING gist (room_id WITH =, during WITH &&)
);
```

PostgreSQL supports transactional DDL for most operations — CREATE TABLE, ALTER TABLE, and even DROP TABLE can be rolled back inside a `BEGIN...COMMIT` block.

---

## MySQL vs. PostgreSQL: Comparison

### Philosophy and Architecture

| Dimension | MySQL | PostgreSQL |
|---|---|---|
| **License** | GPL (Oracle-owned) | PostgreSQL License (MIT-like, open foundation) |
| **SQL compliance** | Partial (no FULL OUTER JOIN until 8.0, no CHECK enforcement in 5.7) | High — implements most SQL:2016 features |
| **Default storage** | InnoDB (since 5.5) | Heap with MVCC (built-in, no pluggable engines) |
| **Concurrency model** | MVCC (InnoDB), table-level locking (MyISAM) | MVCC — readers never block writers, writers never block readers |
| **Storage engines** | Pluggable — InnoDB, MyISAM, NDB, Memory, CSV, more | Single engine (heap + indexes), but extensive index types (B-Tree, Hash, GiST, GIN, BRIN, SP-GiST) |
| **Extensions** | Limited (MySQL HeatWave) | Rich — pg_stat_statements, PostGIS, pg_partman, pg_cron, foreign data wrappers (FDW) |

### Feature Comparison

| Feature | MySQL | PostgreSQL |
|---|---|---|
| Auto-increment | `AUTO_INCREMENT` | `SERIAL` / `GENERATED ... AS IDENTITY` |
| String type | `VARCHAR(n)`, `TEXT` | `VARCHAR(n)`, `TEXT` (identical types in PG — only difference is length constraint) |
| Conditional | `IFNULL()`, `IF()` | `COALESCE()`, `NULLIF()` |
| Limit | `LIMIT n` (must be at end) | `LIMIT n` or `FETCH FIRST n ROWS ONLY` |
| Upsert | `INSERT ... ON DUPLICATE KEY UPDATE` | `INSERT ... ON CONFLICT DO UPDATE` |
| JSON | `JSON` type (validated text) | `JSON` / `JSONB` (binary, indexed with GIN) |
| Full-text search | Built-in (MyISAM/InnoDB FULLTEXT indexes) | Built-in (tsvector/tsquery, ranking, stemming) |
| Geospatial | Basic (MySQL 8.0 spatial) | Advanced (PostGIS extension — industry standard) |
| Table partitioning | Range, list, hash, key | Range, list, hash (declarative, PG 10+) |
| Parallel queries | Limited (MySQL 8.0+) | Robust (parallel seq scan, parallel join, parallel agg) |
| Foreign keys | InnoDB only | All storage (single engine) |
| CHECK constraints | Enforced since MySQL 8.0 (ignored in 5.7) | Enforced from the start |
| Recursive CTEs | MySQL 8.0+ | Since 8.4 (2005) |
| Window functions | MySQL 8.0+ | Since 8.4 (2005) |
| Transactional DDL | No (implicit commit) | Yes (can roll back DDL) |

### When to Choose Which

**Choose MySQL when:**
- Building web applications with high read throughput (content management, e-commerce)
- Using the LAMP/LEMP stack (PHP + MySQL is a proven combination)
- You need a simple, easy-to-manage database with a large ecosystem of tools
- The workload is primarily OLTP with simple queries
- You want managed cloud services (Amazon RDS, Google Cloud SQL, Azure Database)

**Choose PostgreSQL when:**
- You need advanced SQL features (CTEs, window functions, recursive queries)
- Data integrity is critical and you want full ACID compliance
- You work with geospatial data (PostGIS is the standard)
- You need custom data types, operators, or indexing strategies
- You run analytical workloads mixed with OLTP (HTAP)
- You want extensibility through extensions (FDW, pg_partman, pg_cron)
- You need transactional DDL for safe schema migrations

### MySQL Administration Tools

| Tool | Type | Best For |
|---|---|---|
| **MySQL CLI** (`mysql`) | Command line | Scripting, automation, server administration |
| **MySQL Workbench** | Desktop GUI | Database design, query development, performance analysis |
| **phpMyAdmin** | Web GUI | Shared hosting, quick operations, non-technical users |
| **DBeaver** | Desktop GUI | Multi-DB support (MySQL + 70+ others), ERD viewer |

### PostgreSQL Administration Tools

| Tool | Type | Best For |
|---|---|---|
| **psql** | Command line | All operations — the most powerful PostgreSQL client |
| **pgAdmin** | Desktop + Web GUI | Schema design, query tool with explain plan visualization, backup/restore |
| **DBeaver** | Desktop GUI | Universal database client with PostgreSQL support |
| **DataGrip** | Desktop IDE | Advanced SQL refactoring, version control integration |

[Cross-ref: topics/c4_sql_data_types_and_schema_design.md — SQL data types, DDL, relationship implementation]
[Cross-ref: topics/c4_keys_indexes_and_constraints.md — keys, indexes, constraints, normalization]
[Cross-ref: topics/c4_data_modeling_and_erds.md — ERDs, data models, entity mapping]
