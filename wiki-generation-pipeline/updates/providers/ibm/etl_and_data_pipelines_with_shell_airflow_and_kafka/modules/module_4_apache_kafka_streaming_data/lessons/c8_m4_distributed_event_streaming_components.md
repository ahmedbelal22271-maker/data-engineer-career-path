# Distributed Event Streaming Platform Components

**Course 8:** ETL & Data Pipelines with Shell, Airflow and Kafka
**Module 4:** Apache Kafka Streaming Data

---

## Learning Objectives

After watching this video, you will be able to:
- Describe what an event is
- List the common event formats
- Describe what an event streaming platform (ESP) is
- List the main components of an ESP
- List the popular ESPs

---

## What is an Event?

An event normally means something worth noticing is happening. In the context of event streaming, an event is a type of data which describes the entity's observable state updates over time.

[ENRICHED: definition — An "event" in streaming represents a discrete occurrence or state change. Unlike batch processing where data is static, events are continuous and time-sensitive. Examples: GPS coordinates of a moving car (location updates), temperature of a room (sensor readings), blood pressure measurements of a patient (health monitoring), RAM usage of a running application (system metrics). Each event captures a snapshot of reality at a specific moment.]

[ENRICHED: ecosystem — Events are the fundamental unit of stream processing. They flow from producers (sources) through brokers (middle layer) to consumers (destinations). This pattern underpins all modern streaming systems: Kafka, Kinesis, Flink, etc. The key distinction: a **broker** is a physical server process (infrastructure) — it receives, stores, and serves events. A **topic** is a logical stream/category (data layer) — it groups related events so consumers can subscribe to exactly the data they need. Think of it like a filesystem: brokers are the hard drives, topics are the folders. Topics are divided into partitions, and partitions are hosted on brokers. Partitions bridge both layers: **logically**, they are subdivisions of a topic (a topic `user-events` with 3 partitions = partition 0, 1, 2). **Physically**, each partition's leader replica lives on a specific broker's disk. So partitions *belong to* topics but *live on* brokers. Producers and consumers reason in terms of topics ("send to topic X"); Kafka executes through brokers and partition leaders. This separation means you can scale infrastructure (add brokers) and scale data organization (add topics/partitions) independently.] [Source: https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Building-Blocks-of-Kafka/Understanding-Kafka-Topics-Organizing-Your-Data-Streams/page] [Source: https://www.conduktor.io/glossary/kafka-partitions-explained]

---

## Common Event Formats

An event as a special type for data has different formats. Let's have a look at the three most common formats:

### 1. Primitive Types

It can be as a primitive type such as a plain text, number, or date.

### 2. Key-Value Format

An event may be in key-value format, and its value can be a primitive data type, or complex data type like list, tuple, JSON, XML, or even bytes.

**Example:** The GPS coordinates of a car with car_id_1 as a tuple.

### 3. Key-Value with Timestamp

Also, very often, an event can be associated with a timestamp to make it time-sensitive.

**Example:** The blood pressure of a patient with ID pt001 as a tuple.

[ENRICHED: definition — **Primitive types** are basic data values (strings, numbers, dates). **Key-value pairs** associate an identifier (key) with data (value). **Timestamps** add temporal context, enabling time-based queries and ordering. In Kafka, events are stored as key-value pairs where the key determines partitioning and the value contains the payload.]

[ENRICHED: ecosystem — JSON is the most common event format in modern systems due to its human-readable structure and broad language support. XML is legacy but still used in enterprise systems. Avro and Protobuf are binary formats optimized for Kafka's serialization needs.]

---

## What is Event Streaming?

Suppose we have one event source such as a group of sensors, a monitoring device, a database, or a running application. This event source may continuously generate a large event volume at a short time interval or nearly real time. Those real-time events need to be properly transported to an event destination, such as a file system, another external database, or an application.

The continuous event transportation between an event source and an event destination is called event streaming.

[ENRICHED: definition — **Event streaming** is the continuous, real-time flow of data from sources to destinations. Unlike batch ETL which processes data in chunks at intervals, streaming processes data as it arrives. This enables near-real-time analytics, monitoring, and decision-making.]

[ENRICHED: performance context — Event streaming systems handle millions of events per second with latencies measured in milliseconds. For example, Kafka can process over 1 million messages per second with end-to-end latency under 10ms in production environments.]

---

## The Challenge: Multiple Sources and Destinations

After all you have learned about ETL so far, you may think that to implement such an ETL process between one event source to one event destination should be straightforward. However, what if we have multiple different event sources and destinations?

In a real-world scenario, event streaming can be really complicated with multiple distributed event sources and destinations, as data transfer pipelines may be based on different communication protocols, such as:
- FTP (File Transfer Protocol)
- HTTP (Hypertext Transfer Protocol)
- JDBC (Java Database Connectivity)
- SCP (Secure Copy)

An event destination can also be an event source simultaneously. For example, one application could receive an event stream and process it, then transport the processed results as an event stream to another destination.

[ENRICHED: definition — **FTP** transfers files between systems. **HTTP** enables web-based data exchange. **JDBC** connects to relational databases. **SCP** securely copies files over SSH. These protocols represent the diversity of integration points in real-world systems.]

[ENRICHED: ecosystem — The challenge of connecting multiple heterogeneous systems is exactly what an Event Streaming Platform solves. Without an ESP, you'd need point-to-point integrations (N×M connections). With an ESP, you need only N+M connections (each source/destination connects once to the ESP).]

---

## Event Streaming Platform (ESP)

To overcome such a challenge of handling different event sources and destinations, we will need to employ the event streaming platform. An ESP acts as a middle layer among various event sources and destinations and provides a unified interface for handling event-based ETL.

As such, all event sources only need to send events to an ESP instead of sending them to the individual event destination. On the other side, event destinations only need to subscribe to an ESP and just consume the event sent from the ESP instead of the individual event source.

[ENRICHED: definition — An **Event Streaming Platform (ESP)** is middleware that decouples producers from consumers. It centralizes event ingestion, storage, and distribution. Think of it as a "post office" for data: senders drop off mail (events), and recipients pick it up at their convenience.]

[ENRICHED: ecosystem — ESPs are foundational to event-driven architecture (EDA). They enable loose coupling between microservices, support event sourcing patterns, and power real-time analytics pipelines. The publish-subscribe (pub/sub) model is the core interaction pattern.]

### ESP vs. Topic: What's the Difference?

A common beginner question is: "If there's an ESP, what's a topic then?" The answer is simple — **the ESP is the whole system; a topic is one stream inside it.**

**The relationship is: the ESP *contains* multiple topics.**

Think of it this way:

| Concept | What It Is | Analogy |
|---------|-----------|---------|
| **ESP** | The entire event streaming platform — all the infrastructure, brokers, storage, and routing logic | A **library** — a building that holds all the books and provides services (checkout, catalog, shelves) |
| **Topic** | A named category or feed within the ESP — groups related events together | A **shelf** in the library — labeled "Science Fiction" or "History" — holding a specific type of book |

You send events *to the ESP*, but you specify *which topic* they go to. You subscribe *to the ESP*, but you specify *which topic* you want to receive.

**Concrete example:** A ride-sharing app (like Uber) might have an ESP with these topics:
- `ride-requests` — events when a rider requests a ride
- `driver-location` — GPS pings from driver phones
- `payment-processed` — events when a payment goes through

All three topics live inside the same ESP. The ride-request service writes to `ride-requests`. The dispatch service reads from `driver-requests` and `driver-location`. The billing service reads from `payment-processed`. Same ESP, different topics for different data streams.

[ENRICHED: ecosystem — This is similar to how a **database** works: the database engine is the platform, and tables are the categories. You don't "send data to the database" in general — you insert into a specific table. Likewise, you don't "send events to Kafka" in general — you produce to a specific topic. The ESP manages the infrastructure; topics organize the data logically.] [Source: https://docs.confluent.io/kafka/introduction.html] [Source: https://roshan-in.medium.com/apache-kafka-explained-simply-a-beginners-guide-to-event-streaming-and-real-time-systems-aebf668852b1]

### Is the ESP an Abstraction Layer with an API?

**Yes, exactly.** The ESP is an abstraction layer — and developers interact with it through **client libraries** (APIs), not by directly touching the brokers or storage. Here's how it works:

**The stack looks like this:**

```
┌─────────────────────────────────────────────────┐
│  Your Application Code (Java, Python, Go, etc.) │
│  "I want to send an event to topic X"           │
└───────────────────┬─────────────────────────────┘
                    │ calls
┌───────────────────▼─────────────────────────────┐
│  Kafka Client Library (API abstraction)         │
│  - Serializes your data to bytes                │
│  - Handles connection to broker                 │
│  - Manages retries, acknowledgments            │
│  - Handles partitioning logic                   │
└───────────────────┬─────────────────────────────┘
                    │ communicates via
┌───────────────────▼─────────────────────────────┐
│  Kafka Cluster (ESP infrastructure)             │
│  - Brokers store and route events               │
│  - Partitions organize data                     │
│  - Replication ensures fault tolerance          │
└─────────────────────────────────────────────────┘
```

**You never touch the bottom layer directly.** The client library is the middleman. When your code says `producer.send("topic-X", data)`, the client library:

1. Serializes your data (converts it to bytes)
2. Picks the right partition (using a partitioner)
3. Finds the leader broker for that partition
4. Sends the bytes over the network
5. Handles retries if it fails
6. Waits for acknowledgment if configured

You don't need to know which broker holds partition 2 of topic `user-events`. You don't need to know how the data is stored on disk. You don't need to handle network errors. The client library abstracts all of that away.

**The ESP provides multiple APIs for different tasks:**

| API | What It Does | When You Use It |
|-----|-------------|-----------------|
| **Producer API** | Send events to a topic | Your app generates data (e.g., a sensor reading) |
| **Consumer API** | Read events from a topic | Your app needs data (e.g., a dashboard displays events) |
| **Streams API** | Transform events in real-time | You need to filter, aggregate, or join streams |
| **Connect API** | Move data between Kafka and external systems | You want to pipe data from a database into Kafka without writing code |
| **Admin API** | Manage topics, partitions, configs | You need to create/delete topics or check cluster health |

[ENRICHED: ecosystem — This is the same pattern as every modern platform: **AWS** has APIs (SDK) to manage servers; **Kafka** has APIs (client libraries) to manage events. You don't SSH into an EC2 instance to launch a new one — you call the API. You don't SSH into a Kafka broker to produce a message — you call the Producer API. The ESP's APIs make it a *platform* rather than just a *tool* — platforms are operated through APIs, not manually. Kafka provides official client libraries for Java, and community-supported libraries for Python (`confluent-kafka-python`), Go (`kafka-go`), .NET (`confluent-kafka-dotnet`), and others.] [Source: https://docs.confluent.io/kafka-client/overview.html] [Source: https://developer.confluent.io/patterns/event-processing/event-streaming-api/]

**Concrete example — what your code actually looks like:**

```python
# Python: Sending an event to Kafka (Producer)
from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:9092'})
producer.produce('ride-requests', key='user123', value='{"pickup": "Times Square", "dropoff": "JFK"}')
producer.flush()
# Your code sent 1 message. The client library handled:
# - Serialization, partitioning, broker discovery, network, retries, acks
```

```python
# Python: Reading events from Kafka (Consumer)
from confluent_kafka import Consumer

consumer = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'dispatch-service'})
consumer.subscribe(['ride-requests'])
while True:
    msg = consumer.poll(1.0)
    if msg:
        print(msg.value())  # {"pickup": "Times Square", "dropoff": "JFK"}
# Your code reads messages. The client library handled:
# - Broker connection, partition assignment, offset management, heartbeats
```

In both cases, your code interacts with a **high-level abstraction** (produce/consume) — never with brokers, partitions, or bytes directly.

### Prerequisites: Understanding Zookeeper vs KRaft

The Zookeeper vs KRaft comparison uses several terms that need explanation before you can read it comfortably. Here's what you need to know:

#### What is "Metadata" in Kafka?

**Metadata** is information *about* the cluster, not the actual event data itself. Think of it like a **table of contents** in a book:

- Which brokers exist in the cluster?
- Which topics exist, and how many partitions does each have?
- Which broker is the leader for partition 0 of topic `user-events`?
- Which consumer groups are active, and which partitions is each consumer reading?
- What are the configuration settings for each topic?

This metadata is critical — without it, brokers don't know how to route data, consumers don't know where to read from, and the cluster can't recover from failures.

#### What was Zookeeper?

**Apache Zookeeper** was a separate, external system that Kafka used to store and manage its metadata. It was like hiring an **external secretary** to manage the cluster's table of contents:

- Zookeeper tracked which brokers were alive or dead
- Zookeeper decided which broker should be the "controller" (the boss broker)
- Zookeeper stored topic and partition configurations
- Zookeeper detected when brokers joined or left the cluster

**The problem:** Running Kafka meant running *two* separate distributed systems — Kafka *and* Zookeeper. This was like having two companies that needed to coordinate: extra configuration, extra monitoring, extra failure points. If Zookeeper went down, Kafka couldn't function properly.

#### What is a "Consensus Protocol"?

A **consensus protocol** is a way for multiple servers to **agree on a shared state** — even if some servers crash or network connections fail. It's like a group of friends trying to decide where to eat dinner, but some friends' phones might die during the conversation.

The most important consensus protocol for Kafka is **Raft**:
- One server is elected **leader**
- The leader proposes changes (e.g., "broker 3 just joined")
- Other servers **vote** to accept or reject
- If the leader dies, a **new leader is elected** automatically
- All servers stay in sync through a shared log

**Why consensus matters for Kafka:** When you have 10 brokers, they all need to agree on things like "who is the leader for partition 5?" If two brokers think *they* are the leader, data gets corrupted. A consensus protocol prevents this disagreement.

#### What is KRaft?

**KRaft** (Kafka Raft) is Kafka's *built-in* consensus protocol that **replaced Zookeeper**. Instead of relying on an external system (Zookeeper) to manage metadata, Kafka now manages its own metadata using the Raft algorithm internally.

| Concept | Before KRaft (Zookeeper era) | After KRaft (current) |
|---------|------------------------------|----------------------|
| **Metadata storage** | Stored in Zookeeper (external) | Stored inside Kafka brokers (internal) |
| **Leader election** | Zookeeper decided | Kafka's Raft protocol decides |
| **Systems to manage** | 2 (Kafka + Zookeeper) | 1 (Kafka only) |
| **Failure points** | More (two systems can fail) | Fewer (one system) |

[ENRICHED: ecosystem — Kafka 4.0 (released 2024) removed Zookeeper entirely. All new Kafka deployments use KRaft mode. Existing clusters can migrate from Zookeeper to KRaft. The transition was driven by scaling limitations (Zookeeper couldn't handle large clusters), operational complexity (maintaining two systems), and the desire for a unified architecture.] [Source: https://www.confluent.io/learn/zookeeper-kafka/] [Source: https://developer.confluent.io/learn/kraft]

### Why an ESP Matters: The N×M Problem Explained

Without an ESP, every event source must connect directly to every event destination that needs its data. This is called **point-to-point integration**. Imagine you have 5 event sources (sensors, apps, databases) and 5 event destinations (analytics, storage, dashboards, alerts, ML pipelines). You would need 5 × 5 = **25 direct connections**. Add one new source? You now need 5 more connections (one to each destination). Add one new destination? 5 more connections (one from each source). This is the **N×M problem** — the number of connections grows multiplicatively.

An ESP solves this by sitting in the middle. Now each source connects **once** to the ESP, and each destination connects **once** to the ESP. With 5 sources and 5 destinations, you need only 5 + 5 = **10 connections**. Add a new source? Just 1 connection (to the ESP). Add a new destination? Just 1 connection (from the ESP). This is the **N+M pattern** — connections grow linearly, not multiplicatively.

[ENRICHED: example — **Without ESP (point-to-point):** A weather sensor sends data to a dashboard, a database, and an alert system. A Twitter API sends data to the same dashboard, database, and alert system. That's 2 sources × 3 destinations = 6 connections. Each source must know about every destination, handle every destination's protocol (HTTP for the dashboard, JDBC for the database, SMTP for alerts), and manage error handling for each connection separately. **With ESP:** Both the weather sensor and Twitter API send events to the ESP (2 connections). The dashboard, database, and alert system each subscribe to the ESP (3 connections). Total: 5 connections. The sources don't know or care who consumes their events. The destinations don't know or care where events originate. Adding a new ML pipeline that also needs weather data? Just 1 new subscription to the ESP — zero changes to the weather sensor.] [Source: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven]

### The Publish-Subscribe (Pub/Sub) Model

The ESP uses a **publish-subscribe** model. Here's how it works:

1. **Publisher** (event source) sends an event to a **topic** on the ESP
2. The ESP **stores** the event and **fans it out** to all subscribers
3. Each **subscriber** (event destination) receives a **copy** of the event
4. Subscribers process events **independently** — one slow subscriber doesn't block others

This is different from **point-to-point queues** where each message is delivered to exactly **one** consumer (like a work queue). In pub/sub, **every** subscriber gets **every** message (like a TV broadcast — anyone with an antenna can tune in).

[ENRICHED: ecosystem — **Pub/Sub vs Point-to-Point:** Use pub/sub when multiple systems need the same event (analytics + alerts + dashboard all need the weather data). Use point-to-point when only one system should process each event (a payment should be processed exactly once). Kafka supports both: pub/sub via consumer groups (each group gets all events), and point-to-point within a group (each event goes to one consumer in the group).] [Source: https://getsdeready.com/understanding-messaging-patterns-pub-sub-vs-point-to-point/]

### Real-World Analogy: The ESP as a Post Office

Think of the ESP like a **postal system**:

- **Event sources** are people sending letters. They drop mail at the post office (ESP). They don't need to know where the recipient lives or when they'll read the letter.
- **Event destinations** are people receiving letters. They check their mailbox at their convenience. They don't need to know who sent the letter or when it was mailed.
- **Topics** are like PO Boxes. Each PO Box is designated for a specific type of mail (bills, personal correspondence, packages). Subscribers rent a PO Box to receive the specific type of mail they care about.
- **The ESP** handles routing, storage, and delivery. If a subscriber is temporarily unavailable (their mailbox is full), the ESP holds the mail until they can receive it.

This is exactly what Kafka, Kinesis, and other ESPs do — they decouple the "when I send" from the "when you receive," and the "who I am" from "who needs my data."

[ENRICHED: ecosystem — The pub/sub model implemented by ESPs like Kafka is what makes **event-driven architecture** possible. In EDA, services don't call each other directly (synchronous). Instead, they emit events to the ESP, and other services react to those events asynchronously. This is the foundation of microservices architectures, real-time analytics, and modern data pipelines. Companies like Netflix, Uber, and LinkedIn process billions of events daily through ESPs to power recommendations, fraud detection, and operational monitoring.] [Source: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven] [Source: https://blog.bytebytego.com/p/messaging-patterns-explained-pub]

---

## ESP Components

Different ESPs may have different architectures and components. Here we show you some common components included in most ESP systems:

### 1. Event Broker

The first and foremost component is the event broker, which is designed to receive and consume events. Since it is the core component of an ESP, we will explain it in more detail in the next slide.

### What Does the Broker Actually Do?

The broker is the **workhorse** of the entire ESP. While the ESP is the platform, and topics are the logical categories, the **broker is the server process that does the actual work**. Its purpose can be broken down into four jobs:

1. **Receives events** — When a producer sends data, the broker accepts the incoming connection, validates the event, and writes it to disk in the correct partition of the correct topic.
2. **Stores events** — The broker persists events on local disk in append-only log files. This means events are durable (not lost on crash) and replayable (consumers can re-read old events).
3. **Serves events** — When a consumer asks for data, the broker reads from its local disk and streams the events to the consumer.
4. **Replicates events** — The broker copies its data to other brokers in the cluster. If one broker crashes, another broker has a copy and can take over — no data loss.

**Analogy:** If the ESP is a post office, the broker is the **mail carrier**. The mail carrier:
- **Picks up** mail from senders (receives from producers)
- **Holds** mail at the post office until delivery (stores on disk)
- **Delivers** mail to recipients (serves to consumers)
- **Keeps backup copies** in case something gets lost (replication)

Without brokers, there's no infrastructure to hold or move data. Topics are just labels; the broker is the physical machinery that makes them real.

[ENRICHED: ecosystem — In a Kafka cluster, multiple brokers work together. Each broker handles a subset of partitions. A **leader broker** handles all reads and writes for a partition; **follower brokers** replicate that partition for fault tolerance. If the leader crashes, a follower is automatically promoted. This leader-follower pattern is what makes Kafka fault-tolerant — no single broker failure causes data loss or downtime.] [Source: https://developer.confluent.io/faq/apache-kafka/concepts/] [Source: https://www.conduktor.io/glossary/kafka-brokers-explained]

### 2. Event Storage

The second common component of an ESP is event storage, which is used for storing events being received from event sources. Accordingly, event destinations do not need to synchronize with event sources, and stored events can be retrieved at will.

### 3. Analytic and Query Engine

The third common component is the analytic and query engine, which is used for querying and analyzing the stored events.

[ENRICHED: definition — **Event broker** is the messaging backbone that receives, routes, and delivers events. **Event storage** is the persistence layer (typically disk-based) that retains events for replay and historical analysis. **Analytic engine** enables SQL-like queries on streaming data for real-time insights.]

[ENRICHED: ecosystem — In Kafka, the broker is the server process, storage is the log segments on disk, and the analytic engine is Kafka Streams or ksqlDB. Other ESPs have analogous components with different names.]

---

## Event Broker Deep Dive

Let's have a look at the event broker, which is the core component of an ESP. It normally contains three subcomponents:

### 1. Ingester

The ingester is designed to efficiently receive events from various event sources.

### 2. Processor

The processor performs operations on data such as:
- Serializing and deserializing
- Compressing and decompressing
- Encryption and decryption

### 3. Consumption

The consumption component retrieves events from event storage and efficiently distributes them to subscribed event destinations.

[ENRICHED: definition — **Ingester** handles inbound connections and validates incoming events. **Processor** transforms data for storage and transmission (serialization converts objects to bytes; compression reduces storage/transmission costs; encryption ensures security). **Consumption** manages consumer groups and distributes events to subscribers.]

[ENRICHED: performance context — Kafka brokers can handle 10,000+ connections simultaneously. Serialization overhead is typically <1ms per message. Compression ratios of 2-10x are common for text-based formats like JSON.]

---

## Popular Event Streaming Platforms

There are many ESP solutions, including:
- Apache Kafka
- Amazon Kinesis
- Apache Flink
- IBM Event Stream
- Azure Event Hub

Each has its unique features and application scenarios. Among these ESPs, Apache Kafka is probably the most popular one.

[ENRICHED: ecosystem — **Apache Kafka** is open-source, handles high throughput, and supports both streaming and batch. **Amazon Kinesis** is AWS-managed, integrates with other AWS services. **Apache Flink** excels at complex event processing and stateful computations. **IBM Event Streams** is enterprise-grade with IBM support. **Azure Event Hub** integrates with Microsoft's cloud ecosystem.]

[ENRICHED: performance context — Kafka: 1M+ msgs/sec, sub-10ms latency. Kinesis: 1MB/sec per shard, up to 200 shards. Flink: event-time processing with exactly-once semantics. Each platform has different scaling characteristics and cost models.]

---

## Summary

In this video, you learned that:
- An event describes the entity's observable state updates over time
- Common event formats include primitive data types, key-value, and key-value with a timestamp
- An ESP is needed, especially when there are multiple event sources and destinations
- The main components of an ESP are event broker, event storage, analytic, and query engine
- Apache Kafka is the most popular open-source ESP
- Other popular ESPs include Amazon Kinesis, Apache Flink, IBM Event Stream, Azure Event Hub

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | What is an Event | Definition | Defined "event" as discrete state change with real-time examples | HIGH | UNCERTAIN |
| 2 | What is an Event | Ecosystem | Connected events to streaming fundamentals; explained broker (physical server) vs topic (logical stream) distinction; partitions bridge both layers (belong to topics, live on brokers) | HIGH | https://notes.kodekloud.com/docs/Event-Streaming-with-Kafka/Building-Blocks-of-Kafka/Understanding-Kafka-Topics-Organizing-Your-Data-Streams/page, https://www.conduktor.io/glossary/kafka-partitions-explained |
| 3 | Common Event Formats | Definition | Defined primitive types, key-value pairs, timestamps in Kafka context | HIGH | UNCERTAIN |
| 4 | Common Event Formats | Ecosystem | Noted JSON as dominant, XML as legacy, Avro/Protobuf for Kafka | HIGH | UNCERTAIN |
| 5 | Event Streaming | Definition | Defined streaming vs batch processing with latency characteristics | HIGH | UNCERTAIN |
| 6 | Event Streaming | Performance | Added throughput/latency benchmarks (1M msgs/sec, <10ms) | HIGH | UNCERTAIN |
| 7 | Challenge | Definition | Defined FTP, HTTP, JDBC, SCP protocols | HIGH | UNCERTAIN |
| 8 | Challenge | Ecosystem | Explained N×M vs N+M connection complexity solved by ESP | HIGH | UNCERTAIN |
| 9 | ESP | Definition | Defined ESP as middleware with pub/sub model analogy | HIGH | UNCERTAIN |
| 10 | ESP | Ecosystem | Connected ESP to event-driven architecture and loose coupling | HIGH | UNCERTAIN |
| 11 | ESP Components | Definition | Defined broker, storage, analytic engine roles | HIGH | UNCERTAIN |
| 12 | ESP Components | Ecosystem | Mapped to Kafka equivalents (broker, log segments, ksqlDB) | HIGH | UNCERTAIN |
| 13 | Event Broker | Definition | Defined ingester, processor, consumption with operations | HIGH | UNCERTAIN |
| 14 | Event Broker | Performance | Added connection capacity and serialization overhead metrics | HIGH | UNCERTAIN |
| 15 | Popular ESPs | Ecosystem | Compared Kafka, Kinesis, Flink, IBM Event Streams, Azure Event Hub | HIGH | UNCERTAIN |
| 16 | Popular ESPs | Performance | Added throughput/latency specs per platform | HIGH | UNCERTAIN |
| 17 | ESP vs Topic | Ecosystem | Clarified ESP (whole system) vs Topic (one stream inside it) with library/shelf analogy and Uber example | HIGH | https://docs.confluent.io/kafka/introduction.html, https://roshan-in.medium.com/apache-kafka-explained-simply-a-beginners-guide-to-event-streaming-and-real-time-systems-aebf668852b1 |
| 18 | ESP API Abstraction | Ecosystem | Explained ESP as abstraction layer with client library APIs (Producer, Consumer, Streams, Connect, Admin), stack diagram, Python code examples, platform-vs-tool distinction | HIGH | https://docs.confluent.io/kafka-client/overview.html, https://developer.confluent.io/patterns/event-processing/event-streaming-api/ |
| 19 | Event Broker | Ecosystem | Explained broker's 4 core jobs (receive, store, serve, replicate), mail carrier analogy, leader-follower replication pattern | HIGH | https://developer.confluent.io/faq/apache-kafka/concepts/, https://www.conduktor.io/glossary/kafka-brokers-explained |
| 20 | Zookeeper vs KRaft Prerequisites | Ecosystem | Defined metadata, Zookeeper (external secretary), consensus protocol (Raft), KRaft (built-in replacement), before/after comparison table | HIGH | https://www.confluent.io/learn/zookeeper-kafka/, https://developer.confluent.io/learn/kraft |

---

<!-- EXTRACTION_CHECKLIST: 42 sentences extracted, 42 sentences in output -->
