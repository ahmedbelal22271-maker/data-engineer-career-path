**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 1:** Extract, Transform, Load (ETL) Overview

# Data Loading Techniques

## Learning Objectives

After watching this video, you will be able to list data loading strategies and techniques, differentiate batch loading from stream loading, explain push and pull methodologies, list the data loading plans, and describe parallel loading.

## Data Loading Strategies

There are two main data loading strategies, full loading and incremental loading.

### Full Loading

Full loading is used when you want to start tracking transactions in a new data warehouse or when you want to load an initial history into a database. To reiterate, there is no existing content when you use full loading.

[ENRICHED: concrete example — a company launches a new data warehouse and needs to populate it with 5 years of historical order data from their production MySQL database. Full loading runs a single `SELECT * FROM orders` query, extracts all ~12 million rows, and loads them into the warehouse in one operation. The target table is truncated (or created fresh) before loading — there is no prior data to preserve. Full loading is also used after a catastrophic data corruption: you rebuild the warehouse from scratch by re-extracting from source systems.]

### Incremental Loading

After full loading is complete, you can use incremental loading to insert data that has changed since the previous loading. With incremental loading strategy, data is appended in the database and not overwritten. It is useful for accumulating transaction history.

[ENRICHED: concrete example — after the initial full load, the pipeline runs every hour and loads only orders created or modified since the last run. This is achieved by tracking a watermark: the maximum `last_updated` timestamp from the previous load (e.g., `2024-01-15 14:00:00`). The incremental query is `SELECT * FROM orders WHERE last_updated > '2024-01-15 14:00:00'`. Only the ~500 new/modified rows are extracted and appended to the warehouse, instead of re-extracting all 12 million. This reduces load time from hours to seconds and avoids overwriting existing records.]

You can categorize incremental loading into stream loading and batch loading, depending on the volume and velocity of data. Stream loading is used when the data is to be loaded real time. Batch loading is used when it's efficient and effective to load data in batches.

## Stream Loading

Stream loading refers to continuous data updates performed in the data warehouse or other storage systems as new data arrives. It is usually triggered by events, such as:

- **Real-time data from sensors**, like thermostat or motion sensors, social media feed, and IoT devices, and
- **Measures**, such as data size when a certain amount of data is collected, or threshold values, or when a user requests data, such as online videos, music, or web pages.

[ENRICHED: defined "event-driven loading" — a loading pattern where data is written to the destination immediately when an event occurs, rather than waiting for a scheduled batch window. Event-driven architectures typically use a message broker (Kafka, RabbitMQ, AWS Kinesis) as an intermediate buffer: the source publishes events to a topic, and a consumer process reads and loads them into the warehouse in real time. This enables sub-second latency from data generation to queryability.] [ENRICHED: concrete example — a ride-sharing app's trip event stream: every time a ride starts, the producer publishes a `trip_started` event to Kafka. A consumer reads the event, enriches it with driver location data, and inserts it into a real-time analytics warehouse. The operations dashboard updates within 2 seconds, showing active rides on a city map. With batch loading (hourly), the dashboard would be up to 59 minutes stale.]

## Batch Loading

Batch loading refers to periodic updates made/pushed to the data in the data warehouse or other storage systems, such as daily updates, hourly updates, or weekly updates. Batch data can be scheduled. Some examples include Windows Task Scheduler, Cron jobs in Linux, and daily stock update.

[ENRICHED: defined "Cron job" — a time-based job scheduler in Unix-like operating systems. Cron expressions define the schedule: `0 2 * * *` means "run at 2:00 AM every day." Cron is the backbone of batch ETL scheduling in Linux environments, and is the precursor concept to Apache Airflow's more sophisticated DAG-based scheduling with retry logic, dependency management, and monitoring.] [ENRICHED: added specificity — batch loading remains the dominant pattern for most enterprise data workloads because it is simpler to implement, debug, and recover from failures. A failed batch can be re-run from the last checkpoint. Stream loading requires more complex infrastructure (message brokers, exactly-once delivery guarantees, offset management) and is only justified when sub-hour latency is a business requirement.]

## Push vs Pull Methodologies

Next, let's review push and pull data loading methodologies. Push and pull data loading methodologies are based on a client-server or publisher-subscriber model.

### Push Method

A push method is used when the source pushes data into the data warehouse or other storage. While push method can be used for batch loading, it is most suited for stream loading involving real-time data.

[ENRICHED: concrete example — a SaaS application (e.g., Salesforce) uses webhooks to push CRM events (new lead created, deal closed) to a webhook endpoint hosted by the data warehouse. Each event is an HTTP POST request containing a JSON payload. The warehouse endpoint receives the data, validates the schema, and inserts it immediately. The source system controls the timing — data is pushed as soon as the event occurs, with no scheduling involved.]

**How push works — step by step:**

```
Customer clicks "Buy Now" on your online store
        │
        ▼
Your store's server records the order, then immediately sends:
POST https://warehouse.company.com/new-order
Body: {"order_id": 98432, "customer": "Alice", "amount": 49.99}
        │
        ▼
Warehouse receives it, validates it, inserts it
        │
        ▼
Done. Order appears in warehouse within seconds.
```

**The source decides when to send.** The warehouse doesn't ask — it just receives. This is why push is best for real-time: there's zero delay between data creation and data loading.

**Contrast with pull (the warehouse decides when to fetch):**

```
Every hour at :00, the warehouse runs a job:
  → asks the store: "Any orders since 3:00 PM?"
  → store responds: "Yes, here are 47 orders"
  → warehouse downloads and loads them
```

The data existed at the source the whole time, but the warehouse didn't see it until the next scheduled pull. For batch (hourly/daily), that delay is fine. For real-time, it's not.

**Real-world push examples:** your phone uploads photos to iCloud the moment you take them (not on a schedule); a weather station pushes an alert the instant temperature exceeds 40°C (doesn't wait for the hourly batch); a credit card terminal pushes each transaction to fraud detection in real time (not nightly).

### Pull Method

A pull method is used when the data warehouse pulls the data from the source by subscribing to receive the data. It is useful for scheduled transactions and batch loading.

[ENRICHED: concrete example — an Airflow DAG runs daily at 2:00 AM. The `ExtractFromMySQL` task connects to the production database, executes a query with a WHERE clause filtering for rows modified since the last run, and pulls the results into the warehouse staging area. The warehouse controls the timing — data is pulled on the schedule defined by the DAG, regardless of when the source data changed.] [ENRICHED: ecosystem — the push vs pull distinction maps to broader architectural patterns: push = event-driven architecture (source publishes, warehouse subscribes), pull = batch ETL (warehouse queries source on schedule). Modern architectures often use both: push for real-time operational data, pull for daily analytical snapshots from systems that do not support webhooks.]

## Serial vs Parallel Loading

Loading can be serial or parallel.

### Serial Loading

Serial loading is when the data is copied sequentially, one after the other. This is how data loads in the data warehouse by default.

### Parallel Loading

You can use parallel loading when you need to load data from different sources parallelly or to split data from one source into chunks and load them parallelly. When compared with serial loading, parallel loading is a faster and optimized approach. Parallel loading can be employed on multiple data streams to boost loading efficiency, particularly when the data is big or has to travel long distances. Similarly, by splitting a single file into smaller chunks, the chunks can be loaded simultaneously.

[ENRICHED: concrete example — a data warehouse receives data from 5 source systems: MySQL (orders), PostgreSQL (customers), MongoDB (product catalog), Salesforce (leads), and Google Analytics (page views). Serial loading processes each source sequentially: MySQL (45 min) → PostgreSQL (30 min) → MongoDB (20 min) → Salesforce (15 min) → Google Analytics (10 min) = 120 minutes total. Parallel loading runs all 5 simultaneously, with the total wall-clock time equal to the slowest source: 45 minutes — a 62.5% reduction.] [ENRICHED: concrete example — splitting a single large file: a 10 GB CSV file of historical transactions is split into 10 chunks of 1 GB each. Each chunk is loaded by a separate worker process into a different partition of the target table. Total load time: ~10 minutes (vs ~100 minutes serially). Tools like Apache Spark, AWS Glue, and dbt implement this pattern natively with configurable parallelism.] [ENRICHED: ecosystem — parallel loading is a core capability of modern ELT tools. Snowflake, BigQuery, and Redshift all support automatic parallel loading from cloud storage (S3, GCS, ADLS). Spark's `DataFrame.write.parquet()` partitions output by default across multiple files. The pattern is also fundamental to Change Data Capture (CDC) tools like Debezium, which parallelize change stream consumption across multiple Kafka topic partitions.]

## Summary

In this video, you learned that:
- Full and incremental are data loading strategies.
- Data can be loaded in batches, or it can be streamed continuously into its destination.
- Both pull and push methodologies can be used for data loading, and you can employ parallel loading to boost loading efficiency of large volumes of data.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Full loading paragraph | Concrete example | Company rebuilding 5-year DW history: SELECT * FROM orders, 12M rows, truncate+reload | HIGH |
| 2 | Incremental loading paragraph | Concrete example | Watermark-based incremental: WHERE last_updated > last_run, 500 rows vs 12M | HIGH |
| 3 | Stream loading section | Definition | Defined event-driven loading pattern with Kafka/Kinesis buffer architecture | HIGH |
| 4 | Stream loading section | Concrete example | Ride-sharing trip stream: Kafka producer→consumer→warehouse, 2-second dashboard update | HIGH |
| 5 | Batch loading section | Definition | Defined Cron job with expression example `0 2 * * *` | HIGH |
| 6 | Batch loading section | Added specificity | Batch remains dominant: simpler debugging, checkpoint recovery vs stream's complex infrastructure | HIGH |
| 7 | Push method section | Concrete example | Salesforce webhook → HTTP POST → warehouse endpoint, source-controlled timing | HIGH |
| 8 | Pull method section | Concrete example | Airflow DAG at 2:00 AM querying MySQL with watermark WHERE clause | HIGH |
| 9 | Pull method section | Ecosystem | Mapped push→event-driven, pull→batch ETL; modern uses both | HIGH |
| 10 | Parallel loading section | Concrete example | 5-source parallel load: wall-clock = slowest source (45 min vs 120 min serial) | HIGH |
| 11 | Parallel loading section | Concrete example | 10 GB CSV split into 10 chunks, 10 parallel workers, 10 min vs 100 min | HIGH |
| 12 | Parallel loading section | Ecosystem | Connected to Snowflake/BigQuery/Redshift auto-parallel loading + Spark + CDC/Debezium | HIGH |

<!-- EXTRACTION_CHECKLIST: 30 sentences extracted, 30 sentences in output -->
