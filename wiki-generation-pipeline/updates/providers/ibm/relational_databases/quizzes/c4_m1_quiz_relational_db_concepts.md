> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 1:** Fundamental Relational Database Concepts
> **Assessment:** Graded Quiz

# Quiz: Fundamental Relational Database Concepts

**Time:** 15 min
**Due:** Jul 8, 11:59 PM EEST

---

### Question 1

Data classification depends on the degree of structure and its flexibility. Which data type is often stored in SQL databases?

- Regulated data
- Semi-structured data
- Unstructured data
- **Structured data** ✅

<details>
<summary>Explanation</summary>

**Correct answer: Structured data.**

SQL databases (relational databases) are designed to store **structured data** — data that fits neatly into tables with predefined rows and columns, where each column has a specific data type and constraints.

- **Regulated data** is not a data classification category — it refers to data subject to compliance rules (GDPR, HIPAA, etc.).
- **Semi-structured data** (JSON, XML) can be stored in some modern SQL databases (PostgreSQL JSONB, MySQL JSON) but the fundamental model is structured.
- **Unstructured data** (images, PDFs, videos) is typically stored in BLOB fields or external object storage, not as the primary use case of SQL databases.

The three main data categories are **structured**, **semi-structured**, and **unstructured**. SQL databases are built for structured data.
</details>

---

### Question 2

Which of the following is a recognized type of information model?

- Root
- **Hierarchical** ✅
- Organization
- Tree

<details>
<summary>Explanation</summary>

**Correct answer: Hierarchical.**

The **hierarchical model** is a recognized type of information/data model that structures data in a tree-like format with parent-child relationships. It was one of the earliest database models, developed by IBM in the 1960s for IMS (Information Management System).

The other options are not recognized information model types:
- **Root** — a node in a tree/hierarchical structure, not a model type
- **Organization** — not a database model classification
- **Tree** — describes the structure of the hierarchical model, not a model type itself

[ENRICHED: deeper explanation of the hierarchical model]

### What Is the Hierarchical Model?

The hierarchical model organizes data into a **tree structure** where each record (node) has:
- **Exactly one parent** (except the root, which has none)
- **Zero or more children** (subordinate records)

Visual representation:
```
                    [Department]          ← Parent / Root
                   /      |      \
                  /       |       \
           [Employee]  [Project]  [Budget]  ← Children
              /    \
             /      \
      [Dependent] [Salary]                  ← Grandchildren
```

Each parent-child relationship is called a **segment relationship**. To find data, you must navigate the tree from the root, following parent-child paths — there is no direct lookup by value.

### How It Works — IMS (Information Management System)

IBM's IMS, still in production use today at many large banks and airlines, is the canonical implementation. Key mechanics:

- **Segments** — the building blocks, equivalent to a record/row in relational terms
- **Segment types** — the schema definition, equivalent to a table
- **Hierarchical paths** — the only way to access data: you start at the root segment and traverse down
- **DL/I (Data Language/I)** — the data manipulation language used to navigate and query IMS databases

Example — a banking IMS database:
```
[CUSTOMER]               ← Root segment (customer_id, name, address)
    |
    +--[ACCOUNT]         ← Child segment (account_number, balance, type)
    |     |
    |     +--[TRANSACTION]  ← Grandchild (txn_id, date, amount, type)
    |
    +--[LOAN]            ← Child segment (loan_id, amount, interest_rate)
          |
          +--[PAYMENT]   ← Grandchild (payment_id, date, amount, due)
```

To find all transactions for a specific customer, you:
1. Locate the CUSTOMER segment by its key
2. Navigate down to ACCOUNT (first child)
3. Navigate further down to TRANSACTION (child of ACCOUNT)
4. Issue sequential "get next" calls to read all transactions

This is fundamentally different from SQL's `SELECT * FROM transaction JOIN account JOIN customer WHERE customer_id = X` — in the hierarchical model, the physical path IS the query logic.

### Strengths of the Hierarchical Model

| Strength | Why It Matters |
|---|---|
| **Performance** | Extremely fast for predefined, predictable access patterns — data is physically stored in parent-child proximity. IMS can process **tens of thousands of transactions per second** due to minimal overhead. |
| **Data integrity** | The rigid structure ensures referential integrity by design — a child cannot exist without its parent. |
| **Simplicity for tree data** | Natural fit for hierarchical domains: organizational charts, bill of materials, genealogical trees, XML documents. |
| **Proven reliability** | IMS has been in continuous production for **over 55 years** — it powers the majority of the world's top banks' core banking systems, airline reservation systems (like SABRE), and government systems. |

### Weaknesses of the Hierarchical Model

| Weakness | Why It's a Problem |
|---|---|
| **Many-to-many relationships impossible** | A child can only have one parent. To represent "a doctor works at multiple hospitals," you must duplicate the doctor record under each hospital — causing data redundancy and update anomalies. |
| **Navigational access only** | You cannot ask "find all customers with balance > $10,000" directly. You must write procedural code to traverse the tree and check each account. This is the **navigational vs. declarative** divide. |
| **Structural rigidity** | Changing the hierarchy (adding a new child segment type under an existing parent) often requires unloading and reloading the entire database. Schema evolution is expensive. |
| **Query complexity** | Any non-hierarchical query (e.g., "which employees work on Project X AND speak French?") requires complex multi-path traversal in application code rather than a simple query. |

### Hierarchy of Data Models — Historical Evolution

```
1960s ──► Hierarchical Model (IBM IMS)
               │
               ├──► Network Model (CODASYL) ── allowed multiple parents,
               │     many-to-many, still navigational
               │
1970 ──► Relational Model (Codd) ── declarative, set-based,
               │     data independence, SQL
               │
1976 ──► Entity-Relationship Model (Chen)
               │     ── conceptual modeling, not an implementation model
               │
1990s–2000s ──► Object-Oriented, Object-Relational
               │
2000s–2010s ──► NoSQL: Document (MongoDB), Key-Value (Redis),
                    Column-Family (Cassandra), Graph (Neo4j)
```

### The Distractor Options Explained

| Option | Why It's Wrong | What It Actually Is |
|---|---|---|
| **Root** | Not a model type — a root is a specific *node* in a tree (the topmost node with no parent). Every hierarchical database has a root segment, but "root" is a position, not a model. | A node property within the hierarchical model |
| **Organization** | Not a recognized database classification — this is a business term, not a technical one. Sometimes "organization" is used informally to describe structure, but it has no formal definition in data modeling. | A business entity, not a data model |
| **Tree** | Describes the *shape* of the hierarchical model (tree = parent-child branching). But "tree" is a general data structure concept in computer science (used in file systems, routing algorithms, binary search trees), not a named database model. | A data structure, not a database model |

### Why the Hierarchical Model Still Matters Today

Despite being 55+ years old, the hierarchical model is not obsolete:

1. **IMS still runs the world's financial infrastructure** — many major banks run core banking on IMS, with relational databases layered on top for reporting. Migrating off IMS can cost hundreds of millions of dollars and take a decade.

2. **Modern NoSQL databases echo hierarchical concepts** — MongoDB's embedded documents (subdocuments nested within a parent document) mirror hierarchical parent-child relationships. The JSON document tree is essentially a hierarchical model with more flexible schema.

3. **XML databases** (like eXist-db, BaseX) are hierarchical by nature — XML documents are trees, and XPath/XQuery navigate them hierarchically.

4. **File systems are hierarchical** — directories/files, folders/subfolders. The mental model is so universal that users navigate it intuitively.

5. **SQL's recursive CTEs** (Common Table Expressions) handle hierarchical data within relational databases — e.g., `WITH RECURSIVE ...` to traverse org charts or bill-of-materials trees.

### Key Context: The Five Major Data Models

The hierarchical model is one of five historically recognized data models:

| Model | Year | Creator | Key Idea | Modern Descendants |
|---|---|---|---|---|
| **Hierarchical** | 1960s | IBM (IMS) | Tree structure, parent-child | IMS, XML, MongoDB (embedded docs) |
| **Network** | 1969 | CODASYL | Graph with multiple parents, sets | IDMS, Raima Database Manager |
| **Relational** | 1970 | E.F. Codd | Tables, set theory, declarative SQL | Db2, Oracle, MySQL, PostgreSQL |
| **Entity-Relationship** | 1976 | Peter Chen | Conceptual modeling, entities + relationships | ER/Studio, MySQL Workbench (design tools) |
| **Object-Oriented** | 1980s | Various | Objects, classes, inheritance | ObjectDB, Versant, Hibernate (ORM) |

In modern practice, the relational model dominates with **~80%+ market share**, graph models (Neo4j, Amazon Neptune) handle connected-data use cases, and document models (MongoDB) handle schema-flexible workloads. But the hierarchical model's influence persists in every layered system and tree-structured data format.
</details>

---

### Question 3

In Crow's Foot notation, how is the "many" side of a one-to-many relationship shown?

- A perpendicular line
- **A Crow's Foot (three-pronged/fork) symbol** ✅
- Equal sign
- Asterisk

<details>
<summary>Explanation</summary>

**Correct answer: A Crow's Foot (three-pronged/fork) symbol.**

In Crow's Foot notation:
- **Single vertical line (|)** — represents "exactly one"
- **Crow's foot (three-pronged fork, like Ⱬ or 𝌂 on its side)** — represents "many"
- **Circle (O)** — represents "zero" (optional)

A one-to-many relationship between Customer and Order is shown as: `Customer |---< Order` — the vertical line on the Customer side (exactly one customer), the crow's foot on the Order side (many orders).

The symbols derive from Information Engineering (IE) methodology by James Martin. Different notations use different symbols: Chen notation uses `1` and `M` labels; IDEF1X uses a dot on the "many" side.
</details>

---

### Question 4

When converting an ERD into a table, the entity transforms into the table itself. What do the attributes represent?

- Rows
- **Columns** ✅
- Relationships
- Cells

<details>
<summary>Explanation</summary>

**Correct answer: Columns.**

The ERD-to-table mapping process:
1. **Entity → Table** (e.g., the Book entity becomes the `book` table)
2. **Attributes → Columns** (e.g., ISBN, Title, Author become columns in the `book` table)
3. **Data values → Rows** (each row is one instance of the entity)

Common confusion: attributes do NOT become rows. Each row is an *instance* of the entity (one specific book), while each column represents an *attribute* describing every instance. A row represents a single record; a column represents a field that every record has.
</details>

---

### Question 5

Which data type is suitable for storing a variable-length string with a maximum length of 100 characters?

- **VARCHAR(100)** ✅
- CHAR(100)
- TEXT(100)
- ENUM

<details>
<summary>Explanation</summary>

**Correct answer: VARCHAR(100).**

- **VARCHAR(100)** — variable-length character string, up to 100 characters. Stores only the space needed (e.g., "Hello" uses 5 chars + overhead, not 100).
- **CHAR(100)** — fixed-length character string. Always uses 100 characters, padding with spaces. Wastes space for shorter strings.
- **TEXT(100)** — not valid SQL syntax. TEXT types don't take a length parameter in most databases (e.g., PostgreSQL TEXT has no length limit). Some databases like MySQL use TEXT for variable-length strings but the (100) syntax applies to VARCHAR only.

[ENRICHED: deeper explanation of TEXT vs. VARCHAR]

### Why TEXT(100) Is Invalid SQL

The syntax `TEXT(100)` is not valid in any major database. Here is why:

In SQL, **only certain data types accept a length parameter in parentheses**:

| Syntax | Valid? | Behavior |
|---|---|---|
| `VARCHAR(100)` | ✅ | Defines a variable-length string with a **maximum** of 100 characters |
| `CHAR(100)` | ✅ | Defines a fixed-length string of exactly 100 characters (padded with spaces) |
| `TEXT(100)` | ❌ | Not valid SQL — TEXT types do not accept a length parameter |
| `INT(11)` | ⚠️ | Valid in **MySQL only** — but the number is a **display width** for formatting, NOT a storage limit. MySQL's INT is always 4 bytes regardless of (11). This is a common MySQL-specific quirk that confuses beginners. |
| `DECIMAL(5,2)` | ✅ | Defines a decimal number with 5 total digits, 2 after the decimal point |

### What TEXT Actually Means in Different Databases

TEXT is a **variable-length string type with no explicit maximum** — but the actual maximum varies widely across databases:

| Database | TEXT Type | Max Size | Can You Specify (n)? | Notes |
|---|---|---|---|---|
| **PostgreSQL** | `TEXT` | Unlimited (up to 1 GB per column due to page size) | ❌ No | TEXT and VARCHAR are internally identical in PostgreSQL — the only difference is that VARCHAR(n) enforces a length check via a constraint, while TEXT does not. Performance is identical. |
| **MySQL** | `TINYTEXT` | 255 bytes | ❌ No | MySQL has **four** TEXT subtypes, each with a different max. None accepts (n). |
| | `TEXT` | 65,535 bytes (~64 KB) | ❌ No | |
| | `MEDIUMTEXT` | 16,777,215 bytes (~16 MB) | ❌ No | |
| | `LONGTEXT` | 4,294,967,295 bytes (~4 GB) | ❌ No | |
| **SQL Server** | `VARCHAR(MAX)` | ~2 GB | ❌ No (but uses `MAX` keyword) | SQL Server doesn't have a plain TEXT type for new development — it uses `VARCHAR(MAX)`, `NVARCHAR(MAX)`, or `VARBINARY(MAX)` instead. The legacy `TEXT` type exists but is deprecated. |
| **Oracle** | `CLOB` | ~4 GB | ❌ No | Oracle uses CLOB (Character Large Object) for large text. VARCHAR2(n) is the standard string type. |

Key takeaway: **no database allows `TEXT(100)`**. If you see `TEXT(100)`, it is almost certainly a confusion with `VARCHAR(100)`.

### The PostgreSQL Special Case: TEXT and VARCHAR Are the Same

PostgreSQL treats `TEXT` and `VARCHAR` as the **same underlying type** with one difference:

```sql
-- These two are functionally identical in PostgreSQL:
CREATE TABLE t1 (name TEXT);
CREATE TABLE t2 (name VARCHAR);

-- This adds a length constraint:
CREATE TABLE t3 (name VARCHAR(100));
-- Equivalent to:
CREATE TABLE t4 (name TEXT CHECK (LENGTH(name) <= 100));
```

Internally, PostgreSQL stores both as `varlena` (variable-length array) type. The storage format, compression behavior, and performance are **identical**. The only difference is that `VARCHAR(n)` enforces a length check on INSERT/UPDATE.

Many PostgreSQL developers prefer `TEXT` with a CHECK constraint because:
1. It makes the constraint explicit (visible in `information_schema` constraints)
2. Changing the max length later is an ALTER TABLE to drop/recreate the constraint rather than changing the column type
3. It avoids the misconception that `VARCHAR` vs. `TEXT` has performance implications (it doesn't in PostgreSQL)

### The Storage Cost Difference

Even though `VARCHAR(100)` and `TEXT` are functionally similar, there is a subtle storage difference:

| Type | Overhead | Behavior |
|---|---|---|
| `VARCHAR(n)` | 1–2 bytes overhead | Data stored **inline** in the table row. If the string is short, it stays with the rest of the row's data — fast to read. |
| `TEXT` / `VARCHAR(MAX)` | 1–4 bytes overhead + possible **TOAST** | In PostgreSQL, strings exceeding ~2 KB are automatically moved to a **TOAST table** (The Oversized-Attribute Storage Technique). The main row stores a pointer (18 bytes). Reading TOASTed values requires an extra disk lookup — **2x slower** on average than inline storage. |

Practical implication: for columns that will **almost always** be under 100 characters (names, emails, phone numbers), `VARCHAR(100)` keeps data inline and avoids TOAST overhead. For columns that may contain large text blocks (descriptions, comments, JSON), `TEXT` is correct — you want TOAST to kick in for the large values.

### So What Should You Use?

| Scenario | Recommended Type | Why |
|---|---|---|
| Short string, known max | `VARCHAR(n)` | Enforces length, inline storage, universally portable |
| Short string, no fixed max | `VARCHAR(255)` or `TEXT` with CHECK | Flexible, with or without constraint depending on business rules |
| Long text (paragraphs, articles) | `TEXT` (or `CLOB` in Oracle) | Handles large values, TOAST optimization kicks in automatically |
| Fixed-length code (ISO country) | `CHAR(2)` | Fixed length guarantees, no length overhead, semantically correct |
| JSON / structured text | `JSONB` (PostgreSQL) or `TEXT` | Use native JSON type when available (faster querying, validation) |

### Summary Table for Q5's Options

| Option | Analysis | Verdict |
|---|---|---|
| `VARCHAR(100)` | Variable-length, max 100 chars, space-efficient, standard SQL | ✅ **Correct** |
| `CHAR(100)` | Fixed-length, always 100 chars, wastes space for shorter strings | ❌ Not best for variable-length data |
| `TEXT(100)` | **Not valid syntax** in any database. TEXT types don't take (n). | ❌ Invalid syntax |
| `ENUM` | Predefined list of values (e.g., ENUM('Small', 'Medium', 'Large')). Not for free-form text. | ❌ Wrong type for the use case |
- **ENUM** — a list of predefined values (e.g., ENUM('Small', 'Medium', 'Large')). Not appropriate for free-form strings.

VARCHAR is the correct choice for variable-length strings because (1) it's space-efficient (only allocates what's needed up to the max), (2) it enforces the length constraint, and (3) it's the standard SQL type for this purpose across all major databases.
</details>

---

## Answer Key

| Q | Answer | Concept |
|---|---|---|
| 1 | Structured data | Data classification categories |
| 2 | Hierarchical | Types of information/data models |
| 3 | Crow's Foot symbol | ERD notation |
| 4 | Columns | ERD-to-table mapping |
| 5 | VARCHAR(100) | Data types — variable-length strings |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Explanation | Distinguished structured/semi-structured/unstructured with storage system mapping; clarified "regulated data" is not a classification category | HIGH |
| 2 | Q2 | Deeper Explanation | Replaced with comprehensive hierarchical model coverage: tree structure visualization, IMS mechanics and banking example, strengths/weaknesses table, historical evolution timeline, distractor analysis (root/tree/organization), modern relevance (IMS still runs banking, MongoDB echoes hierarchy, XML/file systems), five major data models comparison table | HIGH |
| 3 | Q3 | Explanation | Explained crow's foot symbol system (| for one, Ⱬ for many, O for zero); noted notation differences across Chen/IE/IDEF1X | HIGH |
| 4 | Q4 | Explanation | Walked the full ERD-to-table mapping pipeline; clarified that rows = instances, not attributes | HIGH |
| 5 | Q5 | Deeper Explanation | Expanded TEXT(100) invalidity coverage: DATATYPE(n) syntax rules table, cross-database TEXT type comparison (PostgreSQL/MySQL/SQL Server/Oracle), PostgreSQL TEXT vs. VARCHAR internals (identical), TOAST storage overhead, practical selection guide per scenario | HIGH |
