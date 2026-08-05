# Airflow Logging and Monitoring

**Course 8:** ETL & Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines
**Video Type:** Lesson (4:18)

---

Welcome to Airflow Logging and Monitoring.

After watching this video, you will be able use logging capabilities to monitor the task status and diagnose problems with direct acylic graph, DAG runs. And explain accessing emitted metrics such as counters, gauges, and timers.

[ENRICHED: corrected terminology — "direct acyclic graph" → **Directed Acyclic Graph (DAG)**. A DAG is a graph with directed edges and no cycles. In Airflow, each DAG represents a workflow — a collection of tasks with defined dependencies. The "acyclic" property is critical: it means there are no circular dependencies, which allows the scheduler to determine execution order automatically without infinite loops.]

## Logging in Airflow

The logging capability is required for developers to monitor the status of tasks in DAG runs and to diagnose and debug issues.

By default, Airflow logs are saved to local file systems as log files. This makes it convenient for developers to quickly review the log files, especially in a development environment.

For Airflow production deployments, the log files can be sent to cloud storage such as IBM Cloud, AWS, or Azure for remote accessing.

[ENRICHED: added specificity — Airflow's logging architecture has three layers:

| Layer | Dev Environment | Production Environment |
|-------|----------------|----------------------|
| **Local storage** | `~/airflow/logs/` (default) | Local disk on worker nodes |
| **Remote storage** | — | S3, GCS, Azure Blob, IBM Cloud Object Storage |
| **Log analytics** | — | Elasticsearch, Splunk, Datadog |

In development, logs live on the local filesystem. In production, you configure Airflow to write logs to remote storage (e.g., S3) so they persist across container restarts and are accessible from any node. The `airflow.cfg` setting `remote_logging = True` enables this, along with `remote_log_conn_id` (the Airflow Connection ID for your cloud storage) and `remote_base_log_folder` (the S3/GCS/Azure path prefix).]

The log files can also be sent to search engines and dashboards for further retrieval and analysis. Airflow recommends using Elasticsearch and Splunk, which are two popular document database and search engines to index, search, and analyze log files.

[ENRICHED: definition — **Elasticsearch** is a distributed search and analytics engine built on Apache Lucene. It excels at full-text search, structured queries, and log analytics. In the Airflow context, logs are shipped to Elasticsearch (often via Filebeat or Fluentd), where they become searchable by DAG ID, task ID, execution date, log level, and custom fields. Elasticsearch is the "E" in the ELK stack (Elasticsearch + Logstash + Kibana), where Kibana provides the visualization layer. Elasticsearch is open-source (Apache 2.0 license) and widely used in production for log aggregation.]

[ENRICHED: definition — **Splunk** is a proprietary commercial platform for searching, monitoring, and analyzing machine-generated data. Like Elasticsearch, it indexes log data and provides powerful search capabilities, but it also includes built-in alerting, dashboards, and reporting. Splunk is often chosen in enterprise environments where compliance requirements mandate specific log retention and audit capabilities. The tradeoff: Splunk is expensive (licensed per data volume), while Elasticsearch is free but requires more operational overhead to manage.]

## Log File Organization

By default, log files are organized by `dag_ids`, `run_ids`, `task_ids`, and the attempt numbers. You will need to navigate to a specific log file for a task execution using the path convention.

For example, if you want to find the log for the first attempt of `task1` in `dummy_dag` at a specific time. You will need to navigate to `logs/dag_id=dummy_dag/run_id=scheduled__time/task_id=task1/attempt=1.log` in the file editor.

[ENRICHED: added specificity — the log file path convention:

```
logs/
├── dag_id=my_dag/
│   ├── run_id=scheduled__2024-01-01T00:00:00+00:00/
│   │   ├── task_id=extract/
│   │   │   ├── attempt=1.log
│   │   │   ├── attempt=2.log
│   │   │   └── attempt=3.log
│   │   └── task_id=load/
│   │       └── attempt=1.log
│   └── run_id=manual__2024-01-02T10:30:00+00:00/
│       └── task_id=extract/
│           └── attempt=1.log
```

**Key observations:**
- Each DAG run gets its own directory under `dag_id=<id>/`
- Each task within a run gets its own directory under `task_id=<id>/`
- Each retry attempt is a separate log file (`attempt=1.log`, `attempt=2.log`, etc.)
- The `attempt` number corresponds to `try_number` in the Airflow metadata — attempt 1 is the initial execution, attempt 2 is after the first retry, and so on]

Note, the `run_id` value depends on how the DAG was executed. It can either be manual or scheduled, followed by the time of execution.

[ENRICHED: added specificity — **`run_id` types in Airflow:**

| run_id Format | Trigger | Example |
|---------------|---------|---------|
| `scheduled__<datetime>` | Scheduler (automatic) | `scheduled__2024-01-01T00:00:00+00:00` |
| `manual__<datetime>` | Manual trigger (Web UI/API) | `manual__2024-01-02T10:30:00+00:00` |
| `backfill__<datetime>` | Backfill command | `backfill__2024-01-01T00:00:00+00:00` |
| `dataset_triggered__<datetime>` | Dataset/asset trigger | `dataset_triggered__2024-01-01T06:00:00+00:00` |

The `run_id` is how Airflow uniquely identifies each DAG run. When debugging, the `run_id` tells you whether the run was automatic (scheduled), triggered manually (for testing), or part of a backfill. This distinction matters because manual runs often bypass schedule dependencies, while scheduled runs respect the full DAG structure.]

In the log file, you can view information such as the running command, command result, task result, and so on.

[ENRICHED: added specificity — a typical Airflow task log contains:

```
[2024-01-01 00:00:01] {taskinstance.py:1234} INFO - Dependencies for <Task (extract): [SUCCESS]
[2024-01-01 00:00:02] {taskinstance.py:1234} INFO - Previous dagrun was <DagRun scheduled__2024-01-01T00:00:00+00:00>
[2024-01-01 00:00:03] {taskinstance.py:1234} INFO - Starting attempt 1 of 2
[2024-01-01 00:00:04] {local_task_job_runner.py:123} INFO - Running on host worker-01
[2024-01-01 00:00:05] {subprocess.py:56} INFO - Command: cut -d":" -f1,3,6 /etc/passwd > extracted.txt
[2024-01-01 00:00:06] {subprocess.py:56} INFO - Full command: ...
[2024-01-01 00:00:07] {bash.py:87} INFO - Output: (empty — command wrote to file)
[2024-01-01 00:00:08] {taskinstance.py:1234} INFO - Task exited with return code 0
[2024-01-01 00:00:09] {taskinstance.py:1234} INFO - Marking task as SUCCESS
```

The log shows: dependency checks, the bash command executed, stdout/stderr output, exit code, and final state. Exit code 0 = success, non-zero = failure (which triggers retry if `retries > 0`).]

You can also quickly review the task events via UI provided by the Airflow web server. You can search events with fields like Dag id, Task id, and Logical Date, and quickly get an overview of the specific DAGs and tasks you are looking for.

[ENRICHED: added specificity — in the Airflow Web UI, task logs are accessible via:
1. **Grid view** → click a task instance → click "Logs" tab → shows the full log with expandable sections
2. **Graph view** → click a task node → "View Log" link → opens the log viewer
3. **Search** → use the search bar to filter by `dag_id`, `task_id`, `logical_date`, `state`, or `run_id`

The search feature is particularly useful when debugging across multiple DAGs — you can search for all failed tasks across all DAGs in a date range, or find all runs of a specific task that took longer than expected.]

---

## Airflow Metrics

Airflow produces three different types of metrics for checking and monitoring component's health, these are counters, gauges, and timers.

### Counters

Counters are metrics that will always be increasing, such as the total counts of successful or failed tasks.

[ENRICHED: definition — **Counters** are monotonically increasing metrics. They never decrease — they only go up (or reset to zero on process restart). In Airflow, counter examples include:
- `ti.success.total` — total number of successful task instances since scheduler started
- `ti.failed.total` — total number of failed task instances
- `dag_bag.import_errors` — total number of DAG file import errors

Counters are useful for: (1) calculating rates (successes per minute = counter delta / time delta), (2) detecting anomalies (sudden spike in failures), (3) capacity planning (total task volume over time).]

### Gauges

Gauges are metrics that may fluctuate, for example, the number of currently running tasks or DAG bag sizes.

[ENRICHED: definition — **Gauges** are metrics that represent a current value at a point in time. Unlike counters, gauges can go up AND down. In Airflow, gauge examples include:
- `ti.running` — number of tasks currently running (goes up when tasks start, down when they finish)
- `dag_bag.size` — number of DAGs loaded in the scheduler's DAG bag (changes when DAGs are added/removed)
- `pool.open_slots` — available slots in a task pool (decreases when tasks claim slots, increases when they release)

Gauges are useful for: (1) real-time monitoring (how many tasks are running right now?), (2) capacity alerts (pool slots dropping to zero), (3) resource utilization (DAG bag size approaching memory limits).]

### Timers

Timers are metrics related to time duration, for instance, the time to finish a task, or the time for a task to reach success or failed state.

[ENRICHED: definition — **Timers** measure how long something takes. In Airflow, timer examples include:
- `ti.duration` — time (in seconds) from task start to finish
- `dag.duration` — time from first task start to last task finish
- `scheduler_loop.duration` — time for one scheduler loop iteration

Timers are useful for: (1) performance monitoring (which tasks are slow?), (2) SLA tracking (is the pipeline completing within the expected window?), (3) regression detection (did a recent change make a task slower?). Airflow stores timer values as histograms — showing the distribution of durations, not just the average. This means you can see p50, p95, and p99 latencies, which is more informative than a single average.]

---

## Metrics Collection and Monitoring

Similar to logs, the metrics produced in Airflow production deployments should be sent and analyzed by dedicated repositories and tools.

Airflow recommends using StatsD, which is a network daemon that can gather metrics from Airflow and send them to a dedicated metrics monitoring system.

[ENRICHED: definition — **StatsD** is a lightweight network daemon (typically running on UDP port 8125) that listens for metric events and forwards them to a backend. Airflow has a built-in StatsD integration — when enabled (`[metrics] statsd_on = True` in `airflow.cfg`), Airflow emits metrics as StatsD packets to the configured `statsd_host:statsd_port`. StatsD itself doesn't store or visualize metrics — it's a relay. The actual storage and visualization come from the backend you connect it to (Graphite, Prometheus via statsd_exporter, InfluxDB, etc.).]

For metrics monitoring and analysis, Airflow recommends using Prometheus, which is a popular metrics monitoring and analysis system. Prometheus can also aggregate and visualize metrics in a dashboard for a more interactive visual style.

[ENRICHED: definition — **Prometheus** is an open-source monitoring system and time-series database. It scrapes (pulls) metrics from instrumented endpoints at regular intervals, stores them in a time-series database, and provides a powerful query language (PromQL) for analysis. In the Airflow context, the typical pipeline is:

```
Airflow → StatsD → statsd_exporter → Prometheus → Grafana
```

1. **Airflow** emits metrics via StatsD
2. **statsd_exporter** (Prometheus companion) converts StatsD metrics to Prometheus format
3. **Prometheus** scrapes and stores the metrics
4. **Grafana** (visualization layer) queries Prometheus and displays dashboards

**Grafana** is a separate open-source tool for building dashboards. It's the "V" (visualization) in the modern monitoring stack. The Airflow community provides pre-built Grafana dashboards for common metrics like task success rates, pool utilization, and scheduler performance.]

[ENRICHED: ecosystem — the full Airflow observability stack:

| Component | Role | Open Source? | Purpose |
|-----------|------|-------------|---------|
| **Airflow** | Source | Yes (Apache 2.0) | Emits logs + metrics |
| **Filebeat/Fluentd** | Log shipper | Yes | Collects logs, sends to Elasticsearch |
| **Elasticsearch** | Log storage | Yes (Apache 2.0) | Indexes and searches logs |
| **Kibana** | Log visualization | Yes (Apache 2.0) | Dashboards for log analysis |
| **Splunk** | Log analytics | No (commercial) | Enterprise log management alternative |
| **StatsD** | Metric relay | Yes (MIT) | Forwards Airflow metrics |
| **Prometheus** | Metric storage | Yes (Apache 2.0) | Scrapes and stores time-series metrics |
| **Grafana** | Dashboard | Yes (AGPL-3.0) | Visualizes metrics from Prometheus |

This is the production-grade observability stack for Airflow. In development, you typically only use local log files and the built-in Web UI. The full stack becomes necessary when running Airflow in production with multiple worker nodes, hundreds of DAGs, and strict SLA requirements.]

---

## Summary

In this video, you learned that you can save Airflow logs into local file systems and send them to cloud storage, search engines, and log analyzers. Airflow recommends sending production deployment logs to be analyzed by Elasticsearch or Splunk. With Airflow's UI, you can view DAGs and task events easily.

You also learned that the three types of Airflow metrics are counters, gauges, and timers. Airflow recommends that you send production deployment metrics for analysis by Prometheus via StatsD.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Learning Objectives | Correction | Corrected "direct acyclic graph" → "Directed Acyclic Graph (DAG)" with definition | HIGH |
| 2 | Logging | Specificity | Airflow logging architecture — 3-layer table (local, remote storage, log analytics), `airflow.cfg` settings | HIGH |
| 3 | Logging | Definition | Elasticsearch — distributed search engine, ELK stack, full-text search for logs | HIGH |
| 4 | Logging | Definition | Splunk — proprietary log analytics platform, enterprise compliance, expensive vs Elasticsearch | HIGH |
| 5 | Log Path | Specificity | Log file directory tree structure, `attempt` number = retry tracking, `try_number` mapping | HIGH |
| 6 | Log Path | Specificity | `run_id` types table — `scheduled__*`, `manual__*`, `backfill__*`, `dataset_triggered__*` with examples | HIGH |
| 7 | Log File | Specificity | Sample log file content — dependency checks, bash command, stdout/stderr, exit code, state transition | HIGH |
| 8 | Web UI | Specificity | Task log access — Grid view, Graph view, Search bar; filtering by dag_id/task_id/logical_date/state | HIGH |
| 9 | Metrics | Definition | Counters — monotonically increasing, examples: ti.success.total, ti.failed.total, dag_bag.import_errors | HIGH |
| 10 | Metrics | Definition | Gauges — fluctuate up/down, examples: ti.running, dag_bag.size, pool.open_slots | HIGH |
| 11 | Metrics | Definition | Timers — measure duration, examples: ti.duration, dag.duration, scheduler_loop.duration; histogram storage | HIGH |
| 12 | Metrics | Definition | StatsD — lightweight daemon on UDP 8125, relay (not storage), built-in Airflow integration | HIGH |
| 13 | Metrics | Definition | Prometheus — time-series DB, pull-based scraping, PromQL, statsd_exporter bridge | HIGH |
| 14 | Metrics | Specificity | Full observability stack — Grafana dashboards, pre-built Airflow community dashboards | HIGH |
| 15 | Metrics | Ecosystem | 8-component observability stack table — Airflow→Filebeat→Elasticsearch→Kibana + StatsD→Prometheus→Grafana | HIGH |

---

<!-- EXTRACTION_CHECKLIST: 31 sentences extracted, 31 sentences in output -->
