> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 2:** Creating Tables and Loading Data & Designing Keys, Indexes, and Constraints
> **Quiz:** Graded Quiz — Designing Keys, Indexes, and Constraints

# Graded Quiz: Designing Keys, Indexes, and Constraints

**Total Questions:** 5
**Passing Score:** 80%

---

### Question 1

Which of the following clauses in the CREATE TABLE statement creates a primary key?

A. CONSTRAINT
B. PRIMARY KEY
C. ALTER TABLE
D. REFERENCES

<details>
<summary>Answer</summary>

**B. PRIMARY KEY**

The `PRIMARY KEY` clause in a `CREATE TABLE` statement defines the primary key constraint. It can appear as a column-level constraint (`book_id CHAR(10) PRIMARY KEY`) or a table-level constraint (`PRIMARY KEY (book_id)`).

- **A** `CONSTRAINT` is a keyword used to name a constraint (e.g., `CONSTRAINT pk_book PRIMARY KEY (book_id)`), but it is not the clause that creates the primary key — `PRIMARY KEY` is.
- **C** `ALTER TABLE` is a separate statement used to modify an existing table, not a clause within `CREATE TABLE`.
- **D** `REFERENCES` is used in a `FOREIGN KEY` definition to specify which parent table and column the foreign key links to.
</details>

---

### Question 2

What automatically generates an index when created?

A. Foreign key
B. Table
C. Primary key
D. None of the above

<details>
<summary>Answer</summary>

**C. Primary key**

When you define a `PRIMARY KEY` constraint, the database system automatically creates a unique index on the primary key columns to enforce uniqueness and enable fast lookups. Similarly, a `UNIQUE` constraint also auto-generates an index.

- **A** A foreign key does **not** automatically generate an index. This is a common misconception — while FK columns should almost always be indexed for JOIN performance, the DBMS does not create the index automatically. You must create it manually with `CREATE INDEX`.
- **B** Creating a table does not generate any indexes unless a PK or UNIQUE constraint is defined.
- **D** is incorrect because primary keys do auto-generate indexes.
</details>

---

### Question 3

Which constraint among the following uniquely identifies each tuple (or row) in a table?

A. Check constraint
B. Entity integrity constraint
C. Positive constraint
D. Domain constraint

<details>
<summary>Answer</summary>

**B. Entity integrity constraint**

The entity integrity constraint ensures that every row has a unique, non-null primary key. It is enforced through the `PRIMARY KEY` constraint, which guarantees that no two rows have the same key value and that no part of the primary key is NULL.

- **A** A check constraint validates that column values satisfy a boolean expression — it does not enforce uniqueness.
- **C** "Positive constraint" is not a real SQL constraint type.
- **D** A domain constraint restricts the set of valid values for a column (via data types or CHECK) — it does not uniquely identify rows.
</details>

---

### Question 4

True or False: The term 'database instance' is used consistently across all relational database systems.

A. True
B. False

<details>
<summary>Answer</summary>

**B. False**

The term "instance" has different meanings across relational database systems:

- **In Db2, MySQL, PostgreSQL, SQL Server:** An instance refers to a **running DBMS process** — a server with its own memory, configuration files, authentication, and data directories. One server can run multiple instances. This is the **systems definition** used by this course.
- **In Oracle:** An "instance" refers specifically to the **memory structures and background processes** (System Global Area + processes), while the physical data on disk is called the "database." Oracle uses a two-part model (instance + database) that differs from other RDBMSs.
- **In database theory (Elmasri & Navathe):** A "database instance" or "database state" is the **actual data in the database at a given moment in time** — the set of all tuples currently stored.

Because different RDBMSs and reference sources use the term differently, it is **not** used consistently.
</details>

---

### Question 5

Which requirement specifically characterizes 1NF?

A. The table must already be in the third normal form (3NF) and the second normal form (2NF).
B. The table must have a Primary Key
C. Each table must have no more than three columns
D. Each cell must hold only a single (atomic) value (no lists/repeating groups)

<details>
<summary>Answer</summary>

**D. Each cell must hold only a single (atomic) value (no lists/repeating groups)**

First Normal Form (1NF) requires that every column in a table contains only atomic (indivisible) values. It prohibits:
- **Repeating groups:** multiple values in a single cell (e.g., a `phone_numbers` column containing "555-0101, 555-0102")
- **Arrays or lists:** storing collections within a single column
- **Nested tables:** having a table within a table

To satisfy 1NF, repeating groups must be moved to a separate related table (e.g., a `phone_numbers` table with one row per phone number per person).

- **A** is incorrect — 1NF is the first and most basic normal form. A table does not need to be in 2NF or 3NF first. The normal forms are sequential: 1NF → 2NF → 3NF.
- **B** Having a primary key is not a requirement of 1NF specifically — it is a general good practice (entity integrity), not part of the 1NF definition.
- **C** There is no 3-column limit in any normal form.
</details>

---

## Cross-Reference

- **Lesson:** `lessons/c4_m2_primary_keys_foreign_keys.md` (Q1, Q2)
- **Lesson:** `lessons/c4_m2_relational_model_constraints_advanced.md` (Q3)
- **Lesson:** `lessons/c4_m2_database_objects_and_hierarchy.md` (Q4)
- **Summary:** `summaries/c4_m2_summary_designing_keys_indexes_constraints.md` (Q5)
