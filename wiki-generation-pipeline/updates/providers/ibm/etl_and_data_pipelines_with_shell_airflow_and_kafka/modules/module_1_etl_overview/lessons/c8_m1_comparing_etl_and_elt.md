**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 1:** Extract, Transform, Load (ETL) Overview

# Comparing ETL and ELT

## Learning Objectives

After watching this video, you will be able to list key differences between ETL and ELT, describe ELT as an evolution of ETL and describe the trending shift from ETL to ELT.

## Key Differences Between ETL and ELT

Differences between ETL and ELT, for one thing, the transformations happen in a different order. Transformations for ETL pipelines take place within the data pipeline before the data reaches its destination, whereas transformations for ELT are decoupled from the data pipeline and happen in the destination environment at will.

[ENRICHED: added specificity — "decoupled from the data pipeline" means the transformation logic is not embedded in the pipeline code itself. In ETL, the transformation is a hardcoded step (e.g., a Python function or SQL script) that runs as part of the pipeline DAG. In ELT, the raw data lands in the destination untouched, and transformation happens independently — a data analyst can run a dbt model, a data scientist can write a custom PySpark script, and a BI tool can apply its own aggregations, all against the same raw data without modifying the pipeline.]

They also differ in flexibility in how they can be used. ETL is normally a fixed process meant to serve a very specific function, whereas ELT is flexible, making data readily available for self-serve analytics. They also differ in their ability to handle big data. ETL processes traditionally handle structured relational data, and on-premises computing resources handle the workflow. Thus, scalability can be a problem.

[ENRICHED: defined "structured relational data" — data organized into tables with predefined schemas (columns with fixed data types), where relationships between tables are enforced by foreign keys. Examples: customer tables, order tables, transaction logs stored in RDBMS like PostgreSQL or MySQL.]

[ENRICHED: important clarification — the course links ETL to fixed on-premises hardware and ELT to cloud, which is a historical simplification. ETL **can** run on the cloud (tools like AWS Glue, Azure Data Factory exist). The real difference is not where it runs, but **when** the transformation happens. ETL transforms **before** loading (you must define schemas and transformations in advance), ELT loads raw data **first** and transforms later (on demand). ELT's approach is inherently easier to scale because: (1) raw storage is cheap (~$0.02/GB/month in S3), (2) compute scales to zero when idle, (3) multiple teams can transform the same data independently without modifying the pipeline. The scenario below illustrates the historical pattern the course describes, where ETL was tied to on-premises infrastructure.]

**Why scalability is a problem for ETL but not ELT — a concrete scenario:**

Imagine a grocery chain that processes 1 million transactions per day. Their ETL pipeline runs on two servers they own in a server room:

```
ETL — ON-PREMISES (owned hardware):

January:  1M transactions/day → 2 servers handle it fine ✓
June:     3M transactions/day → servers overload, pipeline crashes ✗
          Solution: buy 2 more servers
          Cost: $40,000
          Time: 6 weeks to procure, install, configure
          
December: 8M transactions/day (holiday rush) → still not enough ✗
          Solution: buy 4 more servers
          Cost: $80,000
          Time: 6 more weeks

January:  1M transactions/day again → 8 servers sitting idle
          You're paying for hardware you don't need 11 months/year
```

**The core problem:** You must buy hardware for the **peak** (December's 8M), but you **pay for it all year** even though you only need it for one month. And you can't predict the future — what if next December hits 12M? You'd need to buy again.

```
ELT — CLOUD (rented hardware, scale on demand):

January:  1M transactions/day → 2 cloud nodes running
          Cost: $200/month
          
June:     3M transactions/day → cloud auto-scales to 6 nodes
          Cost: $600/month
          
December: 8M transactions/day → cloud auto-scales to 16 nodes
          Cost: $1,600/month

January:  1M transactions/day → cloud auto-scales back to 2 nodes
          Cost: $200/month again
```

**The difference:**

| | ETL (On-Premises) | ELT (Cloud) |
|---|---|---|
| **Hardware** | You own it, permanently | You rent it, flexibly |
| **Scaling up** | Buy servers → 6 weeks → $40K+ | Click → instant → pay per hour |
| **Scaling down** | Can't — servers sit idle | Automatic — costs drop immediately |
| **Peak capacity** | Must over-provision year-round | Rents peak capacity only when needed |
| **Data type** | Structured tables only (RDBMS) | Any format: tables, JSON, images, logs |
| **Annual cost example** | $120K+ (fixed, wasteful) | $4K–$20K (varies with actual usage) |

The scalability problem isn't about the data itself — it's about the **infrastructure**. ETL on fixed hardware can't grow or shrink with demand. ELT on cloud infrastructure grows and shrinks automatically, and you only pay for what you use.

ELT, on the other hand, handles any kind of data structured and unstructured. And to handle scalability problems posed by big data, ELT leverages the on-demand scalability offered by cloud-computing services.

[ENRICHED: defined "unstructured data" — data without a predefined schema or tabular structure, such as text documents, images, video files, audio recordings, and raw JSON/XML. Unstructured data accounts for an estimated 80–90% of all data generated globally, and storing it affordably requires object storage (e.g., S3) rather than traditional relational databases.]

With regard to data discovery and time-to-insight, ETL pipelines take time and effort to modify, which means, users must wait for the development team to implement their requested changes. ELT provides more agility with some training in modern analytics applications, end users can easily connect to and experiment with the raw data, create their own dashboards, and run predictive models themselves.

[ENRICHED: concrete example — a marketing analyst wants to see customer lifetime value (CLV) broken down by acquisition channel. In an ETL world, they file a ticket with the data engineering team, who estimate 2 weeks of work to add a new transformation step, join the `customers` and `marketing_attribution` tables, compute CLV, and refresh the data warehouse. In an ELT world, the analyst opens a SQL workbook, connects to the data warehouse, runs a CLV query against the raw data, and has the answer in 30 minutes — no engineering intervention needed.]

## ELT as an Evolution of ETL

ELT is a natural evolution of ETL. One of the factors driving that evolution is the demand to release raw data to a wider user base for the enterprise. Traditionally, ETL processes include an intermediate storage facility called a staging area. This is a holding area for raw, extracted data where you can run processes prior to loading the resulting transformed data into a data warehouse or a data mart.

[ENRICHED: defined "staging area" — an intermediate database or storage location used during the ETL process to hold raw extracted data before it is transformed and loaded into the final destination. The staging area serves as a buffer: it absorbs data from source systems at ingestion speed, provides a clean checkpoint for transformation failures (you can re-transform from staging without re-extracting from source), and isolates source systems from destination writes. Common implementations include temporary database schemas, staging tables in the target warehouse, or cloud storage buckets.]

This sounds a lot like an ELT process, and the staging area fits the description of a data lake, which is a modern self-serve repository for storing and manipulating raw data. A traditional staging area, however, is not something that is usually shared across the company. Its a private siloed area set aside for developing, monitoring and performance tuning the data pipeline and its built-in transformations.

[ENRICHED: added specificity — the staging area and data lake serve similar purposes (holding raw data temporarily) but differ in who uses them, how long data stays, and what you can do with it:]

**Staging Area vs Data Lake — Side-by-Side Comparison:**

```
STAGING AREA (ETL)                    DATA LAKE (ELT)
─────────────────                    ───────────────

┌──────────────────┐                 ┌──────────────────┐
│  Engineering     │                 │  WHOLE COMPANY   │
│  team only       │                 │                  │
│                  │                 │  Data engineers  │
│  Data Engineer A │                 │  Data scientists │
│  Data Engineer B │                 │  Analysts        │
│                  │                 │  Managers        │
│  No one else     │                 │  Marketing       │
│  can access it   │                 │  Finance         │
└──────────────────┘                 └──────────────────┘
```

| Aspect | Staging Area | Data Lake |
|---|---|---|
| **Who uses it** | Data engineers only | Anyone in the company (with permissions) |
| **Purpose** | Temporary holding area during ETL processing | Permanent raw data repository for the whole organization |
| **How long data stays** | Minutes to hours — just long enough to transform and load | Months to years — raw data is preserved indefinitely |
| **Who writes to it** | The ETL pipeline (automated) | Multiple sources (automated + manual uploads) |
| **Who reads from it** | The ETL pipeline only | Data engineers, scientists, analysts, BI tools, ML models |
| **Can you query it directly?** | No — it's not designed for querying | Yes — that's the whole point |
| **Schema** | Fixed (matches the pipeline's transformation logic) | Schema-on-read (apply schema when you read, not when you write) |
| **Analogy** | A loading dock — goods arrive, get processed, and leave | A warehouse — goods arrive and stay, anyone can browse the shelves |

**What they have in common:**
- Both hold raw data before it reaches its final destination
- Both act as a buffer between source systems and the analytics environment
- Both decouple data ingestion from data consumption

**The key difference:**
A staging area is a **private workshop** — data engineers use it behind closed doors, transform the data, and deliver the finished product to the data warehouse. A data lake is a **public library** — raw data sits on the shelves, and anyone with a library card can walk in, pull a book, and read it however they want.

Along with the ever-increasing ease of use and connection capabilities of analytics tools, raw data sources have become much more accessible to less technical end users. Accordingly, the paradigm is shifting to self-service data platforms.

## The Shift from ETL to ELT

There is still a place for conventional ETL in developing data pipelines, so ETL is not disappearing anytime soon. However, there is a trend taking place, a trend which is favoring modern ELT over conventional ETL. The trend is being driven by the pain points that ELT solves, namely, the lengthy time-to-insight, the challenges, for example, scalability imposed by big data, and the conventional siloed nature of data.

[ENRICHED: concrete example — "siloed nature of data" manifests as: the sales team has their CRM data in Salesforce, the marketing team has their campaign data in Google Analytics, the finance team has their transaction data in NetSuite, and none of these teams can easily combine datasets for cross-functional analysis. ELT + a data lake breaks these silos by ingesting all raw data into one central repository where any team can join and analyze it.]

## Summary

In this video, you learned that:
- Key differences between ETL and ELT are the location where the transformation takes place, flexibility, big data support, and time-to-insight.
- One of the factors driving the evolution from ETL to ELT is the demand to release raw data to a wider user base for the enterprise.
- Conventional ETL has many applications and still has its place.
- ELT is more flexible than ETL, enabling end users to perform ad-hoc self-service data analytics in real time.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Transformations paragraph | Added specificity | Explained "decoupled" as independent transformation logic (dbt, PySpark, BI tools) vs hardcoded pipeline steps | HIGH |
| 2 | Big data paragraph | Definition | Defined "structured relational data" with RDBMS examples | HIGH |
| 3 | Big data paragraph | Added specificity | Explained on-premises CapEx vs cloud OpEx scaling | HIGH |
| 4 | ELT paragraph | Definition | Defined "unstructured data" with 80-90% of global data statistic | HIGH |
| 5 | Agility paragraph | Concrete example | CLV by acquisition channel: 2-week ETL ticket vs 30-minute ELT query | HIGH |
| 6 | Staging area paragraph | Definition | Defined "staging area" as intermediate ETL buffer with checkpoint/re-isolation purpose | HIGH |
| 7 | Staging vs data lake paragraph | Added specificity | Distinguished staging (engineering-internal) from data lake (shared organizational asset) | HIGH |
| 8 | Self-service paragraph | Concrete example | Illustrated "siloed data" with CRM/Google Analytics/NetSuite cross-functional analysis gap | HIGH |

<!-- EXTRACTION_CHECKLIST: 30 sentences extracted, 30 sentences in output -->
