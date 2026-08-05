**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 2:** Shell Scripting for ETL

# Practice Quiz: An Introduction to Data Pipelines

**Type:** Practice Quiz (unlimited attempts, does not count toward grade)
**Duration:** ~10 minutes
**Due:** Jul 25, 11:59 PM EEST

---

## Question 1

**What is the main purpose of a data pipeline?**

| Option | Correct? |
|--------|----------|
| Data container | ✗ |
| Storage | ✗ |
| **Move data from one place or form to another** | **✓ CORRECT** |
| 1 point | |

**Answer:** Move data from one place or form to another

**Analysis:** The enriched lesson states: "The purpose of a data pipeline is to move data from one place or form to another. A data pipeline is a system which extracts data and passes it along to optional transformation stages for final loading." [ENRICHED: added specificity — the phrase "optional transformation stages" is important. Not all data pipelines transform data. A simple backup pipeline might just copy data from System A to System B with no transformation at all. The core purpose is *movement*, transformation is secondary.] A data container is a storage mechanism, not a process. Storage is a destination, not a purpose. The pipeline's job is the *movement* and *flow* of data through stages.

---

## Question 2

**There are always stages that are bottlenecks in the data flow of pipelines. Which of the following is a simple way to load balance pipelines?**

| Option | Correct? |
|--------|----------|
| Buffers | ✗ |
| **Parallelize** | **✓ CORRECT** |
| Queues | ✗ |
| Serialize | ✗ |

**Answer:** Parallelize

**Analysis:** The enriched lesson explains: "A simple way to parallelize a process is to replicate it on multiple CPUs cores or threads and distribute data packets as they arrive in an alternating fashion amongst the replicated channels." [ENRICHED: concrete example — if the Transform stage takes 8 seconds and is the bottleneck, splitting it across 2 parallel workers reduces it to 4 seconds, giving a 31% latency reduction and 50% throughput increase.] Buffers smooth out flow between stages of different speeds but do not address the bottleneck itself. Queues hold data waiting to be processed but do not speed up processing. Serialize means processing one at a time, which is the opposite of what you want. Parallelization directly speeds up the bottleneck stage by distributing work across multiple workers.

---

## Question 3

**Which of the following data pipeline tools is specific to ELT?**

| Option | Correct? |
|--------|----------|
| **Panoply** | **✓ CORRECT** |
| Alteryx | ✗ |
| AWS Glue | ✗ |
| Talend Open Studio | ✗ |

**Answer:** Panoply

**Analysis:** The enriched lesson states: "Panoply is another enterprise solution, but its focus is on ELT rather than ETL. It handles data connection and integration without code and comes with SQL functionality so you can generate views of your data." [ENRICHED: ecosystem — Panoply is an ELT tool: it loads raw data into a cloud data warehouse (Redshift or BigQuery) and lets you transform it using SQL views. This contrasts with ETL tools like Talend or DataStage that transform data before loading.] The other three are all ETL tools: **Alteryx** is a commercial self-service analytics platform with drag-and-drop ETL; **AWS Glue** is a fully managed ETL service that crawls data sources and runs ETL jobs on managed Spark clusters; **Talend Open Studio** is an open-source ETL development platform with a drag-and-drop GUI that auto-generates Java code.

---

## Question 4

**Which of the following is the main reason to use Lambda architecture instead of Micro-batch, Streaming, or Batch data pipelines?**

| Option | Correct? |
|--------|----------|
| **Access to earlier data and speed is important** | **✓ CORRECT** |
| Records are processed immediately | ✗ |
| Help with load balancing | ✗ |
| Accuracy is critical | ✗ |

**Answer:** Access to earlier data and speed is important

**Analysis:** The enriched lesson explains: "Lambda can be used in cases where access to earlier data is required, but speed is also important. A downside to this approach is the complexity involved in the design. You usually choose a Lambda architecture when you are aiming for accuracy and speed." [ENRICHED: added specificity — Lambda architecture combines batch and streaming: historical data is delivered in batches to the batch layer, real-time data is streamed to a speed layer, and both are integrated in the serving layer. The batch layer provides accuracy (comprehensive processing of historical data), while the speed layer provides low-latency results for recent data.] "Records are processed immediately" describes streaming only. "Help with load balancing" is a parallelization concern, not an architectural reason. "Accuracy is critical" describes batch processing. Lambda's unique value is combining batch (accuracy + historical data) with streaming (speed + real-time), giving both access to earlier data AND speed.

---

## Question 5

**Which of the following data pipeline processes keep the pipeline running smoothly?**

| Option | Correct? |
|--------|----------|
| **Maintenance and Optimization** | **✓ CORRECT** |
| Monitoring | ✗ |
| Scheduling and Triggering | ✗ |
| Ingestion | ✗ |

**Answer:** Maintenance and Optimization

**Analysis:** The enriched lesson lists the key data pipeline processes: "extraction of data from one or more data sources, ingestion of the extracted data into the pipeline, optional data transformation stages within the pipeline and final loading of the data into a destination facility, a mechanism for scheduling or triggering jobs to run, monitoring the entire workflow, and maintenance and optimization as required to keep the pipeline up and running smoothly." The key phrase is "to keep the pipeline up and running smoothly" — this directly maps to **Maintenance and Optimization**. Monitoring tracks the pipeline's health but does not fix issues. Scheduling and Triggering define when jobs run but do not address operational health. Ingestion is a data movement stage, not an operational process. Maintenance and optimization include fixing issues, tuning performance, and upgrading resources — the active work of keeping the pipeline healthy.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Question 1 | Added specificity | Clarified that "optional transformation stages" means not all pipelines transform — core purpose is movement | HIGH |
| 2 | Question 2 | Concrete example | Added before/after parallelization scenario: Transform bottleneck 8s→4s, 31% latency reduction, 50% throughput increase | HIGH |
| 3 | Question 3 | Ecosystem | Distinguished Panoply (ELT: load first, transform with SQL views) from Alteryx/Glue/Talend (ETL: transform before loading) | HIGH |
| 4 | Question 4 | Added specificity | Explained Lambda's dual-layer architecture: batch layer (accuracy + historical) + speed layer (low-latency + real-time) | HIGH |
| 5 | Question 5 | Quote mapping | Directly mapped "keep the pipeline up and running smoothly" to Maintenance and Optimization from the source transcript | HIGH |

<!-- EXTRACTION_CHECKLIST: 5 questions extracted, 5 questions in output -->
