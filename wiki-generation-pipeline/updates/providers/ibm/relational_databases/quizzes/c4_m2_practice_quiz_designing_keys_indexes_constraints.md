> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 2:** Creating Tables and Loading Data & Designing Keys, Indexes, and Constraints
> **Quiz:** Practice Quiz — Designing Keys, Indexes, and Constraints

# Practice Quiz: Designing Keys, Indexes, and Constraints

**Total Questions:** 5
**Passing Score:** 80%

---

### Question 1

What is the purpose of a primary key in a table?

A. Define columns in the table
B. Define rows in the table
C. Uniquely identify each row in the table
D. Enable real-time data processing

<details>
<summary>Answer</summary>

**C. Uniquely identify each row in the table**

A primary key ensures that every row in a table can be uniquely identified. The entity integrity rule requires that no two rows share the same primary key value and no part of the primary key is NULL.

- **A** describes the purpose of the CREATE TABLE statement column definitions, not the primary key.
- **B** rows are data instances, not defined by the primary key.
- **D** real-time processing is a system capability, unrelated to primary keys.
</details>

---

### Question 2

What function does an index provide?

A. Slowly checks each row in turn
B. Stores primary and foreign keys
C. Easily locate a specific row or set of rows
D. Stores metadata

<details>
<summary>Answer</summary>

**C. Easily locate a specific row or set of rows**

An index is a data structure (typically a B+Tree) that stores sorted key values with pointers to the corresponding table rows. The DBMS uses the index to quickly navigate to the target rows instead of scanning every row in the table (a full table scan).

- **A** describes a sequential/full table scan — the opposite of what an index provides.
- **B** indexes can be created on any column, not just PK/FK columns. PKs and UNIQUE constraints automatically create indexes, but the index itself does not "store" the constraints.
- **D** metadata is stored in system catalogs/schemas (e.g., SYSCAT, information_schema), not in user-created indexes.
</details>

---

### Question 3

Which type of constraint is responsible for defining relationships between tables?

A. Semantic integrity constraint
B. Referential integrity constraint
C. Null constraint
D. Default constraint

<details>
<summary>Answer</summary>

**B. Referential integrity constraint**

Referential integrity is enforced by FOREIGN KEY constraints. It ensures that a value in a foreign key column must match an existing primary key value in the referenced (parent) table, or be NULL. This defines and maintains the relationships between tables.

- **A** semantic integrity ensures data correctness/meaning (e.g., no garbage values in a city column) — it does not define table relationships.
- **C** null constraint (NOT NULL) prevents NULL values in a column — unrelated to relationships.
- **D** default constraint assigns a default value when no value is provided — unrelated to relationships.
</details>

---

### Question 4

Which object in a relational database is the primary structure used to store data?

A. Indexes
B. Functions
C. Tables
D. All of the above

<details>
<summary>Answer</summary>

**C. Tables**

Tables (also called relations) are the fundamental storage structure in a relational database. Data is organized into rows (tuples) and columns (attributes) within tables.

- **A** indexes are supporting structures that speed up data retrieval — they do not store the primary data, only sorted key values with pointers.
- **B** functions (stored procedures, UDFs) are programmatic objects that process data — they are not storage structures.
- **D** is incorrect because indexes and functions are not primary data storage structures.
</details>

---

### Question 5

How does normalization help speed up transactions?

A. Improves data integrity
B. Increases data duplication
C. Creates more tables
D. Enables you to perform updates only once on normalized databases

<details>
<summary>Answer</summary>

**D. Enables you to perform updates only once on normalized databases**

Normalization eliminates data redundancy by organizing data into separate related tables. When data is stored in only one place, an update needs to modify only one row in one table, rather than multiple redundant copies across the database. This speeds up UPDATE and DELETE transactions.

- **A** improving data integrity is a benefit of normalization, but it is about data correctness, not transaction speed.
- **B** normalization reduces duplication — this statement is false.
- **C** creating more tables is a means to eliminate redundancy, not a direct way to speed up transactions. More tables can actually slow down queries that need JOINs.
</details>

---

## Cross-Reference

- **Lesson:** `lessons/c4_m2_database_objects_and_hierarchy.md` (Q4)
- **Lesson:** `lessons/c4_m2_primary_keys_foreign_keys.md` (Q1)
- **Lesson:** `lessons/c4_m2_overview_of_indexes.md` (Q2)
- **Lesson:** `lessons/c4_m2_relational_model_constraints_advanced.md` (Q3)
- **Summary:** `summaries/c4_m2_summary_designing_keys_indexes_constraints.md` (Q5)
