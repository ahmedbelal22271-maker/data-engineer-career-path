# Overview of the Data Engineering Ecosystem

## Course 1: Introduction to Data Engineering — Module 2: The Data Ecosystem and Languages for Data Professionals

A data engineer's ecosystem encompasses the infrastructure, tools, frameworks, and processes for:

- Extracting data from disparate sources
- Architecting and managing data pipelines for transformation, integration, and storage
- Architecting and managing data repositories
- Automating and optimizing workflows and the flow of data between systems
- Developing applications needed throughout the data engineering workflow

---

## Data

### Types of Data

Based on how well-defined its structure is, data falls into three categories:

| Type | Description | Examples |
|---|---|---|
| **Structured** | Follows a rigid format; organized into rows and columns | Databases, spreadsheets |
| **Semi-structured** | Mix of consistent and non-conforming structure | Emails (sender/recipient = structured; body = unstructured) |
| **Unstructured** | Complex, mostly qualitative; cannot be reduced to rows and columns | Photos, videos, text files, PDFs, social media content |

> The type of data drives the kind of data repositories it can be stored in, as well as the tools that can be used to query or process it.

### File Formats and Data Sources

Data comes in a wide variety of file formats and is collected from sources including:
- Relational and non-relational databases
- APIs and web services
- Data streams
- Social platforms
- Sensor devices

---

## Data Repositories

There are two main types of data repositories:

### Transactional Systems (OLTP)
- Full name: **Online Transaction Processing**
- Designed to store high-volume, day-to-day operational data
- Examples: online banking transactions, ATM transactions, airline bookings
- Typically relational, but can also be non-relational

### Analytical Systems (OLAP)
- Full name: **Online Analytical Processing**
- Optimized for conducting complex data analytics
- Includes: relational and non-relational databases, data warehouses, data marts, data lakes, and big data stores

> The type, format, sources of data, and context of use all influence which repository is the right choice.

---

## Data Integration and Pipelines

Once data from disparate sources is collated, it must be processed, cleansed, and integrated so it can be accessed via a single interface.

- **Data Integration Tools** — combine data from disparate sources into a unified view for users to query and manipulate
- **Data Pipelines** — a set of tools and processes covering the entire journey of data from source to destination systems

Data is integrated within a pipeline using one of two approaches:

| Process | Description |
|---|---|
| **ETL** (Extract, Transform, Load) | Data is transformed before loading into the destination |
| **ELT** (Extract, Load, Transform) | Data is loaded first, then transformed at the destination |

---

## Languages

Languages used in data engineering are classified into three categories:

| Category | Purpose | Examples |
|---|---|---|
| **Query Languages** | Querying and manipulating data | SQL |
| **Programming Languages** | Developing data applications and pipelines | Python |
| **Shell & Scripting Languages** | Automating repetitive operational tasks | Bash, Shell scripts |

---

## BI and Reporting Tools

- Collect data from multiple sources and present it in visual formats such as interactive dashboards
- Support real-time and scheduled data visualization
- Drag-and-drop products — no programming knowledge required for end users
- Typically used by Data and BI Analysts, but **enabled and managed by Data Engineers**

---

## Summary

The data engineering ecosystem is a diverse and interconnected set of components:

```
Data Sources → Data Pipelines (ETL/ELT) → Data Repositories → BI & Reporting Tools
                        ↑
          Languages, Integration Tools, Automated Frameworks
```

Each component — from raw data types and storage systems to pipelines and reporting — plays a distinct role in ensuring data flows reliably from source to consumer.

*Source: IBM Data Engineering Fundamentals — Module 2: Overview of the Data Engineering Ecosystem*
