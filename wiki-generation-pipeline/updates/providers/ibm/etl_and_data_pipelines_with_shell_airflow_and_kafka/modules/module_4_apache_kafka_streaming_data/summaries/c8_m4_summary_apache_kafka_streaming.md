> **Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
> **Module 4:** Apache Kafka Streaming Data

# Module 4 Summary: Apache Kafka Streaming Data

## Key Concepts Learned

Congratulations! You have completed this module. At this point, you know:

### Event Streaming Fundamentals
- An **event stream** represents entities' status updates over time — each event is a timestamped record of something that happened (e.g., a transaction, a sensor reading, a user action)
- The main components of an **Event Stream Processing (ESP)** platform are:
  - **Event Broker** — receives and distributes events to consumers
  - **Event Storage** — persists events for replay and historical analysis
  - **Analytics** — processes events in real-time to extract insights
  - **Query Engine** — allows ad-hoc queries against the event stream

### Apache Kafka
- **Apache Kafka** is a very popular open-source ESP platform originally developed at LinkedIn
- Popular Kafka service providers include **Confluent Cloud**, **IBM Event Streams**, and **Amazon MSK** (Managed Streaming for Apache Kafka)
- The core components of Kafka are:
  - **Brokers** — servers that store and serve messages
  - **Topics** — named channels where messages are organized (like tables in a database)
  - **Partitions** — parallel subdivisions of topics for scalability
  - **Replications** — copies of partitions for fault tolerance
  - **Producers** — applications that write messages to topics
  - **Consumers** — applications that read messages from topics

### Kafka CLI Tools
- The **kafka-console-consumer** manages consumers from the command line

### Kafka Streams API
- **Kafka Streams API** is a simple client library supporting data processing in event streaming pipelines
- A **stream processor** receives, transforms, and forwards the processed stream
- Kafka Streams API uses a **computational graph** (topology) to define processing logic
- There are two special types of processors in the topology:
  - **Source processor** — reads from an input topic and feeds events into the topology
  - **Sink processor** — writes processed events to an output topic

---

## Visual Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    KAFKA ARCHITECTURE                             │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │Producer 1│───►│          │    │Consumer 1│                   │
│  └──────────┘    │  Topic   │───►└──────────┘                   │
│  ┌──────────┐    │ (Partitioned)│                                 │
│  │Producer 2│───►│          │    ┌──────────┐                   │
│  └──────────┘    └──────────┘───►│Consumer 2│                   │
│                                  └──────────┘                   │
│                                                                  │
│  Components: Brokers, Topics, Partitions, Replicas               │
└─────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAM PROCESSING TOPOLOGY                    │
│                                                                  │
│  [Source Processor] ──► [Transform] ──► [Sink Processor]        │
│       │                      │                   │               │
│  Reads from             Processes            Writes to           │
│  input topic            events               output topic        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

| Concept | What It Does |
|---------|-------------|
| Event Stream | Timestamped record of state changes over time |
| ESP Platform | Infrastructure for real-time event processing |
| Kafka Broker | Server that stores and serves messages |
| Topic | Named channel for organizing messages |
| Partition | Parallel subdivision for scalability |
| Replication | Copy for fault tolerance |
| Producer | Writes messages to topics |
| Consumer | Reads messages from topics |
| Kafka Streams | Client library for stream processing |
| Source Processor | Entry point — reads from input topic |
| Sink Processor | Exit point — writes to output topic |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Introduction | Context | Added Kafka origin (developed at LinkedIn) | HIGH | https://kafka.apache.org/documentation/ |
| 2 | Visual Summary | Example | Added ASCII diagrams for Kafka architecture and stream topology | MEDIUM | UNCERTAIN |

<!-- EXTRACTION_CHECKLIST: 12 sentences extracted, 12 sentences in output -->
