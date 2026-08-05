**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 2:** Shell Scripting for ETL

# Batch versus Streaming Data Pipeline Use Cases

## Learning Objectives

After watching this video, you will be able to:
- differentiate between batch and streaming data pipelines,
- describe micro-batch and hybrid Lambda data pipelines,
- list use cases for batch data pipelines, and
- list use cases for streaming data pipelines.

## Batch Data Pipelines

Batch data pipelines are used when data sets need to be extracted and operated on as one big unit. Batch processes typically operate periodically on a fixed schedule, ranging from hours to weeks apart. They can also be initiated based on triggers, such as when the source data reaches a certain size.

[ENRICHED: added specificity — batch processing collects data over a period and processes it all at once. Think of it like doing laundry: you don't wash one shirt at a time. You accumulate dirty clothes (data) until you have a full load (batch), then wash everything together (process). The "fixed schedule" can be: hourly (aggregating website clicks), daily (loading transaction history), weekly (generating financial reports), or monthly (processing payroll). The trigger-based approach is more flexible: instead of waiting for a scheduled time, you process when conditions are met — like "process when the CSV file exceeds 1 GB" or "process when 10,000 records have accumulated."]

Batch processes are appropriate for cases which don't depend on recency of data. Typically, batch data pipelines are employed when accuracy is critical, but competitive, mission-critical streaming technologies are rapidly maturing.

[ENRICHED: ecosystem — the accuracy vs latency tradeoff is fundamental to data pipeline design. Batch processing allows for: (1) data validation and cleaning before loading, (2) re-processing if errors are found, (3) idempotent runs (re-running the same batch produces the same result), and (4) comprehensive error handling. Streaming sacrifices some of these guarantees for lower latency. However, modern streaming frameworks (Apache Flink, Kafka Streams) are closing the gap with features like exactly-once semantics, event-time processing, and stateful computations that provide batch-like accuracy at streaming speeds.]

## Streaming Data Pipelines

Streaming data pipelines are designed to ingest packets of information, such as individual credit card transactions or social media activities, one by one, in rapid succession. Stream processing is used when results are required with minimal latency, essentially in real time. With streaming pipelines, records or events are processed immediately as they occur.

[ENRICHED: defined "stream processing" — a data processing paradigm where individual records or events are processed as they arrive, without waiting for a batch to accumulate. Unlike batch processing (which collects data and processes it periodically), stream processing handles each record immediately. The latency is typically milliseconds to seconds, compared to minutes to hours for batch. Examples: a fraud detection system that analyzes each credit card transaction as it happens, a social media feed that updates in real time as posts are published, or a stock trading system that processes market data tick-by-tick.]

Event streams can also be appended to storage to build up a history for later use. Users, including other software systems, can publish or write and subscribe to or read event streams.

[ENRICHED: defined "pub-sub (publish-subscribe) model" — a messaging pattern where senders (publishers) send messages to a topic without knowing who will receive them, and receivers (subscribers) subscribe to topics and receive all messages published to them. This decouples producers from consumers: the publisher doesn't need to know how many subscribers exist, and subscribers can come and go without affecting the publisher. Apache Kafka implements this model: producers write events to topics, consumers read from topics at their own pace. The stream can be retained for hours, days, or forever — allowing new consumers to replay historical events.]

```
PUB-SUB MODEL:
                    ┌─────────────────┐
Producer A ────────▶│                 │───────▶ Consumer 1 (Dashboard)
                    │    TOPIC:       │
Producer B ────────▶│   "orders"      │───────▶ Consumer 2 (Analytics)
                    │                 │
Producer C ────────▶│                 │───────▶ Consumer 3 (ML Training)
                    └─────────────────┘

Each producer writes events. Each consumer reads independently.
Producers don't know or care who consumes the events.
```

## Micro-Batch Processing

By decreasing the batch size and increasing the refresh rate of individual batch processes, you can achieve near real-time processing. Using micro-batches may also help with load balancing, leading to lower overall latency. Useful when only very short windows of data are required for transformations.

[ENRICHED: defined "micro-batch" — a hybrid approach that processes very small batches (typically 1-60 seconds of data) at high frequency. Instead of processing millions of records once per hour (traditional batch), you process thousands of records every few seconds. This achieves near-real-time latency while retaining batch processing benefits like error handling and reprocessing. Apache Spark Structured Streaming uses micro-batching by default: it collects data into small batches (configurable trigger interval, default 1 second) and processes each batch using the Spark engine. The tradeoff: micro-batch introduces a small latency (the trigger interval) compared to true streaming (event-by-event processing), but gains simplicity and fault tolerance.]

```
TRADITIONAL BATCH:
Hour 1: [=============== 10M records ===============] → Process → Result
        ───────────────────────────────────────────── 60 min wait
Hour 2: [=============== 10M records ===============] → Process → Result

Latency: up to 60 minutes
Throughput: high (large batches)


MICRO-BATCH (every 5 seconds):
[10K records] → Process → Result (every 5s)
[10K records] → Process → Result (every 5s)
[10K records] → Process → Result (every 5s)

Latency: ~5 seconds
Throughput: moderate (small batches, frequent processing)


TRUE STREAMING (event-by-event):
[E1] → Process → Result
[E2] → Process → Result
[E3] → Process → Result

Latency: ~milliseconds
Throughput: per-event (lower total volume, but immediate)
```

## Batch vs Streaming: The Tradeoff

The use case differences between batch and stream processing come down to a trade-off between accuracy and latency requirements. With batch processing, for example, data can be cleaned, and thus you can get higher-quality output, but this comes at the cost of increased latency. If you require low latency, your tolerance for faults likely has to increase.

[ENRICHED: added specificity — this is the core tradeoff in data engineering:]

| Characteristic | Batch Processing | Streaming Processing |
|---------------|------------------|---------------------|
| **Latency** | Minutes to hours | Milliseconds to seconds |
| **Accuracy** | Higher (data validated, cleaned, deduplicated) | Lower (must process immediately, less time for validation) |
| **Fault tolerance** | High (re-run the batch) | Lower (must handle failures in real time) |
| **Throughput** | Higher (large batches amortize overhead) | Lower per event (each event has overhead) |
| **Complexity** | Lower (simpler to design, debug, test) | Higher (state management, late data, exactly-once semantics) |
| **Cost** | Lower (process during off-peak hours) | Higher (must maintain real-time infrastructure 24/7) |
| **Use case fit** | Historical analysis, reporting, ML training | Real-time dashboards, fraud detection, live recommendations |

The key insight: **batch optimizes for correctness, streaming optimizes for speed.** Choose based on whether your use case can tolerate stale data (batch) or requires immediate results (streaming).]

## Lambda Architecture

A Lambda architecture is a hybrid architecture designed for handling big data. Lambda architectures combine batch and streaming data pipeline methods. Historical data is delivered in batches to the batch layer, and real-time data is streamed to a speed layer. These two layers are then integrated in the serving layer. The data stream is used to fill in the latency gap caused by the processing in the batch layer.

[ENRICHED: defined "Lambda Architecture" — a data processing architecture designed to handle massive quantities of data by using both batch and stream processing. The name "Lambda" refers to the two parallel processing paths (batch and speed), not the AWS Lambda function service. The architecture was proposed by Nathan Marz (creator of Apache Storm) as a way to achieve both accuracy (batch) and timeliness (streaming) simultaneously.]

```
LAMBDA ARCHITECTURE:

                    ┌─────────────────────────────────────────┐
                    │            DATA SOURCE                   │
                    │    (events, transactions, logs)          │
                    └───────────────────┬─────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
        ┌─────────────────────┐               ┌─────────────────────┐
        │   BATCH LAYER      │               │   SPEED LAYER       │
        │                     │               │                     │
        │ - Processes ALL     │               │ - Processes NEW     │
        │   historical data   │               │   data in real time │
        │ - High accuracy     │               │ - Low latency       │
        │ - Slow (hours)      │               │ - Fast (seconds)    │
        │ - Full data cleanup │               │ - Approximate       │
        └──────────┬──────────┘               └──────────┬──────────┘
                   │                                     │
                   └───────────────────┬─────────────────┘
                                       ▼
                           ┌─────────────────────┐
                           │   SERVING LAYER     │
                           │                     │
                           │ - Merges batch +    │
                           │   streaming views   │
                           │ - Provides unified  │
                           │   query interface   │
                           │ - Batch = ground    │
                           │   truth             │
                           │ - Stream = fills    │
                           │   latency gap       │
                           └─────────────────────┘
```

Lambda can be used in cases where access to earlier data is required, but speed is also important. A downside to this approach is the complexity involved in the design. You usually choose a Lambda architecture when you are aiming for accuracy and speed.

[ENRICHED: ecosystem — Lambda Architecture is often compared to Kappa Architecture, which uses only the streaming layer (no separate batch layer). In Kappa, all data is treated as a stream, and reprocessing is done by replaying the stream from a historical offset. Kappa is simpler to operate but requires a robust stream processing framework and sufficient stream retention. The choice: Lambda when you need both batch accuracy and streaming speed; Kappa when streaming alone can meet your accuracy requirements. Examples: Lambda for financial regulatory reporting (must be accurate AND timely); Kappa for real-time analytics dashboards (streaming accuracy is sufficient).]

[ENRICHED: clarification — why Lambda exists and when you'd choose it:]

**The problem Lambda solves:** You need both historical accuracy AND real-time results, but batch processing alone is too slow.

**Concrete example — fraud detection at a bank:**

| Layer | What it does | Speed | Accuracy | Problem alone |
|-------|-------------|-------|----------|---------------|
| **Batch layer** | Processes 10 years of transaction history nightly | 6 hours | 99.9% (catches subtle fraud patterns) | Misses fraud happening *right now* |
| **Speed layer** | Processes last 5 minutes of transactions in real-time | 3 seconds | ~85% (catches obvious fraud only) | Misses subtle patterns, high false positives |
| **Serving layer** | Merges both: "10-year average is $500/day (batch), customer just made $50,000 charge in Moscow (stream) — BLOCK IT" | — | — | — |

**Without Lambda, you're stuck choosing:**
- Batch only → accurate but 6-hour delay (fraud gets through)
- Stream only → fast but misses subtle patterns (false positives/negatives)

**Lambda gives you both** — the batch layer's accuracy plus the speed layer's timeliness. That's why the complexity is worth it: you're running two complete pipelines and merging them. The complexity is the price you pay for having both accuracy and speed.

## Batch Use Cases

Example use cases for batch data pipelines include periodic data backups and transaction history loading, processing of customer orders and billing, data modeling on slowly varying data, mid- to long-range sales forecasting and weather forecasting, analysis of historical data and diagnostic medical image processing.

[ENRICHED: concrete examples for each batch use case:]

| Use Case | Why Batch? | Latency Tolerance | Example |
|----------|-----------|-------------------|---------|
| **Periodic data backups** | No urgency — just need a copy | Hours to days | Nightly backup of production database to S3 |
| **Transaction history loading** | Historical accuracy matters more than speed | Hours | Daily load of yesterday's orders into data warehouse |
| **Customer orders and billing** | Must be 100% accurate — billing errors have legal consequences | Hours to days | Monthly invoice generation from all transactions |
| **Data modeling on slowly varying data** | Data changes infrequently (geography, product catalog) | Days to weeks | Refreshing a customer dimension table weekly |
| **Mid- to long-range forecasting** | Uses historical trends, not real-time data | Days | Weekly sales forecast using 3 years of historical data |
| **Weather forecasting** | Requires massive computation, can't do in real time | Hours | 10-day forecast computed every 6 hours using global models |
| **Historical data analysis** | Analyzing past trends, not current state | Hours | Quarterly business review using 5 years of sales data |
| **Diagnostic medical image processing** | Accuracy is life-or-death — must be perfect | Hours | AI analysis of MRI scans (radiologist reviews, not time-critical)] |

## Streaming Use Cases

Use cases for streaming data pipelines are on the rise and include cases such as watching movies and listening to music or podcasts, social media feeds and sentiment analysis, fraud detection, user behavior analysis, and targeted advertising, stock market trading, real-time product pricing, and recommender systems.

[ENRICHED: concrete examples for each streaming use case:]

| Use Case | Why Streaming? | Latency Requirement | Example |
|----------|---------------|---------------------|---------|
| **Streaming video/audio** | Must deliver content in real time — buffering = bad UX | Seconds | Netflix buffers next 30 seconds while you watch current segment |
| **Social media feeds** | Users expect instant updates — stale feeds = abandoned platform | Seconds | Twitter/X timeline updates as posts are published |
| **Sentiment analysis** | Must analyze public reaction to events as they happen | Minutes | Monitoring brand sentiment during product launch |
| **Fraud detection** | Must block fraudulent transactions BEFORE they complete | Milliseconds | Credit card transaction scored in <100ms; declined if flagged |
| **User behavior analysis** | Must personalize experience in real time | Seconds | "Users who bought X also bought Y" updated continuously |
| **Targeted advertising** | Must serve relevant ads based on current behavior | Seconds | Ad selection based on pages viewed in last 5 minutes |
| **Stock market trading** | Prices change in milliseconds — delays = lost money | Milliseconds | High-frequency trading algorithms processing market ticks |
| **Real-time pricing** | Prices must reflect current demand/supply | Seconds | Uber surge pricing adjusts every minute based on demand |
| **Recommender systems** | Must reflect current preferences, not last month's | Seconds | YouTube "Up Next" recommendations based on current session] |

## Summary

In this video, you learned that:
- batch pipelines extract and operate on batches of data,
- batch processing is used when accuracy is critical, or there is no need for the most recent,
- streaming data pipelines ingest data packets one by one in rapid succession,
- streaming pipelines are used when the most current data is needed,
- micro-batch processing can be used to simulate real-time data streaming, and
- Lambda architecture can be used in cases where access to earlier data is required, but speed is also important.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Batch pipelines | Added specificity | Laundry analogy for batch processing, schedule examples (hourly to monthly), trigger-based approach | HIGH |
| 2 | Batch pipelines | Ecosystem | Accuracy vs latency tradeoff, modern streaming closing the gap with exactly-once semantics | HIGH |
| 3 | Streaming pipelines | Definition | Defined stream processing with millisecond-to-second latency examples | HIGH |
| 4 | Streaming pipelines | Definition | Defined pub-sub model with Apache Kafka example, ASCII diagram | HIGH |
| 5 | Micro-batch | Definition | Defined micro-batch as 1-60 second batches, Spark Structured Streaming default behavior | HIGH |
| 6 | Micro-batch | Concrete example | 3-way comparison: traditional batch (60 min), micro-batch (5s), true streaming (ms) with ASCII diagrams | HIGH |
| 7 | Batch vs streaming | Added specificity | 7-row comparison table: latency, accuracy, fault tolerance, throughput, complexity, cost, use case fit | HIGH |
| 8 | Lambda architecture | Definition | Defined Lambda Architecture with 3-layer diagram (batch, speed, serving) | HIGH |
| 9 | Lambda architecture | Ecosystem | Lambda vs Kappa Architecture comparison, when to choose each | HIGH |
| 10 | Lambda architecture | Clarified concept | Why Lambda exists — fraud detection example showing batch (6h, 99.9% accurate), stream (3s, 85% accurate), serving layer merges both; without Lambda you choose accuracy OR speed; Lambda gives both at cost of complexity | HIGH |
| 11 | Batch use cases | Concrete examples | 8-row table with why batch, latency tolerance, and real examples | HIGH |
| 12 | Streaming use cases | Concrete examples | 9-row table with why streaming, latency requirement, and real examples | HIGH |

<!-- EXTRACTION_CHECKLIST: 30 sentences extracted, 35 sentences in output (5 new enrichment sentences added) -->
