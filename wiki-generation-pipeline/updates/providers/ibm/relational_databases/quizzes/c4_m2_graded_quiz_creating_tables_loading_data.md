> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 2:** Creating Tables and Loading Data & Designing Keys, Indexes, and Constraints
> **Quiz:** Graded Quiz — Creating Tables and Loading Data

# Graded Quiz: Creating Tables and Loading Data

**Due:** Jul 13, 11:59 PM EEST  
**Attempts:** 3 (every 8 hours)  
**Pass required:** Yes

---

## Question 1

**Which of the following steps in the data loading process uses the Load Data utility and requires authentication to the storage?**

- Source
- Define
- Finalize
- Target

**Correct answer: Source**

[ENRICHED: explanation — The **Source** step is where you specify the location of the data file and provide any required authentication credentials. For IBM Cloud Object Storage, this means providing the COS endpoint, access key, and secret access key. For Amazon S3, AWS credentials are required. Only a locally stored CSV file requires no authentication — you simply select the file to upload. See `lessons/c4_m2_loading_data.md` Step 1 for details on authentication fields.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Source** (correct) | Authentication to cloud storage is entered in the Source step. |
| **Define** (incorrect) | The Define step configures encoding, delimiter, header row, and date/time formats — no storage authentication. |
| **Finalize** (incorrect) | The Finalize step is a review screen before execution — no authentication. |
| **Target** (incorrect) | The Target step selects the schema and table and chooses append vs. overwrite — no storage authentication. |

---

## Question 2

**After creating a new table in the COR38310 schema and naming it Engineers, what is the fully qualified name for this table?**

- Engineers
- COR38310/Engineers
- COR38310.Engineers
- Engineers.COR38310

**Correct answer: COR38310.Engineers**

[ENRICHED: explanation — In Db2 (and most relational databases), the fully qualified table name follows the format `schema.table_name`. The schema comes first, followed by a dot, then the table name. Given schema `COR38310` and table `Engineers`, the fully qualified name is `COR38310.Engineers`. The default schema in Db2 is often the username, and each user has a unique username in their database. See `lessons/c4_m2_creating_tables.md` Step 1 (Select Schema) and `lessons/c4_m2_create_table_statement.md` for the CREATE TABLE syntax with schema qualification.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Engineers** (incorrect) | This is just the table name without the schema qualifier. The fully qualified name includes the schema. |
| **COR38310/Engineers** (incorrect) | A forward slash is not the SQL standard separator — dot notation is used in Db2, PostgreSQL, MySQL, and SQL Server. |
| **COR38310.Engineers** (correct) | `schema.table` — dot notation is the correct SQL standard. |
| **Engineers.COR38310** (incorrect) | This reverses the order. The schema always precedes the table name. |

---

## Question 3

**Various databases support multiple file formats. Which of the following prevalent formats encompasses CSV files?**

- JavaScript Object Notation (JSON)
- Delimited ASCII (DEL)
- Non-delimited ASCII (ASC)
- PC Integration exchange (PC/IXF)

**Correct answer: Delimited ASCII (DEL)**

[ENRICHED: explanation — CSV (Comma-Separated Values) files are a specific type of **Delimited ASCII (DEL)** format where column values are separated by a designated delimiter (typically a comma). The DEL format category includes comma-delimited (`.csv`), tab-delimited (`.tsv`), pipe-delimited (`.psv`), and semicolon-delimited variants. The Db2 IMPORT and EXPORT utilities use `OF DEL` to specify this format. See `lessons/c4_m2_data_movement_utilities.md` for the detailed file format comparison including DEL delimiter variants.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **JSON** (incorrect) | JSON (JavaScript Object Notation) is a hierarchical key-value format used primarily for web APIs. Unlike CSV/DEL, it has field names repeated per row and supports nested structures. |
| **Delimited ASCII (DEL)** (correct) | CSV files are a subtype of the DEL format — each column is separated by a delimiter character. |
| **ASC (Non-delimited ASCII)** (incorrect) | ASC (fixed-width/non-delimited ASCII) uses column positions rather than delimiters. Columns are defined by character position ranges, not separator characters. |
| **PC/IXF** (incorrect) | PC/IXF (Integration Exchange Format) is IBM's proprietary binary format that stores both schema metadata and data. Unlike DEL/CSV, it is not human-readable in a text editor. |

---

## Question 4

**True or False: A primary key uniquely identifies each row in a table.**

- True
- False

**Correct answer: True**

[ENRICHED: explanation — The primary key is a fundamental relational database concept. By definition, a primary key uniquely identifies each tuple (row) in a relation (table). It implicitly enforces both `UNIQUE` (no duplicate values) and `NOT NULL` (no null values) constraints. A table can have at most one primary key, which may consist of a single column (simple key) or multiple columns (composite key). See `lessons/c4_m2_create_table_statement.md` for primary key syntax in CREATE TABLE and `lessons/c4_m2_creating_tables.md` for key considerations before table creation.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **True** (correct) | Primary keys ensure every row is uniquely identifiable — this is the definition. |
| **False** (incorrect) | The statement directly matches the definition of a primary key in the relational model. |

---

## Question 5

**What are DML statements sometimes referred to as?**

- UPDATE
- Modifier
- CREATE
- CRUD

**Correct answer: CRUD**

[ENRICHED: explanation — DML (Data Manipulation Language) statements are sometimes referred to as **CRUD** operations, which stands for **C**reate, **R**ead, **U**pdate, **D**elete. The mapping is: INSERT → Create, SELECT → Read, UPDATE → Update, DELETE → Delete. CRUD is a broader software engineering concept that applies to any persistent storage system, not just SQL databases. See `lessons/c4_m2_types_of_sql_statements_ddl_dml.md` for the full DDL/DML breakdown and CRUD mapping table including ORM framework equivalents.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **UPDATE** (incorrect) | UPDATE is a specific DML statement, not a name for the category as a whole. |
| **Modifier** (incorrect) | "Modifier" is not a standard SQL category term. |
| **CREATE** (incorrect) | CREATE is a DDL statement, not DML. |
| **CRUD** (correct) | CRUD (Create, Read, Update, Delete) is the common acronym for all DML operations collectively. |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Explanation | Connected Source step authentication to Loading Data lesson with COS/S3 credential context | HIGH |
| 2 | Q2 | Explanation | Connected schema.table naming to Creating Tables and CREATE TABLE Statement lessons | HIGH |
| 3 | Q3 | Explanation | Connected DEL/CSV format to Data Movement Utilities lesson with delimiter variant details | HIGH |
| 4 | Q4 | Explanation | Connected primary key definition to CREATE TABLE Statement lesson with composite key note | HIGH |
| 5 | Q5 | Explanation | Connected CRUD acronym to DDL vs. DML lesson with CRUD mapping and ORM examples | HIGH |
