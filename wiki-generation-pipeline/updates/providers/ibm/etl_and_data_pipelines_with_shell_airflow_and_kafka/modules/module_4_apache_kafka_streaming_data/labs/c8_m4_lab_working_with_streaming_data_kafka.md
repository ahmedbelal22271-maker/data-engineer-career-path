> **Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
> **Module 4:** Apache Kafka Streaming Data

# Hands-on Lab: Working with Streaming Data using Kafka

## Lab Overview

| Detail | Value |
|--------|-------|
| **Estimated time** | 20 minutes |
| **Environment** | Skills Network Cloud IDE (Theia + Docker) |
| **License** | Apache 2.0 |
| **Authors** | Lavanya T S, Rav Ahuja |

## Introduction

In this lab, you will work with streaming data using Kafka. You will start by configuring the Kafka server to use the Kraft mode followed by starting the Kafka message broker service, creating a topic and then starting the producer and consumer.

[ENRICHED: definition — "KRaft mode" (Kafka Raft) is Kafka's newer consensus protocol that replaces the need for a separate ZooKeeper cluster. In older Kafka versions (pre-3.x), ZooKeeper was required to manage cluster metadata, leader election, and configuration. KRaft mode embeds this functionality directly into Kafka itself, simplifying deployment and reducing operational overhead. Kafka 3.3+ marks KRaft as production-ready, and ZooKeeper is deprecated as of Kafka 4.0.] [Source: https://kafka.apache.org/documentation/#kraft]

## Objectives

After completing this lab, you will be able to:

- Download Kafka binaries
- Configure the Kafka server to use the KRaft mode
- Start the Kafka message broker service
- Create a topic
- Start a producer
- Start a consumer

## Environment Setup

### About Skills Network Cloud IDE

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands-on labs for course and project-related labs. Theia is an open-source IDE (Integrated Development Environment), that can be run on desktop or on the cloud. To complete this lab, we will be using the Cloud IDE based on Theia running in a Docker container.

### Important Notice About This Lab Environment

Please be aware that sessions for this lab environment are not persistent. A new environment is created for you every time you connect to this lab. Any data you may have saved in an earlier session will get lost. To avoid losing your data, please plan to complete these labs in a single session.

[ENRICHED: context — The non-persistent environment means Kafka data, topics, and configurations exist only during your session. When you disconnect, everything is wiped. This is why the lab walks you through setup from scratch — there is no "resume" path. Plan to complete the entire lab in one sitting.] [Source: UNCERTAIN]

---

## Exercise 3: Start Producer

You need to create a topic before you can start to post messages.

### Step 1 — Open a terminal and navigate to Kafka

Start a new terminal and change to the kafka_2.13-4.3.1 directory.

```bash
cd kafka_2.13-4.3.1
```

### Step 2 — Create the topic

To create a topic named `news`, run the command below.

```bash
bin/kafka-topics.sh --create --topic news --bootstrap-server localhost:9092
```

You will see the message: `Created topic news.`

[ENRICHED: definition — `kafka-topics.sh` is a command-line utility included in Kafka binaries. The `--create` flag tells it to create a new topic. `--topic news` names the topic "news". `--bootstrap-server localhost:9092` tells the tool which Kafka broker to connect to (port 9092 is the default Kafka broker port). This command sends a metadata request to the broker, which then allocates partitions and replication for the new topic.] [Source: https://kafka.apache.org/documentation/#operations]

### Step 3 — Start the producer

Run the command below to start a producer.

```bash
bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic news
```

After the producer starts, and you get the `>` prompt, type any text message and press enter. Or you can copy the text below and paste. The below text sends three messages to Kafka.

```plaintext
Good morning
Good day
Enjoy the Kafka lab
```

[ENRICHED: definition — `kafka-console-producer.sh` is a command-line tool that reads lines from stdin and publishes each line as a Kafka message to the specified topic. The `>` prompt indicates the producer is ready to accept input. Each line you type becomes one message. The producer handles serialization, batching, and sending to the broker automatically. In production, you would use a programmatic producer (Java, Python, etc.) instead of this console tool.] [Source: https://kafka.apache.org/documentation/#basic_ops_console_producer]

### What happens behind the scenes

When you type "Good morning" and press Enter:

```
You (terminal) → kafka-console-producer → Kafka Broker (port 9092) → Topic "news", Partition 0
```

```
┌──────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  You type    │      │  Producer sends   │      │  Broker stores   │
│  "Good       │ ───► │  message to       │ ───► │  message in      │
│  morning"    │      │  broker           │      │  news-0/         │
└──────────────┘      └──────────────────┘      └──────────────────┘
```

---

## Exercise 4: Start Consumer

You need a consumer to read messages from Kafka.

### Step 1 — Open a new terminal

Start a new terminal and change to the kafka_2.13-4.3.1 directory.

```bash
cd kafka_2.13-4.3.1
```

### Step 2 — Start the consumer

Run the command below to listen to the messages in the topic `news`.

```bash
bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic news \
  --from-beginning
```

You should see all the messages you sent from the producer appear here.

You can go back to the producer terminal and type some more messages, one message per line, and you will see them appear here.

[ENRICHED: definition — `kafka-console-consumer.sh` is a command-line tool that reads messages from a Kafka topic and prints them to stdout. The `--from-beginning` flag tells the consumer to start reading from the earliest available message in the topic (not just new ones). Without this flag, the consumer would only receive messages published after it starts. This is useful for testing and debugging.] [Source: https://kafka.apache.org/documentation/#basic_ops_console_consumer]

### What happens behind the scenes

When the consumer starts with `--from-beginning`:

```
Kafka Broker → Consumer reads all stored messages → Prints to your terminal
```

```
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  Broker has      │      │  Consumer reads   │      │  You see:        │
│  messages 0,1,2  │ ───► │  from offset 0    │ ───► │  Good morning    │
│  in news-0       │      │  (beginning)      │      │  Good day        │
└──────────────────┘      └──────────────────┘      │  Enjoy the Kafka │
                                                     │  lab             │
                                                     └──────────────────┘
```

**Live update:** If you type a new message in the producer terminal while the consumer is running, it appears instantly in the consumer terminal — this is the real-time streaming aspect.

---

## Exercise 5: Explore Kafka Directories

Kafka uses the `/tmp/kraft-combined-logs` directory to store the messages.

### Step 1 — Open a new terminal

Start a new terminal and navigate to the kafka_2.13-4.3.1 directory.

```bash
cd kafka_2.13-4.3.1
```

### Step 2 — List the root directory

Explore the root directory of the server.

```bash
ls
```

Notice there is a `tmp` directory. The `kraft-combined-logs` inside the `tmp` directory contains all the logs. To check the logs generated for the topic `news` run the following command:

```bash
ls /tmp/kraft-combined-logs/news-0
```

> **Note:** All messages are stored in the `news-0` directory under the `/tmp/kraft-combined-logs` directory.

[ENRICHED: definition — The `news-0` directory name follows the pattern `<topic>-<partition>`. Since the `news` topic has one partition by default (partition 0), the directory is `news-0`. Inside this directory, Kafka stores message segments as log files. Each segment is a file containing serialized messages. Kafka uses a append-only log structure — new messages are always appended to the end, and old messages are retained based on the topic's retention policy (default: 7 days or until size limit).] [Source: https://kafka.apache.org/documentation/#log_retention]

---

## Exercise 6: Clean Up

### To stop the producer

In the terminal where you are running producer, press `CTRL+C`.

### To stop the consumer

In the terminal where you are running consumer, press `CTRL+C`.

### To stop the Kafka server

In the terminal where you are running Kafka server, press `CTRL+C`.

[ENRICHED: context — `CTRL+C` sends a SIGINT (interrupt signal) to the running process. For the producer and consumer, this gracefully closes the connection to the broker and exits. For the Kafka server, this initiates a controlled shutdown: it flushes any in-memory data to disk, commits offsets, and releases the port. A forced kill (SIGKILL) without CTRL+C could leave orphaned processes or corrupted log segments.] [Source: UNCERTAIN]

---

## Practice Exercises

### Practice 1 — Create a new topic named `weather`

Make sure that the Kafka server is still running. Change to the `kafka_2.13-4.3.1` directory and run the following command:

```bash
bin/kafka-topics.sh --create --topic weather --bootstrap-server localhost:9092
```

### Practice 2 — Post messages to the topic `weather`

Use `kafka-console-producer.sh` and point to topic `weather`.

Make sure that the Kafka server is still running. Run the following command:

```bash
bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic weather
```

Post some test messages.

### Practice 3 — Read the messages from the topic `weather`

Use `kafka-console-consumer.sh` and read from the topic `weather`.

Make sure that the Kafka server is still running. In a new terminal, change to `kafka_2.13-4.3.1` directory and run the following command:

```bash
bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic weather \
  --from-beginning
```

Make sure that the messages you sent from the producer appear here.

---

## Lab Summary

In this lab, you practiced the core Kafka workflow:

```
┌─────────────────────────────────────────────────────────┐
│                    KAFKA WORKFLOW                         │
│                                                          │
│  1. Start Broker ──► 2. Create Topic ──► 3. Produce     │
│         │                    │                  │        │
│         ▼                    ▼                  ▼        │
│  kafka-server-         kafka-topics.sh    kafka-console- │
│  start.sh              --create           producer.sh    │
│                                                          │
│  4. Consume ◄─────────────────────────────────────────── │
│         │                                                │
│         ▼                                                │
│  kafka-console-                                          │
│  consumer.sh                                             │
│  --from-beginning                                        │
└─────────────────────────────────────────────────────────┘
```

### Key Takeaways

1. **Broker** is the Kafka server that stores and serves messages
2. **Topic** is a named channel where messages are organized (like a table in a database)
3. **Producer** writes messages to a topic
4. **Consumer** reads messages from a topic
5. **KRaft mode** eliminates the need for ZooKeeper — Kafka manages its own metadata
6. Messages are stored on disk in `/tmp/kraft-combined-logs/<topic>-<partition>/`
7. Use `--from-beginning` to read all stored messages, not just new ones

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Lab Overview | Definition | Defined KRaft mode as Kafka's built-in consensus protocol replacing ZooKeeper | HIGH | https://kafka.apache.org/documentation/#kraft |
| 2 | Environment | Context | Explained non-persistent environment — no resume path, complete in one sitting | MEDIUM | UNCERTAIN |
| 3 | Exercise 3 | Definition | Defined kafka-topics.sh, --create, --bootstrap-server flags | HIGH | https://kafka.apache.org/documentation/#operations |
| 4 | Exercise 3 | Definition | Defined kafka-console-producer.sh — reads stdin, publishes each line as message | HIGH | https://kafka.apache.org/documentation/#basic_ops_console_producer |
| 5 | Exercise 3 | Example | Added ASCII diagram showing producer → broker → topic flow | MEDIUM | UNCERTAIN |
| 6 | Exercise 4 | Definition | Defined kafka-console-consumer.sh and --from-beginning flag | HIGH | https://kafka.apache.org/documentation/#basic_ops_console_consumer |
| 7 | Exercise 4 | Example | Added ASCII diagram showing consumer reading from beginning and live updates | MEDIUM | UNCERTAIN |
| 8 | Exercise 5 | Definition | Explained news-0 directory naming pattern (topic-partition) and log segment storage | HIGH | https://kafka.apache.org/documentation/#log_retention |
| 9 | Exercise 6 | Context | Explained CTRL+C graceful shutdown behavior for producer, consumer, and broker | MEDIUM | UNCERTAIN |
| 10 | Summary | Example | Added complete workflow diagram showing all steps in sequence | MEDIUM | UNCERTAIN |

<!-- EXTRACTION_CHECKLIST: 24 sentences extracted, 24 sentences in output -->
