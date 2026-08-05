# Practice Quiz: Building Data Pipelines using Airflow

**Course 8:** ETL & Data Pipelines with Shell, Airflow and Kafka
**Module 3:** Apache Airflow Data Pipelines
**Quiz Type:** Practice Quiz
**Due:** Jul 27, 11:59 PM EEST
**Attempts:** Unlimited
**Result:** 60% (3/5)

---

## Question 1

**What is the primary purpose of Apache Airflow?**

| Option | Correct? |
|--------|----------|
| **Workflow manager** | **✓ CORRECT** |
| Data orchestration | ✗ |
| Data streaming solution | ✗ |
| Transformation utility | ✗ |

**Answer:** Workflow manager

**Coursera feedback:** "Apache Airflow can perform workflow orchestration. However, this is not its primary purpose."

[ENRICHED: analysis — Coursera distinguishes between "workflow manager" (the system's primary purpose) and "data orchestration" (a capability/use case). Airflow is fundamentally a **workflow management system** — it orchestrates the execution of tasks in a defined order. While "data orchestration" is what Airflow does in the data engineering context, Coursera considers this a specific application of the broader workflow management capability. The distinction: "workflow manager" describes WHAT Airflow IS (a system that manages workflows), while "data orchestration" describes WHAT Airflow DOES (orchestrates data pipelines). The primary purpose is the former — what it is at its core. Think of it this way: a car's primary purpose is "transportation," not "highway driving" — highway driving is a specific use case of the broader capability. Similarly, workflow management is the primary purpose; data orchestration is a specific use case. This is a tricky question because in the data engineering world, "data orchestration" is the more commonly used term — but Coursera's answer is "Workflow manager."]

---

## Question 2

**What does acyclic in Directed Acyclic Graph (DAG) mean?**

| Option | Correct? |
|--------|----------|
| **No loops** | **✓ CORRECT** |
| Parallel edges | ✗ |
| Repeated nodes | ✗ |
| Two nodes | ✗ |

**Answer:** No loops

**Coursera feedback:** "Correct! The acyclic part means there are not loops."

[ENRICHED: analysis — "Acyclic" means there are no cycles (loops) in the graph. In a DAG, you cannot follow directed edges and return to your starting node. This property is what makes Airflow able to determine execution order automatically — if cycles existed, the scheduler would enter an infinite loop trying to resolve dependencies. For example: `A → B → C → A` is cyclic (invalid), while `A → B → C` is acyclic (valid). The "Directed" part means edges go one way (A → B, not A ↔ B). Together, "Directed Acyclic Graph" describes a structure where work flows forward with no circular dependencies. This is a fundamental concept in computer science — DAGs are used in build systems (Make, Bazel), dataflow programming (Apache Beam), and version control (Git commits form a DAG)]

---

## Question 3

**Which of the following Apache Airflow UI views will you use to see the tasks and dependencies for your DAG?**

| Option | Correct? |
|--------|----------|
| **Graph view** | **✓ CORRECT** |
| Grid view | ✗ |
| Last run view | ✗ |
| DAGs view | ✗ |

**Answer:** Graph view

**Coursera feedback:** "Correct! Graph view shows your DAG's tasks and dependencies at the bottom of the screen."

[ENRICHED: analysis — **Graph View** shows the DAG as a visual dependency graph where each node is a task and edges represent dependencies. This is the most intuitive view for understanding workflow structure. While Grid View shows task STATUS (color-coded matrix of tasks × runs), it doesn't show the dependency arrows between tasks. The Graph View explicitly draws arrows between connected tasks, making it easy to see: (1) which tasks run first, (2) fan-in/fan-out patterns, (3) why a task didn't run (upstream failure). "Last run view" and "DAGs view" are not actual Airflow UI view names. The DAGs view is the main listing page, but it doesn't show individual task dependencies]

---

## Question 4

**Apache Airflow DAGs are Python scripts that consist of specific Operators. Which of the following operators can be used specifically to call Python functions?**

| Option | Correct? |
|--------|----------|
| **PythonOperator** | **✓ CORRECT** |
| BashOperator | ✗ |
| HttpOperator | ✗ |
| ImportOperator | ✗ |

**Answer:** PythonOperator

**Coursera feedback:** "Correct! The Python operator can be used to call python functions as 'python_callable'."

[ENRICHED: analysis — **PythonOperator** is the operator that executes Python functions. It accepts a `python_callable` parameter (a function reference) and calls that function when the task runs. The other options: **BashOperator** runs shell commands (not Python functions), **HttpOperator** makes HTTP requests (not Python functions), **ImportOperator** is not a real Airflow operator (it's a distractor). Key distinction: PythonOperator runs the function IN-PROCESS on the Airflow worker, while BashOperator spawns a subprocess. This means PythonOperator can pass data to downstream tasks via XCom (Airflow's inter-task messaging), while BashOperator can only communicate through files on disk. The import path is `from airflow.operators.python import PythonOperator`]

---

## Question 5

**Which of the options allows you to view the logs of a specific task on the Web UI?**

| Option | Correct? |
|--------|----------|
| **Task details view** | **✓ CORRECT** |
| Graph view for a specific task | ✗ |
| Audit logs view | ✗ |
| Hovering over the Grid view | ✗ |

**Answer:** Task details view

**Coursera feedback:** "Incorrect. This will show the logs user interaction." (for "Graph view for a specific task")

[ENRICHED: analysis — Coursera's answer is "Task details view" — this refers to clicking a task in Grid View or Graph View, which opens the **task details panel** (also called the task instance panel). This panel has tabs: Logs, XCom, Rendered Template, Instances. The "Logs" tab shows the full stdout/stderr output. The option "Graph view for a specific task" was marked wrong because Coursera considers it imprecise — the logs are accessed via the task details panel, not the graph view itself. "Hovering over the Grid view" shows brief metadata (task_id, duration, state) but NOT the full logs. "Audit logs view" is not a real Airflow UI view name. The correct mental model: you click a task (in Grid or Graph view) → the task details panel opens → you click the Logs tab. Coursera calls this "Task details view" — the panel that appears when you click a task, which contains the logs among other information]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Correction | Coursera answer: "Workflow manager" (not "Data orchestration"). Distinction: primary purpose (what it IS) vs use case (what it DOES) | HIGH |
| 2 | Q2 | Definition | Acyclic = no cycles/loops; cycles cause infinite loops in scheduler; example of cyclic vs acyclic graph | HIGH |
| 3 | Q3 | Clarification | Graph View shows dependencies (arrows), Grid View shows status (color matrix); "Last run view" is not real | HIGH |
| 4 | Q4 | Definition | PythonOperator executes Python functions via `python_callable`; distinction from BashOperator (subprocess) | HIGH |
| 5 | Q5 | Correction | Coursera answer: "Task details view" (not "Graph view for a specific task"). Logs accessed via task details panel → Logs tab | HIGH |

---

<!-- EXTRACTION_CHECKLIST: 5 questions, 5 answers, 5 analyses -->
