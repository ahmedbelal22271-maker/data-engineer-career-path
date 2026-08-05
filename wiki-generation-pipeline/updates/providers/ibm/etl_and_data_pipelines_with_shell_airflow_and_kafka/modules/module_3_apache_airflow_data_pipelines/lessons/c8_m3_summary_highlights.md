# Summary & Highlights

**Course 8:** ETL & Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines
**Video Type:** Reading (1:17)

---

Congratulations! You have completed this module. At this point, you know:

---

## Core Concepts

Apache Airflow is scalable, dynamic, extensible, and lean.

[ENRICHED: definition — the four defining characteristics of Apache Airflow:
- **Scalable**: Airflow scales horizontally by adding more worker nodes. The scheduler, triggerer, and web server can all run on separate machines. Celery or Kubernetes executors distribute task execution across a cluster.
- **Dynamic**: DAGs are written in Python — you can use loops, conditionals, and functions to dynamically generate tasks at runtime. No static XML or YAML configuration files.
- **Extensible**: Airflow has a plugin architecture and 2000+ community operators. You can write custom operators, hooks, sensors, and transfer operators. The provider model (e.g., `apache-airflow-providers-google`) lets you install only the integrations you need.
- **Lean**: Airflow's core is minimal — the scheduler, web server, and metadata database. Everything else (operators, hooks, sensors) is modular and optional. The default Celery executor adds Redis/RabbitMQ only if you need distributed execution.]

## Features

The five main features of Apache Airflow are pure Python, useful UI, integration, easy to use, and open-source.

[ENRICHED: added specificity — detailed breakdown of the 5 features:

| Feature | What It Means | Why It Matters |
|---------|---------------|----------------|
| **Pure Python** | DAGs are Python scripts — no XML, YAML, or DSL | Full IDE support (autocomplete, linting), unit testing with pytest, version control with Git |
| **Useful UI** | Web-based interface with Grid, Graph, Calendar, Duration, Details, Code views | Visual debugging, real-time monitoring, task log access, historical analysis — all without SSH |
| **Integration** | 2000+ community operators for cloud services, databases, APIs, ML frameworks | Pre-built connectors for GCS, S3, BigQuery, Snowflake, Spark, dbt, and hundreds more |
| **Easy to use** | Simple Python syntax, minimal boilerplate, clear error messages | A basic DAG can be written in 10 lines of code; the 5-block structure (imports → args → definition → tasks → pipeline) is intuitive |
| **Open-source** | Apache 2.0 license, active community, frequent releases | No vendor lock-in, free to use and modify, large ecosystem of tutorials and examples |

These 5 features are why Airflow became the de facto standard for workflow orchestration — it combines power (Python, integrations) with approachability (UI, simplicity) and openness (Apache 2.0).]

## Use Cases

A common use case is that Apache Airflow defines and organizes machine learning pipeline dependencies.

[ENRICHED: added specificity — Airflow's ML pipeline use case:
- **Data preparation**: extract raw data → clean → feature engineering → store in feature store
- **Model training**: trigger training job → evaluate metrics → register model if metrics pass threshold
- **Model deployment**: deploy to staging → run integration tests → promote to production
- **Monitoring**: schedule daily data quality checks, model drift detection, retraining triggers

The key insight: ML pipelines are DAGs. Each step (data prep, training, evaluation, deployment) is a task with dependencies. Airflow handles the orchestration, scheduling, retry logic, and monitoring — you just define the DAG. Popular ML frameworks integrated with Airflow: Kubeflow Pipelines, MLflow, SageMaker, Vertex AI, Databricks]

## Task and Pipeline Model

Tasks are created with Airflow operators.

Pipelines are specified as dependencies between tasks.

[ENRICHED: recap — the two-layer model:
1. **Operators** define WHAT each task does (BashOperator runs a shell command, PythonOperator runs a Python function, PostgresOperator runs SQL, S3ToGCSOperator transfers files)
2. **Dependencies** define WHEN tasks run (the `>>` operator sets execution order: `task1 >> task2` means "task2 runs after task1 succeeds")

This separation of concerns is why Airflow is called a "workflow orchestrator" — it doesn't do the work itself, it orchestrates when and how work happens across different systems]

## DAGs as Code

Pipeline DAGs defined as code are more maintainable, testable, and collaborative.

[ENRICHED: added specificity — the "DAGs as code" philosophy and its benefits:

| Benefit | How It Works | Real-World Impact |
|---------|-------------|-------------------|
| **Maintainable** | DAGs are Python files — use functions, classes, modules to DRY up repetition | A 100-task DAG can be generated from a loop over a config file, not 100 manually-written task definitions |
| **Testable** | Import DAG functions and test with pytest; use `DagBag` to parse and validate | Catch import errors, missing dependencies, and scheduling bugs before deploying to production |
| **Collaborative** | Git repos, pull requests, code reviews, CI/CD pipelines | Team members review DAG changes before merging; automated tests run on every PR; deployment is automated |

Compare this to UI-only orchestrators (e.g., legacy tools that require clicking through a web form to define tasks): code-based DAGs are version-controlled, diffable, and reviewable — the same benefits that made Git replace FTP for code deployment]

## User Interface

Apache Airflow has a rich UI that simplifies working with data pipelines.

You can visualize your DAG in graph or grid mode.

[ENRICHED: added specificity — the Airflow UI views and when to use each:

| View | Purpose | Best For |
|------|---------|----------|
| **Grid** | Matrix of tasks × runs, color-coded status | Monitoring running DAGs, spotting failures, checking task history |
| **Graph** | Visual dependency graph with color-coded nodes | Understanding workflow structure, debugging upstream failures |
| **Calendar** | Day-level run status overview | Spotting patterns (failures every Monday), verifying consistency |
| **Duration** | Line chart of DAG/task execution times | Performance monitoring, detecting slow tasks |
| **Task Duration** | Per-task timing over time | Identifying performance regressions |
| **Details** | All DAG metadata in structured format | Verifying configuration (catchup, schedule, concurrency) |
| **Code** | Read-only source code display | Version verification, sharing with colleagues |

The default view is Grid (configurable via `default_view='graph'` in the DAG definition). Most operators spend 80% of their time in Grid view (monitoring) and Graph view (debugging)]

## DAG Definition File

Key components of a DAG definition file include DAG arguments, DAG and task definitions, and the task pipeline.

[ENRICHED: recap — the 5-block structure of every DAG file:

```
Block 1: Library imports     → from airflow import DAG; from airflow.operators.bash import BashOperator
Block 2: DAG arguments       → default_args = {'owner': ..., 'start_date': ..., 'retries': ...}
Block 3: DAG definition      → with DAG('my_dag', default_args=..., schedule=...) as dag:
Block 4: Task definitions    → task1 = BashOperator(task_id='extract', ...)
Block 5: Task pipeline       → task1 >> task2 >> task3
```

Every DAG file follows this exact pattern. Understanding this structure means you can read any DAG in the world and immediately know where to look for what. The video "Build a DAG Using Airflow" covers this structure in detail]

## Scheduling

Set a schedule to specify how often to re-run your DAG.

[ENRICHED: recap — scheduling options:

| Format | Example | Use Case |
|--------|---------|----------|
| `timedelta` | `timedelta(hours=1)` | Simple intervals |
| Cron expression | `'0 * * * *'` (hourly) | Complex schedules (e.g., `'0 0 * * 1'` = every Monday at midnight) |
| Preset | `@daily`, `@hourly`, `@weekly` | Common schedules |
| `@once` | `schedule_interval='@once'` | Run exactly once and stop |
| `None` | `schedule_interval=None` | Manual trigger only |

**Key behavior**: the first run happens at `start_date + schedule_interval`, not at `start_date` itself. Setting `catchup=False` prevents backfilling missed runs]

## Logging and Monitoring

You can save Airflow logs into local file systems and send them to cloud storage, search engines, and log analyzers.

Airflow recommends sending production deployment logs to be analyzed by Elasticsearch or Splunk.

[ENRICHED: recap — the logging stack:
- **Local**: `~/airflow/logs/` — default for development
- **Remote**: S3, GCS, Azure Blob — for production (persists across container restarts)
- **Analytics**: Elasticsearch (open-source, ELK stack) or Splunk (commercial, enterprise compliance)

Log files are organized by `dag_id`, `run_id`, `task_id`, and `attempt` number. Access via Grid View → click task → Logs tab]

## Observability

You can view DAGs and task events with Airflow's UI.

The three types of Airflow metrics are counters, gauges, and timers.

Airflow recommends that production deployment metrics be sent to and analyzed by Prometheus via StatsD.

[ENRICHED: recap — the metrics stack:

| Metric Type | Behavior | Example |
|-------------|----------|---------|
| **Counter** | Monotonically increasing | `ti.success.total` (total successful tasks) |
| **Gauge** | Fluctuates up/down | `ti.running` (currently running tasks) |
| **Timer** | Measures duration | `ti.duration` (task execution time) |

**Production pipeline**: `Airflow → StatsD → statsd_exporter → Prometheus → Grafana`

StatsD is the relay daemon (UDP 8125), Prometheus is the time-series database, Grafana is the visualization layer. The Airflow community provides pre-built Grafana dashboards for common metrics]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Core Concepts | Definition | 4 characteristics — scalable (horizontal), dynamic (Python), extensible (plugins), lean (modular) | HIGH |
| 2 | Features | Specificity | 5 features detailed table — pure Python, useful UI, integration, easy to use, open-source | HIGH |
| 3 | Use Cases | Ecosystem | ML pipeline use case — data prep → training → evaluation → deployment; Kubeflow/MLflow/SageMaker integration | HIGH |
| 4 | Tasks | Recap | Two-layer model — operators define WHAT, dependencies define WHEN; "workflow orchestrator" definition | HIGH |
| 5 | DAGs as Code | Specificity | 3-benefit table — maintainable (DRY), testable (pytest), collaborative (Git/PR/CI); vs UI-only tools | HIGH |
| 6 | UI | Specificity | 7-view table with purposes and best-for scenarios; default view is Grid; 80% time in Grid/Graph | HIGH |
| 7 | DAG Definition | Recap | 5-block structure code template with block numbers and examples | HIGH |
| 8 | Scheduling | Specificity | 5 scheduling formats table; first run behavior (start_date + interval); catchup=False prevents backfill | HIGH |
| 9 | Logging | Recap | 3-layer logging stack (local/remote/analytics); Elasticsearch vs Splunk; log path convention | HIGH |
| 10 | Metrics | Specificity | 3 metric types table (counter/gauge/timer); full production pipeline (Airflow→StatsD→Prometheus→Grafana) | HIGH |

---

<!-- EXTRACTION_CHECKLIST: 16 sentences extracted, 16 sentences in output -->
