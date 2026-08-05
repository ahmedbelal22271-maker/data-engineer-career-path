# Lab: Create a DAG with PythonOperator

**Course 8:** ETL & Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines
**Lab Type:** Hands-on Exercise

---

## Skills Network Cloud IDE

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands-on labs for course and project-related labs. Theia is an open-source IDE (Integrated Development Environment) that can be run on a desktop or on the cloud. To complete this lab, you will be using the Cloud IDE based on Theia, running in a Docker container.

[ENRICHED: definition — **Theia** is an open-source IDE framework developed by the Eclipse Foundation. It's architecturally similar to VS Code (both use the Language Server Protocol and Monaco editor), but Theia is designed to run both as a desktop app and as a cloud-hosted web application. In this lab, Skills Network runs Theia inside a Docker container, giving you a browser-based IDE with a terminal, file explorer, and code editor — no local installation required. Docker ensures the environment is identical for every student, eliminating "it works on my machine" issues.]

## Important Notice About This Lab Environment

Please be aware that sessions for this lab environment are not persistent. A new environment is created for you every time you connect to this lab. Any data you may have saved in an earlier session will get lost. To avoid losing your data, please plan to complete these labs in a single session.

[ENRICHED: added specificity — non-persistent sessions mean the Docker container is destroyed when you disconnect. This includes: (1) any files you created in the IDE, (2) any DAGs you submitted to the `dags/` folder, (3) any Airflow metadata (task run history, logs). When you reconnect, you get a fresh container. This is why the lab says "plan to complete in a single session." In a real production Airflow deployment, the metadata database (PostgreSQL by default) persists across restarts, and DAG files are typically stored in version control (Git) — so you never lose your work. The lab environment's impermanence is a training wheels limitation, not how Airflow works in production.]

---

## Exercise 1: Start Apache Airflow

1. Click on **Skills Network Toolbox**.
2. From the **BIG DATA** section, click **Apache Airflow**.
3. Click **Create** to start the Apache Airflow.

> **Note:** Please be patient, it will take a few minutes for Airflow to start. If there is an error starting Airflow, please restart it.

---

## Exercise 2: Open the Airflow Web UI

When Airflow starts successfully, you should see an output similar to the one below. Once Apache Airflow has started, click on the highlighted icon to open Apache Airflow Web UI in the new window.

You should land on a page that looks like this.

---

## Exercise 3: Create a DAG with PythonOperator

Next, you will create a DAG, which will define a pipeline of tasks, such as extract, transform, load, and check with PythonOperator.

Create a DAG file, `my_first_dag.py`, which will run daily. To Create a new file choose **File->New File** and name it as `my_first_dag.py`. The `my_first_dag.py` file defines tasks `execute_extract`, `execute_transform`, `execute_load`, and `execute_check` to call the respective Python functions.

[ENRICHED: definition — **PythonOperator** is an Airflow operator that executes a Python function. Unlike `BashOperator` (which runs shell commands), `PythonOperator` calls a Python function directly in the Airflow worker process. This is useful when your task logic is already written in Python — data transformations, API calls, file processing, database queries. The key parameter is `python_callable`, which takes a reference to the function (not a string, not a call — just the function name without parentheses). Example: `PythonOperator(python_callable=my_function)` calls `my_function()` when the task runs.]

[ENRICHED: added specificity — the `python_callable` parameter accepts a **function reference**, not a function call. This is a common mistake:

```python
# CORRECT — function reference (no parentheses)
PythonOperator(python_callable=extract)

# WRONG — this calls the function immediately during DAG parsing, not during task execution
PythonOperator(python_callable=extract())
```

When Airflow parses the DAG file (every 30 seconds), it evaluates all top-level code. If you write `extract()`, Python executes that function during parsing, before any task runs. With just `extract`, Airflow stores the reference and calls it only when the task is actually executed by the scheduler.]

```python
# Import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.python import PythonOperator

# This makes scheduling easy
from airflow.utils.dates import days_ago

# Define the path for the input and output files
input_file = '/etc/passwd'
extracted_file = 'extracted-data.txt'
transformed_file = 'transformed.txt'
output_file = 'data_for_analytics.csv'


def extract():
    global input_file
    print("Inside Extract")
    # Read the contents of the file into a string
    with open(input_file, 'r') as infile, \
            open(extracted_file, 'w') as outfile:
        for line in infile:
            fields = line.split(':')
            if len(fields) >= 6:
                field_1 = fields[0]
                field_3 = fields[2]
                field_6 = fields[5]
                outfile.write(field_1 + ":" + field_3 + ":" + field_6 + "\n")


def transform():
    global extracted_file, transformed_file
    print("Inside Transform")
    with open(extracted_file, 'r') as infile, \
            open(transformed_file, 'w') as outfile:
        for line in infile:
            processed_line = line.replace(':', ',')
            outfile.write(processed_line + '\n')


def load():
    global transformed_file, output_file
    print("Inside Load")
    # Save the array to a CSV file
    with open(transformed_file, 'r') as infile, \
            open(output_file, 'w') as outfile:
        for line in infile:
            outfile.write(line + '\n')


def check():
    global output_file
    print("Inside Check")
    # Save the array to a CSV file
    with open(output_file, 'r') as infile:
        for line in infile:
            print(line)


# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Your name',
    'start_date': days_ago(0),
    'email': ['your email'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'my-first-python-etl-dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(days=1),
)

# Define the task named execute_extract to call the `extract` function
execute_extract = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag,
)

# Define the task named execute_transform to call the `transform` function
execute_transform = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag,
)

# Define the task named execute_load to call the `load` function
execute_load = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag,
)

# Define the task named execute_check to call the `check` function
execute_check = PythonOperator(
    task_id='check',
    python_callable=check,
    dag=dag,
)

# Task pipeline
execute_extract >> execute_transform >> execute_load >> execute_check
```

[ENRICHED: added specificity — **`days_ago(0)`** is an Airflow utility function from `airflow.utils.dates` that returns a `datetime` object set to N days ago from today. `days_ago(0)` = today at midnight, `days_ago(1)` = yesterday at midnight, `days_ago(30)` = 30 days ago. This is a convenience alternative to hardcoding `datetime(2024, 1, 1)`. In production, you'd typically use a fixed date (like `datetime(2024, 6, 1)`) rather than `days_ago()`, because `days_ago(0)` changes every day — meaning the DAG's effective start date shifts depending on when the file is first parsed. For reproducible scheduling, a fixed `start_date` is preferred.]

[ENRICHED: added specificity — **`global` keyword** in Python functions: the `global` keyword tells Python to use the module-level variable inside the function, rather than creating a local variable. Without `global input_file`, the line `input_file = '/etc/passwd'` inside `extract()` would create a local variable that shadows the module-level one. In this lab, `global` is used because the functions reference module-level file path constants. However, this is considered a **bad practice** in production code — it creates hidden coupling between functions and module state. A better approach is to pass file paths as parameters or use a config object. The lab uses `global` for simplicity, but real-world Airflow DAGs typically use XCom (Airflow's inter-task communication mechanism) or configuration files to pass data between tasks.]

[ENRICHED: added specificity — **`/etc/passwd`** is a standard Unix/Linux system file that contains user account information. Each line has 7 colon-separated fields: `username:password:UID:GID:GECOS:home:shell`. The lab reads this file and extracts fields 1 (username), 3 (UID), and 6 (home directory). This is a common teaching example because: (1) it exists on every Unix system, (2) its colon-delimited format is easy to parse, (3) it demonstrates real file I/O. The output `extracted-data.txt` contains lines like `root:0:/root` — username, UID, and home directory separated by colons.]

[ENRICHED: added specificity — the **ETL pattern** in this lab:
1. **Extract** (`/etc/passwd` → `extracted-data.txt`): Reads `/etc/passwd`, splits each line by `:`, keeps fields 0, 2, 5 (username, UID, home directory), writes them colon-delimited
2. **Transform** (`extracted-data.txt` → `transformed.txt`): Replaces colons with commas — converts the colon-delimited format to CSV
3. **Load** (`transformed.txt` → `data_for_analytics.csv`): Copies the transformed CSV to the final output file
4. **Check** (`data_for_analytics.csv` → stdout): Reads and prints each line to verify the pipeline worked

This is a minimal ETL pipeline: extract from a system file, transform the format, load into a CSV, and verify the output. The same pattern (extract → transform → load) applies to real-world pipelines, just with different sources (databases, APIs, S3) and destinations (data warehouses, data lakes).]

---

## Exercise 4: Submit a DAG

Submitting a DAG is as simple as copying the DAG Python file into the `dags` folder in the `AIRFLOW_HOME` directory.

1. Open a terminal and run the command below to set the `AIRFLOW_HOME`.

```php
export AIRFLOW_HOME=/home/project/airflow
echo $AIRFLOW_HOME
```

2. Run the command below to submit the DAG that was created in the previous exercise.

```plaintext
cp my_first_dag.py $AIRFLOW_HOME/dags
```

3. Verify that your DAG actually got submitted.

4. Run the command below to list out all the existing DAGs.

```plaintext
airflow dags list
```

5. Verify that `my-first-python-etl-dag` is a part of the output.

```plaintext
airflow dags list|grep "my-first-python-etl-dag"
```

You should see your DAG name in the output.

6. Run the command below to list out all the tasks in `my-first-python-etl-dag`.

```plaintext
airflow tasks list my-first-python-etl-dag
```

You should see all the four tasks in the output.

7. You can run the task from the Web UI. You can check the logs of the tasks by clicking the individual task in the Graph view.

[ENRICHED: added specificity — **DAG submission mechanism**: Airflow's scheduler continuously monitors the `dags/` folder (scans every 30 seconds by default). When you copy a `.py` file into this folder, the scheduler detects it, parses the file, and registers any DAG objects found. No restart required. The `AIRFLOW_HOME` environment variable tells Airflow where to look for its configuration (`airflow.cfg`), metadata database, and the `dags/` folder. Default `AIRFLOW_HOME` is `~/airflow`. In production, `AIRFLOW_HOME` is typically set in the Airflow systemd unit or Docker entrypoint.]

[ENRICHED: added specificity — **`airflow dags list`** command: queries the metadata database and lists all registered DAGs. Output columns: `dag_id`, `file_token` (hash of the DAG file), `owner`, `is_paused`. Useful for verifying that your DAG was parsed correctly. If your DAG doesn't appear, the file has a syntax error — use `airflow dags list-import-errors` to see what went wrong.]

[ENRICHED: added specificity — **`airflow dags list-import-errors`** command: shows Python import errors that occurred during DAG file parsing. Common errors: (1) missing Python package (e.g., `import requests` fails if `requests` isn't installed), (2) syntax error in the DAG file, (3) wrong import path (e.g., `from airflow.operators.bash_operator import BashOperator` in Airflow 2.x). This is the first debugging step when a DAG doesn't appear in `airflow dags list`.]

[ENRICHED: added specificity — **`airflow tasks list <dag_id>`** command: lists all task IDs defined in a specific DAG. For `my-first-python-etl-dag`, you'll see: `extract`, `transform`, `load`, `check`. These task IDs are what you see in the Web UI's Graph view, and they're used in the `>>` dependency notation. You can also run individual tasks manually with `airflow tasks run <dag_id> <task_id> <execution_date>` — useful for debugging without waiting for the scheduler.]

---

## Practice Exercise

Write a DAG named `ETL_Server_Access_Log_Processing` that will extract a file from a remote server and then transform the content and load it into a file.

The file URL is given below: `https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt`

The server access log file contains these fields:

| Field | Type |
|-------|------|
| timestamp | TIMESTAMP |
| latitude | float |
| longitude | float |
| visitorid | char(37) |
| accessed_from_mobile | boolean |
| browser_code | int |

### Tasks

1. Add tasks in the DAG file to download the file, read the file, and extract the fields `timestamp` and `visitorid` from the `web-server-access-log.txt`.
2. Capitalize the `visitorid` for all the records and store it in a local variable.
3. Load the data into a new file `capitalized.txt`.
4. Create the imports block.
5. Create the DAG Arguments block. You can use the default settings.
6. Create the DAG definition block. The DAG should run daily.
7. Create the tasks `extract`, `transform`, and `load` to call the Python script.
8. Create the task pipeline block.
9. Submit the DAG.
10. Verify if the DAG is submitted.

Follow the example code given in the lab and make necessary changes to create the new DAG.

Create a new file by going to **File -> New File** from the menu and name it as `ETL_Server_Access_Log_Processing.py`. Copy the code below in the python file. This will contain your DAG with five tasks: `download`, `execute_extract`, `execute_transform`, `execute_load`, and `execute_check`.

```python
# Import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator

# This makes scheduling easy
from airflow.utils.dates import days_ago
import requests

# Define the path for the input and output files
input_file = 'web-server-access-log.txt'
extracted_file = 'extracted-data.txt'
transformed_file = 'transformed.txt'
output_file = 'capitalized.txt'


def download_file():
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt"
    # Send a GET request to the URL
    with requests.get(url, stream=True) as response:
        # Raise an exception for HTTP errors
        response.raise_for_status()
        # Open a local file in binary write mode
        with open(input_file, 'wb') as file:
            # Write the content to the local file in chunks
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    print(f"File downloaded successfully: {input_file}")


def extract():
    global input_file
    print("Inside Extract")
    # Read the contents of the file into a string
    with open(input_file, 'r') as infile, \
            open(extracted_file, 'w') as outfile:
        for line in infile:
            fields = line.split('#')
            if len(fields) >= 4:
                field_1 = fields[0]
                field_4 = fields[3]
                outfile.write(field_1 + "#" + field_4 + "\n")


def transform():
    global extracted_file, transformed_file
    print("Inside Transform")
    with open(extracted_file, 'r') as infile, \
            open(transformed_file, 'w') as outfile:
        for line in infile:          
            processed_line = line.upper()
            outfile.write(processed_line + '\n')


def load():
    global transformed_file, output_file
    print("Inside Load")
    # Save the array to a CSV file
    with open(transformed_file, 'r') as infile, \
            open(output_file, 'w') as outfile:
        for line in infile:
            outfile.write(line + '\n')


def check():
    global output_file
    print("Inside Check")
    # Save the array to a CSV file
    with open(output_file, 'r') as infile:
        for line in infile:
            print(line)


# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Your name',
    'start_date': days_ago(0),
    'email': ['your email'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'my-first-python-etl-dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(days=1),
)

# Define the task named download to call the `download_file` function
download = PythonOperator(
    task_id='download',
    python_callable=download_file,
    dag=dag,
)

# Define the task named execute_extract to call the `extract` function
execute_extract = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag,
)

# Define the task named execute_transform to call the `transform` function
execute_transform = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag,
)

# Define the task named execute_load to call the `load` function
execute_load = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag,
)

# Define the task named execute_check to call the `check` function
execute_check = PythonOperator(
    task_id='check',
    python_callable=check,
    dag=dag,
)

# Task pipeline
download >> execute_extract >> execute_transform >> execute_load >> execute_check
```

[ENRICHED: added specificity — **`requests.get(url, stream=True)`**: the `stream=True` parameter tells the `requests` library to download the response headers immediately but delay downloading the body until you access it. Combined with `response.iter_content(chunk_size=8192)`, this downloads the file in 8KB chunks — memory-efficient for large files. Without `stream=True`, `requests` would download the entire file into memory before writing to disk. For a small lab file this doesn't matter, but for multi-GB files in production, streaming prevents out-of-memory errors.]

[ENRICHED: added specificity — **`response.raise_for_status()`**: this method checks the HTTP response status code. If the status code is 4xx (client error) or 5xx (server error), it raises an `HTTPError` exception. Without this call, a 404 or 500 response would silently return empty content — the file would be created but empty, causing confusing errors downstream. This is a best practice for all HTTP requests in Python.]

[ENRICHED: added specificity — **delimiter choice: `#` vs `:`**: the practice exercise uses `#` as the field delimiter instead of `:` (used in Exercise 3). This is because the web server access log uses `#`-delimited fields. Choosing the right delimiter depends on the source data format. Common delimiters: `,` (CSV), `|` (pipe-separated), `\t` (tab-separated), `#` (custom). The key rule: the delimiter must NOT appear within any field value. If your data contains commas, don't use commas as the delimiter.]

[ENRICHED: added specificity — **`line.upper()`**: Python string method that converts all characters to uppercase. This is the "capitalize" operation for the `visitorid` field. In data engineering, you often normalize string data (uppercase/lowercase/trim whitespace) to ensure consistent joins and comparisons. If one system stores `visitorid` as `ABC123` and another as `abc123`, a JOIN on that field would fail without normalization.]

[ENRICHED: added specificity — **practice exercise DAG name mismatch**: the practice exercise code defines `dag_id='my-first-python-etl-dag'` (same as Exercise 3), but the instructions say "Write a DAG named `ETL_Server_Access_Log_Processing`." The `dag_id` should be changed to `'ETL_Server_Access_Log_Processing'` or `'etl-server-logs-dag'` (as referenced in the verification command `airflow dags list | grep etl-server-logs-dag`). This is a bug in the lab — the code template wasn't updated to match the exercise description.]

Copy the DAG file into the `dags` directory.

```bash
cp ETL_Server_Access_Log_Processing.py $AIRFLOW_HOME/dags
```

Verify if the DAG is submitted by running the following command.

```bash
airflow dags list | grep etl-server-logs-dag
```

If the DAG didn't get imported properly, you can check the error using the following command.

```bash
airflow dags list-import-errors
```

**Authors:** Lavanya T S
**Other Contributors:** Rav Ahuja
© IBM Corporation. All rights reserved.

The content of this lab is licensed under Apache 2.0

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Cloud IDE | Definition | Defined Theia — Eclipse Foundation open-source IDE, similar to VS Code, runs desktop/cloud, Docker container ensures identical environments | HIGH |
| 2 | Cloud IDE | Clarification | Non-persistent sessions — Docker container destroyed on disconnect, including DAGs/metadata; production Airflow uses Git + persistent metadata DB | HIGH |
| 3 | Exercise 3 | Definition | Defined PythonOperator — executes Python function via `python_callable` parameter, vs BashOperator which runs shell commands | HIGH |
| 4 | Exercise 3 | Common pitfall | `python_callable` accepts function reference, not call — `extract()` during parsing vs `extract` during task execution | HIGH |
| 5 | Exercise 3 | Specificity | `days_ago(0)` utility — returns today at midnight, convenience vs fixed datetime; production prefers fixed start_date for reproducibility | HIGH |
| 6 | Exercise 3 | Definition | `global` keyword — tells Python to use module-level variable; bad practice in production, better to use parameters or XCom | HIGH |
| 7 | Exercise 3 | Specificity | `/etc/passwd` — Unix system file, 7 colon-separated fields (username:password:UID:GID:GECOS:home:shell), common teaching example | HIGH |
| 8 | Exercise 3 | Specificity | ETL pattern breakdown — Extract (passwd→extracted), Transform (colon→comma), Load (copy to CSV), Check (print to stdout) | HIGH |
| 9 | Exercise 4 | Specificity | DAG submission — copy to dags/ folder, scheduler scans every 30s, AIRFLOW_HOME env var, no restart required | HIGH |
| 10 | Exercise 4 | Specificity | `airflow dags list` — queries metadata DB, lists registered DAGs with dag_id/file_token/owner/is_paused | HIGH |
| 11 | Exercise 4 | Specificity | `airflow dags list-import-errors` — shows Python import errors during parsing, first debugging step | HIGH |
| 12 | Exercise 4 | Specificity | `airflow tasks list <dag_id>` — lists task IDs, used for verification and manual task execution | HIGH |
| 13 | Practice | Specificity | `requests.get(url, stream=True)` — streaming download, `iter_content(chunk_size=8192)` for memory efficiency | HIGH |
| 14 | Practice | Specificity | `response.raise_for_status()` — raises HTTPError on 4xx/5xx, prevents silent failures | HIGH |
| 15 | Practice | Specificity | Delimiter choice `#` vs `:` — depends on source format, must not appear in field values | HIGH |
| 16 | Practice | Specificity | `line.upper()` — string normalization for consistent joins, common data engineering practice | HIGH |
| 17 | Practice | Bug noted | DAG name mismatch — code uses `my-first-python-etl-dag` but instructions say `ETL_Server_Access_Log_Processing`, verification greps for `etl-server-logs-dag` | HIGH |

---

<!-- EXTRACTION_CHECKLIST: 42 sentences extracted, 42 sentences in output -->
