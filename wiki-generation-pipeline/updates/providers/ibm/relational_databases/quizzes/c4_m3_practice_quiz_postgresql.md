<mark style="background-color: rgba(200, 230, 201, 0.4);">NEW</mark>

> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 3:** MySQL and PostgreSQL
> **Type:** Practice Quiz — PostgreSQL

# Practice Quiz: PostgreSQL

**Due:** Jul 20, 11:59 PM EEST  
**Time:** 10 min  
**Attempts:** Unlimited (ungraded)

---

## Question 1

**True or False: In the pgAdmin Query Tool, it is always possible to modify the outcomes of SQL queries.**

- True
- False

**Correct answer: False**

[ENRICHED: explanation — The pgAdmin Query Tool executes SQL queries and displays results in a read-only grid. You cannot click on a result cell and edit it. To modify data, you use **View/Edit Data** (right-click table → View/Edit Data → All Rows), which opens a separate editable grid where changes are translated into UPDATE statements. The Query Tool is for running ad-hoc SQL and viewing outputs. If you want to change the outcome, you modify the SQL query itself and re-execute it. See `c4_m3_getting_started_with_postgresql.md` for the full pgAdmin Query Tool breakdown (upper pane: SQL input, lower pane: Results/Explain/Messages/Notifications tabs).]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **True** | Common misconception — the Query Tool results grid is read-only |
| **False** (correct) | Results are read-only; use View/Edit Data for in-grid editing |

---

## Question 2

**What is the default delimiter for data files when you load data into a PostgreSQL table?**

- Hyphens
- Comma
- Tab
- Quotation marks

**Correct answer: Comma**

[ENRICHED: explanation — CSV (Comma-Separated Values) is the default format for pgAdmin's Import/Export tool, and the default delimiter for CSV is the **comma** `,`. When loading a CSV file through pgAdmin's Import/Export dialog, the delimiter is automatically set to comma and doesn't need to be specified. For non-CSV files, you can change the delimiter in the Import/Export dialog options (tab, pipe `|`, semicolon `;`, etc.). See `c4_m3_creating_databases_loading_data_postgresql.md` for the full Import/Export dialog reference and COPY command syntax.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Hyphens** | Not a standard delimiter for data files |
| **Comma** (correct) | Default delimiter for CSV — pgAdmin auto-detects and defaults to comma |
| **Tab** | Used for TSV (Tab-Separated Values) files, not the default |
| **Quotation marks** | Used for quoting values containing delimiters, not as a delimiter themselves |

---

## Question 3

**Where can you create views in a PostgreSQL database?**

- In two or more tables
- In a schema
- In a table
- In a query

**Correct answer: In a schema**

[ENRICHED: explanation — In PostgreSQL, views are database objects that belong to a **schema** (usually `public`). In pgAdmin, you create views by navigating to the schema in the tree view, right-clicking **Views** → **Create** → **View**. Similarly, materialized views are created under **Materialized Views** within the same schema. Views source data from tables, but they are stored in schemas — not inside tables or queries. See `c4_m3_views_postgresql.md` for the complete view creation workflow and `c4_m3_getting_started_with_postgresql.md` for the schema concept explanation (namespaces, search_path, fully qualified names).]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **In two or more tables** | Views can **source** data from multiple tables (via JOINs), but they are not created *inside* tables |
| **In a schema** (correct) | Views are schema-level objects, just like tables |
| **In a table** | Views are separate from tables — they reference tables but aren't contained in them |
| **In a query** | A view is defined by a query, but the view object itself is stored in a schema |

---

## Question 4

**Which database becomes the connection point when connecting to a PostgreSQL database server?**

- The default database
- The template0 database
- The template1 database
- No database

**Correct answer: The default database**

[ENRICHED: explanation — PostgreSQL always connects to a specific database — there is no server-level connection without a database. When you connect with psql without specifying a database name (e.g., `psql -U postgres`), it connects to the **default database** with the same name as the user (`postgres`). If that database doesn't exist, the connection fails. In pgAdmin, when registering a server, you specify a **maintenance database** (default: `postgres`) — this is the database you connect to first. The `template0` and `template1` databases are system templates used by `CREATE DATABASE` — they exist but are not connection defaults. See `c4_m3_getting_started_with_postgresql.md` for template database coverage (template0 as recovery fallback, template1 as the default copied on CREATE DATABASE).]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **The default database** (correct) | PostgreSQL connects to a specific database (default: `postgres` or matching the username) |
| **The template0 database** | Pristine template for recovery — not a connection default |
| **The template1 database** | Template copied when creating new databases — not a connection default |
| **No database** | Impossible — a PostgreSQL connection always targets a specific database |

---

## Question 5

**What commands in PostgreSQL are applicable for populating a new database with data retrieved from a backup? [Select two]**

- Load the dump file using the pgAdmin Import/Export data command
- Load the dump file using the CREATE DATABASE command
- Load the dump file using the psql command
- Load the dump file using the pgAdmin Restore command

**Correct answers: Load the dump file using the psql command, Load the dump file using the pgAdmin Restore command**

[ENRICHED: explanation — Dump files (`.sql`, `.dump`) created by `pg_dump` can be restored using two methods: (1) **psql command** — `psql -d database_name -f dump_file.sql` executes the SQL statements in the dump file to recreate objects and data. (2) **pgAdmin Restore** — right-click a database → Restore → select the dump file → executes `pg_restore` internally for non-plain formats. The pgAdmin **Import/Export** tool is for loading flat data files (CSV, text) into individual tables, not for restoring full database dumps. **CREATE DATABASE** creates an empty database — it cannot load dump content. See `c4_m3_creating_databases_loading_data_postgresql.md` for the full pg_dump/restore workflow with format options.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **psql command** (correct) | `psql -d db -f dump.sql` executes the SQL dump to recreate all objects and data |
| **pgAdmin Restore** (correct) | Right-click database → Restore → select dump file → uses pg_restore internally |
| **pgAdmin Import/Export** | Designed for CSV/text file loading into a single table, NOT for full dump restoration |
| **CREATE DATABASE** | Creates an empty database by copying a template — does not load any dump content |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Explanation | Distinguished Query Tool (read-only results) from View/Edit Data (editable grid) | HIGH |
| 2 | Q2 | Explanation | CSV default comma delimiter with Import/Export dialog options reference | HIGH |
| 3 | Q3 | Explanation | Views as schema-level objects vs. tables and queries as data sources | HIGH |
| 4 | Q4 | Explanation | Default database connection behavior (username-matching database), maintenance database, template roles | HIGH |
| 5 | Q5 | Explanation | Two dump restore methods (psql -f for SQL dumps, pgAdmin Restore for pg_restore formats) vs. Import/Export (flat files only) vs. CREATE DATABASE (empty) | HIGH |
