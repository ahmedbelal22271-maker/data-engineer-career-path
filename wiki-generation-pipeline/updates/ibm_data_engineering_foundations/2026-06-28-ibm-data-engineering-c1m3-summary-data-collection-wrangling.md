> **Course 1:** Introduction to Data Engineering
> **Module 3:** Data Engineering Lifecycle

# Summary and Highlights: Data Collection and Data Wrangling

## Overview

This summary consolidates the key concepts covered across the Data Collection, Data Wrangling, and Data Wrangling Tools lessons in this module.

---

## Gathering Data

Depending on where data must be sourced from, a range of methods and tools are available:

| Method | Description |
|---|---|
| **Query Languages** | Extract data from relational and non-relational databases (SQL, CQL, GraphQL) |
| **APIs** | Access endpoints to extract data from databases, web services, and data marketplaces; also used for data validation |
| **Web Scraping** | Download specific data from web pages based on defined parameters |
| **Data Streams** | Aggregate continuous real-time data from IoT devices, instruments, GPS, and social media |
| **RSS Feeds** | Capture continuously refreshed data from forums and news sites |
| **Data Exchanges** | Structured platforms for exchanging data between providers and consumers under defined standards and governance frameworks |

---

## Data Wrangling (Data Munging)

Once data has been gathered and imported, it must be made **analytics-ready** through data wrangling — an iterative process of transformation and cleansing.

### Transformation Tasks

| Transformation | Purpose |
|---|---|
| **Joins** | Combine columns from multiple tables into a single row |
| **Unions** | Combine rows from multiple tables into a single table |
| **Normalization** | Clean the database of unused and redundant data |
| **Denormalization** | Combine data from multiple tables into a single table for faster querying |

### Cleansing Activities

| Activity | Purpose |
|---|---|
| **Data Profiling** | Inspect source data to uncover anomalies and quality issues (nulls, duplicates, out-of-range values) |
| **Data Visualization** | Apply statistical methods to spot outliers |
| **Fixing Data Issues** | Address missing values, duplicate data, irrelevant data, inconsistent formats, syntax errors, and outliers |

---

## Data Wrangling Tools

A variety of tools are available, each with their own features, strengths, limitations, and applications:

| Tool | Type |
|---|---|
| **Excel Power Query / Spreadsheets** | Manual wrangling; add-ins for import and transformation |
| **OpenRefine** | Open-source; format conversion and web service enrichment |
| **Google DataPrep** | Managed cloud service; visual exploration with auto-detection |
| **Watson Studio / IBM Data Refinery** | Enterprise cloud service; governance policy enforcement |
| **Trifacta Wrangler** | Cloud-based; strong collaboration features |
| **Python** (Jupyter, NumPy, Pandas) | Programmatic large-scale data manipulation |
| **R** (Dplyr, Data.table, Jsonlite) | Statistical wrangling and API data interaction |

---

## Key Takeaways

- Data can be gathered using query languages, APIs, web scraping, data streams, RSS feeds, and data exchange platforms.
- **Data wrangling** transforms raw data into analytics-ready information through both structural transformations and cleansing activities.
- Structural transformations include **joins, unions, normalization, and denormalization**.
- Cleansing activities include **profiling, visualization, and fixing** issues such as missing values, duplicates, irrelevant data, format inconsistencies, syntax errors, and outliers.
- Tool selection depends on data size, structure, required capabilities, infrastructure, and team expertise.
