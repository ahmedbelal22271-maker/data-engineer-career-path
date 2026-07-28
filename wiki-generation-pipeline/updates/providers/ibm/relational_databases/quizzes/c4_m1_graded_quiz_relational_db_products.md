> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 1:** Introducing Relational Database Products
> **Assessment:** Graded Quiz

# Graded Quiz: Introducing Relational Database Products

**Time:** 15 min
**Due:** Jul 10, 11:59 PM EEST
**Attempts:** 3 (every 8 hours)

---

### Question 1

What is the purpose of database replication in a distributed database architecture?

- High availability
- Improved performance
- Disaster recovery
- **All of the above** ✅

<details>
<summary>Explanation</summary>

**Correct answer: All of the above.**

Database replication serves all three purposes in a distributed architecture:

1. **High availability** — If the primary node fails, a standby replica can be promoted to take over with minimal downtime. Clients continue to access the database without disruption.
2. **Improved performance** — Read replicas offload query traffic from the primary. Applications can route read-only queries (SELECT) to replicas while writes go to the primary, effectively scaling read throughput linearly with the number of replicas.
3. **Disaster recovery** — Replicas in different geographic regions or data centers protect against site-wide failures (natural disasters, power outages, network partitions). Data survives even if one location is completely destroyed.

[ENRICHED: replication modes — Different replication strategies offer different tradeoffs between these three goals:
- **Synchronous replication** — The primary waits for at least one replica to acknowledge the write before confirming to the client. This guarantees zero data loss (best for disaster recovery) but increases write latency. Used in Db2 HADR SYNC mode and PostgreSQL synchronous_commit = 'on'.
- **Asynchronous replication** — The primary commits without waiting for replicas. This minimizes write latency (best for performance) but risks losing recent transactions if the primary fails before the replica catches up. Used in MySQL async replication and PostgreSQL streaming replication with synchronous_commit = 'off'.
- **Semi-synchronous replication** — A compromise: the primary waits for one replica to acknowledge but does not wait for all. Balances performance with some data-loss protection.

**Reference:** See `../lessons/c4_m1_distributed_architecture_clustered_databases.md` for replication architectures and HADR mode comparison.]

</details>

---

### Question 2

Which of the following classes of database users are more likely to use Object Relational Mapping (ORM) in their workloads?

- Data Scientists
- **Application Developers** ✅
- Database Administrators
- Data Engineers

<details>
<summary>Explanation</summary>

**Correct answer: Application Developers.**

Application Developers are the primary users of ORMs because they build and maintain application code that needs to interact with databases. ORMs (such as Hibernate for Java, SQLAlchemy for Python, Entity Framework Core for .NET, Prisma for TypeScript, ActiveRecord for Ruby on Rails, and Django ORM for Python) allow developers to work with database records as if they were objects in their programming language, abstracting away raw SQL.

- **Data Scientists** typically use SQL directly or through data frame libraries (pandas, dplyr), not ORMs. Their focus is on analysis and modeling, not application CRUD operations.
- **Database Administrators** manage the database infrastructure itself — they use administrative tools (pgAdmin, MySQL Workbench) and SQL directly, not ORMs.
- **Data Engineers** build data pipelines using ETL/ELT tools (Apache Spark, Airflow, dbt) and often write raw SQL or use DataFrame APIs. While some may use ORMs in pipeline code, it is not their defining tool.

[ENRICHED: ORM tradeoffs — ORMs provide developer productivity (auto-generated SQL, migration management, connection pooling) at the cost of:
- **N+1 query problem** — Inefficient lazy loading can generate hundreds of queries where a single JOIN would suffice.
- **SQL transparency** — Complex queries (window functions, recursive CTEs, full-text search) are often easier to write and optimize as raw SQL than as ORM expressions.
- **Performance ceiling** — ORM-generated SQL is rarely as efficient as hand-tuned SQL for high-throughput workloads.

The N+1 problem and ORM comparison table are covered in `../lessons/c4_m1_database_usage_patterns.md`.]

**Reference:** See `../lessons/c4_m1_database_usage_patterns.md` for the full role comparison table and ORM coverage.

</details>

---

### Question 3

MySQL facilitates various storage engines. Among the options provided, which storage engines that MySQL supports employ table-level locking?

- NDB
- InnoDB
- Falcon
- **MyISAM** ✅

<details>
<summary>Explanation</summary>

**Correct answer: MyISAM.**

**MyISAM** is the MySQL storage engine that uses **table-level locking**. When a query writes to a MyISAM table, the entire table is locked — no other session can read or write to it until the write completes. This makes MyISAM simple and fast for read-heavy workloads but poor for concurrent write workloads.

- **InnoDB** (the default since MySQL 5.5) uses **row-level locking** with MVCC (Multi-Version Concurrency Control). Multiple sessions can modify different rows in the same table simultaneously without blocking each other, making it suitable for high-concurrency OLTP workloads.
- **NDB** (MySQL Cluster) uses **row-level locking** with distributed storage across multiple data nodes. It is designed for high availability and real-time performance.
- **Falcon** was an experimental storage engine developed by MySQL AB that used row-level locking. It was never fully released and was discontinued after Oracle acquired Sun Microsystems.

[ENRICHED: locking granularity comparison —
| Engine | Locking Level | Concurrency | Best For |
|---|---|---|---|
| MyISAM | Table-level | Low — one writer blocks all others | Read-only or read-mostly workloads, data warehousing |
| InnoDB | Row-level (with MVCC) | High — concurrent reads and writes to different rows | OLTP, web applications, high-concurrency systems |
| NDB | Row-level (distributed) | Very high — distributed across nodes | Real-time, high-availability, telecom/finance |

MyISAM's table-level locking means a single slow UPDATE can block all other operations on that table for seconds or minutes. InnoDB's row-level locking allows thousands of concurrent transactions on the same table, which is why InnoDB became the MySQL default in 5.5 (2010).]

**Reference:** See `../lessons/c4_m1_mysql_introduction.md` for MySQL storage engines, replication, and history.

</details>

---

### Question 4

PostgreSQL is a database management system with an object-relational architecture. What significance does the "object" aspect hold within PostgreSQL?

- Database management
- Uses Postgres source code
- Supports high availability and scalability
- **Supports inheritance and overloading** ✅

<details>
<summary>Explanation</summary>

**Correct answer: Supports inheritance and overloading.**

The "object" in PostgreSQL's object-relational architecture refers to object-oriented features that extend the standard relational model:

1. **Table inheritance** — A child table can inherit columns from a parent table. Queries on the parent table can optionally include data from all child tables. Example:
   ```sql
   CREATE TABLE vehicle (id SERIAL, make TEXT, model TEXT);
   CREATE TABLE car (doors INT) INHERITS (vehicle);
   -- car inherits id, make, model from vehicle, adds doors
   ```

2. **Function overloading** — Multiple functions can share the same name as long as they have different parameter types. Example:
   ```sql
   CREATE FUNCTION calculate(x INTEGER) RETURNS INTEGER ...
   CREATE FUNCTION calculate(x NUMERIC) RETURNS NUMERIC ...
   -- PostgreSQL resolves which to call based on argument type
   ```

3. **User-defined types (UDTs)** — Developers can define custom data types using `CREATE TYPE`, extending the built-in type system.

4. **Operator overloading** — Custom operators can be defined for user-defined types.

- **Database management** — This is true of all DBMSs, not specific to PostgreSQL's object features.
- **Uses Postgres source code** — This is circular (PostgreSQL derives from POSTGRES) and describes lineage, not the object-relational significance.
- **Supports high availability and scalability** — PostgreSQL supports these through streaming replication, logical replication, and extensions like Patroni and Citus, but these are infrastructure features, not the "object" aspect of its architecture.

[ENRICHED: object-relational vs. pure relational — Traditional relational databases (MySQL, SQLite) strictly follow Codd's relational model with flat tables and scalar types. PostgreSQL extends this by allowing:
- **Nested relations** (composite types as column types)
- **Array columns** (multi-valued attributes in a single column)
- **Custom operators and indexing methods** (GIN for JSONB, GiST for geometric data, BRIN for time-series)
- **Polymorphic functions** (functions accepting or returning `anyelement`, `anyarray`)

These features make PostgreSQL uniquely suited for hybrid workloads that mix structured relational data with semi-structured (JSON/JSONB), geospatial (PostGIS), vector embeddings (pgvector), and time-series (TimescaleDB) data — all within a single database.]

**Reference:** See `../lessons/c4_m1_postgresql_introduction.md` for PostgreSQL object-relational features, extensions, and historical context (1986 POSTGRES project through PG 17).

</details>

---

### Question 5

A relation consists of columns and rows, with columns representing attributes or fields. What is the term used to describe the individual entries in the rows of a table?

- Struct
- Tuples
- Degree
- **Data values** ✅

<details>
<summary>Explanation</summary>

**Correct answer: Data values.**

The "individual entries in the rows of a table" refers to the specific piece of data stored at the intersection of a row and a column — each cell in the table. These are called **data values** (or more precisely in relational theory, **attribute values**).

- **Tuples** — The correct term for entire rows, not individual entries within them. A tuple is a complete set of attribute values representing one record. Example: `(101, 'Alice', 'HR')` is a tuple (one row).
- **Degree** — The number of columns (attributes) in a relation. This is a structural property of the schema, not data within the rows.
- **Struct** — Not a standard relational model term. Struct is a programming language concept (C/C++ struct, Python struct module) that groups related variables but is not used in relational database theory.
- **Data values** — Each cell at a specific row-column intersection contains a single data value. For example, in a Car table with columns (Serial_no, Model, Manufacturer), the entry "Camry" in the Model column for a specific row is a data value.

[ENRICHED: relational terminology hierarchy —
| Term | Refers To | Example (Car table) |
|---|---|---|
| **Relation** | The entire table structure + data | The `Car` table |
| **Attribute** | A column/field definition | `Model` (the column) |
| **Tuple** | A complete row | `(SN001, Camry, Toyota, 25000)` |
| **Data value / Attribute value** | A single cell's content | `"Camry"`, `"Toyota"`, `25000` |
| **Degree** | Number of attributes (columns) | `4` (Serial_no, Model, Manufacturer, Price) |
| **Cardinality** | Number of tuples (rows) | Depends on how many cars are stored |

The natural language confusion: people often say "the value of the Model column" when they mean the column definition, or "the row contains values" when they mean the tuple. The precise term for a single cell entry is **data value** or **attribute value**.]

**Reference:** See `../lessons/c4_m1_relational_model_concepts.md` for the full degree vs. cardinality discussion and relational terminology.

</details>

---

## Summary

| # | Topic | Correct Answer | Key Concept |
|---|---|---|---|
| 1 | Database Replication Purpose | All of the above | Replication serves HA, performance, AND disaster recovery (synchronous vs. asynchronous tradeoffs) |
| 2 | ORM Users | Application Developers | ORMs map database records to programming-language objects for CRUD operations |
| 3 | MySQL Table-Level Locking | MyISAM | MyISAM = table-level locking; InnoDB = row-level + MVCC; NDB = row-level distributed |
| 4 | PostgreSQL Object Aspect | Supports inheritance and overloading | Object-relational features: table inheritance, function overloading, UDTs, operator overloading |
| 5 | Individual Row Entries | Data values | Tuples = entire rows; data values = individual cell entries; degree = column count |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Replication modes | Added synchronous/async/semi-sync comparison with Db2 and PostgreSQL examples | HIGH |
| 2 | Q1 | Cross-reference | Linked to distributed architecture file for HADR modes | HIGH |
| 3 | Q2 | ORM tradeoffs | Added N+1 problem, SQL transparency, and performance ceiling as ORM drawbacks | HIGH |
| 4 | Q2 | Cross-reference | Linked to database usage patterns file for role comparison table | HIGH |
| 5 | Q3 | Locking comparison table | Built 3-row engine comparison (MyISAM/InnoDB/NDB) across locking level, concurrency, and best-use | HIGH |
| 6 | Q3 | Cross-reference | Linked to MySQL introduction file for storage engine details | HIGH |
| 7 | Q4 | Object-relational features | Added concrete SQL example of table inheritance and function overloading | HIGH |
| 8 | Q4 | Object-relational vs. pure relational | Enumerated PostgreSQL extensions beyond standard relational model (composite types, arrays, custom indexing, polymorphic functions) | HIGH |
| 9 | Q4 | Cross-reference | Linked to PostgreSQL introduction file for history and extension ecosystem | HIGH |
| 10 | Q5 | Terminology hierarchy | Built 7-row relational terminology table (relation, attribute, tuple, data value, degree, cardinality) | HIGH |
| 11 | Q5 | Cross-reference | Linked to relational model concepts file for degree/cardinality coverage | HIGH |
