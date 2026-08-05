**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 1:** Extract, Transform, Load (ETL) Overview

# ETL Fundamentals

## Learning Objectives

After watching this video, you will be able to:
- describe what an ETL process is,
- describe what data extraction means,
- describe what data transformation means,
- describe what data loading means, and
- list use cases for ETL processes.

## What is an ETL Process?

ETL stands for Extract, Transform, and Load. ETL is an automated data pipeline engineering methodology, whereby data is acquired and prepared for subsequent use in an analytics environment, such as a data warehouse or data mart. [ENRICHED: defined "data mart" — a focused subset of a data warehouse containing only the tables relevant to one department, business line, or subject area. A data warehouse holds ALL company data (sales, marketing, HR, finance, support, etc.), but the sales team doesn't need HR records and the marketing team doesn't need payroll data. A sales data mart contains only customers, orders, and products — the tables the sales team actually queries. This makes their queries 10–100× faster (they scan far less data) and simpler (they see only relevant tables, not the full warehouse schema). Physically, a mart can exist as: (1) a schema (namespace) within the same warehouse database, (2) a separate small database populated by ETL jobs that copy relevant tables nightly, or (3) a set of database views that filter warehouse tables on the fly without copying data.] ETL refers to the process of curating data from multiple sources, conforming it to a unified data format or structure, and then loading the transformed data into its new environment. The extraction process obtains or reads the data from one or more sources. The transformation process wrangles the data into a format that is suitable for its destination and its intended use. The final loading process takes the transformed data and loads it into its new environment, ready for visualization, exploration, further transformation, and modeling. The curated data may also be utilized to support automation and decision-making.

## What is Extraction?

To extract data is to configure access to it and read it into an application. Normally this is an automated process. Some common methods include:

- **Web scraping**, where data is extracted from web pages using applications such as Python or R to parse the underlying HTML code, and
- **Using APIs** to programmatically connect to data and query it.

[ENRICHED: concrete example — web scraping example: using Python's `requests` + `BeautifulSoup` libraries to fetch an HTML page, parse its structure (the hierarchy of HTML tags like `<table>`, `<tr>`, `<td>`), and extract a table of population statistics into a CSV file. API example: calling the REST API of a CRM system (e.g., Salesforce) with an API key, requesting the `/accounts` endpoint, and receiving a JSON response containing all customer account records.]

The source data may be relatively static, such as a data archive, in which case the extraction step would be a stage within a batch process. On the other hand, the data could be streaming live, and from many locations. Examples include weather station data, social networking feeds, and IoT devices.

[ENRICHED: defined "batch process" — a data processing approach where data is collected over a period (hourly, daily, weekly) and processed all at once in a single run, as opposed to stream processing where each record is processed individually as it arrives. Batch is simpler to implement and debug; streaming enables lower latency but requires more complex infrastructure (Kafka, Flink, Spark Streaming).] [ENRICHED: defined "IoT devices" — Internet of Things devices: physical objects (sensors, actuators, wearables, industrial equipment) embedded with network connectivity that generate and transmit data. A single smart factory may have thousands of IoT sensors producing temperature, pressure, vibration, and humidity readings every second.]

## What is Data Transformation?

Data transformation, also known as data wrangling, means processing data to make it conform to the requirements of both the target system and the intended use case for the curated data. [ENRICHED: defined "data wrangling" — the process of cleaning, restructuring, and enriching raw data into a format suitable for analysis. Also called data munging. The term emphasizes the iterative, exploratory nature of the work — unlike the more structured "data transformation" which implies a defined, repeatable pipeline step.]

Transformation can include any of the following kinds of processes:

- **Cleaning**: fixing errors or missing values. [ENRICHED: concrete example — replacing `NULL` values in a `customer_age` column with the column median, removing duplicate rows where `order_id` appears twice, and correcting a typo where "New Yrok" should be "New York".]
- **Filtering**: selecting only what is needed. [ENRICHED: concrete example — from a raw log file containing 10 million HTTP requests, filtering to only keep requests with a `200 OK` status code and a response time greater than 2 seconds, discarding all other rows.]
- **Joining disparate data sources**: merging related data. [ENRICHED: concrete example — joining a `customers` table (from a CRM database) with an `orders` table (from an e-commerce platform) on `customer_id`, producing a unified dataset that shows each customer's purchase history alongside their contact information.]
- **Feature engineering**: such as creating KPIs for dashboards or machine learning. [ENRICHED: defined "feature engineering" — the process of creating new input variables (features) from raw data to improve model performance or enable new analytics. Examples: computing `average_order_value` from individual transactions, extracting `day_of_week` from a timestamp, or calculating a `churn_risk_score` from usage patterns.]
- **Formatting and data typing**: making the data compatible with its destination. [ENRICHED: concrete example — converting a string column `"2024-01-15"` to a `DATE` type, casting a float `19.99` to a `DECIMAL(10,2)` for a financial database, and encoding a categorical column `"country"` as integers for a machine learning model.]

## What is Data Loading?

Generally this just means writing data to some new destination environment. Typical destinations include databases, data warehouses, and data marts. The key goal of data loading is to make the data readily available for ingestion by analytics applications so that end users can gain value from it. Applications include dashboards, reports, and advanced analytics such as forecasting and classification.

[ENRICHED: added specificity — "ingestion by analytics applications" means the destination must support the query patterns these tools use: dashboards need fast aggregate queries (e.g., "total revenue by region by month"), reports need parameterized filters, and forecasting/classification models need feature stores or direct data access. This is why data warehouse schemas are designed for read performance — columnar storage (e.g., Amazon Redshift, Google BigQuery) and materialized views are common choices.]

## Use Cases for ETL Pipelines

A very large amount of information is either already recorded or being generated, but is not yet captured, or accessible, as a digital file. Examples include paper documents, photos and illustrations, and analog audio and video tapes. Digitizing analog data includes extraction by some form of scanning, analog-to-digital transformation, and, finally, storage into a repository.

[ENRICHED: concrete example — a hospital digitizing 50 years of paper medical records: (1) scanning paper charts into image files (extraction), (2) using OCR (Optical Character Recognition) to convert images into searchable text (transformation), and (3) loading the extracted text into a patient records database with structured fields (diagnosis, date, physician) for querying (loading).]

Online transaction processing (OLTP) systems don't save historical data. Accordingly, ETL processes capture the transaction history and prepare it for subsequent analysis in an online analytical processing (OLAP) system.

[ENRICHED: defined "OLTP (Online Transaction Processing)" — a system optimized for recording individual transactions in real time (e.g., a point-of-sale system, banking application, or e-commerce checkout). OLTP databases are designed for fast writes, ACID compliance, and row-level operations. They typically do not retain historical snapshots — once a row is updated, the old value is overwritten.] [ENRICHED: defined "OLAP (Online Analytical Processing)" — a system optimized for analyzing historical data across multiple dimensions (e.g., "total sales by product by region by quarter"). OLAP databases use denormalized schemas (star/snowflake), columnar storage, and are optimized for read-heavy aggregate queries. The ETL process bridges OLTP and OLAP by capturing transaction history and restructuring it for analytical use.]

Other use cases include engineering 'features', or KPIs, from data sources, as preparation for ingestion by dashboards used by operations, sales and marketing, customers, and executives. Training and deploying machine learning models for prediction and augmented decision-making.

## Summary

In this video, you learned that:
- ETL (Extract, Transform, Load) is an acronym for an automated data pipeline engineering methodology whereby data is acquired and prepared for subsequent use in an analytics environment, such as a data warehouse or data mart.
- The extraction process obtains the data from one or more sources.
- The transformation process wrangles the data into a format that is suitable for its destination and its intended use.
- The final loading process takes the transformed data and loads it into its new environment, ready for visualization, exploration, further transformation, and modeling.
- ETL is used for curating data and making it accessible to end users, for example, training and deploying machine learning models for prediction and augmented decision-making.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | What is ETL section | Definition | Defined "data mart" as DW subset focused on specific business line/department | HIGH |
| 2 | Extraction section | Concrete example | Added web scraping (BeautifulSoup) and API (Salesforce REST API) examples | HIGH |
| 3 | Extraction section | Definition | Defined "batch process" vs stream processing | HIGH |
| 4 | Extraction section | Definition | Defined "IoT devices" with smart factory example | HIGH |
| 5 | Transformation section | Definition | Defined "data wrangling" as iterative data cleaning/enrichment | HIGH |
| 6 | Cleaning row | Concrete example | NULL replacement, duplicate removal, typo correction example | HIGH |
| 7 | Filtering row | Concrete example | HTTP log filtering for 200 OK + slow responses | HIGH |
| 8 | Joining row | Concrete example | CRM customers + e-commerce orders join on customer_id | HIGH |
| 9 | Feature engineering row | Definition | Defined feature engineering with average_order_value, day_of_week examples | HIGH |
| 10 | Formatting row | Concrete example | String→DATE, float→DECIMAL, categorical→integer examples | HIGH |
| 11 | Data loading section | Added specificity | Explained OLAP query patterns (aggregate, parameterized, feature store) | HIGH |
| 12 | Use cases section | Concrete example | Hospital digitizing 50 years of paper records: scan→OCR→database | HIGH |
| 13 | OLTP/OLAP paragraph | Definition | Defined OLTP as transaction-optimized, row-level, ACID-compliant | HIGH |
| 14 | OLTP/OLAP paragraph | Definition | Defined OLAP as analysis-optimized, denormalized, columnar, aggregate queries | HIGH |

<!-- EXTRACTION_CHECKLIST: 28 sentences extracted, 28 sentences in output -->
