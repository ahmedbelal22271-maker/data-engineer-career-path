**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines

# Advantages of Representing Data Pipelines as DAGs in Apache Airflow

## Learning Objectives

After watching this video, you will be able to:
- define what a DAG is,
- describe workflows as DAGs of tasks and dependencies,
- outline the components of a DAG definition file,
- describe how Apache Airflow Scheduler executes tasks on an array of workers, and
- list key advantages of defining workflows as code.

## What is a DAG?

A DAG is a special kind of graph. A simple graph consists of nodes and edges like this. Here, the circles are called nodes, and the lines connecting pairs of nodes are called edges. A directed graph is also a graph, but it has more structure. As you can see here, each edge has a specified direction. It connects a starting node with another node. Lastly, the acyclic part means there are no loops or sequences of directed edges that return to a node in the chain, such as the red cycle shown here.

[ENRICHED: defined "node" — in graph theory, a node (also called a vertex) is a discrete unit that represents an entity: a data source, a transformation step, a load operation, or any processing stage. In Airflow, each node is a task — one atomic unit of work like "extract CSV from S3" or "run SQL query."]

[ENRICHED: defined "edge" — an edge is a connection between two nodes that represents a dependency. An edge from Task A to Task B means: "B cannot start until A finishes." Edges define execution order without hardcoding sequence numbers — you define relationships, not timelines.]

[ENRICHED: concrete example — graph types comparison:

```
SIMPLE GRAPH (undirected):
  A --- B --- C
  (A connects to B, B connects to C — no direction specified)

DIRECTED GRAPH:
  A → B → C
  (A must come before B, B must come before C)

DIRECTED CYCLIC GRAPH (NOT a DAG):
  A → B → C → A  ← cycle! Airflow cannot handle this.
  (C points back to A — infinite loop possible)

DIRECTED ACYCLIC GRAPH (DAG):
  A → B → D
  A → C → D
  (Two paths from A to D, no cycles — Airflow can execute this)
```

The acyclic constraint is not just academic — it's a safety guarantee. If a cycle existed, the scheduler would never reach a "done" state because it would keep looping through the cycle forever.]

## DAG Examples

Let's take a look at a few examples of DAGs. The simplest non-trivial DAG has a single directed edge and looks like this. It has a single root node, which is connected to a single terminal node. Here's another DAG, which we've already seen. It also has single root and terminal nodes. Here's an example of a tree, which is a commonly used graph for representing family trees or directory structures. All trees are DAGs, but not all DAGs are trees. For example, this DAG is not a tree since it has more than one root node. A dag doesn't impose those restrictions, so a single node can have multiple parents, and there may be multiple nodes with no parents.

[ENRICHED: added specificity — tree vs DAG distinction:

```
TREE (a special case of DAG):
       Root
      / | \
     A  B  C
    / \
   D   E

Rules: exactly one root, each node has at most one parent.
Example: Unix directory structure, org charts

DAG (more general — not a tree):
  A → B → D
  C → B
  C → E

Rules: multiple roots allowed (A and C), multiple parents allowed (B has parents A and C).
Example: Airflow pipeline where two independent data sources feed into one transformation.
```

In Airflow, real pipelines are almost always DAGs, not trees. A common pattern: multiple independent extract tasks (multiple roots) feeding into one transform task (multiple parents), which feeds into multiple load tasks (multiple children).]

## DAGs as Workflows

DAGs are used to represent workflows or pipelines in Apache Airflow. Each task performed by your data pipeline is represented as a node in a DAG, while each of the dependencies between two tasks in your pipeline are represented as a directed edge in the DAG. In other words, edges define the order in which the two tasks should run, thus, DAGs are used in Airflow to define what tasks should run and in what sequence they should run.

[ENRICHED: concrete example — mapping a real pipeline to a DAG:

```
REAL PIPELINE: "Nightly Sales Report"

Step 1: Extract sales data from PostgreSQL
Step 2: Extract customer data from MongoDB
Step 3: Transform — join sales with customers
Step 4: Transform — calculate daily aggregates
Step 5: Load aggregated data to Redshift
Step 6: Generate report and email team

DAG REPRESENTATION:
  extract_sales (node) ──→ join_sales_customers (node)
                              ↓
  extract_customers (node) ──→ join_sales_customers (node)
                              ↓
                         calculate_aggregates (node)
                              ↓
                         load_to_redshift (node)
                              ↓
                         send_report_email (node)

Key insight: Steps 1 and 2 can run IN PARALLEL (no edge between them).
The scheduler knows this automatically from the DAG structure.
Without a DAG, you'd have to manually code: "run Step 1, then Step 2,
then Step 3" — losing the parallelism opportunity.
```

This is the core value proposition: you declare relationships (dependencies), not execution order. The scheduler figures out the optimal parallel execution automatically.]

## DAG Definition File

A DAG is defined in a Python script, which represents the DAG structure, thus, the tasks and their dependencies are defined as code. Also, scheduling instructions are specified as code in the DAG script.

[ENRICHED: defined "DAG definition file" — the Python script (typically stored in Airflow's `dags/` directory) that declares everything about a pipeline: what tasks exist, what each task does, what order they run in, and when the pipeline should execute. The scheduler parses this file on a configurable interval (default: every 30 seconds) to detect changes.]

## Tasks and Operators

Let's take a closer look at the nodes or tasks in a DAG. Just like the DAG itself, each task performed within your DAG is also written in Python. Each task implements an operator, for example, a Python operator is used to deploy some Python code, a SQL operator to run a SQL query, and a bash operator can be used to run a bash command. Operators are used to define what each task in your DAG does. Sensors are a class of operators which are used to poll for a certain time or condition to be met. For example, you can use a sensor to check every 30 seconds whether a file exists or whether another DAG has finished running. There are many other types of operators, including email and HTTP request operators.

[ENRICHED: added specificity — operator categories:

| Category | Operator | What It Does | Example Use Case |
|----------|----------|-------------|------------------|
| **Action** | `PythonOperator` | Executes a Python function | Run a data transformation |
| **Action** | `BashOperator` | Executes a shell command | Run a shell script |
| **Action** | `PostgresOperator` | Runs a SQL query | Create table, insert data |
| **Action** | `EmailOperator` | Sends an email | Alert on failure |
| **Transfer** | `S3ToRedshiftOperator` | Copies data between systems | Load CSV from S3 to Redshift |
| **Transfer** | `GoogleCloudStorageToBigQueryOperator` | Cloud-to-cloud transfer | Load GCS file to BigQuery |
| **Sensor** | `S3KeySensor` | Waits for a file to appear in S3 | Wait for upstream upload |
| **Sensor** | `HttpSensor` | Waits for an HTTP endpoint to return 200 | Wait for API availability |
| **Sensor** | `TimeSensor` | Waits until a specific time | Schedule-based triggers |

The key distinction: Action operators DO work immediately. Sensors POLL (check repeatedly) until a condition is met, then the next task can run. Sensors consume a worker slot while polling — this is a tradeoff: simplicity vs resource efficiency.]

[ENRICHED: concrete example — operator in action:

```python
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.s3 import S3KeySensor

# PythonOperator: runs a Python function
transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=my_transform_function,
    op_kwargs={'input_path': '/data/raw/', 'output_path': '/data/clean/'}
)

# BashOperator: runs a shell command
compress_files = BashOperator(
    task_id='compress_files',
    bash_command='gzip /data/clean/*.csv'
)

# Sensor: waits for a condition
wait_for_upload = S3KeySensor(
    task_id='wait_for_upload',
    bucket_name='my-bucket',
    bucket_key='incoming/daily_sales.csv',
    poke_interval=30,  # Check every 30 seconds
    timeout=3600       # Give up after 1 hour
)

# Dependencies
wait_for_upload >> transform_data >> compress_files
```

Each operator encapsulates all the connection logic, error handling, and retry logic for its specific system. You don't write HTTP clients, database connections, or file system checks — the operator handles it.]

## DAG Script Structure

An Apache Airflow DAG is a Python script consisting of the following logical blocks; library imports, DAG arguments, DAG definition, task definitions, and task pipeline. Let's briefly go over an example. The first block of your DAG definition script is where you import any Python libraries that you require, for example, the from Airflow import DAG command to import the DAG module from the airflow collection. Next block of code is for specifying default arguments for your DAG, such as its default start date. Next comes the DAG definition or instantiation block for your DAG, which specifies things like your default arguments.

[ENRICHED: concrete example — complete 5-block DAG structure:

```python
# BLOCK 1: Library imports
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# BLOCK 2: DAG arguments (default_args)
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,        # Don't wait for previous run to finish
    'email': ['team@company.com'],
    'email_on_failure': True,        # Send email if task fails
    'retries': 2,                    # Retry twice before failing
    'retry_delay': timedelta(minutes=5),  # Wait 5 minutes between retries
    'start_date': datetime(2026, 1, 1),   # Pipeline starts Jan 1, 2026
}

# BLOCK 3: DAG definition (instantiation)
with DAG(
    dag_id='nightly_sales_pipeline',
    default_args=default_args,
    description='Extract, transform, and load nightly sales data',
    schedule_interval='@daily',      # Run once per day
    catchup=False,                   # Don't backfill missed runs
    max_active_runs=1                # Only one instance at a time
) as dag:

    # BLOCK 4: Task definitions
    extract = BashOperator(
        task_id='extract',
        bash_command='python /opt/airflow/scripts/extract.py'
    )

    transform = BashOperator(
        task_id='transform',
        bash_command='python /opt/airflow/scripts/transform.py'
    )

    load = BashOperator(
        task_id='load',
        bash_command='python /opt/airflow/scripts/load.py'
    )

    # BLOCK 5: Task pipeline (dependencies)
    extract >> transform >> load
```

The `>>` operator is syntactic sugar for `set_downstream()`. `extract >> transform` means "transform depends on extract — run extract first."]

## Scheduler Deployment

Continuing along with our example DAG code, individual task definitions, which are the nodes of the DAG, form your DAGs next building block. In this example, we have two tasks which happen to be bash operators. Finally, the task pipeline specifies the dependencies between your tasks. Here, Task 2 depends on the result of Task 1, and this forms the last logical block of your DAG script. Your new DAG has been created, but it hasn't yet been deployed. To that end, Airflow Scheduler is designed to run as a persistent service within the Airflow production environment. Apache Airflow Scheduler can be used to deploy your workflow on an array of workers. It follows the tasks and dependencies that you specified in your DAG. Once you start an Airflow Scheduler instance, your DAGs will start running based on the start date you specified as code in each of your DAGs. After that, the scheduler triggers each subsequent DAG run according to the schedule interval that you specified.

[ENRICHED: concrete example — scheduler lifecycle:

```
TIMELINE: Nightly Sales Pipeline

Jan 1, 2026: Scheduler starts
  → Reads DAG file, sees schedule_interval='@daily', start_date=Jan 1
  → Checks: "Should I run? Yes — Jan 1 has passed and no run exists"
  → Triggers DAG Run #1 (backfill for Jan 1)

Jan 2, 2026, 00:00 UTC: Scheduler triggers DAG Run #2
  → extract → transform → load
  → All tasks SUCCESS
  → Next run scheduled for Jan 3

Jan 3, 2026, 00:00 UTC: Scheduler triggers DAG Run #3
  → extract SUCCESS, transform FAILED
  → load: UPSTREAM FAILED (never runs)
  → Scheduler logs: " DAG Run #3 FAILED at transform"
  → Next run still scheduled for Jan 4 (failed run doesn't block future runs)

Jan 4, 2026, 00:00 UTC: Scheduler triggers DAG Run #4
  → extract → transform → load
  → All tasks SUCCESS (the failure was transient)
  → Pipeline self-healed without human intervention
```

The `catchup=False` parameter is critical: if set to `True` (default), Airflow would try to backfill every missed run from Jan 1 to today. For a pipeline running for 6 months, that's 180 DAG runs — potentially thousands of tasks. Always set `catchup=False` unless you specifically need backfill.]

## Advantages of Workflows as Code

One of the key advantages of Apache Airflow's approach to representing data pipelines as DAGs is the fact that they are expressed as code. When workflows are defined as code, they become more maintainable. Developers can follow explicitly what has been specified by reading the code. Versionable; code revisions can easily be tracked by a version control system, such as Git. Collaborative; teams of developers can easily collaborate on both development and maintenance of the code for the entire workflow. Testable; any revisions can be passed through unit tests to ensure the code still works as intended.

[ENRICHED: added specificity — the four advantages in detail:

| Advantage | What It Means | Concrete Benefit |
|-----------|--------------|------------------|
| **Maintainable** | DAG files are readable Python — no XML, no YAML, no custom DSL | New developer reads one file and understands the entire pipeline |
| **Versionable** | Git tracks every change with diffs and blame | "Who changed the load step last week?" → `git log --oneline load.py` |
| **Collaborative** | Multiple developers can edit different tasks, merge via PR, resolve conflicts | Team of 5 engineers can work on 5 different pipelines without stepping on each other |
| **Testable** | Python unit tests work on DAG files | `pytest test_dags.py` — verify task count, dependency order, parameter validity |

[ENRICHED: concrete example — testing a DAG:

```python
# test_dags.py — unit test for your DAG
def test_dag_import():
    """Verify DAG file parses without errors"""
    from nightly_sales_pipeline import dag
    assert dag is not None
    assert dag.dag_id == 'nightly_sales_pipeline'

def test_task_count():
    """Verify correct number of tasks"""
    from nightly_sales_pipeline import dag
    assert len(dag.tasks) == 3

def test_dependency_order():
    """Verify tasks run in correct order"""
    from nightly_sales_pipeline import dag
    extract = dag.get_task('extract')
    transform = dag.get_task('transform')
    load = dag.get_task('load')
    
    # transform depends on extract
    assert transform.task_id in [t.task_id for t in extract.downstream_list]
    # load depends on transform
    assert load.task_id in [t.task_id for t in transform.downstream_list]

# Run: pytest test_dags.py
# If someone accidentally changes extract >> transform to load >> extract,
# this test catches it immediately.
```

Compare this to traditional pipeline tools where you'd click through a GUI to configure steps — there's no way to version-control a GUI configuration or write automated tests for it.]

## Summary

In this video, you learned that in Apache Airflow, DAGs are workflows defined as Python code. Tasks, which are nodes in your DAG, are created by implementing air flows built-in operators. Pipelines are specified as dependencies between tasks, which are the directed edges between nodes in your DAG. Airflow Scheduler schedules and deploys your DAGs. Finally, the key advantage of Apache Airflow's approach to representing data pipelines as DAGs is the fact that they are expressed as code. Accordingly, it makes your data pipelines more maintainable, testable, and collaborative.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | What is a DAG | Definition | Defined "node" — discrete unit representing an entity; in Airflow, a task | HIGH |
| 2 | What is a DAG | Definition | Defined "edge" — connection between nodes representing dependency; defines execution order | HIGH |
| 3 | What is a DAG | Concrete example | Graph types comparison: simple, directed, cyclic (not DAG), acyclic (DAG) with ASCII diagrams | HIGH |
| 4 | What is a DAG | Added specificity | Tree vs DAG distinction — trees have one root, one parent per node; DAGs allow multiple roots and parents | HIGH |
| 5 | DAG as workflows | Concrete example | Real pipeline mapped to DAG: extract_sales + extract_customers → join → aggregate → load → email | HIGH |
| 6 | DAG definition file | Definition | Defined "DAG definition file" — Python script in dags/ directory parsed every 30 seconds | HIGH |
| 7 | Tasks and operators | Added specificity | 9-row operator category table: Action, Transfer, Sensor with examples and use cases | HIGH |
| 8 | Tasks and operators | Clarified concept | Operators vs Sensors: operators DO work, sensors POLL; sensor tradeoff: simplicity vs worker slot consumption | HIGH |
| 9 | Tasks and operators | Concrete example | PythonOperator, BashOperator, S3KeySensor code example with dependencies | HIGH |
| 10 | DAG script structure | Concrete example | Complete 5-block DAG: imports, args, definition, tasks, pipeline with inline comments | HIGH |
| 11 | Scheduler deployment | Concrete example | Scheduler lifecycle: 4-day timeline showing backfill, failure, self-healing; catchup=False explained | HIGH |
| 12 | Advantages as code | Added specificity | 4-advantage table with concrete benefits: Maintainable, Versionable, Collaborative, Testable | HIGH |
| 13 | Advantages as code | Concrete example | Unit test for DAG: test_import, test_task_count, test_dependency_order | HIGH |

<!-- EXTRACTION_CHECKLIST: 47 sentences extracted, 47 sentences in output -->
