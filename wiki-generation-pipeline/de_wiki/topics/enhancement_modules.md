# Post-Track Enhancement Modules

These modules cover topics the IBM Data Engineering track does not address. Complete after finishing all 16 IBM courses.

## Enhancement A — Big Data Analytics at Scale (~23h)

**Gap filled:** The IBM track covers data warehousing (Course 9) and Spark SQL (Course 12) but does not teach Hive/Impala/Pig or Lambda vs Kappa architecture — tools and patterns still common in Hadoop-based enterprise environments.

**Topics:** Apache Hive (DDL/DML, partitioning, bucketing), Apache Impala, Apache Pig, Lambda vs Kappa streaming architectures.

**Learning objective:** Write and optimize HiveQL queries against partitioned tables, explain Hive vs Impala tradeoffs, and diagram a Lambda vs a Kappa architecture for the same use case.

| Resource | Hours |
|----------|-------|
| Apache Hive Language Manual (DDL/DML, partitioning, bucketing) | 8 |
| Apache Impala official documentation | 5 |
| Apache Pig official documentation | 3 |
| Kreps "Questioning the Lambda Architecture" + Confluent Kappa blog posts | 2 |
| Project checkpoint: load NYC Taxi data into Hive-style partitioned tables, write 5 analytical queries, document architecture | 5 |

## Enhancement B — Security & Governance Deep Dive (~8h)

**Gap filled:** Course 7 (DBA) covers database-level security. This enhancement extends to cluster-wide governance with Apache Ranger and Apache Atlas for policy management, metadata, and data lineage.

**Topics:** Apache Ranger (policy model, plugins, Hive/HDFS integration), Apache Atlas (metadata, governance, data lineage).

**Learning objective:** Configure a Ranger policy restricting user/group access to specific Hive tables or HDFS paths; use Atlas to trace data lineage across a pipeline.

| Resource | Hours |
|----------|-------|
| Apache Ranger official documentation | 5 |
| Apache Atlas official documentation | 3 |

## Enhancement C — Modern Pipeline Tooling: dbt & Data Quality (~17h)

**Gap filled:** Course 8 covers ETL with Airflow and Kafka. This enhancement adds dbt (the industry standard for SQL-based transformation) and data quality tooling — skills required by most mid-level+ DE job postings.

**Topics:** dbt (models, tests, documentation, incremental loads), dbt advanced warehouse-specific optimizations, pipeline data quality with Great Expectations.

**Learning objective:** Build a dbt project with models, tests, and documentation; run it against a warehouse; validate data quality with Great Expectations integrated into an Airflow DAG.

| Resource | Hours |
|----------|-------|
| dbt official documentation + dbt Learn "Fundamentals" course | 8 |
| DataTalks.Club DE Zoomcamp Module 4: Analytics Engineering with dbt | 5 |
| Great Expectations "Getting Started" guide | 1 |
| dbt "Advanced" course (warehouse-specific optimizations) | 3 |

## Enhancement D — Revision (~1h)

Self-assessment checkpoint. Watch Mahmoud Mohsen's midterm-style revision video after completing the IBM track.

| Resource | Hours |
|----------|-------|
| Mahmoud Mohsen #20 Revision (Midterm Solutions) — watch without pausing, answer questions mentally | 1 |

[Cross-ref: topics/course_sequence_16.md — the IBM courses that these enhancements extend]
[Cross-ref: topics/certification_roadmap.md — Enhancement C (dbt) is prerequisite for SnowPro Advanced]
[Cross-ref: topics/skills_and_responsibilities.md — Enhancement A fills big data analytics gap in skill taxonomy]
