**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 2:** Shell Scripting for ETL

# Linux Commands and Shell Scripting

## What is a Shell?

A shell is a powerful user interface for Unix-like operating systems. It can interpret commands and run other programs. It also enables access to files, utilities, and applications, and is an interactive scripting language. Additionally, you can use a shell to automate tasks.

[ENRICHED: defined "shell" — a command-line interpreter that sits between you and the operating system kernel. You type commands into the shell (e.g., `ls`, `grep`, `awk`), and the shell translates them into system calls the kernel understands. The most common shells are Bash (Bourne Again Shell, the default on most Linux distributions), Zsh (Z Shell, the default on macOS), and PowerShell (Windows). In data engineering, Bash is the dominant shell for ETL scripting because Linux servers are the standard deployment environment for data pipelines.] [ENRICHED: defined "Unix-like operating systems" — operating systems that behave similarly to Unix, including Linux (Ubuntu, CentOS, Red Hat), macOS, and FreeBSD. Most data engineering infrastructure runs on Linux — cloud servers (AWS EC2, Google Compute Engine), containers (Docker, Kubernetes), and data platforms (Hadoop, Spark clusters) all use Linux. This is why shell scripting is a foundational skill for data engineers.]

[ENRICHED: ecosystem — the shell is the oldest and most universal interface in computing. While modern data engineering uses higher-level tools (Airflow, Spark, dbt), the shell remains the glue that connects them. A typical data pipeline might: (1) use a shell script to download a file from an API, (2) use `awk`/`sed` to clean it, (3) use `psql` to load it into PostgreSQL, and (4) use `cron` to schedule the whole thing daily. Learning the shell is not optional — it is the foundation everything else builds on.]

## Shell Capabilities

Linux shell commands are used for navigating and working with files and directories. You can also use them for file compression and archiving.

[ENRICHED: concrete example — common shell operations in data engineering:]

| Operation | Shell Command | Data Engineering Use Case |
|---|---|---|
| Navigate directories | `cd`, `ls`, `pwd` | Find where your data files and scripts are stored |
| View files | `cat`, `head`, `tail`, `less` | Preview the first/last rows of a CSV before loading |
| Search content | `grep` | Find all error lines in a log file: `grep "ERROR" pipeline.log` |
| Transform text | `awk`, `sed`, `cut` | Extract specific columns from a CSV: `awk -F',' '{print $1,$3}' data.csv` |
| Count lines | `wc -l` | Check how many records were processed: `wc -l orders.csv` |
| Compress files | `gzip`, `tar` | Archive 10 GB of raw data into a 1 GB compressed file for storage |
| Download data | `curl`, `wget` | Fetch data from an API: `curl -o data.json https://api.example.com/records` |
| Schedule jobs | `cron` | Run a pipeline every night at 2 AM automatically |

## What This Lesson Covers

In this lesson, you will learn about how shell scripting can be used to implement an ETL pipeline, and how ETL scripts or tasks can be scheduled.

[ENRICHED: added specificity — "shell scripting for ETL" means using Bash scripts to automate the three ETL stages:]

```
EXTRACT (shell):
  curl -o raw_data.csv https://api.example.com/sales
  # Downloads raw data from an API into a local file

TRANSFORM (shell):
  awk -F',' 'NR>1 {print $1","$3","$5}' raw_data.csv > cleaned.csv
  # Extracts columns 1, 3, and 5 from the CSV, skipping the header

LOAD (shell):
  psql -c "\copy orders FROM 'cleaned.csv' CSV HEADER" my_database
  # Loads the cleaned CSV into a PostgreSQL table
```

This entire sequence can be written as a single `.sh` file and scheduled to run daily using `cron`:

```bash
#!/bin/bash
# daily_etl.sh — runs every night at 2 AM

# Extract
curl -o /data/raw/sales_$(date +%Y%m%d).csv https://api.example.com/sales

# Transform
awk -F',' 'NR>1 {print $1","$3","$5}' /data/raw/sales_*.csv > /data/cleaned/sales_cleaned.csv

# Load
psql -c "\copy orders FROM '/data/cleaned/sales_cleaned.csv' CSV HEADER" my_database

echo "ETL completed at $(date)" >> /var/log/etl.log
```

## Prerequisite: Linux Commands and Shell Scripting

If you are not familiar with Linux commands and shell scripting yet, do enjoy the course 'Hands-on Introduction to Linux Commands and Shell Scripting' before diving into this lesson (ETL using Shell Scripting). In the Hands-on Introduction to Linux Commands and Shell Scripting, you will learn about:

- The characteristics of Linux commands and shell scripting
- The different Linux commands and their outputs
- How to schedule jobs using crontab
- How to work with filters, pipes, and variables

[ENRICHED: defined "crontab" — a configuration file that defines scheduled tasks in Unix-like systems. Each line specifies a command and when to run it. Example: `0 2 * * * /home/user/daily_etl.sh` means "run the ETL script at 2:00 AM every day." The format is: `minute hour day-of-month month day-of-week command`. Crontab is the simplest job scheduler in Linux — for more complex pipelines with dependencies (Task B must finish before Task C starts), you would use Apache Airflow, which is covered in Module 3.] [ENRICHED: defined "filters, pipes, and variables" — **filters** are commands that process text line-by-line (e.g., `grep` selects lines matching a pattern, `awk` extracts columns, `sed` finds and replaces text). **Pipes** (`|`) chain commands together: the output of one command becomes the input of the next. Example: `cat sales.csv | grep "2024" | awk -F',' '{print $5}'` means "read the CSV, keep only 2024 rows, extract column 5." **Variables** store values for reuse: `FILE=sales.csv; wc -l $FILE` counts lines in that file. Together, these three concepts form the core of shell-based data processing.]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | What is a Shell paragraph | Definition | Defined "shell" as command-line interpreter with Bash/Zsh/PowerShell examples | HIGH |
| 2 | What is a Shell paragraph | Ecosystem | Connected shell to data engineering infrastructure (Linux servers, containers, Hadoop/Spark) | HIGH |
| 3 | What is a Shell paragraph | Ecosystem | Showed shell as the glue connecting API download→awk clean→psql load→cron schedule | HIGH |
| 4 | Shell capabilities section | Concrete example | 8-row table mapping shell operations to data engineering use cases | HIGH |
| 5 | ETL lesson paragraph | Concrete example | 3-stage shell ETL: curl extract→awk transform→psql load, with cron scheduling | HIGH |
| 6 | ETL lesson paragraph | Concrete example | Full bash script example with extract/transform/load and timestamp logging | HIGH |
| 7 | Crontab definition | Defined crontab with format explanation and Airflow comparison | HIGH |
| 8 | Filters/pipes/variables definition | Defined grep, awk, sed as filters; pipe `|` as command chaining; variables as value storage | HIGH |

<!-- EXTRACTION_CHECKLIST: 9 sentences extracted, 9 sentences in output -->
