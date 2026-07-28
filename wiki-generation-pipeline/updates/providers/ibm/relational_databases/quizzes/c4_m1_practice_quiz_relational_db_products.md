> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 1:** Introducing Relational Database Products
> **Assessment:** Practice Quiz

# Practice Quiz: Introducing Relational Database Products

**Time:** 10 min
**Due:** Jul 10, 11:59 PM EEST
**Attempts:** Unlimited (not counted toward course grade)

---

### Question 1

Which of the following deployment topologies allows users access to the database stored on a remote server from their client systems?

- Local / Desktop
- **Client / Server** ✅
- Cloud
- Application Server layer

<details>
<summary>Explanation</summary>

**Correct answer: Client / Server.**

The **client-server topology** (also called two-tier architecture) consists of client systems (front-end applications) that connect directly to a database server over a network. The database resides on the remote server, and clients send queries through a driver (ODBC, JDBC) or API to access and manipulate the data.

- **Local / Desktop** — The database runs on the same machine as the application (single-tier). No remote access.
- **Cloud** — While cloud databases are also accessed remotely, the topology question specifically asks about a remote server accessed from client systems, which describes client-server. Cloud is a deployment model built on top of client-server or three-tier, not a distinct topology in the same sense.
- **Application Server layer** — This is part of three-tier architecture, where clients connect to an application server, which then connects to the database server. The question asks about accessing the database directly from clients, which describes two-tier client-server.

**Reference:** See `../lessons/c4_m1_database_architecture.md` for the full comparison of single-tier, two-tier, three-tier, and cloud topologies.

</details>

---

### Question 2

Multiple database servers process the workload in parallel in shared disk architectures. What benefit does this configuration offer when one of the servers fails?

- Simple administration
- Faster processing
- **High availability** ✅
- Scalability

<details>
<summary>Explanation</summary>

**Correct answer: High availability.**

In a **shared disk architecture** (e.g., Oracle RAC), all database servers (nodes) access the same shared storage. When one server fails, the remaining servers can continue processing because the data is still accessible on the shared disk. This provides **failover capability** — the system remains operational despite individual server failures, which is the definition of high availability.

- **Simple administration** — Shared disk actually adds administrative complexity (managing cluster membership, cache coherency, interconnect).
- **Faster processing** — More servers can increase throughput, but the specific benefit when *one fails* is availability, not speed.
- **Scalability** — This is a benefit of adding more nodes, not specifically of handling failure.

**Reference:** See `../lessons/c4_m1_distributed_architecture_clustered_databases.md` for shared disk vs. shared nothing comparison, HADR modes, and failover semantics.

</details>

---

### Question 3

Which of the following categories of database users usually necessitates solely Read access?

- Data engineers
- Application developers
- None
- **Data Scientists and Business Analysts** ✅

<details>
<summary>Explanation</summary>

**Correct answer: Data Scientists and Business Analysts.**

Data Scientists and Business Analysts primarily query data to generate insights, reports, and models. Their workflow is read-intensive: they run SELECT queries, build dashboards, perform statistical analysis, and explore datasets. They generally do not need to write, update, or delete production data.

- **Data engineers** need read AND write access — they build ETL/ELT pipelines that insert, update, and transform data.
- **Application developers** need read AND write access — their applications perform CRUD operations (CREATE, READ, UPDATE, DELETE) on behalf of users.
- **None** is incorrect because Data Scientists and Analysts clearly exist and primarily need read access.

[ENRICHED: role granularity — In practice, Data Scientists may need write access to staging or analytics schemas (creating derived tables, materialized views, feature stores). Business Analysts typically have read-only access to data warehouses or OLAP cubes. The "solely Read" characterization describes the most common baseline — production write access is almost never granted to these roles in properly governed environments.]

**Reference:** See `../lessons/c4_m1_database_usage_patterns.md` for a full role comparison table with tools and access patterns.

</details>

---

### Question 4

Among the following open-source relational databases, which one is available under the General Public License (GPL)?

- SQLite
- **MySQL** ✅
- IBM Db2
- PostgreSQL

<details>
<summary>Explanation</summary>

**Correct answer: MySQL.**

MySQL is available under the **GNU General Public License (GPL)** — specifically, the Oracle-provided MySQL Community Edition is GPLv2 licensed. MySQL is also available under a commercial license for applications that require proprietary distribution (dual licensing model).

- **SQLite** — Public domain (not GPL). The authors have dedicated it to the public domain with a blessing waiver.
- **IBM Db2** — Proprietary commercial software. Not open-source.
- **PostgreSQL** — Uses the **PostgreSQL License**, which is an MIT/BSD-style permissive license, NOT the GPL. The PostgreSQL License allows use, modification, and distribution in both open-source and proprietary software without requiring derived works to be GPL-licensed.

[ENRICHED: licensing distinction — The difference matters for software distribution:
- **GPL (MySQL):** If you distribute an application that incorporates GPL-licensed code, you must also distribute the source code under GPL (copyleft). This is why companies like Facebook and Twitter can use MySQL freely (they distribute web services, not software) but a closed-source SaaS product embedding MySQL would need a commercial license.
- **Permissive license (PostgreSQL, MIT, BSD):** You can use, modify, and distribute the software without making your own code open-source. This makes PostgreSQL preferred by companies building proprietary products that embed a database.
- **Public domain (SQLite):** No restrictions at all — the code can be used for any purpose without attribution.]

**Reference:** See `../lessons/c4_m1_mysql_introduction.md` for MySQL licensing, history (1995→Sun→Oracle), and the MariaDB fork.

</details>

---

### Question 5

Which stack can incorporate PostgreSQL for developing web applications and websites?

- **LAPP stack** ✅
- MEAN stack
- Stack register
- LAMP stack

<details>
<summary>Explanation</summary>

**Correct answer: LAPP stack.**

**LAPP** stands for **L**inux, **A**pache, **P**ostgreSQL, **P**HP/Python/Perl. It is the PostgreSQL variant of the classic LAMP stack.

- **LAMP** — Linux, Apache, **MySQL**, PHP — uses MySQL, not PostgreSQL.
- **MEAN** — MongoDB, Express.js, Angular, Node.js — a JavaScript-based stack using MongoDB (NoSQL), not PostgreSQL.
- **Stack register** — Not a recognized web development stack.

[ENRICHED: stack variants — The acronym naming convention follows the pattern:

| Stack | OS | Web Server | Database | Language |
|---|---|---|---|---|
| LAMP | Linux | Apache | **MySQL** | PHP |
| LAPP | Linux | Apache | **PostgreSQL** | PHP/Python/Perl |
| LEMP | Linux | **Nginx** | MySQL | PHP |
| MEAN | — | Express (Node.js) | MongoDB | Angular |
| MERN | — | Express (Node.js) | MongoDB | React |
| WAMP | **Windows** | Apache | MySQL | PHP |
| XAMPP | Cross-platform | Apache | MariaDB/MySQL | PHP/Perl |

The "P" at the end of LAMP/LAPP stands for the programming language (originally PHP, now often Python or Perl). The "P" in the middle of LAPP specifically represents PostgreSQL.]

**Reference:** See `../lessons/c4_m1_postgresql_introduction.md` and `../lessons/c4_m1_mysql_introduction.md` for the ecosystem and stack context of each database.

</details>

---

## Summary

| # | Topic | Correct Answer | Key Concept |
|---|---|---|---|
| 1 | Deployment Topology | Client / Server | Two-tier architecture: clients connect to remote DB server |
| 2 | Shared Disk Architecture | High availability | Shared storage enables failover when a node fails |
| 3 | Database User Roles | Data Scientists and Business Analysts | Read-only analysis vs. read-write engineering/development |
| 4 | Open-Source Licensing | MySQL | MySQL is GPLv2; PostgreSQL uses permissive license; SQLite is public domain |
| 5 | Web Development Stacks | LAPP | LAPP = Linux, Apache, PostgreSQL, PHP/Python/Perl |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Reference | Cross-referenced database architecture file for topology comparison | HIGH |
| 2 | Q2 | Reference | Cross-referenced distributed architecture file for shared disk details | HIGH |
| 3 | Q3 | Role granularity | Noted that Data Scientists may need write access to staging/analytics schemas in practice | HIGH |
| 4 | Q3 | Reference | Cross-referenced database usage patterns file for full role comparison | HIGH |
| 5 | Q4 | Licensing distinction | Explained GPL (copyleft) vs. permissive (PostgreSQL license) vs. public domain (SQLite) with distribution implications | HIGH |
| 6 | Q4 | Reference | Cross-referenced MySQL introduction file for licensing and history | HIGH |
| 7 | Q5 | Stack variants | Built 7-row comparison table of LAMP/LAPP/LEMP/MEAN/MERN/WAMP/XAMPP stacks | HIGH |
| 8 | Q5 | Reference | Cross-referenced MySQL and PostgreSQL files for stack context | HIGH |
