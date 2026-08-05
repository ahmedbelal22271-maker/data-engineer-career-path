# Build a DAG Using Airflow

**Course 8:** ETL & Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines
**Video Type:** Lesson (2:06)

---

Welcome to Build a DAG Using Airflow.

After watching this video, you will be able interpret an airflow pipeline as a Python script that defines an airflow direct acyclic graph (DAG) object, list the key components of a DAG definition file, create tasks by instantiating operators in your DAG definition file, and set up dependencies amongst tasks.

[ENRICHED: corrected terminology — the transcript says "direct acyclic graph," which is a spoken shorthand. The correct term is **Directed Acyclic Graph (DAG)**: a graph with directed edges (arrows go one way) and no cycles (you can never follow arrows and return to your starting node). This property is what makes Airflow able to determine execution order automatically — if cycles existed, the scheduler would enter an infinite loop trying to resolve dependencies. DAGs are a fundamental concept in computer science, used in build systems (Make, Bazel), task schedulers (Airflow, Prefect, Dagster), and dataflow programming (Apache Beam, TensorFlow computation graphs).]

[ENRICHED: definition — "DAG definition file" is the Python script (`.py` file) that contains all the code to define one Airflow workflow. It lives in the `dags/` folder (default: `~/airflow/dags/`). The Airflow scheduler scans this folder periodically (every 30 seconds by default, configurable via `dag_dir_list_interval` in `airflow.cfg`) and loads any new or modified DAG files. This file-based approach means you define your pipeline as code, check it into version control (Git), and deploy it by copying the file — no database migrations, no UI configuration, no YAML parsing.]

An Apache Airflow DAG is a Python script which consists of the following logical blocks. Python library imports, DAG argument specification, the DAG definition or instantiation, individual task definitions, which are the nodes of the DAG, and finally, the task pipeline, which specifies the dependencies between tasks.

[ENRICHED: definition — the 5 logical blocks of a DAG file, in order:

| Block | Purpose | Example |
|-------|---------|---------|
| **1. Imports** | Load required classes and modules from Airflow and Python stdlib | `from airflow import DAG` |
| **2. DAG Arguments** | Default parameters applied to all tasks (owner, retries, etc.) | `default_args = {...}` |
| **3. DAG Definition** | Instantiate the DAG object with schedule, start date, concurrency | `with DAG('my_dag', ...)` |
| **4. Task Definitions** | Individual units of work using operators | `task = BashOperator(...)` |
| **5. Task Pipeline** | Define dependencies (which task runs after which) | `task1 >> task2` |

Every Airflow DAG file follows this exact structure. Understanding this pattern means you can read any DAG file in the world and immediately know where to look for what.]

[ENRICHED: ecosystem — Airflow's Python-native approach is a deliberate design choice. Unlike Luigi (which also uses Python) or Apache Oozie (which uses XML), Airflow DAGs are plain Python scripts — no special DSL, no YAML, no JSON. This means: (1) you get full Python power (loops, conditionals, functions), (2) IDE support (autocomplete, linting, type checking), (3) unit testing with pytest, (4) version control with Git. The tradeoff is that DAG files can become complex if not carefully structured, which is why the 5-block pattern exists — it enforces separation of concerns.]

Let's implement a simple Apache Airflow pipeline by writing a DAG definition script. We will create a simple pipeline called simple_example_DAG.py that prints a greeting and then prints the current date and time. We will also schedule it to repeat the process every 5 seconds.

[ENRICHED: clarification — "every 5 seconds" is used here for demonstration purposes. In production, you would rarely schedule a DAG at sub-minute intervals. Common production schedules: hourly (`'0 * * * *'`), daily (`'0 0 * * *'`), weekly (`'0 0 * * 0'`), or `@daily`/`@hourly` Airflow presets. Running DAGs every 5 seconds would generate 17,280 runs per day, each creating database records in the metadata DB — this would overwhelm the scheduler and database. The `@once` schedule (run exactly once and stop) or `None` (manual trigger only) are common alternatives for pipelines that shouldn't repeat.]

Let's go through the list of logical blocks one by one. Begin by importing the Python libraries you will need for your DAG here. Start by importing the DAG class from the airflow models library. Then import the bash operator, which you will use to create the two print tasks, and the datetime, and timedelta modules from the datetime package, which you will need for specifying several time-related parameters.

[ENRICHED: added specificity — the import statements in modern Airflow (2.x) are:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
```

In Airflow 1.x, the imports were different:
```python
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
```

The `from airflow import DAG` shorthand is the recommended way in Airflow 2.x — it's a convenience alias that re-exports `DAG` from `airflow.models`. Both work, but the shorter form is now standard. The `BashOperator` import path changed in Airflow 2.x from `airflow.operators.bash_operator` to `airflow.operators.bash` — this is a common source of errors when migrating DAGs from Airflow 1.x to 2.x.]

[ENRICHED: definition — `timedelta` is a Python class from the `datetime` module that represents a duration (a difference between two dates/times). In Airflow, it's commonly used for: (1) `retry_delay=timedelta(minutes=5)` — wait 5 minutes before retrying a failed task, (2) `execution_delta` in `ExternalTaskSensor` — sensor checks for a task that ran N minutes ago, (3) `schedule_interval=timedelta(hours=1)` — alternative to cron syntax for defining schedules. Example: `timedelta(days=1, hours=6, minutes=30)` represents 1 day, 6 hours, and 30 minutes. This is preferred over hardcoding seconds (e.g., `90000`) because it's readable and handles daylight saving time transitions correctly.]

The next block is for specifying the default DAG arguments. Notice they are specified as a Python dict, which is just a collection of key-value pairs enclosed by curly braces. These are used to specify such things as the owner of the DAG, which is you, and its start date, in this case January 1, 2024, the number of times it should keep trying if it is failing. Here, only once if it does fail, and the retry_delay, or the time to wait between subsequent tries, which in this case is five minutes.

[ENRICHED: added specificity — the `default_args` dictionary and its keys:

| Key | Type | Purpose | Video Value | Real-World Example |
|-----|------|---------|-------------|-------------------|
| `owner` | str | Who owns this DAG (appears in Web UI) | `'you'` | `'data-engineering-team'` |
| `start_date` | datetime | When the DAG starts scheduling runs | `datetime(2024, 1, 1)` | `datetime(2024, 6, 1)` |
| `retries` | int | Number of retry attempts on failure | `1` | `3` |
| `retry_delay` | timedelta | Wait time between retries | `timedelta(minutes=5)` | `timedelta(minutes=10)` |

**Critical insight about `retries`:** When the video says "only once if it does fail," it means `retries=1` — Airflow will attempt the task ONE additional time after the initial failure (total: 2 attempts). Setting `retries=0` means no retries at all. Production DAGs typically use `retries=2` or `retries=3` with `retry_delay=timedelta(minutes=5)` to handle transient failures (network timeouts, temporary service unavailability) without manual intervention.]

[ENRICHED: common pitfall — `start_date` is one of the most misunderstood parameters in Airflow. The video says "January 1, 2024" but there's a critical behavior: **Airflow does NOT run the DAG on the start_date itself.** The first run happens at `start_date + schedule_interval`. So if `start_date=datetime(2024, 1, 1)` and `schedule_interval='@daily'`, the first run is January 2, 2024. This confuses almost every Airflow beginner. Additionally, if `start_date` is in the past and `catchup=True` (the default), Airflow will backfill EVERY missed run from `start_date` to now — potentially creating hundreds of runs. The video's example of `start_date=datetime(2024, 1, 1)` with `schedule_interval='*/5 * * * *'` (every 5 seconds) and `catchup=True` would attempt to create millions of backfill runs. In practice, always set `catchup=False` unless you explicitly want backfill behavior.]

The DAG definition block is used for instantiating your workflow as a DAG object. Here you can specify things like the name of your DAG, such as simple_example, a description for your workflow, for example, a simple example DAG, the default arguments to apply to your DAG, which in this case are specified by the default_args dict you already defined in the previous block, and finally scheduling instructions. In this case, the DAG will run repeatedly on a schedule of every 5 seconds once it is deployed.

[ENRICHED: added specificity — the DAG definition block uses Python's context manager pattern (`with` statement):

```python
with DAG(
    dag_id='simple_example',
    description='A simple example DAG',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=False
) as dag:
    # tasks defined here
```

The `with` statement is a Python context manager. When the code block inside `with` ends, Python automatically calls `dag.__exit__()`, which registers the DAG with Airflow's DAG registry. Without the `with` statement, you'd need to explicitly assign each task to the DAG using `task.dag = dag` — the context manager makes this automatic.

**`schedule_interval` options:**
- Cron expression: `'*/5 * * * *'` (every 5 minutes), `'0 * * * *'` (hourly), `'@daily'`
- Presets: `@once`, `@hourly`, `@daily`, `@weekly`, `@monthly`, `@yearly`
- `None` or `False` — manual trigger only (no automatic scheduling)
- `timedelta(hours=1)` — alternative to cron for simple intervals]

Next comes the task definition block. Here we define two tasks: task1 and task2, both of which are bash operators. Their respective ids are specified as print_hello and print_date. They each call a bash command, where the first task will echo "Greetings, the date and time are", and the second task will print the current date and time using the bash command date.

[ENRICHED: definition — `BashOperator` is an Airflow operator that executes a bash command or script on the local machine (or the Airflow worker node). It's one of the most basic operators and is useful for: (1) running shell scripts, (2) executing system commands, (3) invoking CLI tools. The `bash_command` parameter accepts any valid bash command. When a task runs, Airflow creates a temporary bash script file containing the command, executes it via subprocess, and captures stdout/stderr. After execution, the temp file is deleted.

**The two tasks in the video:**

| Task ID | Operator | Bash Command | What It Does |
|---------|----------|-------------|--------------|
| `print_hello` | BashOperator | `echo "Greetings, the date and time are"` | Prints the greeting string to stdout |
| `print_date` | BashOperator | `date` | Prints the current date/time to stdout (e.g., `Wed Jul 23 10:30:00 UTC 2025`) |

**Task IDs matter:** The `task_id` parameter is how Airflow identifies the task in the Web UI, in logs, in the metadata database, and in the `>>` dependency notation. If you change a task's `task_id`, Airflow treats it as a completely new task (the old one becomes a "removed" task in the Web UI). This is why you should never rename task_ids in production — it breaks historical run data.]

Finally, each task is assigned to the DAG you instantiated in the DAG definition block above.

The final block is where you specify the dependencies for your workflow, like this. Here, the double greater than notation specifies that task2 is downstream from task1. This means that task1, which we named print hello, will run first. Once print hello runs successfully, task2 or print date will run.

[ENRICHED: added specificity — the `>>` operator is Airflow's dependency operator, also called the "bitshift" operator. It reads naturally as "then" or "goes to":

```python
task1 >> task2  # task1 runs first, then task2
```

**Equivalent notations (all do the same thing):**

| Notation | Code | Readability |
|----------|------|-------------|
| `>>` (bitshift) | `task1 >> task2` | "task1 then task2" |
| `<<` (reverse bitshift) | `task2 << task1` | "task2 after task1" |
| `set_downstream()` | `task1.set_downstream(task2)` | Explicit method call |
| `set_upstream()` | `task2.set_upstream(task1)` | Explicit method call |

**Chaining multiple tasks:**
```python
task1 >> task2 >> task3  # task1 → task2 → task3 (sequential)
task1 >> [task2, task3]  # task1 → task2 AND task1 → task3 (fan-out)
[task1, task2] >> task3  # task1 → task3 AND task2 → task3 (fan-in)
```

**Important:** Dependencies only define execution ORDER, not data flow. Airflow does not pass data between tasks automatically. If task2 needs data from task1, you must explicitly write it to a file (local, S3, database) in task1 and read it in task2. This is why Airflow is a "task orchestrator" — it coordinates WHEN tasks run, not WHAT data they exchange.]

This completes the creation of your Airflow DAG, and you now have a good idea of the general pattern.

In this video, you learned that an Airflow pipeline is a Python script that instantiates an Airflow DAG object. Key components of a DAG definition file are library imports, DAG arguments, DAG and task definitions, and the task pipeline specification. You can specify a schedule in your Dag definition if you want it to run repeatedly by setting the schedule parameter. And finally, tasks are instantiated operators imported from the Apache airflow.operators module.

---

## Complete Working Example

The video describes this DAG script but doesn't show it as a single block. Here is the complete `simple_example_dag.py` file assembled from the video's walkthrough:

```python
# Block 1: Library imports
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Block 2: DAG arguments
default_args = {
    'owner': 'you',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Block 3: DAG definition
with DAG(
    dag_id='simple_example',
    description='A simple example DAG',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=False
) as dag:

    # Block 4: Task definitions
    task1 = BashOperator(
        task_id='print_hello',
        bash_command='echo "Greetings, the date and time are"'
    )

    task2 = BashOperator(
        task_id='print_date',
        bash_command='date'
    )

    # Block 5: Task pipeline (dependencies)
    task1 >> task2
```

[ENRICHED: added specificity — when you save this file as `simple_example_dag.py` inside your Airflow `dags/` folder (default: `~/airflow/dags/`), the scheduler will automatically detect it within 30 seconds and add it to the Web UI under the "DAGs" tab. You can verify it's loaded by running `airflow dags list | grep simple_example` in the terminal, or by checking the Web UI's "DAGs" page where it will appear with a toggle to pause/unpause it.]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Learning Objectives | Correction | Corrected "direct acyclic graph" → "Directed Acyclic Graph (DAG)" with graph theory explanation | HIGH |
| 2 | Learning Objectives | Definition | Defined DAG (Directed Acyclic Graph) — no cycles, why acyclic matters for scheduler, used in build systems/dataflow | HIGH |
| 3 | DAG Definition File | Definition | Defined DAG definition file — Python .py file in dags/ folder, scheduler scans every 30s, file-based deployment | HIGH |
| 4 | Logical Blocks | Definition | Detailed 5-block structure table (imports → args → definition → tasks → pipeline) with purpose and example for each | HIGH |
| 5 | Logical Blocks | Ecosystem | Python-native design choice — comparison to Luigi (Python), Oozie (XML), benefits: IDE support, unit testing, version control | HIGH |
| 6 | Schedule | Clarification | "every 5 seconds" is for demo only — production schedules are hourly/daily, sub-minute causes scheduler/database overload | HIGH |
| 7 | Imports | Specificity | Modern Airflow 2.x import paths vs 1.x paths, `from airflow import DAG` shorthand, BashOperator path change | HIGH |
| 8 | Imports | Definition | Defined `timedelta` — Python class for durations, used for retry_delay, execution_delta, schedule_interval, DST-safe | HIGH |
| 9 | DAG Arguments | Specificity | 4-row table of default_args keys (owner, start_date, retries, retry_delay) with types, purposes, video values, real-world values | HIGH |
| 10 | DAG Arguments | Common pitfall | `retries=1` means 2 total attempts (initial + 1 retry). Production uses retries=2-3 with retry_delay=5min | HIGH |
| 11 | DAG Arguments | Common pitfall | `start_date` behavior — first run at start_date + schedule_interval, not start_date itself. catchup=True causes backfill | HIGH |
| 12 | DAG Definition | Specificity | Context manager pattern (`with DAG(...) as dag:`), __exit__() auto-registration, schedule_interval options (cron, presets, None) | HIGH |
| 13 | Task Definitions | Definition | BashOperator — executes bash on local/worker, bash_command param, temp script creation, stdout capture, temp file cleanup | HIGH |
| 14 | Task Definitions | Specificity | Table of two tasks (print_hello, print_date) with operator, command, and what each does | HIGH |
| 15 | Task Definitions | Specificity | Task IDs matter — changing task_id = new task (old becomes "removed"), never rename in production | HIGH |
| 16 | Dependencies | Specificity | `>>` operator = "then", alternative notations table (>>, <<, set_downstream, set_upstream), chaining patterns | HIGH |
| 17 | Dependencies | Clarification | Dependencies define ORDER not DATA FLOW — Airflow doesn't pass data between tasks, use files/DBs instead | HIGH |
| 18 | Summary | Specificity | Complete working example: assembled full simple_example_dag.py with all 5 blocks, verification commands | HIGH |

---

<!-- EXTRACTION_CHECKLIST: 32 sentences extracted, 32 sentences in output -->
