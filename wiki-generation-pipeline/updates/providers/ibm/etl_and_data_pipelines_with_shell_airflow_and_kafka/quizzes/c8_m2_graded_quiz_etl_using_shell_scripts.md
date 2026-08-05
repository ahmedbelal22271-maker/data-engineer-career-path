**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 2:** Shell Scripting for ETL

# Graded Quiz: ETL Using Shell Scripts

## Question 1

**Select the correct statement regarding Apache Airflow.**

| Option | Correct? |
|--------|----------|
| Apache Airflow is a well-known commercial tool. | ✗ |
| Apache Airflow tasks can be expressed as Python, but not Bash. | ✗ |
| **Apache Airflow is a workflow orchestration tool.** | **✓ CORRECT** |
| Apache Airflow represents the workflow in DAGs, but not in code. | ✗ |

**Answer:** Apache Airflow is a workflow orchestration tool.

[ENRICHED: added specificity — Apache Airflow is an **open-source** workflow orchestration platform originally developed at Airbnb and now maintained by the Apache Software Foundation. It is NOT a commercial tool — it's free and open-source (Apache 2.0 license). Airflow tasks CAN be expressed as both Python and Bash: the `PythonOperator` runs Python functions, and the `BashOperator` runs shell commands. Airflow represents workflows as DAGs (Directed Acyclic Graphs) **defined in Python code** — you write a Python file that instantiates a `DAG` object and defines tasks with dependencies. The Python code is the source of truth; the DAG visualization in the Airflow UI is derived from that code, not the other way around. Airflow does NOT do the ETL itself — it orchestrates tasks that do. You use Airflow to coordinate: "run Extract, then Transform, then Load, and notify me if anything fails."]

## Question 2

**What is the first stage of the ETL process?**

| Option | Correct? |
|--------|----------|
| Cleaning | ✗ |
| Loading | ✗ |
| **Extraction** | **✓ CORRECT** |
| Transformation | ✗ |

**Answer:** Extraction

[ENRICHED: added specificity — ETL stands for **Extract**, Transform, Load — the acronym itself defines the order. Extraction is Stage 1: data is acquired from source systems (databases, APIs, files, streaming sources). Cleaning is a sub-process within the Transform stage (Stage 2), where errors and missing values are fixed. Transformation is Stage 2: rules are applied to prepare data for the target system (cleaning, filtering, joining, normalizing, aggregating). Loading is Stage 3: the transformed data is written to the target system (data warehouse, database, CSV file). The extraction stage reads data; the transformation stage reshapes it; the loading stage stores it.]

## Question 3

**Select the correct statement regarding batch processing.**

| Option | Correct? |
|--------|----------|
| **Batch processing intervals can be triggered by events.** | **✓ CORRECT** |
| Batch processing triggers are rarely on demand. | ✗ |
| Data is processed in batches, usually on a weekly schedule. | ✗ |
| When an event of interest occurs, such as an intruder alert, the interval would be periodic. | ✗ |

**Answer:** Batch processing intervals can be triggered by events.

[ENRICHED: added specificity — Batch processing intervals are NOT limited to periodic schedules. The enriched lesson content lists three trigger types: (1) **Size-based**: when source data reaches a certain size (e.g., "process when CSV exceeds 1 GB"). (2) **Event-based**: when an event of interest occurs (e.g., an intruder alert triggers immediate log analysis). (3) **On-demand**: triggered by user requests (e.g., a music streaming app generates a personalized playlist when requested). The statement "Batch processing triggers are rarely on demand" is false — on-demand triggers are explicitly listed as a valid batch trigger type. The statement "Data is processed in batches, usually on a weekly schedule" is misleading — batches range from hours to days, not specifically weekly. The statement about intruder alerts being "periodic" is false — event-based triggers are aperiodic (they fire when the event occurs, not on a fixed schedule).]

## Question 4

**Bash uses _____ to turn your file into a Bash shell script.**

| Option | Correct? |
|--------|----------|
| getstat | ✗ |
| **shebang** | **✓ CORRECT** |
| loadstat | ✗ |
| crontab | ✗ |

**Answer:** shebang

[ENRICHED: defined "shebang" — The shebang (`#!`) is a character sequence at the very first line of a script file that tells the operating system which interpreter to use when executing the file. For Bash scripts, the shebang is `#!/bin/bash`. Without a shebang, the system uses the default shell (often `sh`), which may not support all Bash-specific features. Common shebangs: `#!/bin/sh` (POSIX shell), `#!/usr/bin/env python3` (Python 3), `#!/usr/bin/perl` (Perl). The name "shebang" comes from "hash" (`#`) + "bang" (`!`). `getstat` and `loadstat` are functions used in the temperature ETL video (not shell script creation tools). `crontab` is the cron job scheduler for running scripts on a schedule — it does not turn files into scripts.]

## Question 5

**SSIS, Amazon Redshift, IBM InfoSphere Information Server, and Oracle GoldenGate are examples of _____.**

| Option | Correct? |
|--------|----------|
| Popular commercial ELT tools | ✗ |
| **Popular commercial ETL tools** | **✓ CORRECT** |
| Popular open-source ETL tools | ✗ |
| Popular open-source ELT tools | ✗ |

**Answer:** Popular commercial ETL tools

[ENRICHED: added specificity — These are all **commercial** (not open-source) **ETL** (not ELT) tools: **SSIS** (SQL Server Integration Services) — Microsoft's ETL tool bundled with SQL Server, uses a visual designer with drag-and-drop data flows. **Amazon Redshift** — AWS's cloud data warehouse (note: Redshift itself is a destination, not an ETL tool, but AWS positions it as part of ETL workflows with AWS Glue providing the ETL layer). **IBM InfoSphere Information Server** — IBM's enterprise data integration platform, with DataStage as its ETL component (uses parallel processing and graphical job design). **Oracle GoldenGate** — Oracle's real-time data replication and integration tool, focused on CDC (Change Data Capture) for moving data between heterogeneous databases. These are NOT open-source tools — they are commercial products requiring paid licenses. They are NOT ELT tools — they transform data before loading it into the target system (ETL pattern). Open-source ETL alternatives include Apache Airflow, Talend Open Studio, and Pandas.]

## Question 6

**ETL pipelines are frequently used to integrate data from disparate and usually _____ systems within the enterprise.**

| Option | Correct? |
|--------|----------|
| simultaneous | ✗ |
| **siloed** | **✓ CORRECT** |
| aggregating | ✗ |
| batched | ✗ |

**Answer:** siloed

[ENRICHED: defined "siloed systems" — Siloed systems are databases, applications, or data stores that operate independently within an organization, with little or no integration between them. Each department (payroll, sales, purchasing) maintains its own system, and data does not flow freely between them. This is the problem ETL solves: it extracts data from these isolated silos, transforms it into a unified format, and loads it into a centralized repository (data warehouse) where cross-department analysis becomes possible. The enriched lesson gives a concrete example: a manufacturing company with three separate OLTP systems — Oracle for payroll, Salesforce for sales, SAP for purchasing. Without ETL, answering "What is the total cost per department?" requires manual data collection from all three systems. With ETL, a staging area normalizes and joins the data, and a cost accounting OLAP system can query it directly.]

## Question 7

**Select the correct statement regarding ETL workflows as data pipelines.**

| Option | Correct? |
|--------|----------|
| **Overall accuracy of the ETL workflow has been a more important requirement than speed.** | **✓ CORRECT** |
| Data is fed through a data pipeline in large packets. | ✗ |
| With conventional ETL pipelines data is processed in real time. | ✗ |
| Bottlenecks within the pipeline can often be handled by anonymizing slower tasks. | ✗ |

**Answer:** Overall accuracy of the ETL workflow has been a more important requirement than speed.

[ENRICHED: added specificity — The enriched lesson states: "Traditionally, the overall accuracy of the ETL workflow has been a more important requirement than speed, although efficiency is usually an important factor in minimizing resource costs." This reflects the historical priority of data warehousing: correctness matters more than speed because business decisions depend on accurate data. The other options contain deliberate distortions: (1) "Data is fed through a data pipeline in large packets" — FALSE. The lesson says data is fed in **smaller** packets to enable pipelining (overlap of extract/transform/load stages). (2) "With conventional ETL pipelines data is processed in real time" — FALSE. Conventional ETL uses **batch** processing (hours to days apart), not real-time. Real-time is a newer paradigm (stream processing with Kafka, Flink). (3) "Bottlenecks within the pipeline can often be handled by anonymizing slower tasks" — FALSE. The lesson says bottlenecks are handled by **parallelizing** slower tasks (running them across multiple machines or threads), not anonymizing them. Anonymizing is a privacy transformation, not a performance technique.]

## Question 8

**Which of these transformations is correctly described?**

| Option | Correct? |
|--------|----------|
| **Normalizing: Converting data to common units** | **✓ CORRECT** |
| Sorting: selecting only what is needed | ✗ |
| Data Structuring: Fixing any errors or missing values | ✗ |
| Cleaning: merging disparate data sources | ✗ |

**Answer:** Normalizing: Converting data to common units

[ENRICHED: added specificity — The correct mapping of transformation types to their descriptions from the enriched lesson: **Normalizing** = converting data to common units (e.g., converting all currencies to USD, all timestamps to UTC, all measurements to metric). **Sorting** = ordering data to improve search performance (NOT "selecting only what is needed" — that is Filtering). **Data Structuring** = converting one data format to another (e.g., JSON to database tables) (NOT "fixing errors or missing values" — that is Cleaning). **Cleaning** = fixing errors or missing values (NOT "merging disparate data sources" — that is Joining). The quiz deliberately swaps the definitions to test whether you can distinguish between similar-sounding transformations.]

## Question 9

**Which of these is NOT an example of a system in the data load phase?**

| Option | Correct? |
|--------|----------|
| A data warehouse | ✗ |
| **A scanned medical document** | **✓ CORRECT** |
| A comma separated file | ✗ |
| An Excel spreadsheet | ✗ |

**Answer:** A scanned medical document

[ENRICHED: added specificity — A scanned medical document is a **source** in the **Extraction** phase, not a target in the Loading phase. The enriched lesson lists it explicitly: "the data may be completely raw, such as sensor data from IoT devices, or perhaps it is unstructured data from scanned medical documents or company emails." Scanned documents are unstructured data that require OCR (Optical Character Recognition) to extract text before they can be loaded into a structured system. The other three options are all valid **load targets** (destinations for transformed data): **Data warehouse** — centralized analytical repository (Snowflake, BigQuery, Redshift). **CSV file** — simple text format for data exchange. **Excel spreadsheet** — tabular data file for business users. The enriched lesson's Load section explicitly lists: "The system can be as simple as a comma-separated file, which is essentially just a table of data like an Excel spreadsheet. The target can also be a database, which may be part of a much more elaborate system, such as a data warehouse."]

## Question 10

**ETL jobs can be run on a schedule using _____.**

| Option | Correct? |
|--------|----------|
| shebang | ✗ |
| loadstat | ✗ |
| getstat | ✗ |
| **crontab** | **✓ CORRECT** |

**Answer:** crontab

[ENRICHED: defined "crontab" — Cron is a time-based job scheduler in Unix-like operating systems. `crontab` (cron table) is a configuration file that defines scheduled commands. `crontab -e` opens the current user's crontab in an editor. The cron expression format uses five fields: minute (0-59), hour (0-23), day of month (1-31), month (1-12), day of week (0-7). Example: `* * * * * /path/to/Temperature_ETL.sh` runs the script every minute. Common patterns: `0 * * * *` (every hour), `0 9 * * 1-5` (weekdays at 9 AM), `*/5 * * * *` (every 5 minutes). `shebang` (`#!`) is the interpreter directive at the top of a script — it identifies which shell to use, not how to schedule execution. `getstat` and `loadstat` are functions from the temperature ETL video (not scheduling tools). For more complex scheduling needs (dependencies, retries, monitoring), Apache Airflow replaces raw cron.]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Question 1 | Added specificity | Corrected 3 false statements about Airflow: open-source not commercial, Python+Bash operators, code-defined DAGs | HIGH |
| 2 | Question 2 | Added specificity | Explained ETL acronym order and positioned each stage's sub-processes | HIGH |
| 3 | Question 3 | Added specificity | Mapped 3 batch trigger types (size/event/on-demand) and corrected distortions in wrong answers | HIGH |
| 4 | Question 4 | Definition | Defined shebang (#!) with common variants and explained why other options are incorrect | HIGH |
| 5 | Question 5 | Added specificity | Verified each tool is commercial and ETL (not ELT), listed open-source alternatives | HIGH |
| 6 | Question 6 | Definition | Defined siloed systems with concrete manufacturing company example from enriched lesson | HIGH |
| 7 | Question 7 | Added specificity | Corrected 3 distortions: smaller packets not large, batch not real-time, parallelizing not anonymizing | HIGH |
| 8 | Question 8 | Added specificity | Correctly mapped all 4 transformation types to their definitions, showed how quiz swaps them | HIGH |
| 9 | Question 9 | Added specificity | Classified scanned documents as extraction source, validated other 3 as load targets | HIGH |
| 10 | Question 10 | Definition | Defined crontab with expression format, common patterns, and comparison to shebang/loadstat/getstat | HIGH |

<!-- EXTRACTION_CHECKLIST: 30 sentences extracted, 30 sentences in output -->
