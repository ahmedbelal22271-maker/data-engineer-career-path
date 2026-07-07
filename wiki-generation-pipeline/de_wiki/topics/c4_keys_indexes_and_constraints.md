# Keys, Indexes, and Constraints

> **Source:** IBM Introduction to Relational Databases — Module 2 (Creating Tables and Loading Data; Designing Keys, Indexes, and Constraints)

## Overview

Keys uniquely identify rows, indexes accelerate data access, and constraints enforce data integrity. Together they form the structural backbone of any relational database. This topic covers the database object hierarchy, primary and foreign keys, indexing internals, the six relational constraint types, and normalization.

---

## Database Object Hierarchy

Relational databases organize objects in a hierarchy: **Instance → Database → Schema → Object** (table, view, index, etc.). Variations exist across RDBMSs, but the logical structure is consistent.

```
┌──────────────────────────────────────┐
│          Instance                    │
│  (Running DBMS process, config,      │
│   memory, port)                      │
│                                      │
│  ┌──────────────────────────────┐   │
│  │  Database 1                  │   │
│  │  (System catalogs, config)   │   │
│  │  ┌──────────────────────┐   │   │
│  │  │  Schema (hr)         │   │   │
│  │  │  ┌──────┐ ┌──────┐  │   │   │
│  │  │  │Tables│ │Views │  │   │   │
│  │  │  │Indexes││Triggers│ │   │   │
│  │  │  └──────┘ └──────┘  │   │   │
│  │  └──────────────────────┘   │   │
│  └──────────────────────────────┘   │
└──────────────────────────────────────┘
```

### Instance

A running DBMS process with its own memory, configuration files, and port. Db2 supports multiple instances per server (`db2inst1`, `db2inst2`). PostgreSQL calls this a "cluster" (one `postmaster` process per data directory). Cloud RDBMSs (AWS RDS, IBM Db2 on Cloud) treat an instance as a provisioned service with a DNS endpoint.

### Database

A named collection of objects (tables, views, indexes) with its own system catalog tables and configuration. Databases within an instance are isolated from each other.

### Schema

A logical namespace within a database that groups related objects. Schema-qualified names (`hr.employees`, `finance.invoices`) prevent naming conflicts and enable multi-tenant data isolation.

| Database | Hierarchy | Default Schema |
|---|---|---|
| Db2 | Instance → Database → Schema → Object | Username |
| PostgreSQL | Cluster → Database → Schema → Object | `public` |
| MySQL | Instance → Database (= Schema) → Object | N/A (DB = schema) |
| Oracle | Instance → Database → Schema (user-owned) → Object | Username |
| SQL Server | Instance → Database → Schema → Object | `dbo` |

### Objects Within a Schema

- **Tables** — rows and columns storing data
- **Indexes** — sorted data structures for fast lookup
- **Views** — stored queries (virtual tables)
- **Constraints** — PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL
- **Triggers** — procedural code executed on INSERT/UPDATE/DELETE
- **Aliases / Synonyms** — alternative names for objects

### System Schemas

Databases maintain system schemas (catalogs) that store metadata: `SYSCAT` (Db2), `pg_catalog` (PostgreSQL), `information_schema` (MySQL/SQL standard). These are read-only for regular users and queried for introspection:

```sql
-- Db2: list indexes on a table
SELECT INDNAME, UNIQUERULE, COLNAMES
FROM SYSCAT.INDEXES
WHERE TABNAME = 'EMPLOYEE';
```

---

## Primary Keys

A primary key uniquely identifies every row in a table. Each table can have only one primary key, which enforces both `UNIQUE` and `NOT NULL` automatically.

### Types of Primary Keys

| Type | Description | Example | Tradeoffs |
|---|---|---|---|
| **Natural key** | A pre-existing unique attribute | `ISBN` for books, `email` for users | Meaningful but can change (ISBN-10→ISBN-13) |
| **Surrogate key** | Artificially added column with no business meaning | `id INT AUTO_INCREMENT`, `UUID`, `SERIAL` | Never changes, fast for indexing, simplifies FKs |
| **Composite key** | Two or more columns forming a unique combination | `(site_id, employee_id)` | Useful for junction tables; verbose FK references |

**Guideline:** Most production tables use a surrogate integer primary key (`BIGSERIAL`, `AUTO_INCREMENT`, `IDENTITY`) and enforce uniqueness on natural keys with separate `UNIQUE` constraints. Surrogate keys are immune to business-rule changes and keep foreign key references narrow (one integer vs. multiple columns).

### Syntax

```sql
-- Inline (single column only)
CREATE TABLE book (
    book_id CHAR(10) PRIMARY KEY,
    title   VARCHAR(100) NOT NULL
);

-- Table-level (required for composite, preferred for naming)
CREATE TABLE employee_assignment (
    site_id     INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    role        VARCHAR(50),
    PRIMARY KEY (site_id, employee_id)
);

-- Added later
ALTER TABLE book ADD PRIMARY KEY (book_id);
ALTER TABLE book ADD CONSTRAINT pk_book PRIMARY KEY (book_id);
```

Adding a primary key to an existing table requires that all values in the key columns be non-NULL and unique. Pre-validate with:

```sql
SELECT COUNT(*) FROM book WHERE book_id IS NULL;
SELECT book_id, COUNT(*) FROM book GROUP BY book_id HAVING COUNT(*) > 1;
```

---

## Foreign Keys and Referential Actions

A foreign key (FK) is a column (or column group) that references the primary key of another table. FKs enforce **referential integrity**: every FK value must exist in the referenced parent table (or be NULL).

### Referential Actions

```sql
CREATE TABLE copy (
    copy_id       INTEGER NOT NULL,
    book_id       CHAR(10) NOT NULL,
    condition     VARCHAR(20),
    PRIMARY KEY (copy_id),
    CONSTRAINT fk_copy_book
        FOREIGN KEY (book_id)
        REFERENCES book(book_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

| Action | ON DELETE (parent deleted) | ON UPDATE (parent PK changed) |
|---|---|---|
| **NO ACTION** (default) | Reject the delete if child rows exist | Reject the PK change if child rows exist |
| **RESTRICT** | Same as NO ACTION (immediate check) | Same |
| **CASCADE** | Delete child rows automatically | Update FK in child rows automatically |
| **SET NULL** | Set FK to NULL in child rows (FK must be nullable) | Set FK to NULL in child rows |
| **SET DEFAULT** | Set FK to default value in child rows | Set FK to default value |

**Production guidance:**
- `NO ACTION` is the safest default — prevents accidental data loss
- `ON DELETE CASCADE` is appropriate when child data has no meaning without the parent (e.g., order line items)
- `ON DELETE SET NULL` suits optional relationships (e.g., setting `employee.department_id` to NULL when a department is deleted)
- Always index foreign key columns — without an FK index, JOINs and referential checks require full table scans
- In high-throughput OLTP systems, some teams omit FKs for write performance and rely on application-level integrity, but this is a tradeoff against data consistency

---

## Indexes

An index is a data structure that speeds up row lookups by providing a sorted path to data. Without indexes, the database performs a full table scan — O(n) — reading every row from disk.

### B+Tree Structure

Most relational databases use **B+Trees** as the default index type:

```
B+Tree on customer.last_name
        ┌──────────┐
        │ Root     │
        │ [A-M][N-Z]│
        └─────┬────┘
         ┌────┴────┐
     ┌───▼───┐ ┌──▼────┐
     │Branch │ │Branch │
     │A-D E-H│ │N-R S-Z│
     │  I-M  │ │       │
     └─┬─┬───┘ └─┬─┬───┘
   ┌──┘ │     ┌──┘ │
┌──▼┐ ┌▼──┐ ┌▼──┐ ┌▼──┐
│A-C│ │D-F│ │N-P│ │Q-S│
│ptr│ │ptr│ │ptr│ │ptr│
└───┘ └───┘ └───┘ └───┘
```

**B+Tree properties:**
- All data resides in **leaf nodes** (key + pointer to row)
- Internal nodes (root, branch) guide the search — typically 3-4 levels deep even for billions of rows
- Leaf nodes are linked left-to-right for efficient range scans (`WHERE last_name BETWEEN 'A' AND 'M'`)
- Search cost: O(log n) — a few index page reads vs. millions of row reads

### Creating Indexes

```sql
-- Basic index (allows duplicates)
CREATE INDEX idx_customer_last_name ON customer (last_name);

-- Unique index (enforces uniqueness like a UNIQUE constraint)
CREATE UNIQUE INDEX idx_customer_email ON customer (email);

-- Composite index (column order matters!)
CREATE INDEX idx_customer_name ON customer (last_name, first_name);

-- Descending order index
CREATE INDEX idx_order_date_desc ON orders (order_date DESC);
```

Automatic indexes: `PRIMARY KEY` and `UNIQUE` constraints automatically create indexes.

### Leftmost Prefix Rule

For a composite index on `(last_name, first_name)`, the DBMS can efficiently search by:
- `last_name` alone (leftmost prefix)
- `last_name AND first_name` (full key)

It **cannot** efficiently search by `first_name` alone. Create separate single-column indexes for independent search columns.

### Covering Index (Index-Only Scan)

If **all** columns in a query are present in the index, the DBMS reads only the index — never touches the table data:

```sql
-- Index: (last_name, first_name, email)
SELECT email FROM customer WHERE last_name = 'Smith';
-- Satisfied entirely from the index — 10-100x faster than a regular index lookup
```

### Write Overhead

Every index adds cost to INSERT, UPDATE, and DELETE — each write must maintain every index on the table:

| Indexes on Table | Write Amplification |
|---|---|
| 0 | 1× |
| 1 (PK only) | 2× |
| 3 total | 4× |
| 8 total | 9× |

**Guidance:**
- Index columns used in WHERE, JOIN, and ORDER BY
- Avoid over-indexing on high-write OLTP tables
- Drop non-critical indexes before bulk loads; rebuild afterward
- Monitor unused indexes with database tools and drop them

### Advantages and Disadvantages

| Advantage | Disadvantage |
|---|---|
| Faster SELECT (O(log n) vs. O(n)) | Disk space (can exceed table size) |
| Eliminates sorting (index is already sorted) | Slower INSERT/UPDATE/DELETE |
| Enforces uniqueness (UNIQUE index) | Maintenance during writes |
| Accelerates JOINs (FK indexes) | Planner may choose a suboptimal index |
| Enables index-only scans (covering index) | |

---

## Relational Model Constraints

Six constraint types enforce data integrity in the relational model:

| # | Constraint | Purpose | SQL Clause | Scope |
|---|---|---|---|---|
| 1 | Entity integrity | Each row is uniquely identifiable; no NULL in PK | `PRIMARY KEY`, `UNIQUE` | Table |
| 2 | Referential integrity | FK values must exist in parent table | `FOREIGN KEY ... REFERENCES` | Cross-table |
| 3 | Semantic integrity | Data values are correct and meaningful | `CHECK`, triggers, app logic | Column / Row |
| 4 | Domain integrity | Values belong to the allowed set | Data type, `CHECK`, `CREATE DOMAIN` | Column |
| 5 | Null constraint | Mandatory attributes cannot be NULL | `NOT NULL` | Column |
| 6 | Check constraint | Row satisfies a boolean predicate | `CHECK` | Column / Row |

### 1. Entity Integrity

The primary key must be unique and no part of it can be NULL. Every row must be distinguishable from every other row.

```sql
CREATE TABLE author (
    author_id  CHAR(2)     NOT NULL,  -- NOT NULL required for PK
    last_name  VARCHAR(50) NOT NULL,
    PRIMARY KEY (author_id)
);
```

`PRIMARY KEY` vs. `UNIQUE`:

| Feature | PRIMARY KEY | UNIQUE |
|---|---|---|
| NULLs allowed | No | Yes (typically one in SQL Server, multiple in PostgreSQL/MySQL) |
| Per table | One only | Multiple |
| Automatic index | Yes | Yes |
| Referenced by FK | Yes | Yes |

### 2. Referential Integrity

Three rules:
1. A child row cannot exist unless its FK matches a parent PK value (or is NULL)
2. A parent row cannot be deleted if dependent child rows exist (without ON DELETE CASCADE/SET NULL)
3. A parent PK value cannot be updated if dependent child rows exist (without ON UPDATE CASCADE)

### 3. Semantic Integrity

Data must be correct in meaning — not just syntactically valid. Semantic rules prevent garbage values (e.g., `city = 'Abc123'`), contradictory data (`termination_date < hire_date`), and out-of-range timestamps:

```sql
CONSTRAINT chk_author_birth_year
    CHECK (birth_year IS NULL OR (birth_year > 1800 AND birth_year <= EXTRACT(YEAR FROM CURRENT_DATE)))
```

Semantic rules are the hardest to enforce purely at the database level — a combination of CHECK constraints, triggers, and application validation is typical.

### 4. Domain Integrity

A **domain** is the set of allowable values for an attribute. Enforcement mechanisms:

| Mechanism | Example | Granularity |
|---|---|---|
| Data type | `CHAR(2)` | Coarsest |
| CHECK constraint | `CHECK (country IN ('CA', 'US', 'IN'))` | Column |
| CREATE DOMAIN (PostgreSQL) | `CREATE DOMAIN country_code AS CHAR(2) CHECK(...)` | Reusable |
| Lookup table | `country_code` table with FK reference | Most flexible |

### 5. NULL Constraint

`NOT NULL` rejects NULL values at the column level. NULL means "unknown" — distinct from empty string (`''`) or a sentinel value (`-1`, `'9999-12-31'`). Use NULL for genuinely missing values; avoid sentinel values in numeric and date columns.

### 6. Check Constraint

A boolean expression that must evaluate to TRUE (or UNKNOWN — NULL values pass through) for every row:

```sql
CONSTRAINT chk_book_year CHECK (year >= 1900 AND year <= EXTRACT(YEAR FROM CURRENT_DATE)),
CONSTRAINT chk_book_price CHECK (price >= 0),
CONSTRAINT chk_dates CHECK (termination_date IS NULL OR termination_date > hire_date)
```

**Limitations:** CHECK cannot reference other tables or other rows. For cross-row validation, use triggers or exclusion constraints.

---

## Normalization

Normalization reduces data redundancy and prevents update anomalies by organizing data into related tables.

### First Normal Form (1NF)

Each column contains atomic (indivisible) values; no repeating groups.

**Violation:** A single `Author` column stores "Jane Austen, Charles Dickens" — a multi-valued attribute.

**Fix:** Create a separate table with one row per author and a foreign key to the book.

### Second Normal Form (2NF)

Must be in 1NF AND every non-key column must depend on the **entire** primary key (not just part of it).

**Violation:** A table with composite PK `(StudentID, CourseID)` and a column `InstructorName` that depends only on `CourseID`.

**Fix:** Move `InstructorName` to a separate `Course` table.

### Third Normal Form (3NF)

Must be in 2NF AND every non-key column must depend **only** on the primary key (no transitive dependencies).

**Violation:** A table with `EmployeeID → DepartmentID → DepartmentHead`. `DepartmentHead` depends on `DepartmentID`, not directly on `EmployeeID`.

**Fix:** Split into `Employee` (EmployeeID, DepartmentID) and `Department` (DepartmentID, DepartmentHead).

### Boyce-Codd Normal Form (BCNF)

A stricter version of 3NF: every determinant must be a candidate key. Handles overlapping composite keys where 3NF fails.

**Example violation:** A table with `(Student, Subject, Professor)` where each professor teaches only one subject, but a subject can be taught by multiple professors. The key is `(Student, Subject)`, but `Professor → Subject` is a determinant that is not a superkey.

**Fix:** Split into `(Student, Professor)` and `(Professor, Subject)`.

### Normalization Beyond BCNF

4NF handles multi-valued dependencies; 5NF handles join dependencies. Both are rarely needed in practice — BCNF suffices for most production databases. Denormalization (intentionally violating normal forms) is sometimes applied in data warehouse star schemas for query performance.

[Cross-ref: topics/c4_sql_data_types_and_schema_design.md — SQL data types, DDL, data loading]
[Cross-ref: topics/c4_data_modeling_and_erds.md — ERDs, relationship types, entity mapping]
[Cross-ref: topics/c4_mysql_and_postgresql.md — MySQL and PostgreSQL hands-on]
