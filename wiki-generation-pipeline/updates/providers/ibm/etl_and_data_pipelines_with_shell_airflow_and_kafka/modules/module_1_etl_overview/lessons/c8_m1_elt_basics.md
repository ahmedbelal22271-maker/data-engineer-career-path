**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 1:** Extract, Transform, Load (ETL) Overview

# ELT Basics

## Learning Objectives

After watching this video, you will be able to describe what an ELT process is, list use cases for ELT processes, and describe why ELT is an emergent trend.

## What is an ELT Process?

ELT stands for extract, load, and transform. ELT is an acronym for a specific automated data pipeline engineering methodology. ELT is similar to ETL in that similar stages are involved, but the order in which they are performed is different. For ELT processes, data is acquired and directly loaded as is into its destination environment. From its new home, usually a sophisticated analytics platform such as a data lake, it can be transformed on demand and however users wish.

[ENRICHED: defined "data lake" — a centralized storage repository that holds raw data in its native format (structured, semi-structured, and unstructured) at any scale. Unlike a data warehouse which stores pre-processed, schema-on-write data, a data lake uses schema-on-read: raw data is stored as-is, and the schema is applied only when the data is read for analysis. Common data lake implementations include Amazon S3, Azure Data Lake Storage (ADLS), and Google Cloud Storage (GCS).] [ENRICHED: ecosystem — ELT has become the dominant pattern in modern cloud-native architectures because cloud data warehouses (Snowflake, BigQuery, Redshift) and data lakehouses (Databricks Delta Lake, Apache Iceberg) have sufficient compute power to run transformations at query time, eliminating the need for a separate transformation step before loading.]

Like ETL, the first stage in the ELT process is extraction. The extraction process obtains the data from all sources and reads the data often in an asynchronous fashion into an application. [ENRICHED: defined "asynchronous" — a processing mode where the extraction step initiates a data read and continues other work without waiting for the read to complete. The data arrives later, and the application handles it when ready. In contrast, synchronous extraction blocks until the data is fully received. Asynchronous is preferred for large datasets and high-throughput pipelines because it avoids idle waiting.] The loading process takes the raw data as is and loads it into its new environment where modern analytics tools can then be used directly. The transformation process for ELT is much more dynamic than it is for conventional ETL. Modern analytics tools in the destination environment enable interactive, on-demand exploration and visualization of your data, including advanced analytics, such as modeling and prediction.

[ENRICHED: added specificity — "much more dynamic" means transformations are not defined once in a pipeline and executed identically every run. Instead, different users can apply different transformations to the same raw data at different times, depending on their current question. A data scientist might run a feature engineering transformation for a model, while a business analyst runs a different aggregation for a dashboard — both querying the same raw data in the lake, with no predefined pipeline step for either.]

## Use Cases for ELT

Use cases for ELT processes typically fall within the high performance computing and big data realms. Cases include dealing with the massive swings and scale that come with implementing big data products, calculating real-time analytics on streaming big data, and bringing together data sources that are highly distributed around the globe.

In terms of speed, moving data is usually more of a bottleneck than processing it. The less you move it, the better. Therefore, ELT may be your best bet when you want flexibility in building a suite of data products from the same sources.

[ENRICHED: added specificity — "moving data is more of a bottleneck than processing it" is easiest to understand with a concrete scenario. Imagine a retail company with data in three locations:]

```
SOURCE SYSTEMS (where data lives):
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Online Store │  │ Physical    │  │ Marketing   │
│ (New York)   │  │ Stores (LA) │  │ (London)    │
│ 500 GB       │  │ 200 GB      │  │ 50 GB       │
└──────┬───────┘  └──────┬──────┘  └──────┬──────┘
       │                 │                 │
       │    NETWORK SPEED: 100 Mbps–1 Gbps │
       │    (limited by geography)         │
       ▼                 ▼                 ▼
┌─────────────────────────────────────────────────┐
│        CENTRAL DATA WAREHOUSE (Virginia)        │
│                                                  │
│  Time to RECEIVE all 750 GB over network:        │
│  At 1 Gbps = ~100 minutes                        │
│  At 100 Mbps = ~16 hours                         │
│                                                  │
│  Time to PROCESS that same 750 GB locally:        │
│  Filtering, joining, aggregating: ~5 minutes      │
│  (NVMe SSD reads at 3-5 GB/s)                    │
└─────────────────────────────────────────────────┘
```

**The numbers tell the story:**

| Action | Speed | Time for 750 GB |
|---|---|---|
| **Move** data over network (1 Gbps) | 125 MB/s | ~100 minutes |
| **Process** data locally (NVMe SSD) | 3,500 MB/s | ~3.5 minutes |

Processing is **30× faster** than moving. The network is the bottleneck, not the CPU.

**What ETL does (transform before loading):**

```
New York ──move──▶ Transformation Server ──move──▶ Warehouse
  500 GB          (in Virginia)                    (in Virginia)
  100 min         Clean, filter, join              Load result
                  Format for warehouse
                  Takes: 5 min
                  
                  BUT: if marketing in London
                  needs a different view of the
                  same data, you must:
                  
                  Warehouse ──move──▶ Transform ──move──▶ London
                  100 min             5 min
                  
                  TOTAL: ~210 minutes
```

**The problem:** Every new team that needs a different view of the data triggers another move → transform → move cycle. The data gets copied and re-processed repeatedly.

**What ELT does (load first, transform later):**

```
New York ──move once──▶ Data Lake (Virginia)
  500 GB                Raw data sits here, untouched
  100 min               
                        
                        Anyone can query it directly:
                        
Sales team:  "Show me revenue by region"
             → runs SQL on raw data → answer in 30 seconds
             (no data movement needed)

Marketing:   "Show me campaign performance"  
             → runs different SQL on same raw data → answer in 30 seconds
             (no data movement needed)

Data science: "Build a churn prediction model"
              → reads same raw data in Python → model in 2 hours
              (no data movement needed)

TOTAL: 100 minutes (one move, unlimited queries)
```

ELT cuts total time nearly in half by eliminating redundant data movement. The same principle applies at smaller scales: every time you copy data from one system to another for a transformation step, you're paying a network tax that could be avoided by moving the transformation to where the data already sits.]

## Why is ELT Emerging?

Firstly, cloud computing solutions are evolving at tremendous rates due to the demands of big data. They can easily handle huge amounts of asynchronous data, which can be highly distributed around the world. Cloud computing resources are practically unlimited and they can scale on demand. Unlike traditional on-premises hardware, you only pay for the computing resources you use. You do not have to worry about under utilizing resources, that is, overspending on equipment.

[ENRICHED: added specificity — "scale on demand" refers to elastic scaling: a cloud data warehouse like Snowflake can automatically add or remove compute nodes in response to query load, scaling from zero (when idle, costing nothing) to hundreds of nodes (during a heavy analytics workload) in minutes. This eliminates the traditional capacity planning problem where organizations had to buy hardware for peak load and waste money during off-peak hours.]

With ELT, you can have a clean separation between moving data and processing data. Of course, cloud computing is equally prepared to handle the most challenging cases for either of these two tasks. There may be many reasons to transform your data and just as many ways to do it. Thus, ELT is a flexible option that enables a variety of applications from the same source of data. Because you are working with a replica of the source data, there is no information loss. Many kinds of transformations can lead to information loss, and if these happen somewhere upstream in the pipeline, it may be a long time before you can have a change request met. Worse yet, the information may be forever lost if the raw data is not stored.

[ENRICHED: concrete example — a pipeline applies an aggressive deduplication transformation during the ETL step, removing records where `customer_id` + `timestamp` are identical. Months later, the analytics team discovers that some "duplicates" were actually legitimate rapid-fire transactions (e.g., a customer clicking "buy" twice within 1 second on a mobile app). Because the raw data was overwritten during ETL loading, these records are permanently lost. In an ELT approach, the raw data would still exist in the data lake, and the analytics team could re-run the deduplication with corrected logic without data loss.]

## Summary

In this video, you learned that:
- ELT processes are used for cases where flexibility, speed, and scalability are important.
- Cloud-based analytics platforms are ideally suited for handling big data and ELT processes in a cost-efficient manner, and ELT is an emerging trend mainly because cloud platform technologies are enabling it.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | What is ELT section | Definition | Defined "data lake" as schema-on-read raw storage (S3, ADLS, GCS) vs schema-on-write warehouse | HIGH |
| 2 | What is ELT section | Ecosystem | Positioned ELT as dominant in cloud-native (Snowflake, BigQuery, Delta Lake) | HIGH |
| 3 | Extraction paragraph | Definition | Defined "asynchronous" processing mode vs synchronous | HIGH |
| 4 | Transformation paragraph | Added specificity | Explained "much more dynamic" as user-driven, question-time transformations | HIGH |
| 5 | Use cases paragraph | Added specificity | Explained data movement bottleneck: local NVMe 1-10 GB/s vs network 100 Mbps-1 Gbps | HIGH |
| 6 | Why ELT emerging paragraph | Added specificity | Explained elastic scaling with Snowflake zero-to-hundreds of nodes example | HIGH |
| 7 | Information loss paragraph | Concrete example | Added deduplication data loss scenario: rapid-fire transactions permanently lost in ETL | HIGH |

<!-- EXTRACTION_CHECKLIST: 20 sentences extracted, 20 sentences in output -->
