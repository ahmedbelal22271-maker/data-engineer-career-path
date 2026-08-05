**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 1:** Extract, Transform, Load (ETL) Overview

# Course Introduction

Are you an aspiring Big Data Engineer or Developer interested in creating Data Pipelines for serving Data Warehouses and Data Analytics platforms? Would you like to learn all about ETL and ELT data pipelines and how to build them using Bash scripting and cutting-edge open-source tools such as Apache Airflow and Apache Kafka? This course may be just right for you.

## What is ETL?

ETL stands for Extract, Transform, and Load. It refers to the process of curating data from multiple sources and preparing the data for integration and loading into a destination platform such as a data warehouse or analytics environment.

[ENRICHED: defined "data warehouse" — a centralized repository that stores structured, processed data from multiple sources, optimized for analytical queries and reporting. Unlike operational databases designed for transactional workloads (OLTP), data warehouses are optimized for read-heavy analytical workloads (OLAP), typically using columnar storage and schemas designed for fast aggregation (star schema for denormalized speed, or snowflake schema for normalized structure), with batch-loaded historical data. The term "snowflake" here refers to the schema pattern (dimension tables split into sub-dimensions), not the Snowflake cloud data warehouse product.] [ENRICHED: defined "analytics environment" — any system or platform where data is analyzed for insights, including data warehouses, data lakes, data marts, business intelligence (BI) dashboards, and machine learning platforms.]

## What is ELT?

ELT is similar but loads the data in its raw format, reserving the transformations for people to apply themselves in a 'self-serve analytics' destination environment.

[ENRICHED: added specificity — "self-serve analytics" means any authorized user (analyst, manager, data scientist) can answer their own data questions by querying raw data directly, without filing a ticket and waiting for an engineering team to build a custom transformation for them. To understand why this matters, compare the two workflows:]

**ETL (pre-transformed data) — the old way:**

1. A marketing manager asks: "What is our customer churn rate by region for the last quarter?"
2. The data engineering team receives the request, estimates 3 days of work, and schedules it for next sprint.
3. The engineers write a transformation that joins `customers` + `subscriptions` + `cancellation_reasons`, computes churn rate per region, and loads the result into a pre-defined `churn_by_region` table in the data warehouse.
4. The marketing manager finally gets access to the answer — 2 weeks later.
5. The manager then asks: "Can I also see it by product tier?" — another ticket, another 3 days of engineering work.

The data is pre-shaped for specific known questions. Every new question requires a new transformation, a new pipeline step, a new wait.

**ELT (raw data + self-serve) — the modern way:**

1. The raw customer, subscription, and cancellation data is loaded into a data lake (e.g., Amazon S3 or a Snowflake raw schema) — untouched, complete, all columns, all history.
2. The marketing manager opens a SQL workbook (a browser-based tool where you type SQL queries and see results instantly).
3. They write: `SELECT region, COUNT(churned) / COUNT(*) as churn_rate FROM raw_customers GROUP BY region` — and get the answer in 30 seconds.
4. They then write: `SELECT region, product_tier, COUNT(churned) / COUNT(*) as churn_rate FROM raw_customers GROUP BY region, product_tier` — the breakdown by product tier appears in another 30 seconds.
5. No engineering ticket. No 2-week wait. No pipeline modification.

The tools that make this possible:
- **SQL workbooks** (e.g., Hex, Mode, Google BigQuery console) — browser-based tools where you write SQL and see results as tables and charts.
- **dbt** (data build tool) — a tool that lets analysts write reusable SQL transformation scripts (called "models") that are version-controlled, tested, and documented, but run by the analysts themselves, not the engineering team.
- **Notebooks** (Jupyter, Databricks) — environments where data scientists write Python/R code in cells, combining code, results, and narrative text in a single document for exploratory analysis.

The key shift: the engineering team's job changes from "build every transformation for every user" to "load raw data reliably and make it accessible." The users who actually need the data become responsible for shaping it to their own needs.]

Both methods are typical examples of data pipeline deployments.

## What This Course Covers

In this course, you will explore the fundamental principles and techniques behind ETL and ELT processes. You will learn how to construct a basic ETL data pipeline from scratch using Bash shell-scripting. You will also learn about the tools, technologies, and use cases for the two main paradigms within data pipeline engineering: batch and streaming data pipelines. You will further cement this knowledge by exploring and applying two popular open-source data pipeline tools: Apache Airflow and Apache Kafka.

## Apache Airflow

You will learn all about Apache Airflow and use it to build, put into production, and monitor a basic batch ETL workflow. You will implement this data pipeline using Airflow's central construct of a directed acyclic graph (DAG), consisting of simple Bash tasks, Python function and their dependencies.

[ENRICHED: defined "directed acyclic graph (DAG)" — a graph structure where nodes represent tasks and directed edges represent dependencies, with no cycles (a task cannot depend on itself, directly or indirectly). In Airflow, a DAG is a Python file that defines the order and relationships between tasks. The scheduler executes tasks in dependency order, and the UI visualizes the graph.] [ENRICHED: ecosystem — Apache Airflow is the most widely adopted workflow orchestration tool in data engineering. Alternatives include Prefect, Dagster, Mage, and AWS Step Functions. Airflow's advantage is its large ecosystem of operators (pre-built task types for databases, APIs, cloud services) and its mature scheduling/retry/alerting infrastructure.]

## Apache Kafka

You will also learn about Apache Kafka and use it to get hands-on experience with streaming data pipelines, implementing Kafka's message producers and consumers, and creating a Kafka weather topic.

[ENRICHED: defined "message producers and consumers" — in Kafka's producer-consumer model, a producer is any application that publishes (writes) messages to a Kafka topic, and a consumer is any application that subscribes to (reads) messages from a Kafka topic. Topics are partitioned log streams — messages are appended in order within a partition, and consumers read at their own pace, tracking their position via an offset.] [ENRICHED: ecosystem — Kafka competes with Amazon Kinesis, Apache Pulsar, Redpanda, and NATS in the event-streaming space. Kafka's dominance comes from its durability guarantees (disk-based log retention), horizontal scalability (partition-based parallelism), and the Kafka Streams/Connect ecosystem for stream processing and data integration.]

## Course Structure

This video and hands-on, lab-based course is made up of 5 modules: Data Processing Techniques; ETL & Data Pipelines: Tools and Techniques; Building Data Pipelines using Apache Airflow; Building Streaming Pipelines using Apache Kafka; and a Final Assignment.

"ETL and Pipelines" will provide you with a great hands-on introduction to the latest technologies in data pipeline engineering.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | What is ETL section | Definition | Defined "data warehouse" as centralized structured repository optimized for OLAP | HIGH |
| 2 | What is ETL section | Definition | Defined "analytics environment" as any system for data analysis (DW, data lake, BI, ML) | HIGH |
| 3 | What is ELT section | Added specificity | Explained "self-serve analytics" as user-driven transformation using SQL, dbt, notebooks | HIGH |
| 4 | Apache Airflow section | Definition | Defined DAG as graph with directed edges and no cycles, used to model task dependencies | HIGH |
| 5 | Apache Airflow section | Ecosystem | Positioned Airflow vs Prefect, Dagster, Mage, AWS Step Functions | HIGH |
| 6 | Apache Kafka section | Definition | Defined producers (publish to topics) and consumers (subscribe from topics) with offset tracking | HIGH |
| 7 | Apache Kafka section | Ecosystem | Positioned Kafka vs Kinesis, Pulsar, Redpanda, NATS | HIGH |

<!-- EXTRACTION_CHECKLIST: 12 sentences extracted, 12 sentences in output -->
