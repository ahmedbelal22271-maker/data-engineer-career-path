# Lab: Create a DAG for Apache Airflow with BashOperator

**Course 8:** ETL & Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines
**Lab Type:** Hands-on Exercise

---

## Introduction

In this lab, you will create workflows using BashOperator in Airflow DAGs and simulate an ETL process using bash commands that are scheduled to run once a day.

### Objectives

After completing this lab, you will be able to:

1. Explore the Airflow Web UI
2. Create a DAG with BashOperator
3. Submit a DAG and run it through Web UI

### Prerequisites

Please ensure that you have completed the reading on the Airflow DAG Operators before proceeding with this lab. It is highly recommended that you are familiar with bash commands to do this lab.

[ENRICHED: added specificity — **BashOperator** is an Airflow operator that executes a shell command on the local machine (or the Airflow worker node). Unlike `PythonOperator` (which runs Python functions in-process), `BashOperator` spawns a subprocess to run the command. This makes it ideal for: (1) wrapping existing shell scripts, (2) running CLI tools (`curl`, `cut`, `tr`, `zip`), (3) executing system commands (`mkdir`, `cp`, `rm`). The tradeoff: BashOperator tasks can't easily pass data to downstream tasks (they write to files instead of returning Python objects), and debugging requires reading subprocess stdout/stderr logs rather than Python stack traces.]

[ENRICHED: added specificity — **BashOperator vs PythonOperator comparison:**

| Feature | BashOperator | PythonOperator |
|---------|-------------|----------------|
| Execution | Subprocess (shell) | In-process (Python) |
| Input | `bash_command` string | `python_callable` function ref |
| Data passing | Files on disk | XCom (Airflow's inter-task messaging) |
| Error handling | Exit code (0 = success) | Python exceptions |
| Dependencies | System packages (curl, cut, etc.) | Python packages (requests, pandas, etc.) |
| Use case | Wrapping existing scripts, CLI tools | Complex logic, API calls, data processing |

Choose BashOperator when: your task is a simple shell command, you're wrapping an existing bash script, or you need system-level operations (file management, compression, downloads). Choose PythonOperator when: your task involves data transformations, API calls, database queries, or any logic that benefits from Python's ecosystem.]

---

## Skills Network Cloud IDE

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands-on labs for course and project-related labs. Theia is an open-source IDE (Integrated Development Environment) that can be run on a desktop or on the cloud. To complete this lab, you will be using the Cloud IDE based on Theia, running in a Docker container.

## Important Notice About This Lab Environment

Please be aware that sessions for this lab environment are not persistent. A new environment is created for you every time you connect to this lab. Any data you may have saved in an earlier session will get lost. To avoid losing your data, please plan to complete these labs in a single session.

---

## Exercise 1: Start Apache Airflow

1. Click on **Skills Network Toolbox**.
2. From the **BIG DATA** section, click **Apache Airflow**.
3. Click **Create** to start the Apache Airflow.

> **Note:** Please be patient, it will take a few minutes for Airflow to start.

## Exercise 2: Open the Airflow Web UI

When Airflow starts successfully, you should see an output similar to the one below. Once Apache Airflow has started, click on the highlighted icon to open Apache Airflow Web UI in the new window.

You should land on a page that looks like this.

---

## Exercise 3: Create a DAG

Let's create a DAG that runs daily, and extracts user information from `/etc/passwd` file, transforms it, and loads it into a file.

This DAG will have two tasks: `extract` that extracts fields from `/etc/passwd` file and `transform_and_load` that transforms and loads data into a file.

```python
# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'your_name_here',
    'start_date': days_ago(0),
    'email': ['your_email_here'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'my-first-dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(days=1),
)

# define the tasks

# define the first task

extract = BashOperator(
    task_id='extract',
    bash_command='cut -d":" -f1,3,6 /etc/passwd > /home/project/airflow/dags/extracted-data.txt',
    dag=dag,
)

# define the second task
transform_and_load = BashOperator(
    task_id='transform',
    bash_command='tr ":" "," < /home/project/airflow/dags/extracted-data.txt > /home/project/airflow/dags/transformed-data.csv',
    dag=dag,
)

# task pipeline
extract >> transform_and_load
```

[ENRICHED: added specificity — **`cut` command**: the `cut` utility extracts columns from a text file. The flags used here:
- `-d":"` — set the delimiter to `:` (by default `cut` uses TAB)
- `-f1,3,6` — extract fields 1, 3, and 6 (1-indexed)

For a line like `root:x:0:0:root:/root:/bin/bash`, `cut -d":" -f1,3,6` produces `root:0:/root` — username, UID, and home directory. This is equivalent to the Python `split(':')` approach used in the PythonOperator lab, but expressed as a single shell command.]

[ENRICHED: added specificity — **`tr` command**: the `tr` (translate) utility performs character-by-character substitution. The flags used here:
- `":" ","` — replace every `:` with `,`

For a line like `root:0:/root`, `tr ":" ","` produces `root,0,/root` — converting colon-delimited to comma-delimited (CSV). This is equivalent to Python's `line.replace(':', ',')` but expressed as a shell command.

**Other common `tr` uses:**
- `tr "a-z" "A-Z"` — convert lowercase to uppercase
- `tr -d "\n"` — delete newline characters
- `tr -s " "` — squeeze multiple spaces into one]

[ENRICHED: added specificity — **BashOperator command structure**: the `bash_command` parameter accepts any valid bash command. In this lab, both tasks use output redirection (`>`) to write results to files. This is the standard pattern for BashOperator: the command does its work and writes output to a file, which downstream tasks can read. The Airflow scheduler captures stdout and stderr from the subprocess and stores them in the task log — accessible via the Web UI's Grid view.]

Create a new file by choosing **File->New File** and naming it `my_first_dag.py`. Then, copy the code above and paste it into `my_first_dag.py`.

---

## Exercise 4: Submit a DAG

Submitting a DAG is as simple as copying the DAG Python file into the `dags` folder in the `AIRFLOW_HOME` directory.

Airflow searches for Python source files within the specified `DAGS_FOLDER`. The location of `DAGS_FOLDER` can be located in the `airflow.cfg` file, where it has been configured as `/home/project/airflow/dags`.

Airflow will load the Python source files from this designated location. It will process each file, execute its contents, and subsequently load any DAG objects present in the file.

Therefore, when submitting a DAG, it is essential to position it within this directory structure. Alternatively, the `AIRFLOW_HOME` directory, representing the structure `/home/project/airflow`, can also be utilized for DAG submission.

[ENRICHED: added specificity — **DAG submission mechanism explained**:
1. Airflow's scheduler scans the `DAGS_FOLDER` (configured in `airflow.cfg` as `dags_folder = /home/project/airflow/dags`)
2. The scan runs every `min_file_process_interval` seconds (default: 30 seconds)
3. For each `.py` file found, Airflow imports it as a Python module
4. During import, all top-level code executes — including any `with DAG(...)` context managers
5. DAG objects are registered in the metadata database
6. The scheduler then monitors these DAGs for scheduled runs

**What happens if you put the file in the wrong place?** If the file is outside `DAGS_FOLDER`, the scheduler never sees it. If the file has syntax errors, it won't import — use `airflow dags list-import-errors` to see what went wrong. If the file imports but contains no DAG objects, nothing is registered.]

1. Open a terminal and run the command below to set the `AIRFLOW_HOME`.

```php
export AIRFLOW_HOME=/home/project/airflow
echo $AIRFLOW_HOME
```

2. Run the command below to submit the DAG that was created in the previous exercise.

```bash
export AIRFLOW_HOME=/home/project/airflow
cp my_first_dag.py $AIRFLOW_HOME/dags
```

3. Verify that your DAG actually got submitted.

4. Run the command below to list out all the existing DAGs.

```plaintext
airflow dags list
```

5. Verify that `my-first-dag` is a part of the output.

```plaintext
airflow dags list|grep "my-first-dag"
```

You should see your DAG name in the output.

6. Run the command below to list out all the tasks in `my-first-dag`.

```plaintext
airflow tasks list my-first-dag
```

You should see 2 tasks in the output.

[ENRICHED: added specificity — **`airflow tasks list <dag_id>` output** for `my-first-dag`:
```
extract
transform
```
These are the two task IDs defined in the DAG. The output confirms that Airflow parsed the file correctly and registered both tasks. If you see fewer tasks than expected, check for syntax errors in the DAG file. If you see no tasks, the DAG may not have loaded — use `airflow dags list` first to confirm the DAG exists.]

---

## Practice Exercise

Write a DAG named `ETL_Server_Access_Log_Processing.py`.

### Tasks

1. Create the imports block.
2. Create the DAG Arguments block. You can use the default settings.
3. Create the DAG definition block. The DAG should run daily.
4. Create the download task. The download task must download the server access log file, which is available at the URL: `https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt`
5. Create the extract task.
6. Create the transform task. The transform task must capitalize the visitorid.
7. Create the load task. The load task must compress the extracted and transformed data.
8. Create the task pipeline block. The pipeline block should schedule the task in the order listed below: download → extract → transform → load
9. Submit the DAG.
10. Verify if the DAG is submitted.

Follow the example Python code given in the lab and make necessary changes to create the new DAG.

### Server Access Log Fields

| Field | Type |
|-------|------|
| timestamp | TIMESTAMP |
| latitude | float |
| longitude | float |
| visitorid | char(37) |
| accessed_from_mobile | boolean |
| browser_code | int |

Add to the file the following parts of code to `ETL_Server_Access_Log_Processing.py` to complete the tasks given in the problem.

```python
# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'your_name',
    'start_date': days_ago(0),
    'email': ['your email'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'ETL_Server_Access_Log_Processing',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(days=1),
)

# define the tasks

# define the task 'download'

download = BashOperator(
    task_id='download',
    bash_command='curl "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt" -o web-server-access-log.txt',
    dag=dag,
)

# define the task 'extract'

extract = BashOperator(
    task_id='extract',
    bash_command='cut -f1,4 -d"#" web-server-access-log.txt > /home/project/airflow/dags/extracted.txt',
    dag=dag,
)


# define the task 'transform'

transform = BashOperator(
    task_id='transform',
    bash_command='tr "[a-z]" "[A-Z]" < /home/project/airflow/dags/extracted.txt > /home/project/airflow/dags/capitalized.txt',
    dag=dag,
)

# define the task 'load'

load = BashOperator(
    task_id='load',
    bash_command='zip log.zip capitalized.txt' ,
    dag=dag,
)

# task pipeline

download >> extract >> transform >> load
```

[ENRICHED: added specificity — **`curl` command**: the `curl` utility transfers data from URLs. The flags used here:
- `-o web-server-access-log.txt` — write output to a local file instead of stdout

Other common `curl` flags: `-s` (silent, no progress bar), `-f` (fail on HTTP errors), `-L` (follow redirects). In production Airflow DAGs, you'd typically use `HttpSensor` or `S3KeySensor` to wait for data availability before downloading, rather than hardcoding URLs.]

[ENRICHED: added specificity — **`cut -f1,4 -d"#"`**: extracts fields 1 and 4 from the `#`-delimited access log. For a line like `1234567890#40.7128#-74.0060#abc123#true#1`, `cut -f1,4 -d"#"` produces `1234567890#abc123` — timestamp and visitorid. The `#` delimiter was chosen because the access log uses `#` as its field separator (unlike the `/etc/passwd` file which uses `:`).]

[ENRICHED: added specificity — **`tr "[a-z]" "[A-Z]"`**: converts all lowercase letters to uppercase. This capitalizes the visitorid field. The `[a-z]` and `[A-Z]` are character ranges — `tr` maps each character in the first range to the corresponding character in the second range. This is equivalent to Python's `line.upper()` but expressed as a shell command. Note: `tr` operates on ALL characters in the input, not just the visitorid field — so the timestamp is also uppercased (though digits and special characters are unaffected).]

[ENRICHED: added specificity — **`zip log.zip capitalized.txt`**: compresses `capitalized.txt` into `zip` archive `log.zip`. The `zip` command combines compression and archiving in one step. In production, you might use `gzip` (single file compression, `.gz` extension) or `tar` (archiving multiple files). The choice depends on downstream consumers — if the load target is S3, you might skip compression entirely and upload the raw file.]

[ENRICHED: added specificity — **practice exercise task pipeline**: `download >> extract >> transform >> load` — four sequential tasks:
1. `download` — fetches the access log from S3 using `curl`
2. `extract` — extracts fields 1 (timestamp) and 4 (visitorid) using `cut`
3. `transform` — capitalizes all text using `tr`
4. `load` — compresses the result into `log.zip` using `zip`

This is a classic ETL pattern implemented entirely with shell commands. The same 4-step pipeline (acquire → parse → enrich → store) applies to real-world data engineering, just with different tools (Python scripts, SQL queries, API calls) and destinations (data warehouses, data lakes, streaming platforms).]

Submit the DAG by running the following command.

```plaintext
cp  ETL_Server_Access_Log_Processing.py $AIRFLOW_HOME/dags
```

Verify if the DAG is submitted on the Web UI or the CLI using the below command.

```plaintext
airflow dags list
```

**Authors:** Lavanya T S, Ramesh Sannareddy
© IBM Corporation. All rights reserved.

The content of this lab is licensed under Apache 2.0

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Introduction | Definition | Defined BashOperator — executes shell commands via subprocess, when to use vs PythonOperator | HIGH |
| 2 | Introduction | Comparison | BashOperator vs PythonOperator comparison table (execution, input, data passing, error handling, dependencies, use case) | HIGH |
| 3 | Exercise 3 | Specificity | `cut` command — `-d` delimiter flag, `-f` field selection, example with `/etc/passwd` | HIGH |
| 4 | Exercise 3 | Specificity | `tr` command — character translation, `":" ","` replacement, common uses table | HIGH |
| 5 | Exercise 3 | Specificity | BashOperator command structure — `bash_command` param, output redirection pattern, stdout/stderr logging | HIGH |
| 6 | Exercise 4 | Specificity | DAG submission mechanism — `DAGS_FOLDER` in `airflow.cfg`, scan interval, import process, metadata registration | HIGH |
| 7 | Exercise 4 | Specificity | `airflow tasks list` output — expected 2 tasks (extract, transform), verification step | HIGH |
| 8 | Practice | Specificity | `curl` command — `-o` flag for file output, common flags (`-s`, `-f`, `-L`), production alternatives (HttpSensor) | HIGH |
| 9 | Practice | Specificity | `cut -f1,4 -d"#"` — extracting timestamp and visitorid from `#`-delimited log | HIGH |
| 10 | Practice | Specificity | `tr "[a-z]" "[A-Z]"` — uppercase conversion, operates on ALL characters (not just visitorid) | HIGH |
| 11 | Practice | Specificity | `zip log.zip capitalized.txt` — compression, comparison to `gzip`/`tar`, downstream considerations | HIGH |
| 12 | Practice | Specificity | 4-task ETL pipeline breakdown — download→extract→transform→load, classic acquire→parse→enrich→store pattern | HIGH |

---

<!-- EXTRACTION_CHECKLIST: 43 sentences extracted, 43 sentences in output -->
