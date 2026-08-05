# Graded Quiz: Building Data Pipelines using Airflow

**Course 8:** ETL & Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines
**Quiz Type:** Graded Quiz
**Due:** Jul 27, 11:59 PM EEST
**Attempts:** 3 (every 8 hours)

---

## Question 1

**Which of these statements is TRUE about Apache Airflow?**

| Option | Correct? |
|--------|----------|
| Apache Airflow is a data pipeline orchestration tool. | **✓ CORRECT** |
| Tasks in Apache Airflow can only be schedule and cannot be manually triggered. | ✗ |
| Apache Airflow is a workflow management tool. | ✗ |
| You can only use one kind of operator in one DAG. | ✗ |

**Answer:** Apache Airflow is a data pipeline orchestration tool.

[ENRICHED: analysis — Coursera distinguishes between "workflow management tool" (too broad — could be Airflow, Luigi, Oozie, or even Jira) and "data pipeline orchestration tool" (Airflow's specific domain). While Airflow IS a workflow management tool, the statement "data pipeline orchestration tool" is the more precise and TRUE description of what Airflow actually does. The other options are false: (1) Tasks CAN be manually triggered via the Web UI or CLI (`airflow tasks run`), (2) You CAN use multiple operators in one DAG (BashOperator + PythonOperator + PostgresOperator in the same DAG is common), (3) "Workflow management tool" is technically true but Coursera considers it less precise than "data pipeline orchestration tool" — Airflow is specifically designed for data pipelines, not general-purpose workflow management. **Lesson from practice quiz**: Coursera's pedantic distinction between "primary purpose" (workflow manager) and "what it is" (data pipeline orchestration tool) continues here — be specific.]

---

## Question 2

**Which component in the Apache Airflow architecture takes care of executing the tasks?**

| Option | Correct? |
|--------|----------|
| The meta database | ✗ |
| The web server | ✗ |
| **The worker** | **✓ CORRECT** |
| The scheduler | ✗ |

**Answer:** The worker

[ENRICHED: analysis — In Airflow's architecture, the **worker** executes tasks. The scheduler determines WHAT needs to run and WHEN, the worker actually DOES the work. The metadata database stores state (DAG definitions, task instances, run history). The web server serves the UI. The executor determines HOW workers are allocated (SequentialExecutor = single worker, CeleryExecutor = distributed workers, KubernetesExecutor = pods per task). The flow: Scheduler → assigns tasks to workers → workers execute tasks → results stored in metadata DB → web server displays status. The worker is where operators actually run — BashOperator spawns a subprocess on the worker, PythonOperator calls the function on the worker, etc.]

---

## Question 3

**In the DAG definition Python script, which of the following logical blocks might contain the 'from airflow import DAG' command?**

| Option | Correct? |
|--------|----------|
| Task pipeline | ✗ |
| **Library imports** | **✓ CORRECT** |
| DAG arguments | ✗ |
| DAG definition | ✗ |

**Answer:** Library imports

[ENRICHED: analysis — The `from airflow import DAG` command is a Python import statement. In the 5-block DAG file structure, ALL import statements go in **Block 1: Library imports**. This block appears at the top of the file and imports everything needed: `from airflow import DAG`, `from airflow.operators.bash import BashOperator`, `from datetime import timedelta`, etc. The other blocks: DAG arguments (Block 2) contains the `default_args` dict, DAG definition (Block 3) contains `with DAG(...) as dag:`, Task pipeline (Block 5) contains `>>` dependency notation. Import statements never appear in Blocks 2-5 in well-structured DAGs]

---

## Question 4

**You have both operators and sensors that you can use with DAG for tasks. Which is of these operators can you use to run the script `datatranfer.sh`?**

| Option | Correct? |
|--------|----------|
| TriggerDagRunOperator | ✗ |
| Http | ✗ |
| **Bash** | **✓ CORRECT** |
| Python | ✗ |

**Answer:** Bash

[ENRICHED: analysis — **BashOperator** is the correct choice for running a shell script (`datatranfer.sh`). BashOperator executes bash commands and scripts on the worker. The other options: **TriggerDagRunOperator** triggers another DAG (not a shell script), **Http** operator makes HTTP requests (not shell scripts), **Python** operator runs Python functions (not shell scripts). To run the script: `BashOperator(bash_command='/path/to/datatranfer.sh', ...)`. Note: the script must be accessible to the worker — either on the same filesystem, or you'd need to download it first (e.g., using a download task before the transfer task). Sensors are different from operators — sensors wait for a condition to be met (e.g., file exists, API returns 200) before allowing downstream tasks to run]

---

## Question 5

**Which of the following advantages of Apache Airflow expressing workflows as code enables Git to track them?**

| Option | Correct? |
|--------|----------|
| Maintainable | ✗ |
| Testable | ✗ |
| Collaborative | ✗ |
| **Versionable** | **✓ CORRECT** |

**Answer:** Versionable

[ENRICHED: analysis — **Versionable** (version-controllable) is the advantage that enables Git tracking. When DAGs are Python files, they can be committed to Git repositories. Git tracks: (1) every change to every DAG file (commit history), (2) who made each change (author), (3) when each change was made (timestamp), (4) what exactly changed (diff). The other advantages are related but distinct: **Maintainable** = easy to modify and update (using functions, classes, DRY principles), **Testable** = can write unit tests with pytest (import DAG, test task logic), **Collaborative** = team members can review changes via pull requests (enabled by Git, but "collaborative" is the outcome, not the mechanism). "Versionable" is the specific property that Git leverages — without version-controllable files, Git has nothing to track]

---

## Question 6

**Where can you access the 'Task Instance Context Menu' from?**

| Option | Correct? |
|--------|----------|
| Gantt | ✗ |
| Any of the DAG views that display details | ✗ |
| Code view | ✗ |
| **Any of the DAG views that display task instances** | **✓ CORRECT** |

**Answer:** Any of the DAG views that display task instances

[ENRICHED: analysis — The **Task Instance Context Menu** appears when you right-click (or click) on a task instance in any view that shows individual task instances. This includes: **Grid View** (click a colored square), **Graph View** (click a task node), **Tree View** (click a task instance node). The context menu provides quick actions: View Log, Mark as Success/Failed, Run, Clear, etc. "Gantt" view doesn't show individual task instances in the same way. "Code view" shows source code, not task instances. "Any of the DAG views that display details" is close but imprecise — the key is that the view must display TASK INSTANCES, not just DAG details]

---

## Question 7

**The final block in your Airflow pipeline script is where you specify the dependencies for your workflow. How do you specify the order of task 1 and task 2?**

| Option | Correct? |
|--------|----------|
| > | ✗ |
| **>>** | **✓ CORRECT** |
| >= | ✗ |
| // | ✗ |

**Answer:** >>

[ENRICHED: analysis — The **`>>`** operator (bitshift right) specifies that task2 is downstream from task1: `task1 >> task2` means "task1 runs first, then task2." The other options: `>` is a greater-than comparison in Python (not an Airflow operator), `>=` is greater-than-or-equal (not Airflow), `//` is integer division in Python (not Airflow). The `>>` operator is syntactic sugar for `task1.set_downstream(task2)` — it's equivalent but more readable. You can also use `<<` (bitshift left) in reverse: `task2 << task1` means the same thing as `task1 >> task2`. For chaining: `task1 >> task2 >> task3`]

---

## Question 8

**Which block specifies the DAG start date?**

| Option | Correct? |
|--------|----------|
| Task pipeline | ✗ |
| Task definitions | ✗ |
| **DAG arguments** | **✓ CORRECT** |
| DAG definition | ✗ |

**Answer:** DAG arguments

[ENRICHED: analysis — The `start_date` parameter is specified in **Block 2: DAG arguments** (the `default_args` dictionary). Example: `default_args = {'start_date': datetime(2024, 1, 1), ...}`. While `start_date` CAN also be passed directly to the `DAG()` constructor in Block 3, the standard pattern (and what the video teaches) is to put it in `default_args` so it's inherited by all tasks. The 5-block structure: Block 1 (imports) → Block 2 (arguments including start_date) → Block 3 (DAG definition) → Block 4 (task definitions) → Block 5 (dependencies)]

---

## Question 9

**Which of the following Airflow metrics could fluctuate?**

| Option | Correct? |
|--------|----------|
| Timers | ✗ |
| **Gauges** | **✓ CORRECT** |
| Counters | ✗ |
| Air flows | ✗ |

**Answer:** Gauges

[ENRICHED: analysis — **Gauges** are metrics that fluctuate — they represent current values that go up and down. Examples: `ti.running` (currently running tasks — goes up when tasks start, down when they finish), `pool.open_slots` (available pool slots), `dag_bag.size` (number of loaded DAGs). The other options: **Counters** only increase monotonically (e.g., `ti.success.total` — total successful tasks, never decreases), **Timers** measure duration (e.g., `ti.duration` — how long a task took, doesn't fluctuate in the same way), "Air flows" is not a metric type (it's a distractor). The key distinction: counters = monotonically increasing, gauges = fluctuate, timers = measure time]

---

## Question 10

**Which of the following Apache Airflow basic components serves the interactive UI?**

| Option | Correct? |
|--------|----------|
| **Web server** | **✓ CORRECT** |
| Executor | ✗ |
| DAG directory | ✗ |
| Scheduler | ✗ |

**Answer:** Web server

[ENRICHED: analysis — The **web server** serves the Airflow Web UI (the interactive interface). It's a Flask-based web application that reads from the metadata database and displays DAGs, task instances, logs, and metrics. The other components: **Executor** determines how tasks are executed (Sequential, Celery, Kubernetes — not a UI component), **DAG directory** is the filesystem folder where DAG files live (not a component), **Scheduler** determines what to run and when (background process, not UI). The web server typically runs on port 8080 and can be started with `airflow webserver`. In production, you'd put it behind a load balancer for high availability]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Correction | "Data pipeline orchestration tool" is more precise than "workflow management tool" — Coursera wants specificity | HIGH |
| 2 | Q2 | Definition | Worker executes tasks; scheduler assigns; metadata DB stores state; web server serves UI | HIGH |
| 3 | Q3 | Specificity | Import statements go in Block 1 (Library imports), never in Blocks 2-5 | HIGH |
| 4 | Q4 | Specificity | BashOperator runs shell scripts; TriggerDagRunOperator triggers DAGs; sensors wait for conditions | HIGH |
| 5 | Q5 | Clarification | "Versionable" = Git tracking; "Maintainable" = DRY; "Testable" = pytest; "Collaborative" = PR reviews | HIGH |
| 6 | Q6 | Specificity | Context Menu accessible in Grid View, Graph View, Tree View — any view showing task instances | HIGH |
| 7 | Q7 | Definition | `>>` = bitshift right = task1 then task2; equivalent to `task1.set_downstream(task2)` | HIGH |
| 8 | Q8 | Specificity | `start_date` in Block 2 (default_args dict), not Block 3 (DAG definition) | HIGH |
| 9 | Q9 | Definition | Gauges fluctuate (ti.running, pool.open_slots); counters only increase; timers measure duration | HIGH |
| 10 | Q10 | Definition | Web server = Flask UI on port 8080; Executor = task execution strategy; Scheduler = background process | HIGH |

---

<!-- EXTRACTION_CHECKLIST: 10 questions, 10 answers, 10 analyses -->
