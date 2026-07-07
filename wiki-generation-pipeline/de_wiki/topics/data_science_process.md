# Data Science Process

> **LTHP Status:** NEW — Module 4 ecosystem expansion.
> **Source files:** UCSD Big Data Specialization — Course 1, Module 4 (14 hand-written summaries)

## Overview

Data science is a multi-disciplinary craft that extracts actionable insight from data. The UCSD Big Data Specialization presents three complementary frameworks for understanding how data science works: the **problem-formulation process** (asking the right questions), the **Five P's of Data Science** (the structural dimensions), and the **5-step data science process** (the operational workflow). These are bookended by a **Big Data strategy** framework for organizational adoption.

---

## 1. Asking the Right Questions (Problem Formulation)

> *"Without a clearly defined problem, you will not have a clear goal in mind, nor will you know when you have solved it."*

Before any data work begins, the problem must be defined. This four-step sequence ensures the question is grounded in business value and feasibility.

### Step 1 — Define the Problem or Opportunity

Articulate a concrete, answerable question based on business or scientific objectives. Examples:

| Domain | Question | Type |
|--------|----------|------|
| Sales & Customer Service | How can sales figures and call center logs be combined to evaluate a new product? | Data fusion / multi-source integration |
| Industrial IoT | How can data from multiple sensors detect instrument failure? | Predictive maintenance |
| Customer Analytics | How can we understand our customers to achieve effective target marketing? | Customer segmentation / propensity modeling |

**Key rule:** Start with the objectives, not with data collection. The question determines what data is useful.

### Step 2 — Assess the Situation

Before committing resources, evaluate feasibility across six dimensions:

| Dimension | Questions |
|-----------|-----------|
| Requirements | What assumptions and constraints apply? |
| Resources | What personnel, compute, and data infrastructure exist? |
| Costs | What are the main project costs? |
| Benefits | What is the potential value if successful? |
| Risks | What data availability, regulatory, or technical risks exist? |
| Contingencies | What fallback plans exist for each risk? |

Common risks include: data not existing or being inaccessible, regulatory constraints (GDPR, HIPAA, CCPA), and compute cost for large-scale training.

### Step 3 — Define Goals and Success Criteria

Success criteria are two-layered: **technical metrics** (e.g., AUC-ROC ≥ 0.85, precision ≥ 0.70) and **business metrics** (e.g., reduce churn by 15% within 6 months of deployment). Both are needed — the first confirms the model works, the second confirms it delivers value.

### Step 4 — Formulate the Plan

A complete data science plan includes five sub-plans: data sourcing, feature engineering, modeling approach (algorithm selection), evaluation (validation strategy), and deployment (batch scoring, API, dashboard).

---

## 2. The Five P's of Data Science

Developed at the San Diego Supercomputer Center (SDSC), the Five P's framework describes the structural dimensions of any data science project, leading to a sixth P: the **data product**.

### P1: People

Data science is a team discipline. A functional team combines experts in: data and analytics, business domain knowledge, computing and systems engineering, domain science, and big data management. The "unicorn" problem — expecting one person to cover all these — is why organizations build teams instead of hiring individual data scientists.

**Data scientist skills (UCSD framing):** Data science sits at the intersection of three domains: computer science (data engineering, infrastructure, programming), mathematics/statistics (machine learning, statistical modeling, relational algebra), and business expertise (domain knowledge, problem framing, business passion). Key traits include: passion for data, problem understanding, analytical orientation, engineering interest (building solutions, not just analyzing), curiosity about cross-domain work, and communication skills for presenting results. [Cross-ref: topics/data_roles_overview.md — data scientist role]

### P2: Purpose

The challenge or question defined by the organization's big data strategy. Purpose anchors the entire project. The team starts by asking: *"What is the problem at large? How do we see ourselves solving it?"*

### P3: Process

Two views of the process:

**High-level:** Big Data Engineering (infrastructure, pipelines, systems) + Big Data Analytics (modeling, statistical analysis, computation).

**Detailed — five sequential steps:** Acquire → Prepare → Analyze → Report → Act. These steps iterate — findings from one step may require returning to a previous one.

An alternative framing: **Build → Explore → Scale**, emphasizing that big data projects require robust system construction and growth planning from the start.

### P4: Platforms

The computing infrastructure enabling scalability at each step — the Hadoop ecosystem (HDFS, MapReduce, YARN) or cloud-native alternatives (Amazon EMR, Google Dataproc, Databricks). Scalability must be communicated explicitly from the start.

### P5: Programmability

Reusable, reproducible programming interfaces: libraries (pandas, scikit-learn), middleware (gRPC, message queues), analytical tools (Jupyter, Spark MLlib), visualization environments (Tableau, D3.js), and end-user reporting (Looker, Metabase).

### P6: The Data Product

The Five P's lead to the sixth P — the final deliverable grounded in the original purpose. The course emphasizes working *backward from the product*: define what you are building first, then design the process that produces it.

---

## 3. The Data Science Process (5 Steps)

This is the operational workflow that data science teams execute, iterating as needed.

### Step 1 — Acquire
Find, access, authenticate, and transport data from sources to distributed storage. Activities: identify and authenticate to all data sources, transport data to distributed file systems (HDFS, S3), subset data to regions or times of interest (geo-spatial queries).

### Step 2a — Explore (Data Preparation, Part 1)
Understand data before modeling: examine nature (what it represents), meaning (what fields signify), quality (missing values, outliers, errors), and format (CSV, JSON, relational). This is Exploratory Data Analysis (EDA) — summary statistics, distribution plots, correlation matrices, missing-value analysis.

### Step 2b — Pre-process (Data Preparation, Part 2)
Transform raw data into analysis-ready form: clean (handle missing values, fix format inconsistencies), subset/filter relevant records, model raw data into a defined schema, integrate multiple sources into a unified dataset. This is consistently the most time-consuming step — approximately 60% of data scientist time.

### Step 3 — Analyze
Select analytical techniques and build a model. The main categories:

| Technique | Description | Examples |
|-----------|-------------|----------|
| **Classification** | Predict a category | Weather (sunny/rainy), tumor (benign/malignant), digit recognition (0-9) |
| **Regression** | Predict a numeric value | Stock price, weekly sales, test score |
| **Clustering** | Organize similar items into groups | Customer segmentation, topography zones, weather patterns |
| **Association Analysis** | Find items that frequently co-occur | Market basket analysis (e.g., "customers who bought X also bought Y") |
| **Graph Analysis** | Analyze connected data | PageRank, community detection, shortest path |

### Step 4 — Report
Communicate results to stakeholders. Three guiding questions: (1) What is the punchline? (2) What added value do these results provide? (3) How do the results compare to the success criteria? Visualization tools include scatter plots, line graphs, heat maps, and tables. Both favorable and unfavorable results must be presented — inconclusive findings may lead to additional analysis.

> **Analogy (UCSD):** The weather forecast is a model of data science in action. You check the forecast (insight generated from data), decide what to wear (action based on evidence), and the cycle repeats as new data arrives. Business leaders and decision makers do the same — they act based on evidence provided by their data science teams. This is the chain: **Data → Model → Insight → Action.**

### Step 5 — Act
Turn insights into action — the step where value is realized. Actions can be: **decision automation** (model output triggers a system action directly), **decision support** (output surfaced to a human decision-maker), or **policy change** (insights inform business rules). After action, monitor and measure impact, then re-evaluate. This creates a cycle: Act → Evaluate → Re-enter process at Step 1 or 2.

---

## 4. Building a Big Data Strategy

An 8-step iterative framework for organizations adopting Big Data analytics:

| Step | Key Action |
|------|------------|
| 1 | Start with **objectives**, not data collection |
| 2 | Create **organizational buy-in** with leadership commitment |
| 3 | Build a **diverse team** with a partnership mindset, not customer-vendor dynamics |
| 4 | **Train continuously** — Big Data skills into domain experts, domain context into technical team |
| 5 | Maintain a small **experimental/research team** for prototyping before full-scale deployment |
| 6 | **Remove data silos** — barriers to data access must be eliminated |
| 7 | Define explicit **data policies** on privacy, access, data lifetime, curation, quality, interoperability, and regulation |
| 8 | Cultivate an **analytics-driven culture** — analytics integrated into operations, not an afterthought |

The strategy must be **iterated** as technology and business goals evolve.

---

## Summary

| Framework | Core Idea |
|-----------|-----------|
| **Asking the Right Questions** | Define problem → Assess situation → Set success criteria → Formulate plan |
| **Five P's** | People + Purpose + Process + Platforms + Programmability → Product |
| **5-Step Process** | Acquire → Explore → Pre-process → Analyze → Report → Act |
| **Big Data Strategy** | 8 iterative steps for organizational adoption |

[Cross-ref: topics/big_data_foundations.md — 5 V's, distributed computing foundations]
[Cross-ref: topics/big_data_case_studies.md — applications of data science in practice]
[Cross-ref: topics/big_data_specialization_ucsd.md — course 1 module index]
