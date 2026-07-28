---
course: "IBM Data Warehouse Fundamentals"
module: 1
type: graded_quiz
source: Coursera
---

# Module 1 Graded Quiz: An Introduction to Data Warehouses, Data Marts, and Data Lakes

> **Course 9:** IBM Data Warehouse Fundamentals  
> **Module 1:** Introduction to Data Warehouses, Data Marts, and Data Lakes

---

## Question 1

**What is a data warehouse? Choose the best answer.**

| Option | Correct? |
|--------|----------|
| A data distribution system | ✗ |
| A data storage | ✗ |
| **A system that aggregates data from one or more sources into a single consistent data store to support data analytics** | **✓ CORRECT** |
| None of the above | ✗ |

**Answer:** A system that aggregates data from one or more sources into a single consistent data store to support data analytics

[ENRICHED: definition — A data warehouse is a system that aggregates data from one or more sources into a single, central, consistent data store to support various data analytics requirements. It is a database designed to enable business intelligence activities: it exists to help users understand and enhance their organization's performance. It is designed for query and analysis rather than for transaction processing, and usually contains historical data derived from transaction data, but can include data from other sources. Source: Oracle Documentation] [Source: https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html]

**Analysis:** The course definition from the Data Warehouse Overview video explicitly states: "A data warehouse is a system that aggregates data from one or more sources into a single, central, consistent data store to support various data analytics requirements." Options A and B are too narrow — a data warehouse is more than just distribution or storage; it is purpose-built for analytics. Option D is incorrect because C is the precise definition.

---

## Question 2

**What data warehouse vendors offer "on premises and cloud" services?**

| Option | Correct? |
|--------|----------|
| Amazon RedShift | ✗ (cloud-only) |
| Snowflake | ✗ (cloud-only) |
| Google BigQuery | ✗ (cloud-only) |
| **IBM Db2 Warehouse** | **✓ CORRECT** |

**Answer:** IBM Db2 Warehouse

[ENRICHED: ecosystem — Data warehouse vendors are categorized by deployment model: cloud-only (Amazon Redshift, Snowflake, Google BigQuery), appliances (Oracle Exadata, IBM Netezza), and both on-premises and cloud (Teradata, IBM Db2 Warehouse, Vertica, Oracle Autonomous Data Warehouse). IBM Db2 Warehouse provides a containerized scale-out data warehousing solution that can move workloads between public cloud, private cloud, or on-premises with minimal or no changes required. Source: c9_m1_popular_data_warehouse_systems.md] [Source: C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\updates\providers\ibm\data_warehouse_fundamentals\modules\module_1_introduction_to_data_warehouses\lessons\c9_m1_popular_data_warehouse_systems.md]

**Analysis:** Redshift, Snowflake, and BigQuery are cloud-only platforms. IBM Db2 Warehouse explicitly supports "client-managed, on-premises, cloud, and hybrid environments" and can be deployed in containers on Docker across all three models. The course video on Popular Data Warehouse Systems categorizes vendors into three groups and IBM Db2 Warehouse falls in the "both on-premises and cloud" category.

---

## Question 3

**What are data lake benefits?**

| Option | Correct? |
|--------|----------|
| **Handles all types of data – unstructured, semi-structured, and structured** | **✓ CORRECT** |
| Modifiable navigation paths | ✗ |
| Medium storage capacity | ✗ |
| Handles specifically unstructured data | ✗ |

**Answer:** Handles all types of data – unstructured, semi-structured, and structured

[ENRICHED: definition — A data lake is a storage repository that can store large amounts of structured, semi-structured, and unstructured data in their native format, classified and tagged with metadata. Data lakes can store unstructured data (documents, emails), semi-structured data (JSON, XML files), and structured data from relational databases. Source: c9_m1_data_lakes_overview.md] [Source: C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\updates\providers\ibm\data_warehouse_fundamentals\modules\module_1_introduction_to_data_warehouses\lessons\c9_m1_data_lakes_overview.md]

**Analysis:** The Data Lakes Overview video explicitly lists this as a key benefit: "Data lakes can store all types of data including: unstructured data, such as documents and emails; semi-structured data, such as JSON and XML files; and structured data from relational databases." Option B ("Modifiable navigation paths") is not a data lake concept. Option C ("Medium storage capacity") is incorrect — data lakes offer scalable capacity from terabytes to petabytes, not "medium." Option D is too narrow — data lakes handle ALL data types, not just unstructured.

---

## Question 4

**Where have we started hosting data warehouses in the last decade?**

| Option | Correct? |
|--------|----------|
| On-premises | ✗ (traditional, not new) |
| **In the cloud** | **✓ CORRECT** |
| On the shelf | ✗ |
| None of the answers above is correct | ✗ |

**Answer:** In the cloud

[ENRICHED: performance context — In the last decade or so, with exponential amounts of data being generated and stored in the cloud, Cloud Data Warehouses (CDWs) have gained popularity, where organizations don't purchase hardware or install warehousing software. CDWs offer benefits of cloud computing such as data storage at petabyte scale, highly scalable compute and storage, and pay-as-you-go pricing. They are typically delivered as fully managed SaaS offerings, eliminating the need for upfront investment in hardware or software. Examples include Amazon Redshift, Google BigQuery, Snowflake, and IBM Db2 Warehouse on Cloud. Source: IBM] [Source: https://www.ibm.com/think/topics/data-warehouse]

**Analysis:** The Data Warehouse Overview video explicitly states: "In the last decade or so, with exponential amounts of data being generated and stored in the cloud, Cloud Data Warehouses, frequently called CDWs, have gained popularity." On-premises was the traditional model before this shift. "On the shelf" is not a deployment option.

---

## Question 5

**What are the benefits of a data warehouse?**

| Option | Correct? |
|--------|----------|
| Hosted on-premises | ✗ (deployment model, not a benefit) |
| Large-scale data warehousing management overhead | ✗ (this is a drawback) |
| **Faster business insights** | **✓ CORRECT** |
| None of the answers is correct | ✗ |

**Answer:** Faster business insights

[ENRICHED: ecosystem — The benefits of a data warehouse include: (1) Data integration, removing bad data, eliminating duplicates, and standardizing data create a single source of the truth that results in better data quality for analysis; (2) A single source of truth empowers users to leverage all the company's data and access that data more efficiently; (3) Separating database operations from data analytics generally improves data access performance, leading to faster business insights. Source: c9_m1_data_warehouse_overview.md] [Source: C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\updates\providers\ibm\data_warehouse_fundamentals\modules\module_1_introduction_to_data_warehouses\lessons\c9_m1_data_warehouse_overview.md]

**Analysis:** "Hosted on-premises" is a deployment location, not a benefit. "Large-scale data warehousing management overhead" is explicitly a drawback/challenge, not a benefit. "Faster business insights" is directly stated in the video: "separating database operations from data analytics generally improves data access performance, leading to faster business insights."

---

## Question 6

**What are data marts used for?**

| Option | Correct? |
|--------|----------|
| Better data quality | ✗ |
| **Help end users focus only on relevant data** | **✓ CORRECT** |
| Can quickly repurpose data for a wide range of use cases | ✗ |
| Scalable storage capacity | ✗ |

**Answer:** Help end users focus only on relevant data

[ENRICHED: ecosystem — Data marts are designed to provide specific support for making tactical decisions. As such, data marts are focused only on the most relevant data, which saves end users the time and effort that would otherwise be spent searching the data warehouse for insights. Tactical decisions are short-term, department-level decisions (e.g., which products to promote this quarter, which customers to target), as opposed to strategic decisions that affect the entire enterprise over longer time horizons. Source: DataCamp] [Source: https://www.datacamp.com/blog/data-mart-vs-data-warehouse]

**Analysis:** "Better data quality" is a benefit of data warehouses in general, not specifically data marts. "Can quickly repurpose data for a wide range of use cases" describes data lakes, not data marts (data marts are narrow in scope). "Scalable storage capacity" describes data lakes. The Data Marts Overview video explicitly states: "data marts are focused only on the most relevant data, which saves end users the time and effort that would otherwise be spent searching the data warehouse for insights."

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Q1 Analysis | Definition | Expanded data warehouse definition with Oracle Documentation | HIGH | https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html |
| 2 | Q2 Analysis | Ecosystem connection | Categorized vendors by deployment model (cloud-only, appliance, both) | HIGH | c9_m1_popular_data_warehouse_systems.md |
| 3 | Q3 Analysis | Definition | Expanded data lake data type support with source video quote | HIGH | c9_m1_data_lakes_overview.md |
| 4 | Q4 Analysis | Performance context | Added CDW context with cloud benefits and examples | HIGH | https://www.ibm.com/think/topics/data-warehouse |
| 5 | Q5 Analysis | Ecosystem connection | Listed all three DW benefits from source video | HIGH | c9_m1_data_warehouse_overview.md |
| 6 | Q6 Analysis | Ecosystem connection | Connected tactical decisions to data mart purpose | HIGH | https://www.datacamp.com/blog/data-mart-vs-data-lake |
