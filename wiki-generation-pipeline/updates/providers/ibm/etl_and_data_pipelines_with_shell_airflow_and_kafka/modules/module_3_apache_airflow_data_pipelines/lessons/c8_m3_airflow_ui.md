**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines

# Apache Airflow UI

## Learning Objectives

After watching this video, you will be able to:
- identify current directed acyclic graphs (DAGs) in your environment,
- list different ways to visualize a specific DAG,
- review the code that defines your DAG,
- analyze the duration of each task in your DAG over multiple runs, and
- select context metadata for any task instance.

## The DAGs View

Let's start with the landing page for the Apache Airflow user interface. The image on the screen is how the interface appears in your browser. It defaults to the DAGs view, which is a table containing data about each DAG in your environment. Each row displays interactive information about a DAG in your environment, such as the DAG's name, the DAG's owner, which is set to Airflow, indicating this is a built-in example from Airflow, the status of the tasks from the current or most recent DAG run, the DAG's run schedule, which in this case, will be in the crontab format, the status of all previous DAG runs, date and time of the last run, date and time of the next scheduled run, plus, a collection of quick links to drill down into more information related to the DAG. In the preceding column, you can toggle to pause a DAG. Example_bash_operator DAG is running, but all other DAGs are currently paused.

[ENRICHED: defined "crontab format" — a standard syntax for expressing recurring time-based schedules. The format has 5 fields: `minute hour day-of-month month day-of-week`. Examples: `0 2 * * *` = every day at 2 AM, `0 */6 * * *` = every 6 hours, `0 9 * * 1-5` = weekdays at 9 AM. Airflow's `@daily`, `@hourly`, `@weekly` are shorthand aliases for common crontab patterns. `@daily` = `0 0 * * *` (midnight UTC every day).]

[ENRICHED: concrete example — DAGs view table columns:

```
┌─────────────────┬───────┬──────────┬──────────┬──────────┬─────────────┬──────────────┐
│ DAG Name        │ Owner │ Status   │ Schedule │ Last Run │ Next Run    │ Actions      │
├─────────────────┼───────┼──────────┼──────────┼──────────┼─────────────┼──────────────┤
│ example_bash    │ airflow│ RUNNING │ @daily   │ Jul 22   │ Jul 23 00:00│ [Graph][Tree]│
│ _operator      │       │          │          │ 00:00    │             │              │
├─────────────────┼───────┼──────────┼──────────┼──────────┼─────────────┼──────────────┤
│ sales_pipeline │ data  │ PAUSED   │ @daily   │ Jul 21   │ — (paused)  │ [Graph][Tree]│
│                │ team  │          │          │ 00:00    │             │              │
├─────────────────┼───────┼──────────┼──────────┼──────────┼─────────────┼──────────────┤
│ inventory_sync │ data  │ PAUSED   │ @hourly  │ Jul 22   │ — (paused)  │ [Graph][Tree]│
│                │ team  │          │          │ 11:00    │             │              │
└─────────────────┴───────┴──────────┴──────────┴──────────┴─────────────┴──────────────┘

Key columns:
- Status: RUNNING, SUCCESS, FAILED, PAUSED (from current/recent run)
- Last Run: timestamp of most recent execution
- Next Run: when scheduler will trigger next (blank if paused)
- Toggle column: on/off switch to pause/unpause DAG
```

The pause toggle is critical for production: you can disable a broken pipeline without deleting it, fix the code, then re-enable it. The scheduler won't trigger paused DAGs.]

## Grid View

You can visualize DAGs in several ways. Start by selecting the name of the DAG you want to visualize. Let's consider the DAG named simple-example. Notice that the button is on, indicating that the DAG is running in the production environment. When you select the DAG name, the DAG's grid view opens. It shows a timeline of the status of your DAG and its tasks for each run. Here, you can select the base date and the number of runs to display. Each status is color-coded according to the legend displayed here. You can also hover your mouse pointer over any task in the timeline to view more information about it.

[ENRICHED: concrete example — grid view visualization:

```
GRID VIEW: sales_pipeline (last 4 runs)

              Run 1    Run 2    Run 3    Run 4
              Jul 19   Jul 20   Jul 21   Jul 22
extract       ✅       ✅       ✅       🔄 (running)
transform     ✅       ✅       ❌       —
load          ✅       ✅       —       —
send_email    ✅       ✅       —       —

Legend:
✅ = SUCCESS (green)
❌ = FAILED (red)
🔄 = RUNNING (blue)
— = UPSTREAM FAILED (gray, task never ran)
⏳ = QUEUED (yellow)
```

The grid view is your primary debugging tool. When a pipeline fails, you immediately see: (1) which task failed, (2) whether it's a one-time failure or a recurring pattern, (3) how long each task took on previous successful runs. Hovering over a task shows: task ID, execution date, duration, and try number.]

## Graph View

Next, let's review the elements of a multi-operator DAG. Click "Graph" to display the graph view. You can see the DAG's tasks and dependencies. In this example, execute_function depends on print_hello to be executed first. Each task is color-coded by its operator type. In this example, print_hello is a bash operator, and execute_function is a Python operator. Here, you can filter your view by toggling the status option buttons.

[ENRICHED: concrete example — graph view:

```
GRAPH VIEW: simple-example DAG

  ┌─────────────┐      ┌──────────────────┐
  │ print_hello │ ───→ │ execute_function  │
  │  (BashOp)   │      │   (PythonOp)     │
  └─────────────┘      └──────────────────┘
  
  Color coding:
  Blue = BashOperator (print_hello)
  Green = PythonOperator (execute_function)
  
  Status filter buttons: [All] [Success] [Failed] [Running] [Upstream Failed]
  
  Click any task → context menu opens (see below)
```

The graph view shows the actual execution topology — you can visually verify that dependencies are correct. If you expected parallel execution but see serial (no branching), the graph view reveals the mistake immediately.]

## Task Instance Context Menu

The task instance context menu can be accessed from both grid and graph views by clicking on the task. This menu allows you, for example, to drill down on a selected task instance to view and edit several details or to view the task's log file.

[ENRICHED: concrete example — context menu options:

```
CONTEXT MENU: Right-click on "transform" task

┌────────────────────────────────────┐
│ View Instance                     │  → Detailed task metadata page
│ View Log                         │  → See stdout/stderr from this task run
│ Mark as Success                  │  → Manually override failed status
│ Mark as Failed                   │  → Manually override success status
│ Clear                            │  → Reset task to re-run on next scheduler cycle
│ Run                              │  → Trigger task immediately (bypass schedule)
│ Retry                            │  → Re-queue task for retry
│ Add Pool Slot                    │  → Manually allocate a worker slot
│ Delete                           │  → Remove this task instance record
│ See more                         │  → Additional options (upstream/downstream deps)
└────────────────────────────────────┘

Most common debugging flow:
1. Pipeline fails at "transform"
2. Click "View Log" → see error message
3. If transient error: click "Clear" → scheduler re-runs task
4. If code bug: fix code → click "Clear" → scheduler re-runs with new code
5. If false alarm: click "Mark as Success" → pipeline continues
```

The "Clear" action is the most important for operational debugging. It doesn't change the code — it just resets the task's state so the scheduler will attempt it again. This is how you recover from transient failures (network timeout, temporary disk full, API rate limit) without touching the underlying code.]

## Code View

By clicking on the Code button, you can also view the complete Python source code that defines your DAG. Here, we see the building blocks of your DAG, such as the library imports and the individual task definitions, which invoke bash operators in this case.

[ENRICHED: concrete example — code view:

```python
# Code view shows the actual DAG file content
# This is useful for debugging without SSH access to the server

# LIBRARY IMPORTS
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# DEFAULT ARGS
default_args = {
    'owner': 'data-team',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
}

# DAG DEFINITION
with DAG(
    dag_id='simple-example',
    default_args=default_args,
    schedule_interval='@daily',
) as dag:

    # TASK DEFINITIONS
    print_hello = BashOperator(
        task_id='print_hello',
        bash_command='echo "Hello from Airflow"'
    )

    execute_function = BashOperator(
        task_id='execute_function',
        bash_command='python /opt/scripts/process.py'
    )

    # DEPENDENCIES
    print_hello >> execute_function
```

The Code view is read-only in the UI — you cannot edit it there. But it's invaluable for: (1) verifying the deployed code matches what you expect, (2) debugging without SSH access, (3) reviewing recent code changes (the Code view shows the current file on disk).]

## Task Duration View

By clicking on "Task duration", you can view a timeline chart of your DAG's task durations to see how they have been performing. Here, you can toggle the tasks to highlight the last n runs.

[ENRICHED: concrete example — task duration chart:

```
TASK DURATION: sales_pipeline (last 10 runs)

Duration (seconds)
  60 │
  50 │         ╭─╮
  40 │    ╭─╮  │ │     ╭─╮        ╭─╮
  30 │    │ │  │ │ ╭─╮ │ │  ╭─╮  │ │
  20 │╭─╮ │ │  │ │ │ │ │ │  │ │  │ │
  10 ││ │ │ │  │ │ │ │ │ │  │ │  │ │
   0 │└─┘ └─┘  └─┘ └─┘ └─┘  └─┘  └─┘
     └──────────────────────────────────
      R1  R2   R3  R4  R5   R6  R7  R8  R9  R10

Legend: ╭─╮ = transform task duration
        Other tasks (extract, load) are flat at ~5s

Observation: transform task takes 40-50s consistently
             (processing ~10M rows — expected behavior)
             
Anomaly detection: if transform suddenly takes 300s,
                   investigate: data volume spike? network issue?
```

The Task Duration view answers: "Is my pipeline getting slower over time?" If you see a gradual upward trend, it usually means: (1) data volume is growing (most common), (2) database queries are degrading (missing indexes, table bloat), (3) network latency is increasing. This is your early warning system for capacity planning.]

## Summary

In this video, you learned that:
- Apache Airflow has a rich UI that simplifies working with data pipelines,
- you can visualize your DAG in several informative ways, including graph and grid mode,
- you can also review the Python code that originally defined your DAG,
- you can analyze the duration of each task in your DAG over multiple runs, and
- finally, you can select context metadata for any task instance.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | DAGs view | Definition | Defined "crontab format" — 5-field schedule syntax with examples and Airflow aliases | HIGH |
| 2 | DAGs view | Concrete example | DAGs view table mockup showing columns: name, owner, status, schedule, last/next run, actions | HIGH |
| 3 | DAGs view | Added specificity | Pause toggle explained: disable broken pipeline without deleting; scheduler ignores paused DAGs | HIGH |
| 4 | Grid view | Concrete example | 4-run grid showing extract/transform/load/send_email with color-coded statuses | HIGH |
| 5 | Grid view | Added specificity | Grid as debugging tool: identify failed task, recurring patterns, task duration history | HIGH |
| 6 | Graph view | Concrete example | Graph view mockup: print_hello (BashOp) → execute_function (PythonOp) with color coding | HIGH |
| 7 | Context menu | Concrete example | 9-option context menu table with descriptions and common debugging flow (Clear → re-run) | HIGH |
| 8 | Context menu | Added specificity | "Clear" action explained: resets task state without code change; recovers from transient failures | HIGH |
| 9 | Code view | Concrete example | Complete DAG file shown in code view with inline comments for each block | HIGH |
| 10 | Code view | Added specificity | Code view is read-only; useful for verifying deployed code, debugging without SSH, reviewing changes | HIGH |
| 11 | Task duration | Concrete example | Duration chart mockup showing transform task 40-50s baseline with anomaly detection guidance | HIGH |
| 12 | Task duration | Added specificity | Duration trend interpretation: data volume growth, query degradation, network latency | HIGH |

<!-- EXTRACTION_CHECKLIST: 38 sentences extracted, 38 sentences in output -->
