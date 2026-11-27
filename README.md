# Data Engineering Career Path — Workspace & Portfolio Root

Root repository index for the comprehensive data engineering career path, containing verified course credentials, hands-on enterprise projects, distributed data pipelines, and the documentation wiki pipeline.

---

## 🏆 Verified Professional Certificates & Projects Matrix

### IBM Data Engineering Professional Certificate (Complete 16-Course Specialization)

| # | Course Name | Credential PDF | Hands-on Project & Repository Directory |
|---|---|---|---|
| **C1** | Introduction to Data Engineering | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Introduction to Data Engineering.pdf>) | Foundational Concepts & Modern Data Ecosystem |
| **C2** | Python for Data Science, AI & Development | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Python for Data Science, AI & Development.pdf>) | [Multi-Source Data Aggregator](projects/course2-data-aggregator/) |
| **C3** | Python Project for Data Engineering | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Python Project for Data Engineering.pdf>) | [Global Banking Market Cap ETL Pipeline](projects/course3-banks-project/) |
| **C4** | Introduction to Relational Databases (RDBMS) | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Introduction to Relational Databases (RDBMS).pdf>) | [Coffee Shop Relational Database & Views](projects/c4_coffee_shop_database_final_project/) |
| **C5** | Databases and SQL for Data Science with Python | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Databases and SQL for Data Science with Python.pdf>) | [Chicago Socioeconomic & Public School Analytics](projects/c5_databases_and_sql_for_data_science_final_project/) |
| **C6** | Hands-on Introduction to Linux Commands and Shell Scripting | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Hands-on Introduction to Linux Commands and Shell Scripting.pdf>) | [Automated Directory Backup & Archive Engine](projects/c6_linux_shell_scripting_final_project/) |
| **C7** | Relational Database Administration (DBA) | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Relational Database Administration (DBA).pdf>) | [PostgreSQL & MySQL DBA Operations & Tuning](projects/c7_relational_database_administration_dba_final_project/) |
| **C8** | ETL and Data Pipelines with Shell, Airflow and Kafka | [Certificate](<certificates/IBM Data Engineering Professional Certificate/ETL and Data Pipelines with Shell, Airflow and Kafka.pdf>) | [Highway Toll Plaza Analytics (Airflow & Kafka)](projects/c8_etl_data_pipelines_with_shell_airflow_and_kafka_final_project/) |
| **C9** | Data Warehouse Fundamentals | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Data Warehouse Fundamentals.pdf>) | [Waste Management DW (Star Schema, CUBE, ROLLUP)](projects/c9_data_warehouse_fundamentals_final_project/) & [Retail DW Practice](projects/c9_data_warehouse_fundamentals_practice_project/) |
| **C10** | BI Dashboards with IBM Cognos Analytics and Google Looker | [Certificate](<certificates/IBM Data Engineering Professional Certificate/BI Dashboards with IBM Cognos Analytics and Google Looker.pdf>) | [Automotive Sales & Sentiment Dashboards](projects/c10_bi_dashboards_cognos_looker_final_project/) |
| **C11** | Introduction to NoSQL Databases | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Introduction to NoSQL Databases.pdf>) | [Polyglot NoSQL Consulting (MongoDB & Cassandra)](projects/c11_nosql_databases_final_project/) |
| **C12** | Introduction to Big Data with Spark and Hadoop | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Introduction to Big Data with Spark and Hadoop.pdf>) | [Big Data Analytics (PySpark & Hadoop MapReduce)](projects/c12_big_data_with_spark_and_hadoop_final_project/) |
| **C13** | Machine Learning with Apache Spark | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Machine Learning with Apache Spark.pdf>) | [NASA Airfoil Sound Pressure SparkML Pipeline](projects/c13_machine_learning_with_apache_spark_final_project/) |
| **C14** | Data Engineering Capstone Project | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Data Engineering Capstone Project.pdf>) | [SoftCart E-Commerce Enterprise Data Platform](projects/c14_data_engineering_capstone_project/) |
| **C15** | Generative AI: Elevate your Data Engineering Career | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Generative AI- Elevate your Data Engineering Career.pdf>) | GenAI Prompts, Augmentation & Data Engineering Copilots |
| **C16** | Data Engineering Career Guide and Interview Preparation | [Certificate](<certificates/IBM Data Engineering Professional Certificate/Data Engineering Career Guide and Interview Preparation.pdf>) | Technical Portfolio & Interview Case Studies |

### Additional Credentials & Specializations
- **IBM / Coursera**: [NoSQL, Big Data, and Spark Foundations Specialization](<certificates/NoSQL, Big Data, and Spark Foundations Specialization/Specialization Certificate.pdf>)
- **DataCamp**: [Associate Data Engineer in SQL](<certificates/Datacamp/SQL Associate Data Engineer Career Path/Associate Data Engineer in SQL.pdf>)
- **NTI-ITIDA**: [Big Data Analysis Certification](<certificates/NTI-ITIDA/NTI ITIDA Big Data Analysis.pdf>)
- **UC San Diego**: [Introduction to Big Data](<certificates/UCSD Big Data Specialization/Introduction to Big Data.pdf>)

---

## 📁 Top-Level Workspace Structure

### `projects/`
Completed hands-on projects organized into standardized, standalone subdirectories:
- **[`course2-data-aggregator/`](projects/course2-data-aggregator/)** — Course 2: Ingests World Bank macro indicators (CSV) and REST API JSON feeds into merged analytical datasets.
- **[`course3-banks-project/`](projects/course3-banks-project/)** — Course 3: Automated web scraping ETL pipeline calculating bank market capitalizations across currencies (USD, GBP, EUR, INR) into SQLite.
- **[`c4_coffee_shop_database_final_project/`](projects/c4_coffee_shop_database_final_project/)** — Course 4: Coffee shop relational database design, ERDs, normalization, and views.
- **[`c5_databases_and_sql_for_data_science_final_project/`](projects/c5_databases_and_sql_for_data_science_final_project/)** — Course 5: Chicago socioeconomic, school safety, and crime statistics SQL study.
- **[`c6_linux_shell_scripting_final_project/`](projects/c6_linux_shell_scripting_final_project/)** — Course 6: Automated backup and directory compression engine scheduled via `cron`.
- **[`c7_relational_database_administration_dba_final_project/`](projects/c7_relational_database_administration_dba_final_project/)** — Course 7: PostgreSQL RBAC security, MySQL storage engines (InnoDB/MyISAM), B-tree index optimization, and automated backup scripting.
- **[`c8_etl_data_pipelines_with_shell_airflow_and_kafka_final_project/`](projects/c8_etl_data_pipelines_with_shell_airflow_and_kafka_final_project/)** — Course 8: Dual-architecture batch (Airflow) and streaming (Kafka + MySQL) highway toll analytics pipeline.
- **[`c9_data_warehouse_fundamentals_practice_project/`](projects/c9_data_warehouse_fundamentals_practice_project/)** — Course 9 Practice: Containerized retail star schema warehouse in PostgreSQL.
- **[`c9_data_warehouse_fundamentals_final_project/`](projects/c9_data_warehouse_fundamentals_final_project/)** — Course 9 Final: Solid waste management data warehouse with `GROUPING SETS`, `ROLLUP`, `CUBE`, and materialized views.
- **[`c10_bi_dashboards_cognos_looker_final_project/`](projects/c10_bi_dashboards_cognos_looker_final_project/)** — Course 10: Automotive executive BI dashboards built in IBM Cognos Analytics and Google Looker Studio.
- **[`c11_nosql_databases_final_project/`](projects/c11_nosql_databases_final_project/)** — Course 11: Polyglot persistence with MongoDB document aggregation, CLI export, and Apache Cassandra CQL tables and secondary indexes.
- **[`c12_big_data_with_spark_and_hadoop_final_project/`](projects/c12_big_data_with_spark_and_hadoop_final_project/)** — Course 12: Dockerized Apache Spark master-worker cluster, PySpark DataFrame jobs, and Hadoop MapReduce word count.
- **[`c13_machine_learning_with_apache_spark_final_project/`](projects/c13_machine_learning_with_apache_spark_final_project/)** — Course 13: NASA Airfoil Self-Noise 3-stage SparkML pipeline (VectorAssembler, StandardScaler, LinearRegression, model evaluation and persistence).
- **[`credit_card_default_prediction/`](projects/credit_card_default_prediction/)** — Collaborative ML Project: Supervised classification model predicting credit card default probabilities.
- **[`c14_data_engineering_capstone_project/`](projects/c14_data_engineering_capstone_project/)** — Course 14: Comprehensive SoftCart enterprise data platform spanning MySQL OLTP, MongoDB catalog, PostgreSQL warehouse, Airflow ETL DAGs, BI reporting, and PySpark MLOps.

### `certificates/`
PDF certificates organized by provider:
- **`IBM Data Engineering Professional Certificate/`** — All 16 course certificates.
- **`NoSQL, Big Data, and Spark Foundations Specialization/`** — Specialization certificate.
- **`Datacamp/`** — Track certificates for Data Engineer in Python and SQL Associate.
- **`NTI-ITIDA/`** — Big Data Analysis certificate.
- **`UCSD Big Data Specialization/`** — UCSD Introduction to Big Data certificate.

### `big data and data engineering plan/`
Master learning plan and automated tracking tooling:
- **`data-engineer-career-path/big_data_de_learning_plan.md`** — Comprehensive curriculum tracking (~950h).

### `wiki-generation-pipeline/`
Automated knowledge base pipeline organizing course transcripts, labs, and deep-dive documentation into Markdown and deployable single-file HTML wiki.
