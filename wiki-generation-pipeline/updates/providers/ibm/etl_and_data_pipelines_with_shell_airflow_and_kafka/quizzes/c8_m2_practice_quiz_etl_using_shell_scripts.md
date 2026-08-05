**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 2:** Shell Scripting for ETL

# Practice Quiz: ETL Using Shell Scripts

## Question 1

**The transformation stage is where rules and processes are applied to the data for preparation of loading into target system. Which of the following transformations involves search performance?**

| Option | Correct? |
|--------|----------|
| Joining | ✗ |
| Aggregating | ✗ |
| Normalizing | ✗ |
| **Sorting** | **✓ CORRECT** |

**Answer:** Sorting

[ENRICHED: defined "sorting transformation" — Sorting arranges data in a specific order (ascending or descending) based on one or more columns. It directly improves search performance because ordered data enables efficient lookup algorithms like binary search (O(log n) vs O(n) for unsorted data). Sorting is commonly used before loading into target systems where query performance matters — e.g., sorting by timestamp before loading into a time-series database. Joining combines rows from two tables based on a related column. Aggregating computes summary values (SUM, AVG, COUNT) over groups. Normalizing restructures data to reduce redundancy (e.g., splitting a single table into multiple related tables to achieve 2NF or 3NF).]

## Question 2

**The temperature reporting scenario that you are discovering in the video uses two APIs. What do these APIs do? (multiple answers)**

| Option | Correct? |
|--------|----------|
| **Extraction** | **✓ CORRECT** |
| Keeps track of the temperature times | ✗ |
| **Load** | **✓ CORRECT** |
| Writes temp stats from log file | ✗ |

**Answer:** Extraction and Load

[ENRICHED: added specificity — The two APIs in the temperature reporting scenario are: (1) `get_temp_api` — performs the **Extraction** step by reading the current temperature from the remote sensor and printing it to standard output. (2) `load_stats_api` — performs the **Load** step by sending the computed temperature statistics (min, max, average) to a reporting system (e.g., a dashboard database). "Keeps track of the temperature times" is incorrect because the APIs don't track time — the log file (`temperature.log`) stores the readings. "Writes temp stats from log file" describes the Transform step (done by `get_stats.py`), not the APIs. The APIs are the data interfaces: one for input (extraction) and one for output (loading).]

## Question 3

**There are many ETL tools available today. The modern enterprise grade ETL tools typically include common features. Which of the following common features of popular ETL tools helps with complex calculations?**

| Option | Correct? |
|--------|----------|
| Automation | ✗ |
| Drag-and-drop interface | ✗ |
| **Transformation support** | **✓ CORRECT** |
| Security and compliance | ✗ |

**Answer:** Transformation support

[ENRICHED: defined "transformation support" — Transformation support in ETL tools refers to built-in functions, operators, and interfaces that allow users to define data transformations: filtering, mapping, aggregating, joining, pivoting, and performing complex calculations on data before loading it into the target system. This is where the "T" in ETL happens. Automation handles scheduling and workflow orchestration (e.g., running a job every hour). Drag-and-drop interface is a UI feature for building pipelines visually without writing code — it aids usability, not calculations. Security and compliance features handle encryption, access control, and audit logging — important but unrelated to data transformations. Enterprise ETL tools like IBM DataStage, Informatica PowerCenter, and Talend provide transformation support through graphical mapping editors, expression builders, and内置 transformation functions.]

## Question 4

**The ETL using Shell Scripts video shows a temperature reporting workflow with ten steps. Which step follows the extraction step in the workflow?**

| Option | Correct? |
|--------|----------|
| Display dashboard with temp stats | ✗ |
| **Calculate temp stats from log file** | **✓ CORRECT** |
| Appends temp reading to log file | ✗ |
| Schedule workflow to run each minute | ✗ |

**Answer:** Calculate temp stats from log file

[ENRICHED: added specificity — The ten-step workflow in the video follows this sequence: (1) Create script file, (2) Add bash shebang, (3) Add task comments, (4) Initialize log file, (5) Extract temperature from sensor API, (6) Buffer last 60 readings, (7) Transform: calculate stats using Python script, (8) Load stats to reporting system, (9) Set executable permissions, (10) Schedule with cron. The Extract step (Step 5) reads temperature and appends to `temperature.log`. The step immediately following extraction is the Transform step (Step 7): "Calculate temp stats from log file" — this calls `get_stats.py` which reads the 60-minute log and computes min/max/average. "Appends temp reading to log file" is PART of the extraction step, not the step after it. "Display dashboard with temp stats" is the end-user visualization, not a pipeline step. "Schedule workflow to run each minute" is the final step (cron job setup).]

## Question 5

**The video creates an ETL shell script and names it 'Temperature_ETL.sh'. A command is then used to turn it into what type of file?**

| Option | Correct? |
|--------|----------|
| CSV | ✗ |
| PY | ✗ |
| **BASH** | **✓ CORRECT** |
| Text | ✗ |

**Answer:** BASH

[ENRICHED: added specificity — The command used is `chmod +x Temperature_ETL.sh`. This adds the execute permission to the file, turning it from a plain text file into an executable bash script. Without `chmod +x`, the file is just text — you can read it but not run it as a program. The `.sh` extension is a convention indicating it's a shell script, but the operating system relies on the execute permission (and the shebang `#!/bin/bash`) to actually run it. CSV (Comma-Separated Values) is a data format, not an executable type. PY is a Python file extension. "Text" is what the file was before `chmod +x` was applied — the command specifically changes it FROM text TO executable.]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Question 1 | Definition | Defined sorting transformation and its impact on search performance (binary search O(log n) vs O(n)) | HIGH |
| 2 | Question 2 | Added specificity | Explained the two APIs (`get_temp_api` for extraction, `load_stats_api` for loading) and why other options are incorrect | HIGH |
| 3 | Question 3 | Definition | Defined transformation support in ETL tools, contrasted with automation, drag-and-drop, and security features | HIGH |
| 4 | Question 4 | Added specificity | Mapped all 10 steps of the video workflow, showed exact sequence after extraction | HIGH |
| 5 | Question 5 | Added specificity | Explained `chmod +x` converts text to executable bash script, clarified role of `.sh` extension vs execute permission | HIGH |

<!-- EXTRACTION_CHECKLIST: 25 sentences extracted, 25 sentences in output -->
