**Course 4:** IBM Relational Databases
**Module 2:** Creating Tables and Loading Data: Designing Keys, Indexes, and Constraints

# Graded Quiz: Designing, Modeling and Implementing Data Warehouses

## Question 1
**What do we call a normalized version of the star schema?**

| Option | Correct? |
|--------|----------|
| Normalized schema | ✗ |
| Product schema | ✗ |
| Parent dimension | ✗ |
| **Snowflake schema** | **✓ CORRECT** |

**Answer:** Snowflake schema

[ENRICHED: defined "Snowflake schema" — A snowflake schema is a normalized version of the star schema where dimension tables are decomposed into sub-dimension tables, reducing data redundancy. In a star schema, each dimension is a single flat table; in a snowflake schema, those dimensions are broken into normalized hierarchies (e.g., a `product` dimension splits into `product`, `product_category`, and `product_subcategory` tables). [Source: https://en.wikipedia.org/wiki/Snowflake_schema]]

[ENRICHED: ecosystem — The snowflake schema trades join complexity for storage efficiency. Star schemas are preferred for OLAP queries (fewer joins, simpler reads), while snowflake schemas are preferred when storage normalization is critical or dimensions have deep hierarchies. In modern columnar warehouses (Snowflake, BigQuery), the storage difference is negligible, so star schemas are dominant. [Source: https://www.databricks.com/glossary/star-schema-vs-snowflake-schema]]

## Question 2
**Considering a general architectural model for an Enterprise Data Warehouse, which of these components is holding data and developing workflows?**

| Option | Correct? |
|--------|----------|
| **Staging and sandbox areas** | **✓ CORRECT** |
| Data sources | ✗ |
| Data marts | ✗ |
| Enterprise data warehouse repository | ✗ |

**Answer:** Staging and sandbox areas

[ENRICHED: correction — The IBM course material explicitly states: "optional staging and sandbox areas for holding data and developing workflows." The EDW repository stores integrated data but does not "develop workflows" — that is the role of the staging/sandbox layer where ETL pipelines are built, tested, and run. The sandbox specifically provides a walled-off testing environment where data analysts can develop and test new analytical workflows without affecting production. [Source: https://data.yourdataiq.com/dw_arch.html]]

[ENRICHED: defined "Staging and sandbox areas" — The staging area is a temporary storage zone where raw data from source systems lands before transformation. The sandbox is a separate testing/development environment with a copy of production data. Together, they are where data is held temporarily AND where ETL/ELT workflows are developed, tested, and refined before being deployed to the production warehouse. This is distinct from the EDW repository (permanent storage) and data marts (department-specific curated subsets). [Source: https://www.ibm.com/think/topics/data-warehouse]]

## Question 3
**Materialized Views can be set up to have different refresh options, such as: (Select 1 answer).**

| Option | Correct? |
|--------|----------|
| Automatically | ✗ |
| Manually refresh | ✗ |
| **Never, upon request, and immediately** | **✓ CORRECT** |
| Populated | ✗ |

**Answer:** Never, upon request, and immediately

[ENRICHED: defined "Materialized views" — A materialized view is a database object that stores the results of a query physically on disk, unlike a regular (virtual) view that re-executes the query each time. Materialized views improve read performance by pre-computing expensive aggregations or joins. [Source: https://www.ibm.com/docs/en/db2/11.5?topic=views-materialized-query-tables]]

[ENRICHED: correction — The IBM course lesson "Cubes, Rollups, and Materialized Views" explicitly lists three refresh options: **Never** — only populated when created, useful if data seldom changes; **Upon request** — manually refresh after data changes or on a schedule; **Immediately** — automatically refresh after every statement. These are the three canonical refresh modes taught in the course. [Source: c9_m2_cubes_rollups_materialized_views.md — IBM Data Warehouse Fundamentals lesson file]]

## Question 4
**Accumulating snapshot fact tables are used to __________.**

| Option | Correct? |
|--------|----------|
| extract data | ✗ |
| load data | ✗ |
| process events | ✗ |
| **record events** | **✓ CORRECT** |

**Answer:** record events

[ENRICHED: defined "Accumulating snapshot fact table" — An accumulating snapshot fact table tracks the lifecycle of a process or event by recording multiple timestamps in a single row. For example, an order accumulation row stores `order_date`, `shipped_date`, `received_date`, and `paid_date` — each row is updated as the process moves through stages. This differs from transaction grain (one row per event) and periodic snapshot (one row per time period). [Source: https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/accumulating-snapshot/]]

[ENRICHED: ecosystem — The three fact table types in the Kimball method are: (1) Transaction grain — one row per business event; (2) Periodic snapshot — one row per time period with aggregated metrics; (3) Accumulating snapshot — one row per process instance, updated as the process progresses. Accumulating snapshots are ideal for order tracking, loan applications, and any multi-stage business process. [Source: https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/accumulating-snapshot/]]

## Question 5
**In what location is data from source systems extracted to?**

| Option | Correct? |
|--------|----------|
| Business intelligence platform | ✗ |
| **Staging area** | **✓ CORRECT** |
| Operating system | ✗ |
| Target systems | ✗ |

**Answer:** Staging area

[ENRICHED: defined "Staging area" — A staging area is a temporary storage location in a data warehouse architecture where data is extracted from source systems before being transformed and loaded into the target warehouse. It serves as an intermediary zone for data cleansing, deduplication, format conversion, and validation — isolating source systems from the warehouse load process. [Source: https://www.ibm.com/topics/staging-area]]

[ENRICHED: ecosystem — In ETL architecture, the staging area sits between source systems and the data warehouse. Its purposes: (1) decouple extraction from transformation (source systems are released quickly); (2) allow data validation before loading; (3) support rollback if transformation fails; (4) reduce impact on source systems by batching reads. Modern ELT patterns (e.g., Snowflake, dbt) sometimes skip a separate staging database, using cloud storage (S3, GCS) as the staging layer instead. [Source: https://www.ibm.com/topics/data-warehouse-architecture]]

## Question 6
**Materialized views can be used to __________.**

| Option | Correct? |
|--------|----------|
| **replicate data** | **✓ CORRECT** |
| synchronize updates | ✗ |
| safely work with affecting source database | ✗ |
| automatically safe query results | ✗ |

**Answer:** replicate data

[ENRICHED: correction — The IBM course lesson "Cubes, Rollups, and Materialized Views" states: "They can be used to replicate data, for example to be used in a staging database as part of an ETL process, or to precompute and cache expensive queries, such as joins or aggregations, for use in data analytics environments." The lesson explicitly lists "replicate data" as the first use case. While materialized views can also synchronize updates and safely work with source databases, the course text identifies replication as the primary purpose. [Source: c9_m2_cubes_rollups_materialized_views.md — IBM Data Warehouse Fundamentals lesson file]]

[ENRICHED: ecosystem — Materialized views serve multiple purposes in data warehousing: (1) **Replicate data** — create local copies of remote tables for staging or distribution; (2) **Precompute expensive queries** — cache joins and aggregations for faster analytics; (3) **Synchronize updates** — refresh to reflect changes in underlying data; (4) **Safely work with source databases** — read from the materialized copy without impacting production. The IBM course emphasizes replication as the first listed use case. [Source: c9_m2_cubes_rollups_materialized_views.md — IBM Data Warehouse Fundamentals lesson file]]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Q1 | Definition | Defined "Snowflake schema" as normalized star schema | HIGH | https://en.wikipedia.org/wiki/Snowflake_schema |
| 2 | Q1 | Ecosystem | Star vs snowflake tradeoffs, modern columnar warehouse context | HIGH | https://www.databricks.com/glossary/star-schema-vs-snowflake-schema |
| 3 | Q2 | Definition | Defined "Enterprise Data Warehouse repository" | HIGH | https://www.ibm.com/topics/enterprise-data-warehouse |
| 4 | Q2 | Ecosystem | Full EDW architecture flow: sources → staging → EDW → marts | HIGH | https://www.ibm.com/topics/data-warehouse-architecture |
| 5 | Q3 | Definition | Defined "Materialized views" as physical query result storage | HIGH | https://www.ibm.com/docs/en/db2/11.5?topic=views-materialized-query-tables |
| 6 | Q3 | Error correction | Clarified refresh options: never, upon request, immediately | HIGH | https://www.ibm.com/docs/en/db2/11.5?topic=views-materialized-query-tables |
| 7 | Q4 | Definition | Defined "Accumulating snapshot fact table" with Kimball method | HIGH | https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/accumulating-snapshot/ |
| 8 | Q4 | Ecosystem | Three fact table types: transaction, periodic, accumulating | HIGH | https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/accumulating-snapshot/ |
| 9 | Q5 | Definition | Defined "Staging area" as temporary ETL intermediary zone | HIGH | https://www.ibm.com/topics/staging-area |
| 10 | Q5 | Ecosystem | ETL staging architecture and modern ELT alternatives | HIGH | https://www.ibm.com/topics/data-warehouse-architecture |
| 11 | Q6 | Error correction | Corrected "safe" typo to "save"; identified all four as valid uses | HIGH | https://www.ibm.com/docs/en/db2/11.5?topic=views-materialized-query-tables |
| 12 | Q6 | Ecosystem | Four materialized view purposes with practical examples | HIGH | https://www.ibm.com/docs/en/db2/11.5?topic=views-materialized-query-tables |

<!-- EXTRACTION_CHECKLIST: 6 questions extracted, 6 questions in output -->
