<mark style="background-color: rgba(200, 230, 201, 0.4);">NEW</mark>

> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 3:** MySQL and PostgreSQL
> **Type:** Practice Quiz — MySQL

# Practice Quiz: MySQL

**Due:** Jul 17, 11:59 PM EEST
**Time:** 10 min
**Attempts:** Unlimited (ungraded)

---

## Question 1

**Which of the following editions of MySQL can you use freely under a General Public License?**

- [ ] Standard
- [ ] Cluster
- [x] Community
- [ ] Enterprise

**Correct Answer:** Community

**Explanation:** MySQL Community Edition is the free, open-source version distributed under the GNU General Public License (GPL). It includes InnoDB, the default storage engine, and full SQL support.

[ENRICHED: defined "GPL" — The GNU General Public License is a copyleft license that grants users the freedom to run, study, share, and modify the software. MySQL's dual-licensing model (GPL for open-source use, commercial license for proprietary distribution) is maintained by Oracle Corporation.]

**Distractor Analysis:**
- **Standard** — Not a real MySQL edition. The actual tiers are Community → Standard (paid) → Enterprise (paid). "Standard" is sometimes used as an internal edition name in some Oracle products but is not a free GPL offering.
- **Cluster** — MySQL Cluster (NDB Cluster) is a separate distributed database product. It is available under GPL but is a specialized offering for high-availability, real-time workloads — not the standard general-purpose free edition the question asks about.
- **Enterprise** — MySQL Enterprise Edition is a paid commercial product with additional features (Enterprise Monitor, Audit Plugin, Thread Pool, advanced security) and Oracle support.

---

## Question 2

**True or False: You can create MySQL databases and tables only through the command line interface or a graphical user interface, like phpMyAdmin.**

- [ ] True
- [x] False

**Correct Answer:** False

**Explanation:** The statement is false because the word "only" makes it an absolute claim. MySQL databases and tables can be created through multiple interfaces beyond CLI and phpMyAdmin:
- **MySQL Workbench** — Official GUI for visual database design, SQL development, and administration
- **Programmatic APIs** — Connectors for Python (`mysql-connector-python`), PHP (`mysqli`, `PDO`), Java (JDBC), Node.js (`mysql2`), and others
- **SQL scripts executed via `source`** — Batch SQL files loaded through the CLI
- **Third-party tools** — DBeaver, TablePlus, Sequel Ace, Adminer, DataGrip, Navicat
- **ORM frameworks** — SQLAlchemy (Python), Sequelize (Node.js), Hibernate (Java), Eloquent (PHP/Laravel) abstract table creation behind code

[ENRICHED: ecosystem — The wide variety of MySQL interfaces reflects its position as one of the most widely deployed databases in the world. Each interface serves different use cases: CLI for automation/scripts, Workbench for visual design, programmatic connectors for application integration, ORMs for developer productivity.]

---

## Question 3

**Which MySQL commands are suitable for filling a single database table with data from a CSV file? [Select two]**

- [ ] source
- [ ] INSERT
- [x] mysqlimport
- [x] load data infile

**Correct Answers:** `mysqlimport` and `LOAD DATA INFILE`

**Explanation:**

1. **`LOAD DATA INFILE`** — A SQL statement that reads rows from a text file (including CSV) into a table at very high speed. It is the fastest way to bulk-load data in MySQL, capable of inserting millions of rows per minute. Syntax:
   ```sql
   LOAD DATA INFILE '/path/to/file.csv'
   INTO TABLE my_table
   FIELDS TERMINATED BY ','
   ENCLOSED BY '"'
   LINES TERMINATED BY '\n'
   IGNORE 1 ROWS;  -- skip header
   ```

2. **`mysqlimport`** — A command-line utility that wraps `LOAD DATA INFILE`. It automatically determines the target table from the filename (e.g., `mysqlimport mydb file.csv` targets `mydb.file`). It is effectively the CLI wrapper around `LOAD DATA INFILE`.

[ENRICHED: performance context — `LOAD DATA INFILE` is 20x faster than INSERT for bulk loads because it reads data in batches and performs fewer log flushes. With large files (100M+ rows), tuning `bulk_insert_buffer_size` and disabling indexes during load (`ALTER TABLE ... DISABLE KEYS`) can further improve performance.]

**Distractor Analysis:**
- **`source`** — The `source` command executes SQL statements from a file within the MySQL CLI (e.g., `source dump.sql`). It expects SQL statements (INSERT/UPDATE/CREATE), not raw CSV data. You would need to pre-convert the CSV into INSERT statements to use `source`.
- **`INSERT`** — The `INSERT` statement adds individual rows one at a time. While you could write a script that parses a CSV file and generates INSERT statements, `INSERT` itself is not a CSV-loading command — it inserts literal values expressed in SQL syntax. Using single INSERTs for CSV data would be impractically slow.

---

## Question 4

**True or False: A primary key is a type of index.**

- [x] True
- [ ] False

**Correct Answer:** True

**Explanation:** A primary key (PK) is implemented internally as a special type of unique index with these properties:
1. **Uniqueness** — No two rows can have the same PK value (enforced by a unique index)
2. **NOT NULL** — PK columns cannot contain NULL values
3. **Clustered (in InnoDB)** — In MySQL's InnoDB storage engine, the PK is a clustered index, meaning the actual table data is physically stored in the order of the PK. Secondary indexes store the PK value as the row pointer.
4. **One per table** — A table can have only one primary key, unlike regular indexes which can be many

[ENRICHED: defined "Clustered Index" — An index that determines the physical order of data in a table. InnoDB tables are always clustered on the primary key. If no PK is defined, InnoDB creates a hidden 6-byte row ID as an implicit clustered index. Clustered indexes offer fast PK lookups (one B+Tree traversal to find the row) but slower inserts at non-sequential PK values (page splits).]

[ENRICHED: performance context — The choice of primary key significantly impacts write performance in InnoDB. Auto-increment integer PKs are optimal because new rows are appended sequentially, avoiding page splits. UUID or randomly-generated PKs cause random insert patterns that lead to frequent page splits and index fragmentation, which degrades write throughput and increases storage usage.]

---

## Question 5

**After creating a new table in your database, you decide that you want to ensure that one of the fields always contains a value. What steps should you take?**

- [ ] Select the Unique option for the field.
- [ ] Turn off the Distinct values option for the field.
- [ ] There is no need to change anything in your table definition to make this happen.
- [x] Turn on the Not Null option for the field.

**Correct Answer:** Turn on the Not Null option for the field.

**Explanation:** The NOT NULL constraint prevents NULL values from being inserted into a column. When a column has NOT NULL, any INSERT or UPDATE that omits or sets NULL for that column will fail with an error. This enforces the requirement that the field "always contains a value."

SQL syntax:
```sql
CREATE TABLE employees (
    id INT NOT NULL,
    name VARCHAR(100) NOT NULL,  -- this field must always have a value
    email VARCHAR(255)           -- this field can be NULL
);
```

Or alter an existing table:
```sql
ALTER TABLE employees MODIFY name VARCHAR(100) NOT NULL;
```

[ENRICHED: defined "NULL" — In SQL, NULL represents the absence of a value, not the value zero or an empty string. It is a special marker indicating "unknown" or "missing." NULL propagates through expressions: any arithmetic or comparison involving NULL yields NULL, which is why `WHERE column = NULL` is incorrect — the correct check is `WHERE column IS NULL`.]

**Distractor Analysis:**
- **Unique option** — UNIQUE ensures all values in the column are distinct (no duplicates). It does not prevent NULLs. In MySQL, a UNIQUE constraint allows multiple NULL values (unlike some other databases).
- **Turn off the Distinct values option** — There is no "Distinct values" option in MySQL. This appears to be a fabricated distractor option, likely included to confuse students unfamiliar with MySQL's available constraints.
- **No need to change anything** — This is incorrect. By default, all columns in MySQL allow NULL values unless explicitly declared as NOT NULL. If you need a field to always contain a value, you must add the NOT NULL constraint.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Question 1 | Definition | Defined GPL and MySQL's dual-licensing model | HIGH |
| 2 | Question 2 | Ecosystem | Listed all MySQL interfaces beyond CLI and phpMyAdmin: Workbench, programmatic connectors, ORMs, third-party tools | HIGH |
| 3 | Question 3 | Performance context | Added LOAD DATA INFILE performance benchmark (20x faster than INSERT) and optimization tips | HIGH |
| 4 | Question 4 | Definition | Defined clustered index with InnoDB PK behavior, hidden row ID fallback, and page splits | HIGH |
| 5 | Question 4 | Performance context | Explained auto-increment vs. UUID PK performance tradeoffs with page split impact | HIGH |
| 6 | Question 5 | Definition | Defined NULL semantics in SQL (unknown marker, propagation, correct IS NULL check) | HIGH |
