**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 2:** Shell Scripting for ETL

# Graded Quiz: An Introduction to Data Pipelines

**Type:** Graded Quiz (3 attempts, every 8 hours)
**Duration:** ~30 minutes
**Due:** Jul 26, 11:59 PM EEST
**Status:** 2 of 3 attempts used

---

## Question 1

**Which of the following data pipelines corresponds with the fraud detection use case?**

| Option | Correct? |
|--------|----------|
| Lambda architectures | ✗ |
| Batch data pipeline | ✗ |
| **Streaming data pipeline** | **✓ CORRECT** |
| Micro-batch data pipeline | ✗ |

**Answer:** Streaming data pipeline

**Analysis:** The enriched lesson lists fraud detection as a streaming use case: "Use cases for streaming data pipelines are on the rise and include cases such as... fraud detection, user behavior analysis, and targeted advertising." [ENRICHED: added specificity — fraud detection requires millisecond-level latency because the transaction must be scored and potentially declined *before* it completes. A credit card transaction is scored in <100ms; if flagged, it's declined instantly. Batch processing (hourly or daily) would let fraud pass through undetected for hours.] Lambda architectures combine batch and streaming but are not *specific* to fraud detection. Batch pipelines process data periodically (too slow for real-time fraud). Micro-batch processes data every few seconds (close, but true fraud detection needs event-by-event streaming).

---

## Question 2

**Batch data pipelines usually run periodically on fixed schedules. Which of the following is another method to run these?**

| Option | Correct? |
|--------|----------|
| Flags | ✗ |
| Manually | ✗ |
| Error occurrence | ✗ |
| **Triggers** | **✓ CORRECT** |

**Answer:** Triggers

**Analysis:** The enriched lesson states: "Batch processes typically operate periodically on a fixed schedule, ranging from hours to weeks apart. They can also be initiated based on triggers, such as when the source data reaches a certain size." [ENRICHED: concrete example — a trigger-based batch pipeline might run when an S3 bucket accumulates 10 GB of new files, or when a message arrives in a queue, or when a sensor reports a threshold breach. This is more responsive than a fixed schedule: instead of waiting for the next hourly run, the pipeline fires immediately when data is ready.] "Flags" are boolean indicators, not execution methods. "Manually" means human-initiated, which is not a standard batch pipeline method. "Error occurrence" would trigger recovery, not normal batch execution.

---

## Question 3

**Pipelines that incorporate parallelism are referred to as being_____ ?**

| Option | Correct? |
|--------|----------|
| Aligned | ✗ |
| Static | ✗ |
| **Dynamic or non-linear** | **✓ CORRECT** |
| Linear | ✗ |

**Answer:** Dynamic or non-linear

**Analysis:** The enriched lesson states: "Pipelines that incorporate parallelism are referred to as being dynamic or nonlinear, as opposed to static, which applies to serial pipelines." [ENRICHED: clarified concept — "nonlinear" refers to the shape of data flow: data splits into multiple parallel paths (branches) and merges back, rather than following a single straight line. "Dynamic" means the structure can change at runtime (more or fewer parallel workers based on load). Static/linear pipelines have a fixed single path with no branching.] "Aligned" is not a pipeline classification term. "Static" describes serial (non-parallel) pipelines. "Linear" describes pipelines with a single straight path — the opposite of parallel/branched.

---

## Question 4

**Which streaming data pipeline tool allows you to build applications using the Streams Processing Language (SPL)?**

| Option | Correct? |
|--------|----------|
| Apache Samza | ✗ |
| **IBM Streams** | **✓ CORRECT** |
| SQLstream | ✗ |
| Apache Spark | ✗ |

**Answer:** IBM Streams

**Analysis:** The enriched lesson states: "IBM Streams is a streaming data pipeline technology, which enables you to build real time analytical applications using the Streams processing language or SPL, plus Java, Python, or C++." [ENRICHED: ecosystem — IBM Streams is designed for high-throughput, low-latency event processing (millions of events per second with sub-millisecond latency). SPL (Streams Processing Language) is IBM's domain-specific language for defining stream processing logic. Stream Flows provides a visual editor for non-programmers. Alternatives: Apache Kafka Streams, Apache Flink, Apache Storm, Azure Stream Analytics.] Apache Samza is a LinkedIn/Kafka stream processing framework (uses Java/Scala, not SPL). SQLstream uses SQL for stream processing. Apache Spark is a general-purpose distributed computing framework (uses Scala/Python/SQL, not SPL).

---

## Question 5

**Which of the following data pipeline use cases is the simplest?**

| Option | Correct? |
|--------|----------|
| Raw data preparation | ✗ |
| Transactional record movement | ✗ |
| **File backup** | **✓ CORRECT** |
| Send/receive messages | ✗ |

**Answer:** File backup

**Analysis:** The enriched lesson states: "The simplest pipeline has no transformations and is used as file backups, integrating disparate raw data sources into a data lake, moving transactional records to a data warehouse..." [ENRICHED: concrete example — a file backup pipeline is literally `cp -r /data/ /backup/` — copy files from one location to another with zero transformation. No extraction logic, no cleaning, no schema mapping, no loading into a database. Just copy. This is the simplest possible data pipeline: source → destination, no intermediate steps.] Raw data preparation involves extraction and cleaning (transformation). Transactional record movement requires ETL (extract from OLTP, transform for analytics, load into OLAP). Send/receive messages involves routing and formatting logic. File backup is the only use case with *no transformations*.

---

## Question 6

**Which of the following common features of modern ETL and ELT products is known as "no-code"?**

| Option | Correct? |
|--------|----------|
| Fully automated | ✗ |
| Security | ✗ |
| Data crawling | ✗ |
| **Drag-and-drop** | **✓ CORRECT** |

**Answer:** Drag-and-drop

**Analysis:** The enriched lesson states: "a drag-and-drop GUI for specifying rules and data pipeline flows, also known as No-Code ETL." [ENRICHED: ecosystem — "No-Code ETL" means business analysts who can't write SQL or Python can still build data pipelines using a visual workflow builder. You drag components (extract, transform, load operations) onto a canvas, connect them with arrows, and configure parameters through forms. Examples: Talend Open Studio, Alteryx, AWS Glue visual editor. The tradeoff: no-code tools are faster to learn but harder to version-control, test, and debug compared to code-based tools.] "Fully automated" refers to end-to-end pipeline creation, not the no-code paradigm. "Security" is a compliance feature (encryption, HIPAA/GDPR). "Data crawling" is schema discovery (Glue Crawlers). Only "drag-and-drop" is explicitly called "No-Code ETL" in the course.

---

## Question 7

**How does data flow through pipelines?**

| Option | Correct? |
|--------|----------|
| Processing threads | ✗ |
| **Data packets** | **✓ CORRECT** |
| Software processes | ✗ |
| Files | ✗ |

**Answer:** Data packets

**Analysis:** The enriched lesson states: "We can think of data flowing through the pipeline in the form of data packets. A term which we will use to broadly refer to to units of data. Packets can range in size from a single record or event to large collections of data." [ENRICHED: added specificity — "data packets" is an abstract and flexible term. In different contexts, a "packet" might be: a single row (one customer record), a single event (one website click), a batch of records (all yesterday's transactions), or a large file (a 10 GB CSV). The pipeline doesn't care about packet size — it processes whatever it receives. This abstraction allows the same pipeline architecture to handle both real-time streaming (small packets, one event at a time) and batch processing (large packets, millions of records at once).] "Processing threads" are units of execution, not units of data flow. "Software processes" run the pipeline but are not what flows through it. "Files" can be a format for data packets but are not the general term for data flow.

---

## Question 8

**Which of the following pipeline monitoring considerations affects the amount of data that passes through the pipeline over time?**

| Option | Correct? |
|--------|----------|
| **Throughput** | **✓ CORRECT** |
| Logging and alerting system | ✗ |
| Utilization | ✗ |
| Latency | ✗ |

**Answer:** Throughput

**Analysis:** The enriched lesson states: "Throughput demand, the volume of data passing through the pipeline over time." [ENRICHED: clarified concept — throughput measures the *rate* of data flow: how many records, events, or bytes pass through the pipeline per unit of time. Example: "Processing 2.5 TB/day, capacity is 3 TB/day." Throughput is distinct from latency (time for ONE packet to traverse the pipeline) and utilization (how fully resources are used). A pipeline can have high throughput (many packets/second) but high latency (each packet takes a long time to traverse all stages).] "Logging and alerting system" records events and alerts on failures — it tracks pipeline health, not data volume. "Utilization" measures how fully pipeline resources (CPU, memory) are being used, which affects cost but not data volume. "Latency" measures time for a single packet to traverse the pipeline, not the volume of data over time.

---

## Question 9

**Latency is the total time it takes for a single packet of data to pass through the pipeline. Which of the following limits latency?**

| Option | Correct? |
|--------|----------|
| **Slowest process** | **✓ CORRECT** |
| Bad data | ✗ |
| Data leak | ✗ |
| Small data packets | ✗ |

**Answer:** Slowest process

**Analysis:** The enriched lesson states: "overall latency is limited by the slowest process in the pipeline." [ENRICHED: concrete example — a 3-stage pipeline: Extract (2s) + Transform (8s) + Load (3s) = 13s latency. The Transform stage is the bottleneck. Even if you speed up Extract to 0.5s, latency drops to only 0.5 + 8 + 3 = 11.5s. To meaningfully reduce latency, you must speed up the SLOWEST stage. This is Amdahl's Law in computing: overall speedup is limited by the slowest component.] "Bad data" causes errors and reprocessing but does not inherently limit latency. "Data leak" is a security concern, not a performance constraint. "Small data packets" would actually *reduce* latency (less data to process per packet), not limit it.

---

## Question 10

**Micro-batch data pipelines decrease the batch size. Which of the following do micro-batch pipelines increase?**

| Option | Correct? |
|--------|----------|
| Storage | ✗ |
| Latency | ✗ |
| **Batch process refresh rate** | **✓ CORRECT** |
| Simple transformation | ✗ |

**Answer:** Batch process refresh rate

**Analysis:** The enriched lesson states: "By decreasing the batch size and increasing the refresh rate of individual batch processes, you can achieve near real-time processing." [ENRICHED: concrete example — traditional batch processes 10M records every 60 minutes (latency: up to 60 min). Micro-batch processes 10K records every 5 seconds (latency: ~5 seconds). The batch size decreased (10M → 10K), but the refresh rate increased (every 60 min → every 5 sec). This trades throughput per batch for lower latency.] "Storage" is not affected by micro-batching. "Latency" *decreases* (improves) with micro-batching, not increases. "Simple transformation" is not a metric that micro-batching affects — transformations can be simple or complex regardless of batch size.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Question 1 | Added specificity | Fraud detection requires <100ms scoring — too fast for batch or micro-batch | HIGH |
| 2 | Question 2 | Concrete example | Trigger-based pipeline fires when S3 accumulates 10 GB, or queue gets a message | HIGH |
| 3 | Question 3 | Clarified concept | "Nonlinear" = branching data flow shape, "Dynamic" = structure changes at runtime | HIGH |
| 4 | Question 4 | Ecosystem | IBM Streams: millions events/sec, sub-millisecond latency, SPL + Java/Python/C++ | HIGH |
| 5 | Question 5 | Concrete example | File backup = `cp -r /data/ /backup/` — zero transformation, simplest possible pipeline | HIGH |
| 6 | Question 6 | Ecosystem | No-Code ETL: drag-and-drop for analysts vs code-based for engineers, tradeoffs | HIGH |
| 7 | Question 7 | Added specificity | Data packets flexible: single row, single event, batch, or large file | HIGH |
| 8 | Question 8 | Clarified concept | Throughput = rate (records/sec), distinct from latency (time/packet) and utilization (%) | HIGH |
| 9 | Question 9 | Concrete example | 3-stage pipeline: Transform bottleneck (8s) limits total latency to 13s, Amdahl's Law | HIGH |
| 10 | Question 10 | Concrete example | Micro-batch: 10M→10K records, 60min→5sec, refresh rate increase, latency decrease | HIGH |

<!-- EXTRACTION_CHECKLIST: 10 questions extracted, 10 questions in output -->
