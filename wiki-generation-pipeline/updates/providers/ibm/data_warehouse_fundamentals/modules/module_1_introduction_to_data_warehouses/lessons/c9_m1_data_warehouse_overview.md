> **Course 9:** Data Warehouse Fundamentals
> **Module 1:** An Introduction to Data Warehouses, Data Marts, and Data Lakes

# Data Warehouse Overview

## Learning Objectives
After watching this video, you will be able to:
- Define a data warehouse
- Identify data warehouse use cases and
- List the benefits of a data warehouse.

## What Is a Data Warehouse?

A data warehouse is a system that aggregates data from one or more sources into a single, central, consistent data store to support various data analytics requirements. [ENRICHED: definition — A data warehouse is a database designed to enable business intelligence activities: it exists to help users understand and enhance their organization's performance. It is designed for query and analysis rather than for transaction processing, and usually contains historical data derived from transaction data, but can include data from other sources. Source: Oracle Documentation] [Source: https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html]

[ENRICHED: clarification — The Oracle definition says the warehouse is "designed for query and analysis rather than for transaction processing." This raises the question: if the warehouse isn't for transaction processing, then what is? The answer is **OLTP (Online Transaction Processing)** systems — a completely separate category of databases designed for exactly that purpose. Here is the full picture:

**OLTP = running the business. OLAP = analyzing the business.**

Every company runs two fundamentally different types of data workloads:

1. **Transactional workloads (OLTP):** When a customer places an order, makes a payment, updates their address, or cancels a reservation, the system must process that action instantly, accurately, and reliably — even if thousands of other users are doing the same thing simultaneously. OLTP systems are purpose-built for this: they handle large volumes of short, concurrent read/write operations, each touching a small number of rows, with strict ACID consistency guarantees. If a payment fails halfway through, the system rolls back cleanly. If two customers try to buy the last unit simultaneously, the system handles the race condition correctly. Examples: MySQL, PostgreSQL, Oracle Database, SQL Server, MongoDB — these run e-commerce platforms, banking systems, CRM applications, ERP systems, and reservation systems.

2. **Analytical workloads (OLAP / data warehouses):** When an analyst asks "how did sales trend over the past 18 months, broken down by product category and region?", the system must scan billions of rows, aggregate across multiple dimensions, and return a coherent result. Speed matters here too, but it's measured in seconds rather than milliseconds, and the concern is throughput over large datasets rather than concurrent write consistency. Data warehouses are purpose-built for this: they store historical, denormalized data optimized for fast aggregations, complex joins, and multidimensional analysis. Examples: Snowflake, Google BigQuery, Amazon Redshift, Azure Synapse.

**Why they must be separate systems:**

The reason OLTP and OLAP can't be the same system is that they optimize for opposite trade-offs. OLTP databases use normalized schemas (many small tables, minimal redundancy) to make writes fast and consistent. OLAP databases use denormalized schemas (few large tables, redundant data) to make reads fast. If you ran an analytical query that scans 3 years of order history directly against a production OLTP database, it would lock tables, slow down transactions, and degrade the experience for every active user. This is why ETL pipelines exist — they copy data from OLTP systems into OLAP systems on a schedule, keeping the two workloads isolated.

**The modern nuance — HTAP:**

A newer category called HTAP (Hybrid Transactional and Analytical Processing) tries to serve both workloads from a single system. Systems like TiDB, SingleStore, and some configurations of Google BigQuery claim to handle both transactions and analytics. In practice, most organizations above a certain scale still find dedicated OLAP systems necessary for serious analytical work, but HTAP is closing the gap for smaller-scale use cases.

**Key differences at a glance:**

| Dimension | OLTP (Transactional) | OLAP (Analytical / Warehouse) |
|---|---|---|
| Purpose | Run daily operations | Analyze historical data |
| Query type | Simple inserts, updates, deletes | Complex aggregations, joins, drill-downs |
| Data scope | Current state (last hours/days) | Historical (months/years) |
| Response time | Milliseconds | Seconds to minutes |
| Schema | Normalized (many tables, few columns) | Denormalized (few tables, many columns) |
| Storage format | Row-oriented (fast individual reads/writes) | Columnar (fast scans over one column) |
| Concurrency | Thousands of simultaneous writers | Few analysts running heavy reads |
| Examples | MySQL, PostgreSQL, Oracle, SQL Server | Snowflake, BigQuery, Redshift, Synapse |

Source: TDWI, ThoughtSpot, Data Warehouse Info] [Source: https://tdwi.org/blogs/data-101/2026/05/olap-vs-oltp.aspx]

[ENRICHED: clarification — The comparison table says OLTP uses "row-oriented" storage and OLAP uses "columnar" storage. This is the single most important architectural difference between the two systems, and it determines what operations are fast vs slow. Here is exactly what it means:

**Row-oriented storage (OLTP):** Data is stored row by row on disk. Imagine an `employees` table:

| id | name | city | salary |
|----|------|------|--------|
| 1 | Ram | Delhi | 50000 |
| 2 | Sam | Mumbai | 60000 |
| 3 | Raj | Pune | 55000 |

On disk, a row-oriented database stores it like this:

```
Block 1: [1, Ram, Delhi, 50000] [2, Sam, Mumbai, 60000] [3, Raj, Pune, 55000]
```

Each block contains complete rows — all column values for one record sit together. When you run `SELECT * FROM employees WHERE id = 2`, the database reads one block and gets the entire row in one go. This is extremely fast for transactional operations: inserting a new order, updating a customer's address, looking up a user by ID. The database never needs to touch unrelated columns.

**Columnar storage (OLAP):** Data is stored column by column on disk. The same table on disk looks like this:

```
id column:     [1, 2, 3]
name column:   [Ram, Sam, Raj]
city column:   [Delhi, Mumbai, Pune]
salary column: [50000, 60000, 55000]
```

Each column is a separate contiguous block. When you run `SELECT SUM(salary) FROM employees`, the database reads ONLY the `salary` column block — it completely skips id, name, and city. For a table with 50 columns where an analytical query only needs 2, this means reading 4% of the data instead of 100%.

**Why this matters at scale:**

Consider a table with 1 billion rows and 50 columns, where each row is 1 KB:

- **Row-oriented query** (`SELECT * FROM orders WHERE id = 12345`): Reads ~1 KB (one row). Fast. This is what OLTP does thousands of times per second.
- **Columnar query** (`SELECT SUM(amount) FROM orders`): Reads only the `amount` column — ~1 GB instead of ~50 GB. The database skips the other 49 columns entirely. This is why analytical queries that scan billions of rows finish in seconds on columnar databases.

**Compression advantage:** Columnar storage also compresses far more efficiently. A column of repeated values like `country = "India"` appearing millions of times compresses to almost nothing. Row-oriented databases can't achieve this because each block mixes different data types (strings, integers, dates) that don't compress well together. Columnar databases typically achieve 5-20x compression ratios vs row-oriented databases.

**Vectorized execution:** Columnar databases process values in batches of 10,000+ at once (vectorized execution) instead of one row at a time. This exploits modern CPU SIMD instructions and cache lines, making aggregations 10-100x faster than row-oriented equivalents.

**The bottom line:** Row-oriented storage is optimized for "give me one complete record" (OLTP). Columnar storage is optimized for "scan millions of rows but only touch a few columns" (OLAP). This is why data warehouses use columnar storage — analytical queries almost never need all columns, and scanning only what you need is the difference between a query taking 2 seconds vs 2 minutes. Source: ClickHouse, MotherDuck, blog.nishikanta.in] [Source: https://clickhouse.com/resources/engineering/row-vs-column-database]

Let's take a closer look at data warehouse analytics.

## Data Warehouse Analytics

Data warehouse systems support data mining, including the application of artificial intelligence and machine learning.

[ENRICHED: clarification — Data mining explained:

**What is Data Mining?**
Data mining is the process of discovering hidden patterns, correlations, trends, and actionable insights from large datasets stored in a data warehouse. It combines techniques from statistics, machine learning, and database systems to extract knowledge that is not immediately obvious through simple queries or standard reporting. The term "data mining" is actually a misnomer — it's not about extracting data, but about extracting patterns and knowledge FROM data. The more technical name is KDD (Knowledge Discovery in Databases).

**How Data Mining Relates to Data Warehouses:**
A data warehouse stores large volumes of integrated, historical, cleansed data from multiple sources — making it the ideal foundation for data mining. Without a warehouse, data mining would require collecting and cleaning data from scattered source systems every time. The warehouse provides the organized, consistent, high-quality data that mining algorithms need to produce reliable results.

**Key Data Mining Techniques:**

| Technique | What It Does | Warehouse Use Case |
|-----------|--------------|-------------------|
| **Classification** | Assigns data to predefined categories | Categorizing customers by risk level (high/medium/low) |
| **Clustering** | Groups similar data points without predefined labels | Segmenting customers by purchasing behavior |
| **Association Rules** | Finds relationships between variables ("if X, then Y") | Market basket analysis ("customers who buy X also buy Y") |
| **Regression** | Predicts continuous numeric values | Forecasting future sales based on historical trends |
| **Anomaly Detection** | Identifies unusual data points that deviate from patterns | Fraud detection in financial transactions |
| **Decision Trees** | Creates tree-like models to classify or predict outcomes | Credit approval decisions based on applicant attributes |
| **Neural Networks** | Mimics brain structure to model complex relationships | Image recognition, natural language processing |
| **Time Series Analysis** | Analyzes data points collected over time | Demand forecasting, seasonal trend detection |

**The Data Mining Process (KDD):**
1. **Business Understanding** — Define what questions you're trying to answer
2. **Data Selection** — Extract relevant data from the warehouse
3. **Data Preprocessing** — Clean, transform, and prepare data for analysis
4. **Data Mining** — Apply algorithms to discover patterns
5. **Pattern Evaluation** — Validate that discovered patterns are meaningful and not just noise
6. **Knowledge Presentation** — Visualize and communicate findings to stakeholders

**Why Data Mining Matters for Data Warehouses:**
Data warehouses store the "what happened" (historical records). Data mining answers "why it happened," "what will happen next," and "what should we do about it." Together, they transform raw data into competitive advantage — from predicting customer churn to detecting fraud to optimizing supply chains. Source: IBM, Databricks, Wikipedia, TechTarget] [Source: https://www.ibm.com/think/topics/data-mining]

Data transformation during the ETL process speeds front-end reporting, delivering critical information fast. [ENRICHED: definition — ETL (Extract, Transform, Load) is a data integration process that extracts data from source systems, transforms it in a staging area (cleaning, standardizing, deduplicating), and loads it into the data warehouse. Modern warehouses also use ELT (Extract, Load, Transform), which loads raw data first and transforms it using the warehouse's compute resources. Source: IBM] [Source: https://www.ibm.com/think/topics/data-warehouse]

Data warehouses enable online analytical processing, known as OLAP, which provides fast, flexible, multidimensional data analysis for business intelligence and decision support applications. [ENRICHED: definition — OLAP (Online Analytical Processing) systems are designed for high-speed, complex queries and multidimensional analysis on large volumes of data. They use "cubes" (array-based multidimensional data structures) to enable faster, more flexible analysis across multiple dimensions. Common use cases include data mining, financial analysis, budgeting and forecast planning. Three main types: MOLAP (multidimensional OLAP), ROLAP (relational OLAP), and HOLAP (hybrid OLAP). Source: IBM] [Source: https://www.ibm.com/think/topics/data-warehouse]

## Evolution of Data Warehousing

Traditionally, data warehouses have been hosted on-premises within enterprise data centers, initially on mainframes and then on Unix, Windows, and Linux systems.

Data warehouse appliances emerged with the growth of more extensive data volumes in the 2000s.

These appliances consisted of a pre-integrated bundle of specialized hardware and optimized data warehousing software that reduced large-scale data warehousing management overhead.

In the last decade or so, with exponential amounts of data being generated and stored in the cloud, Cloud Data Warehouses, frequently called CDWs, have gained popularity, where organizations don't purchase hardware or install warehousing software. [ENRICHED: performance context — Cloud data warehouses offer benefits of cloud computing such as data storage at petabyte scale, highly scalable compute and storage, and pay-as-you-go pricing. They are typically delivered as fully managed SaaS offerings, eliminating the need for upfront investment in hardware or software. Examples include Amazon Redshift, Google BigQuery, Snowflake, and IBM Db2 Warehouse on Cloud. Source: IBM] [Source: https://www.ibm.com/think/topics/data-warehouse]

Instead, organizations access data warehouses as a scalable, pay-as-you-go service.

Now that you can define what a data warehouse is, identify where data warehouses exist, and understand their basic structure and outputs, let's examine what organizations use data warehouses.

## Industries Using Data Warehouses

Data warehouses are a part of almost every industry, including e-commerce, transportation, medical, banking and fin-tech, social media, and governments.

But why do these types of organizations use data warehouses?

Let's learn more.

### Industry-Specific Use Cases

Retail and e-commerce organizations use data warehouses to analyze and report on sales performance.

These organizations also apply machine learning assisted shopping that provides shoppers with relevant recommendations that drive additional sales.

By applying artificial intelligence to patient data, healthcare providers can access the most recent insights and use that information to diagnose and treat their patients with greater accuracy.

BI capabilities enable transportation providers to optimize routes, travel times, equipment needs, and staffing requirements.

Financial tech organizations, including banking, apply data analytics to evaluate risks, detect fraud, and cross-sell services.

Social media organizations need analytic capabilities that can quickly measure ever-changing customer sentiment and project product sales.

Governments apply business intelligence to analyze and evaluate citizen-focused programs and assist with policy change decisions.

## Benefits of a Data Warehouse

What are the benefits of a data warehouse?

Data warehouses enable organizations to centralize data from disparate data sources, such as transactional systems, operational databases, and flat files.

Data integration, removing bad data, eliminating duplicates, and standardizing data create a single source of the truth that results in better data quality for analysis. [ENRICHED: ecosystem — A single source of truth eliminates data silos and enables business users to confidently access the organization's pertinent data. Enterprise-grade data warehouses may also support open source formats like Apache Iceberg, Parquet, and CSV, enabling further data access and sharing across the enterprise. Source: IBM] [Source: https://www.ibm.com/think/topics/data-warehouse]

A single source of truth empowers users to leverage all the company's data and access that data more efficiently.

In addition, separating database operations from data analytics generally improves data access performance, leading to faster business insights. [ENRICHED: performance context — Data warehouses are read-oriented systems with far higher amounts of data reading versus writing and updating. This separation enables far better analytical performance and avoids impacting transaction systems. Typical SLOs include data freshness, query latency percentiles, and ingestion success rate. Source: Oracle] [Source: https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html]

Next, large-scale BI functions such as data mining, artificial intelligence, and machine learning tools facilitate smarter decisions by data professionals and business leaders.

These capabilities build on each other to give organizations the means and opportunity to realize competitive advantages and gains.

## Key Takeaways

In this video, you learned that:

A data warehouse is a system that aggregates data from one or more sources into a single consistent data store to support data analytics.

Data warehouses support data mining, AI and machine learning, OLAP, and front-end reporting.

And finally, data warehouses and BI help organizations improve data quality, speed business insights, and improve decision-making, all of which can result in competitive gains.

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | What Is a Data Warehouse | Definition | Data warehouse defined as a system aggregating data from multiple sources into a single consistent store for analytics | HIGH | https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html |
| 2 | ETL | Definition | ETL (Extract, Transform, Load) defined with full process explanation; ELT variant noted | HIGH | https://www.ibm.com/think/topics/data-warehouse |
| 3 | OLAP | Definition | OLAP defined with cube-based multidimensional analysis; three types (MOLAP, ROLAP, HOLAP) enumerated | HIGH | https://www.ibm.com/think/topics/data-warehouse |
| 4 | Cloud Data Warehouses | Performance context | CDWs offer petabyte-scale storage, elastic compute, pay-as-you-go pricing as managed SaaS | HIGH | https://www.ibm.com/think/topics/data-warehouse |
| 5 | Single Source of Truth | Ecosystem | Single source of truth eliminates data silos; supports open formats (Iceberg, Parquet, CSV) | HIGH | https://www.ibm.com/think/topics/data-warehouse |
| 6 | Data Access Performance | Performance context | Data warehouses are read-oriented; separation of analytics from transactions improves performance | HIGH | https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html |
| 7 | What Is a Data Warehouse | Clarification | Full OLTP vs OLAP explanation: OLTP handles day-to-day transactions (MySQL, PostgreSQL, Oracle) with normalized schemas and millisecond response; OLAP handles historical analysis (Snowflake, BigQuery) with denormalized schemas; why they must be separate systems; HTAP hybrid category; comparison table with 8 dimensions | HIGH | https://tdwi.org/blogs/data-101/2026/05/olap-vs-oltp.aspx |
| 8 | What Is a Data Warehouse | Clarification | Deep explanation of row-oriented vs columnar storage: visual disk layout examples, 1B-row scaling scenario (1KB vs 50GB read), 5-20x compression advantage, vectorized execution (10-100x faster), why columnar is essential for OLAP | HIGH | https://clickhouse.com/resources/engineering/row-vs-column-database |
| 9 | Data Warehouse Analytics | Clarification | Full data mining explanation: definition (KDD process), 8 key techniques (classification, clustering, association rules, regression, anomaly detection, decision trees, neural networks, time series), 6-step KDD process, and how data mining relates to data warehouses | HIGH | https://www.ibm.com/think/topics/data-mining |

<!-- EXTRACTION_CHECKLIST: 37 sentences extracted, 37 sentences in output + 1 enrichment added via clarification question -->
