# SQL Data Types and Schema Design

> **Source:** IBM Introduction to Relational Databases — Modules 1-3

## Overview

A data type is a classification that specifies: (1) the type of value a column can hold, (2) the storage format and size, (3) the operations that can be performed on it, and (4) the comparison semantics. Every column must have exactly one data type, assigned at table creation time.

---

## Character String Types

### VARCHAR(n) — Variable-Length Character Strings

Stores strings up to n characters, using only the space needed. Storage: n characters + 1-4 bytes overhead depending on DBMS.

**VARCHAR vs. CHAR:** VARCHAR saves space; CHAR can be faster for fixed-length rows because the DBMS can predict record offsets. Use CHAR only for truly fixed-length codes (ISO country codes, currency codes, hash values).

**VARCHAR(n) vs. TEXT:** Most modern databases treat them identically in storage and performance. PostgreSQL explicitly treats VARCHAR(n) and TEXT as the same type — the only difference is the length constraint. Many designers prefer TEXT with a CHECK constraint for flexibility.

### CHAR(n) — Fixed-Length Character Strings

Always uses n characters, padding with spaces. 'ABC' in CHAR(10) becomes 'ABC       ' (7 trailing spaces). Most databases trim trailing spaces on retrieval.

---

## Numeric Types

### Integer Types

| Type | Storage | Range | Use Case |
|------|---------|-------|----------|
| SMALLINT | 2 bytes | -32,768 to 32,767 | Age, rating, small status codes |
| INTEGER / INT | 4 bytes | -2.1B to 2.1B | Most counters, IDs |
| BIGINT | 8 bytes | -9.2Q to 9.2Q | High-volume IDs, timestamps in ms |
| TINYINT (MySQL, SQL Server) | 1 byte | 0-255 or -128 to 127 | Boolean-like flags |

Choosing the smallest sufficient type saves storage: SMALLINT vs BIGINT saves 6 bytes per row × 100M rows × 3 columns = 1.8 GB savings.

### FLOAT vs. DECIMAL

**FLOAT** — approximate precision, IEEE 754 representation. Hardware-accelerated (SIMD). Good for scientific measurements, percentages, geospatial coordinates.

**DECIMAL/NUMERIC** — exact arithmetic. Use for currency, tax calculations, financial ratios. `DECIMAL(5,2)` stores values from -999.99 to 999.99 exactly.

**The precision trap:** `SELECT 0.1::float + 0.2::float` returns `0.30000000000000004` due to IEEE 754. Always use DECIMAL for financial calculations.

---

## Date and Time Types

| Feature | PostgreSQL | MySQL | SQL Server | Oracle |
|---------|-----------|-------|------------|--------|
| Date only | DATE | DATE | DATE | DATE |
| Time only | TIME | TIME | TIME | DATE (format mask) |
| Date + Time | TIMESTAMP | DATETIME | DATETIME2 | DATE (format mask) |
| With timezone | TIMESTAMPTZ | TIMESTAMP (session tz) | DATETIMEOFFSET | TIMESTAMP WITH TZ |
| High precision | TIMESTAMP(6) µs | DATETIME(6) µs | DATETIME2(7) 100ns | TIMESTAMP(9) ns |
| Range | 4713 BC–294276 AD | 1000–9999 AD | 1753–9999 AD | -4712–9999 AD |

**Best practices:**
- Always store timestamps in UTC; convert to local time in the application layer
- Use TIMESTAMPTZ (or equivalent) rather than separate date + time columns
- Never store dates as VARCHAR — sorting alphabetically gives wrong results
- Be aware of the 2038 problem: legacy MySQL TIMESTAMP overflows on 2038-01-19

---

## Binary Data

BLOB (Binary Large Object) stores binary data like images or files.

**Industry pattern:** Store files in object storage (S3, GCS, Azure Blob) and store only the URL/reference in the database. This "external BLOB storage" pattern avoids database bloat, enables CDN caching, and keeps backups manageable.

---

## Constraints and Validation

| Constraint | Description |
|------------|-------------|
| NOT NULL | Column must have a value |
| UNIQUE | No duplicate values in the column |
| CHECK | Row satisfies a boolean expression |
| FOREIGN KEY | Value must exist in a referenced table |
| PRIMARY KEY | NOT NULL + UNIQUE — identifies each row uniquely |
| DEFAULT | Default value when none is provided |

Constraints must be enforced at the database level, not just the application level — application-level validation can be bypassed by direct SQL connections, bulk loads, and migration scripts.

---

## Default Values

Strategies: static defaults (0, 'Unknown'), sequence-based (SERIAL, IDENTITY), expression-based (gen_random_uuid(), CURRENT_TIMESTAMP), application-assigned.

---

## DDL — Data Definition Language

SQL statements that define the database structure:

```sql
CREATE TABLE book (
    book_id       SERIAL PRIMARY KEY,
    isbn          VARCHAR(13) UNIQUE NOT NULL,
    title         VARCHAR(255) NOT NULL,
    published_year INTEGER CHECK (published_year >= 1400),
    price         NUMERIC(10, 2),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE book ADD COLUMN edition INTEGER;
ALTER TABLE book DROP COLUMN IF EXISTS obsolete_field;
DROP TABLE IF EXISTS old_table;
TRUNCATE TABLE temp_data;
```

**Degree** — number of columns (width of the table). Changes require ALTER TABLE (schema migration).

**Cardinality** — number of rows (height of the table). Changes happen constantly via INSERT/DELETE.

---

## DDL Operations — Detailed Reference

### CREATE TABLE — Full Syntax

Generalized syntax:

```
CREATE TABLE [schema_name.]table_name (
    column_name   data_type   [column_constraints],
    column_name   data_type   [column_constraints],
    ...
    [table_constraints]
);
```

**Column constraints:** `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `DEFAULT <expression>`, `CHECK (<predicate>)`, `REFERENCES <table>(<column>)`

**Table constraints:** `PRIMARY KEY (col, ...)`, `UNIQUE (col, ...)`, `FOREIGN KEY (col, ...) REFERENCES <table>(<col>, ...)`, `CHECK (<predicate>)`

**Example — library database author table:**

```sql
CREATE TABLE author (
    Author_ID CHAR(2)     PRIMARY KEY NOT NULL,
    Lastname  VARCHAR(15) NOT NULL,
    Firstname VARCHAR(15) NOT NULL,
    Email     VARCHAR(40),
    City      VARCHAR(15),
    Country   CHAR(2)
);
```

**Example — bookstore schema with foreign keys:**

```sql
CREATE TABLE book (
    ISBN      VARCHAR(13) PRIMARY KEY,
    Author_ID CHAR(2)     NOT NULL REFERENCES author(Author_ID),
    Title     VARCHAR(100) NOT NULL,
    Year      SMALLINT,
    Publisher VARCHAR(50)
);

CREATE TABLE loan (
    Loan_ID       INTEGER PRIMARY KEY,
    ISBN          VARCHAR(13) NOT NULL REFERENCES book(ISBN),
    Card_ID       CHAR(8)     NOT NULL REFERENCES borrower(Card_ID),
    Date_Borrowed DATE        NOT NULL DEFAULT CURRENT_DATE,
    Date_Due      DATE        NOT NULL,
    Date_Returned DATE
);
```

### ALTER TABLE — Variations by DBMS

| Operation | Db2 | PostgreSQL | MySQL |
|---|---|---|---|
| Add column | `ADD COLUMN col type` | `ADD COLUMN col type` | `ADD COLUMN col type` |
| Drop column | `DROP COLUMN col` | `DROP COLUMN col` | `DROP COLUMN col` |
| Modify type | `ALTER COLUMN col SET DATA TYPE type` | `ALTER COLUMN col TYPE type [USING expr]` | `MODIFY COLUMN col type` |
| Add PK | `ADD PRIMARY KEY (col)` | `ADD PRIMARY KEY (col)` | `ADD PRIMARY KEY (col)` |
| Add FK | `ADD FOREIGN KEY (col) REFERENCES t(col)` | `ADD FOREIGN KEY (col) REFERENCES t(col)` | `ADD FOREIGN KEY (col) REFERENCES t(col)` |
| Rename column | `RENAME COLUMN old TO new` | `RENAME COLUMN old TO new` | `CHANGE old new type` |
| Rename table | `RENAME TO new_name` | `RENAME TO new_name` | `RENAME TO new_name` |

Type modification requires existing data compatibility — changing VARCHAR to INTEGER fails if any non-numeric value exists. PostgreSQL's `USING` clause defines the conversion logic; without it, PostgreSQL rejects the change if implicit conversion is unavailable.

### DROP TABLE — CASCADE vs. RESTRICT

```sql
DROP TABLE IF EXISTS author;       -- Safe/idempotent
DROP TABLE author RESTRICT;        -- Refuse if dependencies exist (default in most DBs)
DROP TABLE author CASCADE;         -- Drop dependent views, FKs, triggers too
```

`CASCADE` is useful in development but dangerous in production — it silently removes dependent objects. Always audit dependencies before cascading a drop.

### TRUNCATE vs. DELETE

| Aspect | TRUNCATE (DDL) | DELETE (DML) |
|---|---|---|
| Rows affected | All — no WHERE clause | All or filtered — WHERE supported |
| Speed | Very fast (deallocates pages) | Slower (logs each row deletion) |
| Transactional | Varies: PostgreSQL=yes, MySQL=no, Db2=no (IMMEDIATE) | Fully transactional |
| Triggers | Does not fire per-row triggers | Fires BEFORE/AFTER DELETE triggers |
| Auto-increment | Resets counter | Retains current value |
| Space reclamation | Releases data pages | Marks rows deleted, space remains allocated |

TRUNCATE is the standard approach for clearing staging tables in ETL pipelines.

---

## Data Movement Utilities

Data movement falls into three categories: **backup/restore** (whole database, full fidelity), **import/export** (table-level, SQL-based), and **load** (page-level, fastest, skips constraint checks).

### Backup and Restore

| Database | Backup Command | Restore Command |
|---|---|---|
| Db2 | `BACKUP DATABASE mydb TO /backup` | `RESTORE DATABASE mydb FROM /backup` |
| PostgreSQL | `pg_dump mydb > mydb.sql` | `psql mydb < mydb.sql` |
| MySQL | `mysqldump mydb > mydb.sql` | `mysql mydb < mydb.sql` |

**Backup types:** full (entire DB), incremental (changes since last backup), differential (changes since last full), transaction log (point-in-time recovery). RPO (Recovery Point Objective) determines backup frequency; RTO (Recovery Time Objective) determines restore speed requirements.

### Import and Export — File Formats

| Format | Characteristics | Best For |
|---|---|---|
| **DEL / CSV** | Delimiter-separated (comma, tab, pipe), human-readable, universal | Interchange between systems, scripting |
| **ASC** | Fixed-width columns, no delimiters, positional | Legacy/mainframe exports |
| **PC/IXF** | IBM proprietary binary, self-describing (schema + data), type-preserving | Db2-to-Db2 transfer |
| **JSON** | Nested structure, verbose, REST API native | Web integrations, document-oriented data |

**Db2 EXPORT example:**
```sql
EXPORT TO author_export.del OF DEL MESSAGES export_msg.txt
SELECT * FROM author WHERE City = 'Toronto';
```

**Db2 IMPORT modes:**
```sql
IMPORT FROM new_authors.del OF DEL INSERT INTO author;              -- Append
IMPORT FROM refreshed_authors.del OF DEL REPLACE INTO author;       -- Replace all
IMPORT FROM author_backup.ixf OF IXF CREATE INTO temp_author;       -- Create from IXF
```

### Load Utilities vs. IMPORT

| Aspect | IMPORT (SQL INSERT) | LOAD (page-level) |
|---|---|---|
| Mechanism | Row-by-row INSERT | Direct page formatting, bypasses SQL engine |
| Speed | Moderate | 10-50x faster for large volumes |
| Constraint checking | Full (PK, FK, UNIQUE, CHECK, NOT NULL) | None by default; `SET INTEGRITY` after load |
| Logging | Fully logged | Minimal or none |
| Triggers | Fires all INSERT triggers | Does not fire triggers |
| Table availability | Row-level locking | Table unavailable (table-level lock) |
| Best for | Tables < 100K rows, validation-critical | Tables > 1M rows, data warehouse fact tables |

**Db2 LOAD with deferred constraints:**
```sql
LOAD FROM big_table.del OF DEL INSERT INTO target_table;
SET INTEGRITY FOR target_table IMMEDIATE CHECKED;
```

---

## Loading Data Methods

### Bulk Load vs. Row-by-Row INSERT

| Factor | Row-by-Row INSERT | Bulk Load Utility |
|---|---|---|
| Rows per second | 100-5,000 | 10,000-1,000,000+ |
| Network overhead | N round-trips | Single request |
| Index maintenance | Incremental per row | Rebuilt at end |
| Locking | Row-level | Table-level |

### Db2 Web Console Load — Four-Step Process

1. **Source** — Select file location (local CSV, Amazon S3, IBM Cloud Object Storage) and provide authentication
2. **Target** — Choose schema/table; specify Append (preserves existing data), Overwrite (destructive — a failed load still deletes existing data), or New Table (schema inferred from CSV)
3. **Define** — Configure character encoding (UTF-8 recommended), delimiter, header row, date/time formats, null indicator
4. **Finalize** — Review settings, execute, inspect results (Completed / Completed with warnings / Failed / Partially completed)

[Cross-ref: topics/c4_keys_indexes_and_constraints.md — keys, constraints, indexes, normalization]
[Cross-ref: topics/c4_mysql_and_postgresql.md — MySQL and PostgreSQL hands-on]

---

## Relationship Implementation

- **One-to-Many:** Foreign key on the "many" side table referencing the parent's primary key
- **Many-to-Many:** Junction table with composite primary key (FK1, FK2)
- **One-to-One:** Foreign key with UNIQUE constraint on either side

Always index foreign key columns — querying "all orders for customer X" without an index on `orders.customer_id` requires a full table scan O(n) instead of O(log n).

---

## MySQL and PostgreSQL Quick Reference

| Operation | MySQL | PostgreSQL |
|-----------|-------|------------|
| Create database | `CREATE DATABASE db;` | `CREATE DATABASE db;` |
| Connect | `USE db;` | `\c db` |
| Create table | Same SQL standard | Same SQL standard |
| Auto-increment | `INT AUTO_INCREMENT` | `SERIAL` or `IDENTITY` |
| String type | `VARCHAR(n)` | `VARCHAR(n)` or `TEXT` |
| Conditional | `IFNULL()` | `COALESCE()` |
| Limit | `LIMIT n` | `LIMIT n` |
| Upsert | `INSERT ... ON DUPLICATE KEY UPDATE` | `INSERT ... ON CONFLICT DO UPDATE` |

[Cross-ref: topics/relational_databases.md — RDBMS principles, ACID, normalization]
[Cross-ref: topics/c4_data_modeling_and_erds.md — ERDs, data models, relationship types]
