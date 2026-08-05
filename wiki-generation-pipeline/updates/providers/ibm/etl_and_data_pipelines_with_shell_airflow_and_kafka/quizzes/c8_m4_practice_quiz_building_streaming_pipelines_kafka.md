> **Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
> **Module 4:** Apache Kafka Streaming Data

# Practice Quiz: Building Streaming Pipelines using Kafka

## Quiz Overview

| Detail | Value |
|--------|-------|
| **Type** | Practice Quiz |
| **Module** | Module 4 — Apache Kafka Streaming Data |
| **Estimated time** | 10 minutes |
| **Attempts** | Unlimited |

---

## Question 1

**Event streams represent entity status updates over time. Events have different formats, which of the most common formats can be either a primitive or complex data type? (multiple answers)**

| Option | Correct? |
|--------|----------|
| **Key-value with a timestamp** | ✗ |
| **Complex format** | ✗ — This format is ONLY complex (tuple, JSON, XML), not both primitive and complex |
| **Key-value format** | **✓ CORRECT** — This format can be a primitive data type OR complex data type |
| **Primitive format** | ✗ |

**Answer:** Key-value format

[ENRICHED: analysis — The question asks which format can be EITHER primitive OR complex. Key-value format is the only one that fits: the value can be a primitive (string, int, long) OR complex (JSON object, Avro record, Protobuf). "Complex format" is wrong because it's ONLY complex — it can't be primitive. "Primitive format" is wrong because it's ONLY primitive — it can't be complex. "Key-value with a timestamp" is wrong because the timestamp is always primitive (long/epoch), so this format isn't truly "either primitive or complex."] [Source: Coursera feedback]

---

## Question 2

**How does Kafka increase fault-tolerance and throughput?**

| Option | Correct? |
|--------|----------|
| **Maps** | ✗ |
| **Topic partitions and replications** | **✓ CORRECT** |
| **Keys** | ✗ |
| **Indexes** | ✗ |

**Answer:** Topic partitions and replications

[ENRICHED: analysis — Partitions increase throughput by splitting a topic into parallel queues that can be processed simultaneously by multiple brokers and consumers. Replications increase fault-tolerance by maintaining copies of data across brokers — if one broker fails, another replica takes over. "Maps" and "Keys" are data structures, not throughput/fault-tolerance mechanisms. "Indexes" are lookup structures, not Kafka's replication strategy.] [Source: https://docs.confluent.io/kafka/design/replication.html]

---

## Question 3

**The ad hoc processors that perform stream processing can become complicated. The Kafka Streams API helps solve this complication. How does the Streams API help stream processing? (multiple answers)**

| Option | Correct? |
|--------|----------|
| **Provides client library** | ✗ — "A simple client library is what Streams API uses" — this describes what it IS, not how it HELPS |
| **Processes one record at a time** | **✓ CORRECT** — It ensures each record is only processed once |
| **Scripts for CLI** | ✗ |
| **Processes and analyzes data** | **✓ CORRECT** — It processes and analyzes data stored in Kafka topics; both input and output are Kafka topics |

**Answer:** Processes one record at a time, Processes and analyzes data

[ENRICHED: analysis — The question asks HOW the Streams API HELPS, not what it IS. This is a common trick in multiple-choice questions.

**Simple Analogy — A Hammer:**

Imagine this question: "How does a hammer help you build a house?"

| Answer | Type | Why It's Wrong/Right |
|--------|------|---------------------|
| "It's a tool made of metal and wood" | WHAT it is | Describes the hammer itself, not how it helps |
| "It drives nails into wood" | HOW it helps | Describes what it DOES for you |

**Another Example — A Car:**

"How does a car help you get to work?"

| Answer | Type |
|--------|------|
| "It's a vehicle with 4 wheels" | WHAT it is ✗ |
| "It transports you quickly" | HOW it helps ✓ |

**Back to Kafka Streams:**

The question: "How does the Streams API HELP stream processing?"

| Answer | Type | Correct? |
|--------|------|----------|
| "Provides client library" | WHAT it is | ✗ — Tells me it's a library, not how it helps |
| "Processes one record at a time" | HOW it helps | ✓ — Solves the complication by processing individually |
| "Processes and analyzes data" | HOW it helps | ✓ — Transforms input → output |

**The two ways it HELPS are:**

1. **Processes one record at a time** — Instead of complex batch processing, each record is handled individually, ensuring no record is processed twice. This eliminates the complexity of tracking batch state.

2. **Processes and analyzes data** — Both input and output are Kafka topics. You read from a topic, process/analyze the data, and write back to another topic. This is simpler than ad hoc processors that might read from files, databases, or APIs.

**The key word in the question is "HELP" — not "IS".**] [Source: Coursera feedback]

---

## Question 4

**Which of the following describes event streaming?**

| Option | Correct? |
|--------|----------|
| **Continuous event transportation** | **✓ CORRECT** — This describes the continuous flow/movement of events |
| **Observable state updates over time** | ✗ — This describes an EVENT (a single state update), not EVENT STREAMING (the continuous flow) |
| **Large event volume** | ✗ |
| **External database** | ✗ |

**Answer:** Continuous event transportation

[ENRICHED: analysis — Coursera's feedback says "Observable state updates over time" is wrong because "this describes an event." The key distinction:

- **Event** = a single state update at a specific time (e.g., "truck moved to Main Street at 10:00 AM")
- **Event streaming** = the continuous flow/transportation of these events over time

"Continuous event transportation" describes the STREAMING aspect — events flowing continuously from producers to consumers through Kafka. It's about the movement/transportation, not the individual state updates.

Think of it like this:
- A single water droplet = an event
- A river flowing = event streaming (continuous transportation of water)

"Observable state updates over time" describes what EVENTS are, not what EVENT STREAMING is. Event streaming is the CONTINUOUS TRANSPORTATION of those events.] [Source: Coursera feedback]

---

## Question 5

**What was Apache Kafka originally used for?**

| Option | Correct? |
|--------|----------|
| **Payments and transactions** | ✗ |
| **Auditing** | ✗ |
| **Data storage** | ✗ |
| **Track user activities** | **✓ CORRECT** |

**Answer:** Track user activities

[ENRICHED: analysis — Kafka was originally developed at LinkedIn in 2011 for tracking user activity data — page views, clicks, searches, and other behavioral events. LinkedIn needed a scalable, real-time system to collect and process massive volumes of user activity logs for analytics and data pipelines. While Kafka can handle payments, auditing, and data storage, these were not its original use case.] [Source: https://kafka.apache.org/41/implementation/]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Question 1 | Correction | Fixed: Only "Key-value format" is correct (not "Complex format") — complex format is ONLY complex, not both primitive and complex | HIGH | Coursera feedback |
| 2 | Question 2 | Analysis | Explained partitions for throughput and replications for fault-tolerance | HIGH | https://docs.confluent.io/kafka/design/replication.html |
| 3 | Question 3 | Correction | Fixed: "Provides client library" is wrong — question asks HOW it HELPS, not what it IS | HIGH | Coursera feedback |
| 4 | Question 4 | Correction | Fixed: "Continuous event transportation" is correct — "Observable state updates" describes an event, not event streaming | HIGH | Coursera feedback |
| 5 | Question 5 | Analysis | Documented Kafka's origin at LinkedIn for user activity tracking | HIGH | https://kafka.apache.org/41/implementation/ |

<!-- EXTRACTION_CHECKLIST: 5 questions extracted, 5 questions in output -->
