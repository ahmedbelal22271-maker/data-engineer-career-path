> **Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
> **Module 4:** Apache Kafka Streaming Data

# Graded Quiz: Building Streaming Pipelines using Kafka

## Quiz Overview

| Detail | Value |
|--------|-------|
| **Type** | Graded Quiz |
| **Module** | Module 4 — Apache Kafka Streaming Data |
| **Estimated time** | 30 minutes |
| **Attempts** | 3 (every 8 hours) |
| **Passing grade** | Required to pass course |
| **User's score** | 80% (8/10) |

---

## Question 1

**The Kafka server side is a cluster with many associated servers. What are the associated servers called?**

| Option | Correct? |
|--------|----------|
| Sub-servers | ✗ |
| **Brokers** | **✓ CORRECT** |
| Associates | ✗ |
| Controllers | ✗ |

**Answer:** Brokers

[ENRICHED: analysis — A Kafka cluster is made up of multiple servers called "brokers." Each broker is a single Kafka server process that stores data and handles client requests. Brokers handle read/write requests, manage partition replication, and coordinate with other brokers in the cluster. "Controllers" are a special role within KRaft mode (one broker acts as controller), but the general term for associated servers is "brokers."] [Source: https://kafka.apache.org/documentation/]

---

## Question 2

**Which of the following is Kafka Streams API based on?**

| Option | Correct? |
|--------|----------|
| Transformational graph | ✗ |
| Java | ✗ |
| Gantt chart | ✗ |
| **Computational graph** | **✓ CORRECT** |

**Answer:** Computational graph

[ENRICHED: analysis — From the Kafka documentation: "The computational logic of a Kafka Streams application is defined as a processor topology, which is a graph of stream processors (nodes) and streams (edges)." This is a computational graph — a directed acyclic graph (DAG) where nodes represent processing steps and edges represent data flow. "Transformational graph" is not a standard term. "Java" is the programming language, not the graph type. "Gantt chart" is a project management tool.] [Source: https://kafka.apache.org/43/streams/developer-guide/write-streams-app/]

> **⚠️ NOTE:** The Coursera quiz marked this answer as WRONG (0/1 point) despite all authoritative sources confirming "Computational graph" is correct. The feedback said "Incorrect, please review the Kafka Streaming Process video." This appears to be a quiz error. The networkingfunda.com answer key for this exact course also lists "Computational graph" as correct for the same question.

---

## Question 3

**Which of the following do stream processors do?**

| Option | Correct? |
|--------|----------|
| **Receives, transforms, and forwards** | **✓ CORRECT** |
| Extracts, transforms, and loads | ✗ |
| Extracts, loads, and transforms | ✗ |
| Processes and forwards | ✗ |

**Answer:** Receives, transforms, and forwards

[ENRICHED: analysis — From the Kafka documentation: "A stream processor is a node in the processor topology; it represents a processing step to transform data in streams by receiving one input record at a time from its upstream processors in the topology, applying its operation to it, and may subsequently produce one or more output records to its downstream processors." The three actions are: (1) receives input, (2) transforms/processes it, (3) forwards output downstream. "Extracts, transforms, and loads" is ETL (a different concept). "Processes and forwards" is incomplete — it misses the "receives" part.] [Source: https://kafka.apache.org/0102/streams/core-concepts/]

---

## Question 4

**Kafka Streams API is based on a computational graph called a stream processing topology. And in the topology, each node is a stream processor, while edges are the I/O streams. In this topology we find two special types of processors: What are they called?**

| Option | Correct? |
|--------|----------|
| **Source and sink processor** | **✓ CORRECT** |
| Aggregation and stream processor | ✗ |
| Stream and topic processor | ✗ |
| Mapping and transformation processor | ✗ |

**Answer:** Source and sink processor

[ENRICHED: analysis — From the Kafka documentation: "There are two special processors in the topology: Source Processor — A source processor is a special type of stream processor that does not have any upstream processors. It produces an input stream to its topology from one or multiple Kafka topics. Sink Processor — A sink processor is a special type of stream processor that does not have downstream processors. It sends any received records from its upstream processors to a specified Kafka topic."] [Source: https://kafka.apache.org/0102/streams/core-concepts/]

---

## Question 5

**Which of the following Kafka main features provides consumption without a deadline?**

| Option | Correct? |
|--------|----------|
| Distribution system | ✗ |
| **Permanent persistency** | **✓ CORRECT** |
| Open source | ✗ |
| Reliability | ✗ |

**Answer:** Permanent persistency

[ENRICHED: analysis — Kafka stores messages on disk with configurable retention (default: 7 days or until size limit). This "permanent persistency" means messages remain available for consumption even after time passes — there's no deadline by which you must consume them. You can read messages from hours, days, or weeks ago. "Distribution system" describes architecture, not consumption timing. "Open source" is a licensing model. "Reliability" describes fault tolerance, not consumption deadlines.] [Source: https://kafka.apache.org/documentation/]

---

## Question 6

**Once events are published and properly stored in topic partitions, you can create _________ to read them.**

| Option | Correct? |
|--------|----------|
| Producers | ✗ |
| Brokers | ✗ |
| **Consumers** | **✓ CORRECT** |
| Partitions | ✗ |

**Answer:** Consumers

[ENRICHED: analysis — Producers write/publish events to topics. Brokers store events. Partitions are subdivisions of topics. Consumers read/consume events from topics. The flow is: Producer → Topic (stored in Partitions on Brokers) → Consumer.] [Source: https://kafka.apache.org/documentation/]

---

## Question 7

**The core component of any ESP is the event broker. Which event broker sub-component performs encryption on data?**

| Option | Correct? |
|--------|----------|
| **Processor** | **✓ CORRECT** |
| Storage | ✗ |
| Ingester | ✗ |
| Consumption | ✗ |

**Answer:** Processor

[ENRICHED: analysis — The processor sub-component of an event broker handles data transformation, which includes encryption, decryption, compression, and format conversion. Storage handles persistence, ingester handles incoming data, and consumption handles reading data. The processor is where data transformation logic (including encryption) lives.] [Source: IBM Module 4 material]

---

## Question 8

**ESPs are a middle layer between multiple event sources and destinations. ESPs may have different architectures and components but also some common components. Which of the following common components receives and consumes events?**

| Option | Correct? |
|--------|----------|
| Query engine | ✗ |
| **Event broker** | **✓ CORRECT** |
| Event storage | ✗ |
| Analytic engine | ✗ |

**Answer:** Event broker

[ENRICHED: analysis — From the IBM course: The four main components of an ESP are: (1) Event Broker — receives and distributes events, (2) Event Storage — persists events, (3) Analytics — processes events, (4) Query Engine — allows ad-hoc queries. The event broker is the component that "receives and consumes events" — it's the entry point that accepts events from producers and distributes them to consumers.] [Source: IBM Module 4 Summary]

> **⚠️ NOTE:** The Coursera quiz marked this answer as WRONG (0/1 point) despite all authoritative sources confirming "Event broker" is correct. The feedback said "Incorrect, please review the Distributed Event Streaming Platform Components video." This appears to be a quiz error. The networkingfunda.com answer key for this exact course also lists "Event broker" as correct for the same question.

---

## Question 9

**Which of the following Kafka core components publish events into topics?**

| Option | Correct? |
|--------|----------|
| **Producers** | **✓ CORRECT** |
| Consumers | ✗ |
| Brokers | ✗ |
| Partitions | ✗ |

**Answer:** Producers

[ENRICHED: analysis — Producers are applications that publish/write events to Kafka topics. Consumers read from topics. Brokers store and serve data. Partitions are subdivisions of topics. The flow is: Producers → publish to Topics → Consumers read from Topics.] [Source: https://kafka.apache.org/documentation/]

---

## Question 10

**Which of the Kafka CLI script files manages topics?**

| Option | Correct? |
|--------|----------|
| Kafka-console | ✗ |
| Kafka-console-consumer | ✗ |
| **Kafka-topics** | **✓ CORRECT** |
| Kafka-console-producer | ✗ |

**Answer:** Kafka-topics

[ENRICHED: analysis — The `kafka-topics.sh` script is used to create, describe, list, modify, and delete topics. `kafka-console-consumer.sh` manages consumers. `kafka-console-producer.sh` manages producers. "Kafka-console" is not a real script.] [Source: https://kafka.apache.org/documentation/]

---

## Summary

| Question | Topic | Correct Answer | Coursera Result |
|----------|-------|---------------|-----------------|
| Q1 | Kafka cluster servers | Brokers | ✓ Correct |
| Q2 | Kafka Streams API basis | Computational graph | ✗ Wrong (quiz error) |
| Q3 | Stream processor actions | Receives, transforms, forwards | ✓ Correct |
| Q4 | Special processor types | Source and sink processor | ✓ Correct |
| Q5 | Consumption without deadline | Permanent persistency | ✓ Correct |
| Q6 | Reading from partitions | Consumers | ✓ Correct |
| Q7 | ESP encryption component | Processor | ✓ Correct |
| Q8 | ESP receives/consumes events | Event broker | ✗ Wrong (quiz error) |
| Q9 | Publishing to topics | Producers | ✓ Correct |
| Q10 | Topic management CLI | Kafka-topics | ✓ Correct |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Q1 | Definition | Brokers are Kafka cluster servers | HIGH | https://kafka.apache.org/documentation/ |
| 2 | Q2 | Definition | Computational graph = processor topology | HIGH | https://kafka.apache.org/43/streams/developer-guide/write-streams-app/ |
| 3 | Q3 | Definition | Stream processors: receive, transform, forward | HIGH | https://kafka.apache.org/0102/streams/core-concepts/ |
| 4 | Q4 | Definition | Source and sink are special processors | HIGH | https://kafka.apache.org/0102/streams/core-concepts/ |
| 5 | Q5 | Analysis | Permanent persistency = no consumption deadline | HIGH | https://kafka.apache.org/documentation/ |
| 6 | Q6 | Definition | Consumers read from topics | HIGH | https://kafka.apache.org/documentation/ |
| 7 | Q7 | Analysis | Processor handles encryption in ESP | MEDIUM | IBM Module 4 material |
| 8 | Q8 | Definition | Event broker receives and consumes events | HIGH | IBM Module 4 Summary |
| 9 | Q9 | Definition | Producers publish to topics | HIGH | https://kafka.apache.org/documentation/ |
| 10 | Q10 | Definition | kafka-topics manages topics | HIGH | https://kafka.apache.org/documentation/ |

<!-- EXTRACTION_CHECKLIST: 10 questions extracted, 10 questions in output -->
