> **Course 9:** Data Warehouse Fundamentals
> **Module 1:** An Introduction to Data Warehouses, Data Marts, and Data Lakes

# Data Lakes Overview

Welcome to Data Lakes Overview. After watching this video, you will be able to: Define what a data lake is. List benefits of using a data lake. And, compare data lakes to data warehouses.

## What Is a Data Lake?

A data lake is a storage repository that can store large amounts of structured, semi-structured, and unstructured data in their native format, classified and tagged with metadata. [ENRICHED: definition — A data lake is a centralized repository designed to store vast amounts of data in its native, raw format. It allows organizations to ingest, store, and process structured, semi-structured, and unstructured data from various sources without the need for predefined schemas. Modern data lakes in 2026 are predominantly cloud-native, leveraging platforms like AWS S3, Azure Data Lake Storage, and Google Cloud Storage, with the emergence of lakehouse architecture combining data lake flexibility with data warehouse performance. Source: IBM] [Source: https://www.ibm.com/think/topics/data-lake]

While a data warehouse stores data processed for a specific need, a data lake is a pool of raw data where each data element is given a unique identifier and is tagged with metatags for further use.

You would opt for a data lake if you generate, or have access to, large amounts of data on an ongoing basis but don't want to be restricted to specific or pre-defined use cases. Data lakes are sometimes also used as a staging area for transforming data prior to loading into a data warehouse or a data mart.

## Data Lake Architecture

Let's break this information down a bit.

A data lake is a data repository that can store a large amount of structured, semi-structured and unstructured data in its native format. You do not need to define the structure and schema of data before loading the data into the data lake. You do not even need to know all the use cases for which you will be analyzing the data. [ENRICHED: definition — Data lakes use a schema-on-read approach, meaning data is stored in its raw format and the schema is applied only when the data is queried. This contrasts with schema-on-write used by data warehouses, where data must conform to a predefined structure before loading. Schema-on-read provides flexibility to ingest any data type without upfront design, but requires data quality validation at query time rather than at ingestion time. Source: Databricks] [Source: https://www.databricks.com/blog/data-lake-vs-cloud-data-warehouse]

### Data Quality Validation Procedures

[ENRICHED: clarification — Since data lakes accept data without upfront schema validation (schema-on-read), data quality validation becomes critical to prevent "data swamps." Modern data lakes implement multi-layered validation procedures at different stages of the data lifecycle:

**1. Ingestion-Time Validation (Bronze Layer)**
- **Schema validation:** Verify incoming data matches expected structure (column names, data types, nesting)
- **Completeness checks:** Ensure required fields are present and non-null
- **Volume validation:** Detect sudden drops or spikes in row counts compared to historical baselines
- **Freshness checks:** Verify data arrives within expected time windows
- **Format validation:** Confirm data formats match specifications (e.g., date formats, email patterns)
- **Example tools:** Great Expectations, AWS Deequ, Soda Core

**2. Transformation-Time Validation (Silver Layer)**
- **Referential integrity:** Verify foreign keys resolve to valid primary keys in reference tables
- **Business rule enforcement:** Validate domain-specific constraints (e.g., start_date ≤ end_date, percentages within 0-100%)
- **Anomaly/outlier detection:** Identify values that deviate significantly from historical patterns
- **Deduplication:** Remove duplicate records that may have been ingested multiple times
- **Cross-dataset consistency:** Ensure related datasets agree (e.g., order totals match sum of line items)

**3. Serving-Time Validation (Gold Layer)**
- **Aggregate consistency:** Validate totals, ratios, and rollups match expected values
- **KPI threshold monitoring:** Alert when business metrics exceed defined thresholds
- **Distribution drift detection:** Monitor for gradual changes in data distributions over time
- **Freshness SLAs:** Ensure data is updated within business-required timeframes

**Validation Frameworks and Tools:**

| Framework | Type | Key Features |
|-----------|------|--------------|
| Great Expectations | Open-source Python library | Declarative expectations, Data Docs reporting, Spark/Pandas integration |
| Soda Core | Open-source SQL-based | SodaCL language, anomaly detection, cloud integration |
| AWS Deequ | Open-source Spark library | Data quality as unit tests, distributed validation |
| dbt tests | Built-in to dbt | Deterministic invariant checks (not-null, unique, relationships) |
| Monte Carlo | Commercial platform | End-to-end data observability, automated anomaly detection |
| Elementary | Open-source dbt extension | Z-score-based drift detection for dbt models |

**Validation Pattern: The Three-Checkpoint Architecture**
- **Checkpoint A (Ingest Gate):** Runs before data is written to bronze layer. Enforces source contract: column set, nullability, value ranges. Violating rows are quarantined.
- **Checkpoint B (Gold Gate):** Runs after transformations, before BI/ML consumers access data. Enforces business invariants. If this fails, the pipeline halts and dashboards continue reading yesterday's data.
- **Checkpoint C (Drift Watch):** Runs on schedule (hourly/daily), comparing current snapshot distributions to rolling baselines. Catches slow failures like gradual null-rate increases or category distribution shifts.

**Key Principle:** Validation should be treated like unit tests in software engineering — run in CI/CD, version-controlled, and failures should block deployment. The goal is to catch data issues before they reach consumers, not after. Source: Great Expectations documentation, Databricks, TD Labs, Microsoft Fabric documentation] [Source: https://docs.greatexpectations.io/]

A data lake exists as a repository of raw data, straight from the source to be transformed based on the use case for which it needs to be analyzed, which does not mean that a data lake is a place where data can be dumped without governance. A data lake is also a reference architecture that is independent of technology.

### Deployment Options

Data lakes can be deployed using cloud object storage, such as Amazon S3. Or, large-scale distributed systems such as Apache Hadoop, used for processing Big Data. You can deploy data lakes on relational database management systems, as well as NoSQL data repositories that can store very large amounts of data. [ENRICHED: ecosystem — While Hadoop was the dominant data lake platform historically, cloud object storage (S3, Azure Data Lake Storage, Google Cloud Storage) has become the standard for modern data lakes in 2026. Hadoop's role has declined significantly as organizations migrate to cloud-native architectures using serverless compute and Spark instead of MapReduce. Cloud storage costs approximately $0.02-0.03/GB/month, making it significantly cheaper than traditional database storage. Source: OvalEdge] [Source: https://www.ovaledge.com/blog/advantages-data-lake]

[ENRICHED: ecosystem — Apache Hadoop's relationship to data lakes: Hadoop was the original platform that made data lakes possible at scale, and the concept of a "data lake" emerged directly from the Hadoop ecosystem circa 2010-2011. Hadoop provides three core components that map directly to data lake requirements: (1) HDFS (Hadoop Distributed File System) — a distributed storage layer that can hold petabytes of raw, unstructured data across commodity hardware nodes; (2) MapReduce/Spark — a processing engine that can run transformations and analytics on data where it sits, without requiring it to be loaded into a database first; (3) YARN — a resource scheduler that manages compute resources across the cluster. Before Hadoop, storing raw unstructured data at scale required expensive proprietary storage systems. Hadoop made it economically feasible to store everything — logs, sensor data, images, emails — in its native format on cheap commodity hardware, which is precisely what a data lake does. However, Hadoop required significant operational expertise to manage (cluster provisioning, node management, security configuration), which is why cloud object storage like AWS S3 has largely replaced it for new data lake deployments. S3 offers the same "store anything, pay for what you use" model without the operational burden of managing a Hadoop cluster. The video mentions Hadoop because it remains relevant in legacy enterprise environments and because understanding the Hadoop-to-cloud migration helps explain why modern data lake architecture looks the way it does. Source: DataCamp, Apache Hadoop documentation] [Source: https://www.datacamp.com/blog/hadoop-architecture]

## Benefits of Data Lakes

Data lakes offer a number of benefits.

### All Data Types

Data lakes can store all types of data including: unstructured data, such as documents and emails semi-structured data, such as JSON and XML files, and structured data from relational databases. [ENRICHED: performance context — The global datasphere is expected to reach 175 zettabytes by 2026, with 463 exabytes produced daily. Data lakes are uniquely positioned to handle this volume because they accept any data format without transformation, enabling organizations to capture and store diverse data types including IoT sensor streams, social media content, multimedia files, and enterprise application outputs. Source: OvalEdge] [Source: https://www.ovaledge.com/blog/advantages-data-lake]

### Scalability

Scalability is another data lake benefit. Data lakes can make use of scalable storage capacity—from terabytes to petabytes of data. [ENRICHED: performance context — Cloud-native data lakes can scale seamlessly from gigabytes to petabytes without re-architecture. The decoupled architecture separates compute from storage, allowing organizations to scale analytics workloads independently of data storage. This elasticity means companies pay only for the storage and compute they actually use, avoiding the over-provisioning common with on-premises solutions. Source: DataCamp] [Source: https://www.datacamp.com/blog/what-is-a-data-lake]

### Time Savings and Flexibility

By retaining data in its original format, data lakes save organizations time that would have been used to define structures, create schemas, and transform the data. The ability to access data in its original format enables fast, flexible reuse of the data for a wide range of current and future use cases. [ENRICHED: ecosystem — This flexibility is particularly valuable for machine learning and advanced analytics, where data scientists need access to raw, unprocessed data for feature engineering and model training. Data warehouses require ETL (Extract, Transform, Load) before analysis, while data lakes enable ELT (Extract, Load, Transform) where raw data lands first and transformations happen at query time. Source: Databricks] [Source: https://www.databricks.com/blog/data-lake-vs-cloud-data-warehouse]

### Vendor Ecosystem

Some of the vendors that provide technologies, platforms, and reference architectures for data lakes include: Amazon, Cloudera, Google, IBM, Informatica, Microsoft, Oracle, SAS, Snowflake, Teradata, And, Zaloni.

## Data Lakes vs. Data Warehouses

All in all, data lakes were designed in response to the limitations of data warehouses. Depending on the requirements, a typical organization will require both a data warehouse and a data lake as they serve different needs. [ENRICHED: ecosystem — Modern data architectures increasingly combine both approaches through the lakehouse pattern, which provides the flexibility of data lakes with the performance and governance of data warehouses. The lakehouse uses open table formats like Delta Lake, Apache Iceberg, or Apache Hudi to add ACID transactions, schema enforcement, and time travel capabilities to data lake storage. Source: eWeek] [Source: https://www.eweek.com/big-data-and-analytics/data-lakehouse]

Let's compare data lakes with data warehouses:

### Data Structure

When it comes to data, in a data lake, data is integrated in its raw and unstructured form. A data warehouse is different. Here all data has already been processed and conformed to standards prior to loading to the warehouse.

### Schema

Talking about schema, when using data lakes, you do not need to define the structure and schema of the data before loading into the data lake. A data warehouse on the other hand requires strict conformance to schema and therefore a schema needs to be designed and implemented prior to loading the data.

### Data Quality

How does data quality differ when looking at data lakes and data warehouses? In data lakes the data might or might not be curated, for example raw data. And data is agile and does not necessarily comply with governance guidelines. In comparison, the data in data warehouses is curated and adheres to data governance. [ENRICHED: ecosystem — Data quality management is a critical challenge for data lakes. Without proper governance, data lakes can become "data swamps" where raw data accumulates without discoverability or quality controls. Modern data lakes address this through metadata catalogs (AWS Glue, Apache Hive, Unity Catalog), data quality frameworks, and access control policies that enforce governance while maintaining flexibility. Source: OvalEdge] [Source: https://www.ovaledge.com/blog/advantages-data-lake]

[ENRICHED: clarification — How metadata catalogs prevent data swamps — detailed breakdown of the three systems mentioned:

**What is a Metadata Catalog?**
A metadata catalog is a centralized inventory that stores descriptive information about your data assets — table names, column names, data types, location, ownership, access permissions, and lineage (where data came from and where it goes). Think of it as a "search engine for your data lake." Without a catalog, a data lake is just a pile of files — nobody knows what exists, who owns it, or whether it's trustworthy. The catalog makes data discoverable and governable.

**1. AWS Glue Data Catalog**
- **What it is:** A fully managed, serverless metadata service on AWS. It automatically crawls data stores (S3, RDS, DynamoDB), extracts schema information, and stores it in a central catalog.
- **How it prevents data swamps:** When new data lands in S3, an AWS Glue Crawler automatically discovers its schema, registers table definitions, and makes the data queryable via Athena, EMR, or Redshift Spectrum. This means every dataset gets documented without manual effort.
- **Key features:** Automatic schema discovery, built-in PII detection, integration with AWS Lake Formation for fine-grained access control (row-level and column-level permissions), and support for Apache Iceberg tables.
- **Governance mechanism:** Lake Formation acts as the access control layer — you grant permissions on tables/columns to specific IAM roles or users, and all queries are enforced through this layer.

**2. Apache Hive Metastore**
- **What it is:** The original open-source metadata catalog for Hadoop ecosystems. It stores table definitions (schema, location, serialization/deserialization info) in a relational database (MySQL, PostgreSQL).
- **How it prevents data swamps:** Hive Metastore provides a consistent schema registry — when data engineers define tables, the metastore enforces that the schema matches what's actually stored. It's the foundation that most data lake tools (Spark, Presto, Trino) use to understand data structure.
- **Key features:** Schema registry, partition management, ACID transaction support (with Hive 3+), and broad compatibility with query engines.
- **Limitation:** Traditional Hive Metastore lacks fine-grained access control (row/column-level security), which is why organizations often layer Apache Ranger or AWS Lake Formation on top of it.

**3. Databricks Unity Catalog**
- **What it is:** A modern, unified governance layer for the lakehouse architecture. Unlike Hive Metastore (which only handles tables), Unity Catalog governs tables, volumes, ML models, functions, and AI assets in a single namespace.
- **How it prevents data swamps:** Unity Catalog provides automatic data discovery, lineage tracking (you can trace any column back to its source), row-level and column-level security, and auditing. It federates with AWS Glue and Hive Metastore, meaning you can govern existing data without migrating it.
- **Key features:** Fine-grained RBAC (role-based access control), data lineage, cross-workspace access, Delta Sharing (secure data sharing across organizations), and integration with MLflow for model governance.
- **Federation capability:** As of 2025, Unity Catalog can federate AWS Glue and Hive Metastore catalogs directly — connecting your existing metadata without manual migration. This means organizations with legacy Hive deployments can add Unity Catalog governance on top.

**How they work together in modern architectures:**
A typical 2026 data lake might use AWS Glue to crawl raw S3 data, store metadata in the Glue Data Catalog, apply Lake Formation permissions for access control, and then use Unity Catalog to provide a unified governance layer across multiple clouds and analytic engines. The catalog ensures that every dataset is documented, discoverable, and accessible only to authorized users — preventing the "data swamp" scenario where raw data accumulates without governance. Source: AWS documentation, Databricks documentation, Databricks blog] [Source: https://docs.databricks.com/aws/en/query-federation/hms-federation-concepts]

[ENRICHED: clarification — The video's statement that data in a lake "does not necessarily comply with governance guidelines" refers to TWO distinct layers of governance, and understanding this distinction answers your question about whether data that violates policies should have been rejected at collection time:

**Layer 1 — Technical/Operational Governance (what the video is mainly about):**
This is about data quality standards, naming conventions, formatting, metadata tagging, and organizational data policies. In a data warehouse, every table must conform to a predefined schema before it can be loaded — this is schema-on-write. The schema acts as a gatekeeper: data that doesn't fit is rejected or transformed before entry. In a data lake, there is no such gatekeeper at ingestion. A data lake accepts raw data in any format — CSV files with inconsistent column names, JSON logs with missing fields, images without metadata, sensor readings without timestamps. The data lands first, and quality/formatting is addressed later (if at all). This means the lake accumulates data that is technically "non-compliant" with the organization's internal data quality standards — not because the data was collected illegally, but because it wasn't cleaned, standardized, or tagged according to internal conventions.

**Layer 2 — Regulatory/Legal Compliance (your deeper question):**
This is where your question becomes critical. Regulations like GDPR, HIPAA, and CCPA impose requirements on BOTH collection AND storage, but they address different things at each stage:

- **At collection time:** Regulations govern consent, purpose limitation, and lawful basis. GDPR requires that you have a legal basis (consent, legitimate interest, etc.) before collecting personal data. HIPAA requires that PHI (Protected Health Information) is collected only for treatment, payment, or healthcare operations. These are "gate" rules — data that fails these checks SHOULD be rejected at collection, and your intuition is correct: if proper governance is in place, this data should never reach the lake.

- **At storage time:** Even data that was collected legally can violate regulations in storage. Examples: (a) A customer consented to their email being used for marketing, but the data lake stores it alongside browsing behavior data that was collected without consent — mixing consented and non-consented data violates purpose limitation. (b) A patient's medical records were collected legally for treatment, but the data lake makes them accessible to unauthorized analysts who don't have a treatment relationship — violating access control requirements. (c) PII (Personally Identifiable Information) is stored without encryption or masking — violating data protection requirements. (d) Data was collected legally but is retained beyond the allowed retention period — violating storage limitation principles.

**The full picture:** The video's statement is describing a scenario where data lakes, because they accept everything without gatekeeping, can accumulate data that fails BOTH layers. The "data swamp" problem is not just about messy formatting — it's about the risk that data entering without quality gates may also be entering without compliance checks. This is why modern data lakes implement "data governance frameworks" that include: (1) Ingestion policies that screen data at entry (your collection-time gate), (2) Metadata catalogs that track provenance, consent, and access rights (your storage-time controls), (3) Access control layers that restrict who can query what data, and (4) Retention policies that automatically purge data past its legal retention window. The distinction the video draws between data lakes ("might not comply") and data warehouses ("adheres to governance") is that warehouses enforce these checks at load time through schema validation and ETL processes, while data lakes require additional tooling to achieve the same governance. Source: Accountable HQ, The Data Governor] [Source: https://www.accountablehq.com/post/how-to-build-a-hipaa-compliant-healthcare-data-lake-architecture-security-and-best-practices]

### Users

Here, we are looking at users of data lakes and data warehouses. Data scientists, data developers, and machine learning engineers are the typical users of data lakes. Data warehouses, on the other hand, are mainly used by business analysts, and data analysts.

## Key Takeaways

In this video, you learned that: A data lake is a storage repository that can store large amounts of structured, semi-structured, and unstructured data in their raw or native format, classified and tagged with metadata. You do not need to define the structure and schema of data before loading into the data lake. Data lakes offer several benefits, such as storage for all types of data, scalable storage capacity, time savings, and flexible data reuse. Finally, you learned that data lakes can be used as a kind of self-serve staging area for a variety of use cases, including machine learning development and advanced analytics.

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | What Is a Data Lake | Definition | Defined data lake with modern cloud-native context and lakehouse evolution | HIGH | https://www.ibm.com/think/topics/data-lake |
| 2 | Data Lake Architecture | Definition | Defined schema-on-read vs schema-on-write paradigm | HIGH | https://www.databricks.com/blog/data-lake-vs-cloud-data-warehouse |
| 3 | Deployment Options | Ecosystem connection | Connected Hadoop decline to cloud object storage dominance with cost data | HIGH | https://www.ovaledge.com/blog/advantages-data-lake |
| 4 | All Data Types | Performance context | Added global datasphere projections (175 ZB by 2026) and data type examples | HIGH | https://www.ovaledge.com/blog/advantages-data-lake |
| 5 | Scalability | Performance context | Added decoupled architecture and elasticity benefits | HIGH | https://www.datacamp.com/blog/what-is-a-data-lake |
| 6 | Time Savings | Ecosystem connection | Connected to ML/analytics workflows and ELT vs ETL patterns | HIGH | https://www.databricks.com/blog/data-lake-vs-cloud-data-warehouse |
| 7 | Data Lakes vs Warehouses | Ecosystem connection | Added lakehouse architecture and open table formats | HIGH | https://www.eweek.com/big-data-and-analytics/data-lakehouse |
| 8 | Data Quality | Ecosystem connection | Added data swamp risk and governance solutions (catalogs, quality frameworks) | HIGH | https://www.ovaledge.com/blog/advantages-data-lake |
| 9 | Deployment Options | Ecosystem connection | Explained Apache Hadoop's historical role as the original data lake platform (HDFS, MapReduce, YARN) and why it was replaced by cloud storage | HIGH | https://www.datacamp.com/blog/hadoop-architecture |
| 10 | Data Quality | Clarification | Distinguished technical governance (schema, formatting, naming) from regulatory compliance (GDPR/HIPAA/CCPA), explained collection-time vs storage-time obligations, purpose limitation, and why data that violates policies may still enter a lake without gatekeeping | HIGH | https://www.accountablehq.com/post/how-to-build-a-hipaa-compliant-healthcare-data-lake-architecture-security-and-best-practices |
| 11 | Data Lake Architecture | Clarification | Detailed multi-layered data quality validation procedures (ingestion/transformation/serving), validation frameworks comparison table, and three-checkpoint architecture pattern for preventing data swamps | HIGH | https://docs.greatexpectations.io/ |
| 12 | Data Quality | Clarification | Explained metadata catalogs (AWS Glue, Apache Hive, Unity Catalog) — what each is, how it prevents data swamps, key features, and how they work together in modern architectures | HIGH | https://docs.databricks.com/aws/en/query-federation/hms-federation-concepts |

<!-- EXTRACTION_CHECKLIST: 45 sentences extracted, 45 sentences in output + 4 enrichments added via clarification questions -->
