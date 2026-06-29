> **Course 1:** Introduction to Data Engineering
> **Module 3:** Data Engineering Lifecycle

# How to Gather and Import Data

## Overview

Collecting data from its sources and loading it into a data repository is the first practical step in the data engineering lifecycle. This lesson covers the primary methods for gathering data from various source types, and the tools and considerations for importing that data into the appropriate destination repository.

```mermaid
flowchart LR
    subgraph Sources["Data Sources"]
        S1[(Relational DBs)]
        S2[Web APIs]
        S3[Web Pages]
        S4[RSS Feeds]
        S5[Sensors / IoT]
        S6[Data Exchanges]
    end

    subgraph Methods["Gathering Methods"]
        M1[SQL Queries]
        M2[API Calls]
        M3[Web Scraping]
        M4[RSS Readers]
        M5[Streaming]
        M6[Exchange Platforms]
    end

    subgraph Destination["Destination Repositories"]
        D1[(RDBMS)]
        D2[(NoSQL)]
        D3[(Data Lake)]
    end

    S1 --> M1
    S2 --> M2
    S3 --> M3
    S4 --> M4
    S5 --> M5
    S6 --> M6

    M1 --> D1
    M2 --> D2
    M3 --> D3
    M4 --> D2
    M5 --> D3
    M6 --> D1
```

---

## Part 1: Methods for Gathering Data

### SQL — Querying Relational Databases

SQL (Structured Query Language) is the standard method for extracting data from relational databases. Core SQL capabilities include:

- Specifying **what** to retrieve
- Identifying the **table** to extract from
- **Grouping** records with matching values
- **Ordering** query results
- **Limiting** the number of results returned

Non-relational databases can also be queried using SQL or SQL-like tools. Some NoSQL systems have their own native query languages:

| Database | Query Language |
|---|---|
| Cassandra | CQL (Cassandra Query Language) |
| Neo4J | GraphQL / Cypher |

Extraction queries typically use `SELECT` statements, often with incremental filtering (e.g., `WHERE created_at > last_run`) to pull only new or changed records since the previous extraction.

---

### APIs — Application Programming Interfaces

APIs are widely used for extracting data from a broad range of sources. Key characteristics:

- Invoked by applications that require the data
- Access **endpoints** containing the data — endpoints can be databases, web services, or data marketplaces
- Also used for **data validation** (e.g., validating postal addresses and zip codes)

APIs typically return data in **JSON** or **XML** format. RESTful APIs are the most common architecture; GraphQL is an emerging alternative that allows the caller to specify exactly which fields they need.

---

### Web Scraping

Also known as **screen scraping** or **web harvesting** — used for downloading specific data from web pages based on defined parameters.

Common types of data extracted via web scraping:
- Text and contact information
- Images, videos, and podcasts
- Product listings and pricing data

> **Legal note:** Web scraping exists in a gray area legally. Always check the target website's `robots.txt` and terms of service before scraping. Some sites explicitly prohibit automated data collection.

---

### RSS Feeds

RSS feeds capture **continuously refreshed data** from online sources such as:
- Online forums
- News sites

Useful when data at the source is updated on an ongoing basis and needs to be captured incrementally. RSS is a lightweight XML-based format — data engineers often set up feed readers or scheduled scripts to poll feeds at regular intervals.

---

### Data Streams

Data streams aggregate **constant, real-time flows** of data from:
- Instruments and sensors
- IoT devices and applications
- GPS data from vehicles

Data streams and feeds are also used to extract data from **social media platforms** and **interactive platforms**.

Common streaming technologies include **Apache Kafka**, **Amazon Kinesis**, and **Google Pub/Sub**. Unlike batch extraction, streaming ingests data as it is produced, enabling near-real-time analytics.

---

### Data Exchange Platforms

Data Exchange platforms facilitate the exchange of data between **data providers** and **data consumers** under well-defined standards, protocols, and formats.

Beyond data transfer, these platforms provide:

| Feature | Description |
|---|---|
| **Security and governance** | Maintained throughout the exchange process |
| **Data licensing workflows** | Legal frameworks governing data use |
| **De-identification and PII protection** | Personal information is protected before exchange |
| **Quarantined analytics environment** | Safe environment for analyzing exchanged data |

**Popular data exchange platforms:**
- AWS Data Exchange
- Crunchbase
- Lotame
- Snowflake

---

### Specialized Research and Advisory Sources

For specific data needs, trusted external sources include:

| Data Need | Trusted Sources |
|---|---|
| Marketing trends and ad spending | Forrester, Business Insider |
| Strategic and operational guidance | Gartner, Forrester |
| User behavior, mobile/web usage, market surveys, demographics | Various industry-specific providers |

---

## Part 2: Importing Data into Repositories

Once data is gathered, it must be **loaded into a data repository** before it can be wrangled, mined, or analyzed. The importing process combines data from multiple sources into a unified view that can be queried and manipulated through a single interface.

The right approach depends on three factors: **data type**, **volume of data**, and **type of destination repository**.

```mermaid
flowchart TD
    subgraph ImportFlow["Import Process"]
        EX[Extract from source]
        TR[Transform &#40;if needed&#41;]
        LO[Load into repository]
    end

    EX --> TR --> LO

    TR -->|ETL| OLAP[(Warehouse / OLAP)]
    TR -->|ELT| DL[(Data Lake)]

    LO --> QA[Query &amp; Analyze]
```

> **ETL vs. ELT:** In the traditional **ETL** pattern, data is transformed before loading — suited for warehouses with rigid schemas. In **ELT** (Extract, Load, Transform), raw data is loaded first and transformed in-place — preferred for data lakes and cloud-scale platforms where compute is cheap and storage is flexible.

---

### Data Types and Their Compatible Repositories

| Data Type | Description | Examples | Compatible Repositories |
|---|---|---|---|
| **Structured** | Well-defined schema, tabular | OLTP systems, spreadsheets, online forms, sensor data, network/web logs | Relational databases, NoSQL |
| **Semi-structured** | Some organizational properties, no rigid schema | Emails, XML, zipped files, binary executables, TCP/IP protocols | NoSQL clusters; XML and JSON formats |
| **Unstructured** | No structure, cannot be organized into a schema | Web pages, social media feeds, images, videos, documents, media logs, surveys | NoSQL databases, Data Lakes |

> **Note:** Data Lakes can accommodate **all data types and schemas** — structured, semi-structured, and unstructured — making them the most flexible destination for large-scale raw data storage.

> **JSON** is the preferred data type for web services and is also commonly used alongside XML for storing and exchanging semi-structured data.

---

### Batch vs. Streaming Ingestion

| Dimension | Batch Ingestion | Streaming Ingestion |
|---|---|---|
| **Frequency** | Scheduled intervals (hourly, daily) | Continuous, event-driven |
| **Latency** | Minutes to hours | Seconds to milliseconds |
| **Typical volume per run** | Large, bounded datasets | Small, unbounded records |
| **Common tools** | Apache Airflow, Talend, cron jobs | Apache Kafka, Kinesis, Flink |
| **Use case** | Nightly warehouse loads, ETL jobs | Real-time dashboards, fraud detection |

---

### Tools for Importing Data

| Tool / Language | Type |
|---|---|
| **Talend** | ETL tool — automates data import pipelines |
| **Informatica** | ETL tool — enterprise data integration |
| **Python** (with libraries) | Programming language for custom import workflows |
| **R** (with libraries) | Programming language for statistical data import |
| **Apache NiFi** | Data flow automation with visual UI |
| **dbt** | Transformation tool focused on ELT workflows |

ETL tools and data pipelines provide **automated functions** that streamline the importing process end-to-end.

#### Python Import Example

```python
import pandas as pd
from sqlalchemy import create_engine

# Extract: read from a CSV source
df = pd.read_csv("source_data.csv")

# Transform: clean and type-cast
df["event_date"] = pd.to_datetime(df["event_date"])
df.dropna(subset=["user_id"], inplace=True)

# Load: write to a PostgreSQL database
engine = create_engine("postgresql://user:pass@host:5432/mydb")
df.to_sql("events", engine, if_exists="append", index=False)
```

---

## Key Takeaways

- Data can be gathered using **SQL**, **APIs**, **web scraping**, **RSS feeds**, **data streams**, **data exchange platforms**, and **specialized research sources** — each suited to different source types and use cases.
- APIs serve dual purposes: **data extraction** and **data validation**.
- **Data exchange platforms** go beyond simple transfer — they enforce security, governance, licensing, and PII protection.
- The destination repository must match the data type: **structured → RDBMS or NoSQL**; **semi-structured → NoSQL clusters**; **unstructured → NoSQL or Data Lake**.
- **Data Lakes** are the most flexible option, capable of storing all data types and schemas.
- **JSON** is the preferred format for web services; **XML and JSON** are standard formats for semi-structured data exchange.
- **ETL tools** (Talend, Informatica) and programming languages (Python, R) automate and facilitate the data import process.

---

## Glossary

| Term | Definition |
|---|---|
| **ETL** | Extract, Transform, Load — transformation happens before loading |
| **ELT** | Extract, Load, Transform — raw data loaded first, transformed in-place |
| **REST API** | Representational State Transfer — stateless web API architecture using HTTP verbs |
| **RSS** | Really Simple Syndication — XML-based format for publishing frequently updated content |
| **Data Stream** | Continuous flow of data records, typically processed in near-real-time |
| **Web Scraping** | Automated extraction of data from web page HTML |
| **Data Exchange Platform** | Marketplace or intermediary for sharing data between providers and consumers with governance controls |
