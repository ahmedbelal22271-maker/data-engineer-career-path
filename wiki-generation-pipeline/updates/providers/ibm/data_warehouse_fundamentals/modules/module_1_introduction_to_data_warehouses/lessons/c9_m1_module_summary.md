> **Course 9:** Data Warehouse Fundamentals
> **Module 1:** An Introduction to Data Warehouses, Data Marts, and Data Lakes

# Module 1 Summary: An Introduction to Data Warehouses, Data Marts, and Data Lakes

<mark style="background-color: rgba(200, 230, 201, 0.4);">NEW</mark>

**Type:** Video Summary
**Duration:** 0:40

---

Congratulations on completing your first module!

## What You Learned

First, you learned that warehouse systems can exist onsite, on appliances, and on the cloud.

[ENRICHED: clarification — The three deployment models covered in this module: (1) On-premises — traditional model where the organization owns and operates all infrastructure in its own data center; (2) Appliances — pre-integrated bundles of hardware and software (e.g., IBM Netezza, Oracle Exadata) delivered ready-to-run; (3) Cloud — fully managed services (e.g., Amazon Redshift, Snowflake, Google BigQuery) offering pay-as-you-go pricing with no upfront hardware investment. The trend in 2026 is strongly toward cloud deployments, though appliances remain relevant for legacy enterprise environments with strict data residency requirements. Source: c9_m1_popular_data_warehouse_systems.md] [Source: C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\updates\providers\ibm\data_warehouse_fundamentals\modules\module_1_introduction_to_data_warehouses\lessons\c9_m1_popular_data_warehouse_systems.md]

You discovered that scalable data lakes enable organizations to provide fast, flexible data access, and serve as a self-serve staging area for machine learning development and advanced analytics.

[ENRICHED: clarification — Data lakes serve two critical functions: (1) Self-serve staging area — raw data lands in the lake first, then data scientists and analysts can access it directly without waiting for IT to build ETL pipelines; this dramatically reduces time-to-insight for exploratory analysis; (2) ML development platform — machine learning requires access to raw, unprocessed data for feature engineering and model training, which data warehouses (with their schema-on-write constraints) cannot efficiently provide. The lake's schema-on-read approach lets ML engineers work with data in its native format, applying transformations as needed for each specific model. Source: c9_m1_data_lakes_overview.md] [Source: C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\updates\providers\ibm\data_warehouse_fundamentals\modules\module_1_introduction_to_data_warehouses\lessons\c9_m1_data_lakes_overview.md]

and that data marts provide specific, timely, and rapid support for making tactical decisions.

[ENRICHED: clarification — Tactical decisions are short-term, department-level decisions (e.g., which products to promote this quarter, which customers to target for a campaign). Data marts enable this by containing only the relevant data for a specific business function, eliminating the need to search through the entire enterprise data warehouse. This narrow scope delivers sub-second query responses compared to minutes for complex warehouse queries. Source: c9_m1_data_marts_overview.md] [Source: C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\updates\providers\ibm\data_warehouse_fundamentals\modules\module_1_introduction_to_data_warehouses\lessons\c9_m1_data_marts_overview.md]

You discovered that when selecting a data warehouse system, you need to consider the total cost of ownership, including infrastructure, compute and storage, data migration, and administration and data maintenance costs.

[ENRICHED: clarification — Total Cost of Ownership (TCO) for data warehouse systems includes five categories: (1) Infrastructure — hardware (servers, storage, networking) or cloud subscription fees; (2) Compute and storage — ongoing costs for processing power and data storage, which scale with data volume and query complexity; (3) Data migration — one-time costs for moving data from legacy systems to the new warehouse, often the most underestimated category; (4) Administration — salaries for database administrators, data engineers, and support staff; (5) Data maintenance — ongoing costs for data quality, backups, security patches, and compliance monitoring. The selection criteria framework from this module helps organizations evaluate vendors across features, compatibility, ease of use, support, and cost. Source: c9_m1_selecting_a_data_warehouse_system.md] [Source: C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\updates\providers\ibm\data_warehouse_fundamentals\modules\module_1_introduction_to_data_warehouses\lessons\c9_m1_selecting_a_data_warehouse_system.md]

---

## Module 1 Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Data Warehouses | Centralized repositories for integrated, historical, cleansed data; support OLAP, data mining, AI/ML |
| Deployment Models | On-premises, appliances (pre-integrated HW+SW), cloud (managed services) |
| Data Marts | Department-specific subsets of warehouses; optimized for tactical decisions; star/snowflake schemas |
| Data Lakes | Raw data repositories; schema-on-read; support ML and advanced analytics |
| Data Lakehouses | Combine lake flexibility with warehouse performance; ACID transactions on lake storage |
| Selection Criteria | TCO analysis: infrastructure, compute/storage, migration, administration, maintenance |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Deployment models | Clarification | Expanded three deployment models (on-premises, appliances, cloud) with 2026 context | HIGH | c9_m1_popular_data_warehouse_systems.md |
| 2 | Data lakes | Clarification | Explained self-serve staging and ML development platform functions | HIGH | c9_m1_data_lakes_overview.md |
| 3 | Data marts | Clarified tactical decisions with performance comparison | HIGH | c9_m1_data_marts_overview.md |
| 4 | TCO | Clarification | Broke down 5 TCO categories with explanations for each | HIGH | c9_m1_selecting_a_data_warehouse_system.md |

<!-- EXTRACTION_CHECKLIST: 4 sentences extracted, 4 sentences in output + 4 enrichments added via clarification questions -->
