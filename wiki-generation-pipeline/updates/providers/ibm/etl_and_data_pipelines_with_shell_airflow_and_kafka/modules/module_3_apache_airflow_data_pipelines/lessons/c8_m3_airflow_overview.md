**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines

# Apache Airflow Overview

## Learning Objectives

After watching this video, you will be able to:
- recognize Apache Airflow as a platform to programmatically author, schedule, and monitor workflows,
- list the main features and principles of Apache Airflow, and
- list common use cases for Apache Airflow.

## What is Apache Airflow?

Apache Airflow is a great, open-source workflow orchestration tool that is supported by an active community. It is a platform that lets you build and run workflows, such as batch data pipelines. With Apache Airflow, a workflow is represented as a directed acyclic graph (DAG). The DAG is made of tasks that are arranged in a specific order of execution.

[ENRICHED: defined "workflow orchestration" — the automated coordination, scheduling, and monitoring of complex data tasks. Instead of manually running scripts in order and checking if each step succeeded before starting the next, an orchestrator handles this automatically: it knows which tasks depend on which, runs them in the right order, retries failed tasks, and alerts you when something goes wrong. Think of it as a conductor for an orchestra — each musician (task) plays their part, but the conductor (orchestrator) ensures they play in sync, at the right time, and handles it when someone makes a mistake.]

[ENRICHED: defined "Directed Acyclic Graph (DAG)" — a graph is a collection of nodes (tasks) connected by edges (dependencies). "Directed" means the edges have direction — Task A → Task B means A must finish before B starts. "Acyclic" means there are no cycles — you can't have A → B → C → A (that would be an infinite loop). A DAG defines: (1) what tasks exist, (2) what order they run in, (3) which tasks depend on others. Example:

```
DAG: "nightly_sales_pipeline"
  Task 1: extract_data (no dependencies — runs first)
  Task 2: clean_data (depends on Task 1)
  Task 3: aggregate_sales (depends on Task 2)
  Task 4: load_to_warehouse (depends on Task 3)
  Task 5: send_report_email (depends on Task 4)

Execution order: 1 → 2 → 3 → 4 → 5
If Task 3 fails: Tasks 4 and 5 never run (dependencies not met)
```

The "acyclic" constraint is critical: without it, the scheduler could enter an infinite loop. DAGs guarantee finite execution.]

[ENRICHED: important clarification — "Apache Airflow is not a data streaming solution. Apache Airflow is a workflow manager, and is not an event or data streaming solution." This distinction matters: Airflow orchestrates batch workflows (run every hour, process yesterday's data). It does NOT handle real-time event streams (process each event as it arrives). For streaming, you need Apache Kafka, Apache Flink, or Apache Spark Streaming. Airflow can *trigger* a streaming job, but it doesn't *run* the streaming logic itself. Analogy: Airflow is the project manager who schedules the work; Kafka is the worker who processes events in real time.]

## Airflow Architecture

Let's take a look at a simplified overview of Apache Airflow's basic components.

[ENRICHED: added specificity — Airflow's architecture has 5 core components that work together:]

| Component | What It Does | Analogy |
|-----------|-------------|---------|
| **Scheduler** | Handles triggering of all scheduled workflows. Responsible for submitting individual tasks from each scheduled workflow to the executor. | The dispatcher — decides *what* runs and *when* |
| **Executor** | Handles running of tasks by assigning them to workers, which then run the tasks. | The foreman — assigns work to available workers |
| **Workers** | Individual processes that execute tasks. Can scale horizontally (add more workers for more parallelism). | The workers — actually do the work |
| **Web Server** | Provides a user-friendly GUI. From this UI, you can inspect, trigger, and debug any of your DAGs and their individual tasks. | The dashboard — lets you see and control everything |
| **Metadata Database** | Used by the scheduler, executor, and web server to store the state of each DAG and its tasks. | The ledger — remembers everything that happened |

[ENRICHED: concrete example — here's what happens when a DAG runs:

```
1. SCHEDULER checks metadata DB: "sales_nightly_load DAG is scheduled for 2 AM"
2. SCHEDULER reads DAG file from DAG directory
3. SCHEDULER determines: "extract_data task has no dependencies — ready to run"
4. SCHEDULER submits extract_data to EXECUTOR
5. EXECUTOR checks: "Worker 3 is idle — assign task to Worker 3"
6. WORKER 3 picks up task, starts running extract_data
7. WORKER 3 finishes → updates metadata DB: "extract_data = SUCCESS"
8. SCHEDULER sees: "clean_data depends on extract_data — extract_data is SUCCESS — clean_data is ready"
9. SCHEDULER submits clean_data to EXECUTOR
10. ... process repeats until all tasks complete
11. WEB SERVER shows real-time status: "sales_nightly_load: 4/5 tasks SUCCESS, 1 RUNNING"
```

The DAG directory contains all of your DAG files, ready to be accessed by the scheduler, the executor, and each of its employed workers.]

## Task State Lifecycle

Let's have a look at the life cycle of a task's state. In this diagram, you can see how Apache Airflow might assign states to a task during its lifecycle.

[ENRICHED: added specificity — Airflow tasks go through a defined state machine. Understanding these states is critical for debugging production pipelines:]

| State | What It Means | When You See It |
|-------|--------------|-----------------|
| **No status** | The task has not yet been queued for execution. | Initial state before the DAG run starts |
| **Scheduled** | The scheduler has determined that the task's dependencies are met and has scheduled it to run. | Between DAG parse and task submission |
| **Removed** | For some reason, the task has vanished from the DAG since the run started. | Rare — usually a code change during a running DAG |
| **Upstream failed** | An upstream task has failed. | Common — one broken step stops all downstream work |
| **Queued** | The task has been assigned to the executor, and is waiting for a worker to become available. | All workers are busy — task waits in queue |
| **Running** | The task is being run by a worker. | Task is actively executing |
| **Success** | The task completed successfully, and no errors were encountered. | Goal state — task finished cleanly |
| **Failed** | The task could not be completed successfully due to an error. | Something broke — needs investigation |
| **Up for retry** | The task will be rescheduled as per the retrial configuration. | Transient failure — Airflow will try again |

```
IDEAL TASK LIFECYCLE:
No status → Scheduled → Queued → Running → Success

COMMON FAILURE LIFECYCLE:
No status → Scheduled → Queued → Running → Failed → Up for retry → Running → Success

UPSTREAM FAILURE:
No status → Scheduled → Upstream failed (task never runs)
```

[ENRICHED: concrete example — imagine a 4-task pipeline:

```
Task 1: extract_data     → SUCCESS
Task 2: clean_data       → RUNNING (slow — processing 10M rows)
Task 3: aggregate_sales  → UPSTREAM FAILED (Task 2 hasn't finished yet)
Task 4: load_to_warehouse → UPSTREAM FAILED (Task 3 never ran)

What happened:
- Task 1 finished successfully
- Task 2 started but is still running
- Task 3 depends on Task 2, but Task 2 isn't SUCCESS yet → "Upstream failed"
- Task 4 depends on Task 3, which never ran → "Upstream failed"

Once Task 2 finishes:
- Task 3 changes from "Upstream failed" → "Scheduled" → "Queued" → "Running"
- Task 4 waits for Task 3 to finish

If Task 2 fails:
- Task 3 stays "Upstream failed" permanently
- Task 4 stays "Upstream failed" permanently
- You get an alert: "sales_nightly_load DAG FAILED at Task 2"
```

This is why DAGs are powerful: the dependency graph automatically handles cascading failures. You don't need to write "if Task 2 fails, don't run Task 3" — the DAG structure enforces it.]

## Five Main Features

Now, let's have a look at the five main features and benefits of Apache Airflow.

### 1. Pure Python

Create your workflows using standard Python. This allows you to maintain full flexibility when building your data pipelines.

[ENRICHED: added specificity — "Pure Python" means your DAG files are regular Python scripts. No YAML, no JSON, no custom DSL. This gives you: (1) IDE support (autocomplete, linting, debugging), (2) version control (Git), (3) testing (pytest), (4) reuse (import functions from other modules), (5) dynamic generation (generate tasks in a loop based on a config file). Example:

```python
# A DAG file is just Python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG('sales_pipeline', start_date=datetime(2026, 1, 1), schedule='@daily') as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_data)
    transform = PythonOperator(task_id='transform', python_callable=transform_data)
    load = PythonOperator(task_id='load', python_callable=load_data)
    
    extract >> transform >> load  # Define dependencies with >> operator
```

Compare this to a non-Python orchestrator where you'd write YAML with custom syntax — Python gives you full programming power.]

### 2. Useful UI

Provides the ability to monitor the workflow, schedule the workflow, or manually run it, and manage the workflows via a sophisticated web app, offering you full insight into the status of your tasks.

[ENRICHED: concrete example — the Airflow web UI shows:

```
DAG: sales_nightly_load
├── Last run: 2026-07-23 02:00 UTC
├── Status: ✅ SUCCESS
├── Duration: 45 seconds
├── Tasks: 5/5 SUCCESS
│   ├── extract_data: ✅ (12s)
│   ├── clean_data: ✅ (18s)
│   ├── aggregate_sales: ✅ (8s)
│   ├── load_to_warehouse: ✅ (5s)
│   └── send_report_email: ✅ (2s)
└── History: Last 10 runs: ✅✅✅✅✅✅✅✅✅✅

[Graph View] [Tree View] [Calendar View] [Gantt View]
```

You can click any task to see its logs, retry it, or mark it as success/failed. The Gantt view shows exactly how long each task took and where bottlenecks are.]

### 3. Integration

Apache Airflow provides many plug-and-play integrations, such as IBM Data Band that helps achieve continuous observability and monitoring.

[ENRICHED: ecosystem — Airflow has 80+ provider packages that integrate with external systems. Common integrations:

| Category | Tools | What Airflow Can Do |
|----------|-------|---------------------|
| **Cloud Storage** | S3, GCS, Azure Blob | Extract from / load to cloud storage |
| **Databases** | PostgreSQL, MySQL, BigQuery, Redshift | Run queries, load data |
| **Streaming** | Kafka, Kinesis | Trigger streaming jobs |
| **ML** | MLflow, SageMaker, Vertex AI | Train models, deploy endpoints |
| **Monitoring** | Datadog, PagerDuty, Slack | Send alerts, update dashboards |
| **Orchestration** | Kubernetes, Docker | Deploy containerized tasks |

Each integration is an "operator" — a pre-built Python class that handles the connection and API calls. You don't write HTTP requests; you use `S3ToRedshiftOperator` and it handles everything.]

### 4. Easy to Use

A workflow is easy to create and deploy for anyone with prior knowledge of Python. The Airflow pipeline can combine many tasks created with many options of operators and sensors without any limits. Airflow does not limit the scope of your pipelines.

[ENRICHED: clarified concept — "operators" and "sensors":

**Operators** are the building blocks — they define *what* a task does. Examples:
- `PythonOperator` — runs a Python function
- `BashOperator` — runs a shell command
- `PostgresOperator` — runs a SQL query
- `S3ToRedshiftOperator` — copies data from S3 to Redshift

**Sensors** are a special type of operator that *waits* for something to happen. Examples:
- `S3KeySensor` — waits until a file appears in S3
- `HttpSensor` — waits until an HTTP endpoint returns 200
- `TimeSensor` — waits until a specific time

The difference: operators *do* work, sensors *wait* for conditions. A sensor is useful when your pipeline depends on external data arriving (e.g., "wait until yesterday's CSV file is uploaded to S3 before processing it").]

### 5. Open Source

Whenever you want to share your improvement, you can do this by opening a pull request. Airflow has many active users who are sharing their experiences in the Apache Airflow community.

[ENRICHED: ecosystem — Airflow was created at Airbnb in 2014, open-sourced in 2016, and donated to the Apache Software Foundation in 2019. It has 35,000+ GitHub stars and 2,000+ contributors. The open-source model means: (1) bugs are found and fixed by the community, (2) new integrations are added constantly, (3) documentation and examples are crowdsourced, (4) you can fork and customize for your needs. The tradeoff: open-source Airflow requires you to manage the infrastructure (scheduler, workers, metadata DB). Managed alternatives: Amazon Managed Workflows for Apache Airflow (MWAA), Google Cloud Composer, Astronomer.]

## Four Main Principles

Apache Airflow pipelines are built on four main principles.

### 1. Scalable

Airflow has a modular architecture and uses a message queue to orchestrate an arbitrary number of workers. It is ready to scale to infinity.

[ENRICHED: concrete example — Airflow's scalability works through the executor:

```
SMALL DEPLOYMENT (1 machine):
Scheduler + Executor + 1 Worker + Metadata DB = all on one server
Handles: 50 DAGs, 500 tasks/day

MEDIUM DEPLOYMENT (message queue):
Scheduler + Executor → Redis/RabbitMQ → 5 Workers + Metadata DB
Handles: 500 DAGs, 5,000 tasks/day

LARGE DEPLOYMENT (Kubernetes):
Scheduler + Executor → Redis → 100 Workers (auto-scaled) + PostgreSQL
Handles: 5,000 DAGs, 50,000 tasks/day

The message queue is the key: it decouples the scheduler from workers.
The scheduler doesn't care how many workers exist — it just publishes tasks
to the queue. Workers pull tasks from the queue. Add more workers = more parallelism.
```

The "scale to infinity" claim is theoretical — in practice, you hit limits at the metadata database (thousands of concurrent tasks) and scheduler (parsing thousands of DAG files). But for most organizations, Airflow scales足够大.]

### 2. Dynamic

Airflow pipelines are defined in Python, and allow dynamic pipeline generation. Thus, your pipelines can contain multiple simultaneous tasks.

[ENRICHED: concrete example — "dynamic" means you can generate tasks programmatically:

```python
# STATIC: manually define each task
task1 = PythonOperator(task_id='process_us_sales', ...)
task2 = PythonOperator(task_id='process_eu_sales', ...)
task3 = PythonOperator(task_id='process_apac_sales', ...)

# DYNAMIC: generate tasks from a config file
regions = ['us', 'eu', 'apac']
for region in regions:
    PythonOperator(
        task_id=f'process_{region}_sales',
        python_callable=process_sales,
        op_kwargs={'region': region}
    )

# Result: 3 tasks generated automatically from a list
# Add a new region? Just add it to the list — no new code needed
```

This is powerful for pipelines that process multiple datasets, regions, or tables — you write the logic once, and Airflow generates N tasks from a config.]

### 3. Extensible

You can easily define your own operators and extend libraries to suit your environment.

[ENRICHED: concrete example — if no existing operator fits your needs, you create one:

```python
# Custom operator: check if a database table has data
class TableHasDataSensor(BaseSensorOperator):
    def __init__(self, table_name, min_rows=1, **kwargs):
        super().__init__(**kwargs)
        self.table_name = table_name
        self.min_rows = min_rows
    
    def poke(self, context):
        # Check if table has enough rows
        result = PostgresHook(postgres_conn_id='my_db').get_first(
            f"SELECT COUNT(*) FROM {self.table_name}"
        )
        return result[0] >= self.min_rows

# Use it in your DAG
wait_for_data = TableHasDataSensor(
    task_id='wait_for_sales_data',
    table_name='raw_sales',
    min_rows=1000,
    poke_interval=60  # Check every 60 seconds
)
```

This extensibility means Airflow can orchestrate *anything* — even systems that don't have pre-built operators.]

### 4. Lean

Airflow pipelines are lean and explicit. Parameterization is built into its core using the powerful Jinja templating engine.

[ENRICHED: defined "Jinja templating" — Jinja is a Python template engine that lets you embed dynamic values in static text. In Airflow, you use Jinja to parameterize SQL queries, file paths, and command arguments:

```python
# Jinja template in an Airflow task
sql = """
    SELECT * FROM sales
    WHERE date = '{{ ds }}'  -- ds is an Airflow variable: the execution date
    AND region = '{{ params.region }}'  -- params are passed from the DAG
"""

# At runtime, Airflow replaces:
# {{ ds }} → '2026-07-22'
# {{ params.region }} → 'us'

# Final SQL:
# SELECT * FROM sales WHERE date = '2026-07-22' AND region = 'us'
```

"Lean" means Airflow doesn't add unnecessary abstraction — your DAG files are readable Python with embedded templates, not verbose XML or JSON configurations.]

## Real-World Use Cases

Apache Airflow supports various companies in reaching their goals. Let's look at some examples.

| Company | What They Use Airflow For | Key Benefit |
|---------|--------------------------|-------------|
| **Adobe Experience Platform** | Uses Airflow's plugin interface to write custom operators to meet their use cases. Airflow manages all scheduling and dependency management. | Focus on business use cases, not infrastructure |
| **Adyen** | Extended existing operators and sensors to make writing ETL DAGs as easy as possible. | Faster ETL development |
| **Big Fish** | Programmatically controls workflows and efficiently uses the Web UI to monitor tasks. | Real-time pipeline visibility |
| **Walmart** | Automates data processing tasks, such as extracting data from databases and loading data into its data warehouse. | Automated data warehouse loading |

[ENRICHED: ecosystem — these examples show Airflow's versatility: Adobe uses it for custom data platform operations, Adyen for financial ETL, Big Fish for gaming analytics, and Walmart for retail data warehousing. The common pattern: all four companies needed to orchestrate multiple data tasks with dependencies, scheduling, and monitoring. Airflow provides all three out of the box.]

## Summary

In this video, you learned that:
- Apache Airflow is a platform to programmatically author, schedule, and monitor workflows,
- the five main features of Airflow are its use of Python, its intuitive and useful user interface, extensive plug-and-play integrations, ease of use, and the fact that it is open source,
- you also learned that Apache Airflow is scalable, dynamic, extensible, and lean,
- finally, defining and organizing machine learning and pipeline dependencies with Apache Airflow is one of the common use cases.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | What is Airflow | Definition | Defined "workflow orchestration" — automated coordination, scheduling, monitoring; conductor analogy | HIGH |
| 2 | What is Airflow | Definition | Defined DAG — directed (ordered), acyclic (no loops), graph (tasks + dependencies); ASCII example of sales pipeline DAG | HIGH |
| 3 | What is Airflow | Added specificity | Clarified Airflow is NOT a streaming solution — it orchestrates batch workflows; Kafka/Flink for streaming | HIGH |
| 4 | Architecture | Added specificity | 5-component table (Scheduler, Executor, Workers, Web Server, Metadata DB) with role and analogy | HIGH |
| 5 | Architecture | Concrete example | Step-by-step walkthrough of what happens when a DAG runs (11 steps from scheduler check to task completion) | HIGH |
| 6 | Task states | Added specificity | 9-state table with meaning and when to see each; ideal vs failure lifecycle diagrams | HIGH |
| 7 | Task states | Concrete example | 4-task pipeline showing cascading failures and recovery flow | HIGH |
| 8 | Features | Concrete example | Pure Python: DAG file code example showing PythonOperator, >> dependency operator, IDE benefits | HIGH |
| 9 | Features | Concrete example | Web UI: ASCII mockup of DAG status view with task durations and history | HIGH |
| 10 | Features | Ecosystem | 6-category integration table (Cloud Storage, Databases, Streaming, ML, Monitoring, Orchestration) | HIGH |
| 11 | Features | Clarified concept | Operators vs Sensors: operators DO work, sensors WAIT for conditions; S3KeySensor example | HIGH |
| 12 | Features | Ecosystem | Airflow history (Airbnb 2014 → Apache 2019), 35K+ stars, managed alternatives (MWAA, Composer, Astronomer) | HIGH |
| 13 | Principles | Concrete example | Scalability: small/medium/large deployment configs with worker counts and task capacity | HIGH |
| 14 | Principles | Concrete example | Dynamic: static vs dynamic task generation from config list, add region = no new code | HIGH |
| 15 | Principles | Concrete example | Extensible: custom TableHasDataSensor operator with poke logic | HIGH |
| 16 | Principles | Definition | Defined Jinja templating: {{ ds }} for execution date, {{ params.region }} for task parameters | HIGH |
| 17 | Use cases | Ecosystem | 4-company table (Adobe, Adyen, Big Fish, Walmart) with use case and key benefit | HIGH |

<!-- EXTRACTION_CHECKLIST: 42 sentences extracted, 42 sentences in output -->
