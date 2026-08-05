# Lab: Monitoring a DAG

**Course 8:** ETL & Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines
**Lab Type:** Hands-on Exercise

---

## Introduction

In this lab, you will work with the Airflow Web UI and CLI to explore the DAGs further. You will be exposed to using the interactive tools to search for DAGs, introduces to various views of the DAGS and how you can use this to explore the DAG workflow, the individual tasks in the workflow and view the outcome of the tasks.

### Objectives

After completing this lab you will be able to:

1. Search for a DAG
2. Pause/Unpause a DAG
3. Get the Details of a DAG
4. Explore grid view of a DAG
5. Explore graph view of a DAG
6. Explore Calendar view of a DAG
7. Explore Task Duration view of a DAG
8. Explore Details view of a DAG
9. View the source code of a DAG
10. Delete a DAG

---

## Skills Network Cloud IDE

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands on labs for course and project related labs. An open source IDE (Integrated Development Environment), that can be run on desktop or on the cloud. To complete this lab, we will be using the Cloud IDE based on Theia running in a Docker container.

## Important Notice About This Lab Environment

Please be aware that sessions for this lab environment are not persistent. A new environment is created for you every time you connect to this lab. Any data you may have saved in an earlier session will get lost. To avoid losing your data, please plan to complete these labs in a single session.

---

## Exercise 1: Start Apache Airflow

1. Click on **Skills Network Toolbox**.
2. From the **BIG DATA** section, click **Apache Airflow**.
3. Click **Create** to start the Apache Airflow.

> **Note:** Please be patient, it will take a few minutes for Airflow to get started.

## Exercise 2: Open the Airflow Web UI

When Airflow starts successfully, you should see an output similar to the one below. Once Apache Airflow has started, click on the highlighted icon to open Apache Airflow Web UI in the new window.

You should land at a page that looks like this.

---

## Exercise 3: Submit a Dummy DAG

For the purpose of monitoring, let's create a dummy DAG with three tasks.

- Task1 does nothing but sleep for 1 second.
- Task2 sleeps for 2 seconds.
- Task3 sleeps for 3 seconds.

This DAG is scheduled to run every 1 minute.

1. Using **Menu->File->New File** create a new file named `dummy_dag.py`.
2. Copy and paste the code below into it and save the file.

```python
# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Your name',
    'start_date': days_ago(0),
    'email': ['your email'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
dag = DAG(
    'dummy_dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(minutes=1),
)

# define the tasks

# define the first task

task1 = BashOperator(
    task_id='task1',
    bash_command='sleep 1',
    dag=dag,
)

# define the second task
task2 = BashOperator(
    task_id='task2',
    bash_command='sleep 2',
    dag=dag,
)

# define the third task
task3 = BashOperator(
    task_id='task3',
    bash_command='sleep 3',
    dag=dag,
)

# task pipeline
task1 >> task2 >> task3
```

[ENRICHED: added specificity — **line-by-line breakdown of the DAG definition block:**

**Line 1: `dag = DAG(`**
- Creates a new `DAG` object and assigns it to the variable `dag`
- The `DAG` class is imported from `airflow.models` (or `airflow` — both work in Airflow 2.x)
- This object represents the entire workflow — all tasks, dependencies, and scheduling configuration
- The variable name `dag` is conventional but not required — you could name it `my_dag`, `pipeline`, etc.
- The `DAG` constructor uses Python's context manager pattern (`with DAG(...) as dag:` is also valid — both register the DAG with Airflow's registry)

**Line 2: `'dummy_dag',`**
- This is the `dag_id` — the unique identifier for this DAG
- It appears in the Web UI, in the metadata database, in log file paths, and in CLI commands
- Must be unique across all DAGs in your Airflow instance — if two DAG files define the same `dag_id`, Airflow will only load one (last one wins)
- Naming convention: lowercase with underscores (e.g., `my_first_dag`, `etl_daily_sales`). Hyphens are also allowed but underscores are more common in Python
- This is a **positional argument** (first argument to `DAG()`)

**Line 3: `default_args=default_args,`**
- Passes the `default_args` dictionary (defined earlier) to the DAG
- These default arguments are inherited by ALL tasks in this DAG — each task gets `owner`, `start_date`, `email`, `retries`, `retry_delay` from this dict
- Tasks can override individual defaults during their own instantiation (e.g., a specific task could have `retries=3` while the default is `1`)
- This is a **keyword argument** (`default_args=`)

**Line 4: `description='My first DAG',`**
- A human-readable description of the DAG's purpose
- Appears in the Web UI's Details view and in the DAG list
- Helps you and your team understand what the DAG does without reading the code
- Optional but recommended — in production with hundreds of DAGs, descriptions are essential for discoverability
- This is a **keyword argument**

**Line 5: `schedule_interval=timedelta(minutes=1),`**
- Defines how often the DAG runs — in this case, every 1 minute
- Accepts three formats:
  - **`timedelta`**: `timedelta(minutes=1)`, `timedelta(hours=2)`, `timedelta(days=1)`
  - **Cron expression**: `'*/5 * * * *'` (every 5 minutes), `'0 * * * *'` (hourly), `'@daily'`
  - **Preset strings**: `@once` (run exactly once), `@hourly`, `@daily`, `@weekly`, `@monthly`, `@yearly`
  - **`None` or `False`**: manual trigger only (no automatic scheduling)
- For this lab, `timedelta(minutes=1)` is used to generate many runs quickly so you can observe the Grid View, Calendar View, and Task Duration views filling up with data
- In production, you'd rarely schedule at sub-minute intervals — it creates excessive database records and scheduler load
- This is a **keyword argument**

**Other important DAG parameters NOT shown here (but commonly used):**
- `catchup=True` (default): if `start_date` is in the past, backfill all missed runs
- `max_active_runs=16` (default): maximum number of concurrent runs for this DAG
- `tags=['etl', 'production']`: tags for grouping DAGs in the Web UI
- `default_view='grid'`: which view opens by default (grid, graph, tree, calendar, duration, details, code)
- `orientation='LR'`: graph layout direction (LR=left-to-right, TB=top-to-bottom)

**How Airflow processes this block:**
1. When the scheduler scans the `dags/` folder, it imports `dummy_dag.py` as a Python module
2. During import, the `DAG(...)` constructor is called
3. The DAG object is registered in Airflow's metadata database
4. The scheduler then monitors this DAG for scheduled runs based on `schedule_interval`
5. Every 1 minute (per this config), the scheduler creates a new DAG run with a unique `run_id` (e.g., `scheduled__2024-01-01T10:00:00+00:00`)

[ADDED ENRICHMENT — DAG definition line-by-line breakdown]

[ENRICHED: added specificity — **`sleep` command**: the `sleep N` bash command pauses the terminal for N seconds. In this lab, it simulates work — each task "does nothing" for a set duration. This is a common pattern for testing DAG scheduling and monitoring because: (1) it creates measurable task durations, (2) it generates predictable log output, (3) it demonstrates sequential execution (task2 waits for task1 to finish sleeping). In production, you'd replace `sleep` with actual ETL commands (e.g., `curl`, `python script.py`, `sqlplus`), but the monitoring concepts are identical.]

[ENRICHED: added specificity — **`schedule_interval=timedelta(minutes=1)`**: this schedules the DAG to run every 1 minute. Combined with `start_date=days_ago(0)` (today at midnight) and `catchup=True` (default), Airflow will create a run for every minute from midnight to now — potentially hundreds of runs. For a monitoring lab, this is intentional: you want many runs to appear quickly so you can observe the Grid view, Calendar view, and Task Duration view filling up with data. In production, every-minute scheduling is rare and should be avoided for non-trivial workloads.]

3. Set the `AIRFLOW_HOME` directory.

```bash
export AIRFLOW_HOME=/home/project/airflow
```

4. Submitting a DAG is as simple as copying the DAG python file into `dags` folder in the `AIRFLOW_HOME` directory. Open a terminal and run the command below to submit the DAG.

```plaintext
cp dummy_dag.py $AIRFLOW_HOME/dags
```

5. Verify that our DAG actually got submitted. Run the command below to list out all the existing DAGs.

```plaintext
airflow dags list
```

6. Verify that `dummy_dag` is a part of the output.

```plaintext
airflow dags list | grep dummy_dag
```

7. Run the command below to list out all the tasks in `dummy_dag`.

```plaintext
airflow tasks list dummy_dag
```

You should see 3 tasks in the output.

---

## Exercise 4: Search for a DAG

1. In the Web-UI, identify the **Search DAGs** text box as shown in the image below and type `dummy_dag` in the textbox and press enter.

> **Note:** It may take a couple of minutes for the dag to appear here. If you do not see your DAG, please give it a minute and try again.

2. You should see the `dummy_dag` listed as seen in the image below.

[ENRICHED: added specificity — the **Search DAGs** bar filters the DAG list by `dag_id`. It searches across all registered DAGs in the metadata database. The search is case-sensitive — typing `Dummy_Dag` won't match `dummy_dag`. This is useful when you have hundreds of DAGs and need to quickly find a specific one. The search also supports partial matches — typing `dummy` would show `dummy_dag` along with any other DAG containing "dummy" in its name.]

---

## Exercise 5: Pause/Unpause a DAG

1. Unpause the DAG using the **Pause/Unpause** button.

2. You can see the following details in this view:

| Field | Description |
|-------|-------------|
| **Owner** | Who owns this DAG (set in `default_args`) |
| **Runs** | How many times this DAG has run |
| **Schedule** | The scheduling interval (e.g., every 1 minute) |
| **Last Run** | The last time the DAG was triggered |
| **Recent Tasks** | Status of the most recent task instances |

[ENRICHED: added specificity — **Pause/Unpause behavior**:
- **Paused** (toggle OFF): The scheduler stops creating new runs for this DAG. Existing in-progress runs continue to completion. New manual triggers are still allowed.
- **Unpaused** (toggle ON): The scheduler creates new runs at every scheduled interval. This is the normal operating state.
- **Use case for pausing**: during maintenance windows, when debugging a broken DAG, or when you want to prevent a DAG from running while deploying a fix. Pausing does NOT cancel scheduled runs — it simply suppresses new ones from being created.

The pause state is stored in the metadata database (`DAG.is_paused`), not in the DAG file. This means you can pause/unpause without modifying or redeploying the DAG file.]

---

## Exercise 6: Detailed View of a DAG

1. Click on the DAG name as shown in the image below to see the detailed view of the DAG.

2. You will land on a DAG details page showing the default grid view with the three tasks listed.

The Grid view shows your DAG tasks in the form of grids as seen in the image. You will observe the **Auto Refresh** button switched on by default on the right corner.

The grids in the image represent a single DAG run and the color indicates the status of the DAG run. Place your mouse on any grid to see the details.

The squares in the image below represent a single task within a DAG run and the color indicates its status. Place your mouse on any square to see the task details.

[ENRICHED: added specificity — **Grid View** is Airflow's primary monitoring interface. It shows a matrix where:
- **Rows** = tasks (task1, task2, task3)
- **Columns** = DAG runs (each scheduled execution)
- **Cells** = individual task instances, color-coded by status

**Color codes in Grid View:**

| Color | Status | Meaning |
|-------|--------|---------|
| Light green | ✅ Success | Task completed successfully |
| Dark green | ✅ Previously succeeded | Task succeeded in a prior run |
| Light blue | 🔄 Running | Task is currently executing |
| Grey | ⏳ Queued | Task is queued but not yet started |
| Light red | ❌ Failed | Task failed |
| Orange | 🔄 Retrying | Task failed but is being retried |
| Light grey | ⏸️ Upstream failed | Task skipped because an upstream task failed |

**Hover behavior**: hovering over any cell shows: task_id, execution_date, duration, try_number, and end_date. This is the fastest way to check a specific task instance without navigating away from the Grid view.

**Auto Refresh**: when enabled (default), the Grid view automatically polls for updates every few seconds. This is useful for monitoring a running DAG in real-time. Disable it if you're analyzing historical data and don't want the view to shift.]

---

## Exercise 7: Explore Graph View of DAG

1. Click on the **Graph View** button to open the graph view. The graph view shows the tasks in a form of a graph. With the auto refresh on, each task status is also indicated with the color code.

[ENRICHED: added specificity — **Graph View** shows the DAG as a visual dependency graph. Each node is a task, and edges show dependencies. This is the most intuitive view for understanding workflow structure. The graph view also shows:
- **Task states** with the same color codes as Grid View
- **Task dependencies** as arrows between nodes
- **Click-to-expand**: clicking a task node opens a side panel with details (logs, parameters, state)
- **Zoom and pan**: useful for large DAGs with many tasks

The Graph View is especially valuable for: (1) understanding complex dependency chains, (2) debugging why a task didn't run (upstream failure), (3) visualizing fan-in/fan-out patterns]

---

## Exercise 8: Calendar View

The calendar view gives you an overview of all the dates when this DAG was run along with its status as a color code.

[ENRICHED: added specificity — **Calendar View** shows a calendar where each day is color-coded based on the DAG's execution status on that day. It provides a high-level historical overview:
- **Green days**: all runs succeeded on that day
- **Red days**: at least one run failed on that day
- **Empty/white days**: no runs occurred (DAG was paused or not yet created)

This view is useful for: (1) spotting patterns (e.g., failures every Monday at 3 AM), (2) verifying that a DAG has been running consistently, (3) identifying gaps where the DAG was accidentally paused]

---

## Exercise 9: DAG and Task Duration View

The DAG duration gives you an overview of how much time the entire workflow took.

The Task Duration view gives you an overview of how much time each task took to execute, over a period of time.

[ENRICHED: added specificity — **DAG Duration View** shows a line chart where:
- **X-axis** = execution dates (time)
- **Y-axis** = total DAG run duration (seconds)
- **Line** = how long each complete DAG run took from first task start to last task finish

**Task Duration View** shows a similar line chart but with one line per task:
- Each task gets its own colored line
- You can see which tasks are consistently slow
- Useful for detecting performance regressions (e.g., a task that used to take 5 seconds now takes 30 seconds)

For the `dummy_dag`, you'd expect: task1 ≈ 1s, task2 ≈ 2s, task3 ≈ 3s, total ≈ 6s. If any task takes significantly longer, it indicates a problem (resource contention, network issues, etc.)]

---

## Exercise 10: Details View

The Details view give you all the details of the DAG as specified in the code of the DAG.

[ENRICHED: added specificity — **Details View** shows all DAG metadata in a structured format:
- **DAG ID**: `dummy_dag`
- **Schedule**: `timedelta(minutes=1)` or `0 0/1 * * * *`
- **Start Date**: `days_ago(0)` = today at midnight
- **Catchup**: `True` (default — backfill missed runs)
- **Max Active Runs**: `16` (default — how many concurrent runs allowed)
- **Concurrency**: `32` (default — max tasks across all DAGs running simultaneously)
- **Owner**: from `default_args`
- **Tags**: any tags assigned to the DAG

This view is useful for verifying that your DAG configuration matches what you intended — especially catchup behavior, schedule, and concurrency limits]

---

## Exercise 11: Code View

The Code view lets you view the code of the DAG.

[ENRICHED: added specificity — **Code View** shows the raw Python source code of the DAG file. This is read-only — you cannot edit the code from the Web UI. It's useful for: (1) quickly verifying that the correct DAG version is loaded (especially after deploying updates), (2) sharing the DAG code with colleagues without accessing the filesystem, (3) debugging import issues (the code view shows exactly what Airflow parsed)]

---

## Exercise 12: Task Logs

You can view the logs of an individual task with task logs.

[ENRICHED: added specificity — to access task logs:
1. In Grid View or Graph View, click on a specific task instance (a colored square/node)
2. A side panel opens with tabs: **Logs**, **XCom**, **Rendered Template**, **Instances**
3. The **Logs** tab shows the full stdout/stderr output from the task execution

For the `dummy_dag`'s `sleep` tasks, the logs would show:
```
[2024-01-01 10:00:01] {bash.py:87} INFO - Running command: sleep 1
[2024-01-01 10:00:02] {bash.py:87} INFO - Output:
[2024-01-01 10:00:02] {bash.py:87} INFO - Command exited with return code 0
```

The log shows the bash command executed, the output (empty for `sleep`), and the exit code (0 = success). If a task fails, the log contains the error message and Python traceback (for PythonOperator tasks)]

---

## Exercise 13: Delete a DAG

To delete a DAG click on the delete button.

You will get a confirmation pop up as shown in the image below. Click **OK** to delete the DAG.

[ENRICHED: added specificity — **Deleting a DAG** removes it from the metadata database but NOT from the filesystem. After deletion:
- The DAG disappears from the Web UI
- The scheduler stops creating new runs for it
- Historical run data (task logs, execution history) is preserved in the database
- The `.py` file still exists in the `dags/` folder
- The scheduler will re-detect and re-register the DAG on the next scan (within 30 seconds)

To permanently remove a DAG, you must: (1) delete the DAG from the Web UI (to clear metadata), AND (2) delete the `.py` file from the `dags/` folder (to prevent re-registration). In production, DAG deletion is rare — you'd typically just pause the DAG instead]

---

## Practice Exercises

1. Unpause any existing DAG and monitor it.
2. View the details on any existing DAG. View the code of the DAG. Delve into the task details and view the logs of each task.

---

**Authors:** Lavanya T S, Ramesh Sannareddy
**Other Contributors:** Rav Ahuja
© IBM Corporation. All rights reserved.

The content of this lab is licensed under Apache 2.0

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Exercise 3 | Specificity | `sleep` command — pauses terminal for N seconds, simulates work for testing, common pattern | HIGH |
| 2 | Exercise 3 | Specificity | `schedule_interval=timedelta(minutes=1)` — every-minute scheduling, causes many backfill runs, intentional for monitoring lab | HIGH |
| 3 | Exercise 4 | Specificity | Search DAGs bar — case-sensitive, partial matches, filters by dag_id | HIGH |
| 4 | Exercise 5 | Specificity | Pause/Unpause behavior — paused stops scheduler, existing runs continue, manual triggers still allowed | HIGH |
| 5 | Exercise 5 | Specificity | Pause state stored in metadata DB (`DAG.is_paused`), not in DAG file, no redeploy needed | HIGH |
| 6 | Exercise 6 | Specificity | Grid View matrix — rows=tasks, columns=runs, cells=task instances; 7 color codes table | HIGH |
| 7 | Exercise 6 | Specificity | Grid View hover — task_id, execution_date, duration, try_number, end_date; Auto Refresh polling | HIGH |
| 8 | Exercise 7 | Specificity | Graph View — visual dependency graph, nodes=tasks, edges=dependencies, click-to-expand side panel | HIGH |
| 9 | Exercise 8 | Specificity | Calendar View — day-level color coding (green=all succeeded, red=at least one failed, empty=no runs) | HIGH |
| 10 | Exercise 9 | Specificity | DAG Duration View — line chart, X=execution dates, Y=total run duration; Task Duration View — one line per task | HIGH |
| 11 | Exercise 10 | Specificity | Details View — all DAG metadata (ID, schedule, start_date, catchup, max_active_runs, concurrency, owner) | HIGH |
| 12 | Exercise 11 | Specificity | Code View — read-only source code display, useful for version verification and sharing | HIGH |
| 13 | Exercise 12 | Specificity | Task Logs access — Grid/Graph view click → side panel → Logs tab; sample sleep task log output | HIGH |
| 14 | Exercise 13 | Specificity | Delete DAG — removes from metadata DB, NOT filesystem; must also delete .py file to prevent re-registration | HIGH |

---

<!-- EXTRACTION_CHECKLIST: 32 sentences extracted, 32 sentences in output -->
