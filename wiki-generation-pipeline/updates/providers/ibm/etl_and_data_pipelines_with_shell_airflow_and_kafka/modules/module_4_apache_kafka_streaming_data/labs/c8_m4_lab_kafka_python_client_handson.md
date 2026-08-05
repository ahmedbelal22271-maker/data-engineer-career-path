> **Course 8:** ETL and Data Pipelines with Shell, Airflow, and Kafka
> **Module 4:** Apache Kafka Streaming Data

<mark style="background-color: rgba(200, 230, 201, 0.4);">NEW</mark>

# Hands-on Lab: Kafka Python Client

## Lab Overview

| Detail | Value |
|--------|-------|
| **Estimated time** | 30 minutes |
| **Environment** | Skills Network Cloud IDE (Theia + Docker) |
| **License** | IBM Corporation |
| **Authors** | Ramesh Sana Reddy, Lavanya T S, Shreya Khurana |

## Objectives

After completing this lab, you will be able to:

- Use kafka-python to interact with Kafka server in Python
- Send and receive messages through the Kafka-python client

## About Skills Network Cloud IDE

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands on labs for course and project-related labs. Theia is an open-source IDE (Integrated Development Environment) that can be run on desktop or on the cloud. To complete this lab, we will be using the Cloud IDE based on Theia running in a Docker container.

[ENRICHED: definition — "Theia" is an open-source IDE framework developed by Eclipse Foundation. It provides a browser-based development environment similar to VS Code, supporting multiple programming languages and extensions. Theia is designed to be cloud-native, making it ideal for educational lab environments where users need consistent, pre-configured development setups.] [Source: https://theia-ide.org/]

## Important Notice About This Lab Environment

Please be aware that sessions for this lab environment are not persistent. A new environment is created for you every time you connect to this lab. Any data you may have saved in an earlier session will get lost. To avoid losing your data, please plan to complete these labs in a single session.

[ENRICHED: context — The non-persistent environment means Kafka data, topics, and configurations exist only during your session. When you disconnect, everything is wiped. This is why the lab walks you through setup from scratch — there is no "resume" path. Plan to complete the entire lab in one sitting.] [Source: UNCERTAIN]

---

## Exercise 1: Download and Extract Kafka

### Step 1 — Open a terminal

Open a new terminal by clicking the menu bar and selecting Terminal->New Terminal.

This will open a new terminal at the bottom of the screen.

### Step 2 — Download Kafka

Run the command below to download Kafka:

```bash
wget https://downloads.apache.org/kafka/4.3.1/kafka_2.13-4.3.1.tgz
```

[ENRICHED: definition — "wget" is a command-line utility for downloading files from the web using HTTP, HTTPS, and FTP protocols. It works non-interactively, making it ideal for automated scripts and lab environments. The name stands for "World Wide Web get."] [Source: https://www.gnu.org/software/wget/]

[ENRICHED: context — The download URL points to Apache Kafka 4.3.1 with Scala 2.13. The "2.13" refers to the Scala version Kafka is built with. Kafka is written in Scala and runs on the JVM (Java Virtual Machine). Version 4.3.1 is the latest stable release as of July 2026. Note: Kafka 3.8.0 is no longer available on the Apache downloads server — older versions are archived at archive.apache.org.] [Source: https://kafka.apache.org/downloads]

[ENRICHED: correction — The original lab used Kafka 3.8.0 which is no longer available (404 error). Updated to Kafka 4.3.1, the latest stable release. Kafka 4.x dropped ZooKeeper support entirely — KRaft is now the only mode. The commands remain compatible since the binary structure hasn't changed.] [Source: https://downloads.apache.org/kafka/]

### Step 3 — Extract Kafka

Extract Kafka from the zip file by running the command below:

```bash
tar -xzf kafka_2.13-4.3.1.tgz
```

[ENRICHED: definition — "tar" is a tape archive utility used to combine multiple files into a single archive file (tarball) and extract them. The flags "-xzf" mean: -x (extract), -z (decompress with gzip), -f (specify filename). This is the standard way to distribute source code and binaries on Linux/Unix systems.] [Source: https://www.gnu.org/software/tar/]

This creates a new directory `kafka_2.13-4.3.1` in the current directory.

---

## Exercise 2: Configure KRaft and Start Server

### Step 1 — Navigate to Kafka directory

Change to the `kafka_2.13-4.3.1` directory:

```bash
cd kafka_2.13-4.3.1
```

### Step 2 — Generate Cluster UUID

Generate a Cluster UUID that will uniquely identify the Kafka cluster:

```bash
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```

[ENRICHED: definition — "KRaft" (Kafka Raft) is Kafka's built-in consensus protocol that replaces the need for Apache ZooKeeper. In older Kafka versions (pre-3.x), ZooKeeper was required to manage cluster metadata, leader election, and configuration. KRaft mode embeds this functionality directly into Kafka itself, simplifying deployment and reducing operational overhead. Kafka 3.3+ marks KRaft as production-ready, and ZooKeeper is deprecated as of Kafka 4.0.] [Source: https://kafka.apache.org/documentation/#kraft]

[ENRICHED: context — The cluster UUID is a unique identifier for your Kafka cluster. It's used by KRaft to coordinate between brokers and maintain cluster state. Each Kafka cluster must have a unique ID to prevent conflicts in multi-cluster environments.] [Source: UNCERTAIN]

Note: This cluster ID will be used by the KRaft controller.

### Step 3 — Configure log directories

KRaft requires the log directories to be configured. Run the following command to configure the log directories passing the cluster ID:

```bash
bin/kafka-storage.sh format --cluster-id $KAFKA_CLUSTER_ID --standalone --config config/server.properties
```

[ENRICHED: definition — "Log directories" in Kafka are where message data is physically stored on disk. Each topic partition has its own log directory containing segment files. Kafka uses append-only log files for high write throughput and efficient disk I/O.] [Source: https://kafka.apache.org/documentation/#design]

[ENRICHED: correction — In Kafka 4.x, the `config/kraft/` directory no longer exists. KRaft configuration is now directly in `config/server.properties`. The lab was using outdated paths (`config/kraft/server.properties`) which caused `NoSuchFileException`. Updated to use `config/server.properties`. [Source: https://medium.com/@meet.gada/how-to-install-apache-kafka-4-2-on-linux-kraft-mode-no-zookeeper-7d8ad986cb46]]

[ENRICHED: correction — The `--standalone` flag is required for single-node KRaft setup in Kafka 4.3+. Without it, you get "controller.quorum.voters is not set" error. This flag creates a meta.properties file and makes this node the only voter in the quorum. [Source: https://kafka.apache.org/43/operations/kraft/]]

### Step 4 — Start Kafka server

Now that KRaft is configured, you can start the Kafka server by running the following command:

```bash
bin/kafka-server-start.sh config/server.properties
```

Note: You can be sure it has started when you see an output contains messages that confirm the Kafka Server started successfully.

[ENRICHED: context — The server.properties file contains all Kafka broker configuration. Key settings include: `node.id` (unique node identifier), `process.roles` (broker, controller, or both), `listeners` (network endpoints), `log.dirs` (data storage locations), and `controller.quorum.voters` (controller nodes for consensus). In Kafka 4.x, this single file handles both broker and controller roles in combined mode.] [Source: https://kafka.apache.org/43/configuration/broker-configs/]

---

## Exercise 3: Create a Topic in the admin.py File

### Step 1 — Install kafka-python

Open a new terminal and navigate to the `kafka_2.13-4.3.1` directory:

```bash
cd kafka_2.13-4.3.1
```

Install the kafka-python package by running the following command:

```bash
pip3 install kafka-python
```

[ENRICHED: definition — "kafka-python" is a pure Python client library for Apache Kafka. It provides a Pythonic interface for interacting with Kafka brokers, including producing messages, consuming messages, and administrative operations. While convenient for development and learning, it has lower performance than C-based alternatives like confluent-kafka-python.] [Source: https://github.com/dpkp/kafka-python]

[ENRICHED: alternative — For production workloads requiring high throughput, consider using `confluent-kafka-python` instead. It wraps librdkafka (a C library) and provides 5-10x better performance. Install with `pip install confluent-kafka`. See the reading material for detailed comparison.] [Source: https://github.com/confluentinc/confluent-kafka-python]

### Step 2 — Create admin.py

Create a file named `admin.py` by running the following command:

```bash
touch admin.py
```

[ENRICHED: definition — "touch" is a Unix command that creates an empty file if it doesn't exist, or updates the timestamp if it does. It's commonly used to create placeholder files in scripts and lab exercises.] [Source: https://man7.org/linux/man-pages/man1/touch.1.html]

Click the button below to open the file in edit mode and paste the following content in the file and save it.

```python
from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id='test'
)

topic_list = []
new_topic = NewTopic(
    name="bankbranch",
    num_partitions=2,
    replication_factor=1
)
topic_list.append(new_topic)
admin_client.create_topics(new_topics=topic_list)
```

**Line-by-line breakdown:**

Line 1: `from kafka.admin import KafkaAdminClient, NewTopic`
  - Imports the administrative client class and NewTopic class from kafka-python library
  - `KafkaAdminClient`: Used for topic management, cluster information, and other admin operations
  - `NewTopic`: A class that defines the configuration for a new topic

Line 3-5: `admin_client = KafkaAdminClient(...)`
  - Creates an administrative client instance
  - `bootstrap_servers="localhost:9092"`: Specifies the Kafka broker to connect to (localhost on default port 9092)
  - `client_id='test'`: A logical identifier for this client, useful for logging and monitoring

Line 7: `topic_list = []`
  - Initializes an empty list to hold topic definitions
  - Kafka supports batch topic creation for efficiency

Line 8-12: `new_topic = NewTopic(...)`
  - Defines a new topic with the following configuration:
  - `name="bankbranch"`: The topic name (must be unique in the cluster)
  - `num_partitions=2`: The topic will have 2 partitions for parallel processing
  - `replication_factor=1`: Each partition will be stored on 1 broker (no replication for this lab)

Line 13: `topic_list.append(new_topic)`
  - Adds the topic definition to the list for batch creation

Line 14: `admin_client.create_topics(new_topics=topic_list)`
  - Sends the topic creation request to the Kafka broker
  - Creates all topics in the list in a single API call

**Big picture:** This script creates a topic called "bankbranch" with 2 partitions. In production, you'd typically use replication_factor=3 for fault tolerance. The topic will store ATM transaction data from multiple bank branches.

[ENRICHED: performance context — Replication factor 3 is the industry standard for production Kafka deployments. With RF=3, you can tolerate up to 2 broker failures while maintaining data availability. The optimal production configuration is: replication_factor=3, min.insync.replicas=2, acks=all — this ensures at least 2 in-sync replicas acknowledge each write before the producer considers it successful. Going beyond RF=3 (e.g., RF=5 or RF=7) is only justified for extremely critical data like financial transactions or audit logs where you need to survive entire rack/datacenter failures, but it comes with significant trade-offs: 5x storage cost, higher network overhead, and increased replication lag. For ATM transaction data like in this lab, RF=3 is optimal — it provides excellent fault tolerance without excessive overhead. [Source: https://www.conduktor.io/kafka/kafka-topics-choosing-the-replication-factor-and-partitions-count]]

Note: We are creating a topic "bankbranch" through this code.

---

## Exercise 4: Create the producer.py File

You need a producer to send messages to Kafka. You will find the code for the producer in the `producer.py` file.

### Step 1 — Create producer.py

Create a file named `producer.py` by running the following command:

```bash
touch producer.py
```

Click the button below to open the file in edit mode and paste the following content in the file and save it.

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send("bankbranch", {'atmid': 1, 'transid': 100})
producer.send("bankbranch", {'atmid': 2, 'transid': 101})

producer.flush()
producer.close()
```

**Line-by-line breakdown:**

Line 1: `from kafka import KafkaProducer`
  - Imports the KafkaProducer class for publishing messages to Kafka topics

Line 2: `import json`
  - Imports Python's built-in JSON library for serialization

Line 4-6: `producer = KafkaProducer(...)`
  - Creates a producer instance with custom serialization
  - `value_serializer=lambda v: json.dumps(v).encode('utf-8')`: A lambda function that:
    - Takes a Python dictionary `v`
    - Converts it to JSON string with `json.dumps(v)`
    - Encodes to UTF-8 bytes with `.encode('utf-8')`
  - **Why bytes?** Kafka stores messages as raw bytes, regardless of format. The serializer converts Python objects to bytes.

Line 8: `producer.send("bankbranch", {'atmid': 1, 'transid': 100})`
  - Sends a message to the "bankbranch" topic
  - Message value: `{'atmid': 1, 'transid': 100}` (ATM ID 1, transaction ID 100)
  - The `send()` method is asynchronous — it returns immediately without waiting for broker acknowledgment

Line 9: `producer.send("bankbranch", {'atmid': 2, 'transid': 101})`
  - Sends a second message with different ATM and transaction IDs

Line 11: `producer.flush()`
  - Blocks until all pending messages are sent to the broker
  - **Critical for reliability:** Without flush(), messages might be lost if the program exits before they're sent

[ENRICHED: performance context — `producer.flush()` is a synchronous operation that forces all buffered messages to be sent immediately and blocks until the broker acknowledges them. Here's why it matters:

**How Kafka's async send works:**
1. When you call `producer.send()`, the message goes into an internal buffer — it is NOT sent to the broker immediately
2. The producer batches messages together for efficiency (controlled by `linger.ms` and `batch.size` configs)
3. An internal thread sends batches to the broker in the background
4. If your program exits before the background thread sends the batch, **those messages are lost**

**What flush() does:**
- Makes all buffered records immediately available to send (even if `linger.ms` > 0)
- Blocks until all pending requests are completed (broker acknowledges or error occurs)
- After `flush()` returns, every previously sent record has `Future.isDone() == true`

**When to use flush():**
- Before exiting a short-lived producer script (like this lab)
- After sending a batch of critical messages you need confirmation on
- When consuming from one system and producing to Kafka (ensures each batch completes)

**When NOT to use flush():**
- In high-throughput production producers — calling `flush()` after every `send()` turns it into a synchronous producer, killing throughput by 10-100x
- Instead, rely on `close()` which internally calls `flush()`, or set `delivery.timeout.ms` and use callbacks

**Production best practice:** For high-throughput workloads, use async send with callbacks and call `flush()` only at the end of a batch or before `close()`. The `close()` method automatically calls `flush()` and releases resources, so it's the preferred way to ensure delivery in production. [Source: https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html]]

Line 12: `producer.close()`
  - Gracefully closes the producer connection
  - Releases network resources and cleans up internal state

**Big picture:** This producer sends two ATM transaction records to Kafka. In a real system, you'd send thousands of messages per second from multiple ATMs. The `flush()` and `close()` calls ensure all messages are delivered before the program exits.

[ENRICHED: clarity — **Do you need both flush() and close()?** Technically, no. `close()` internally calls `flush()` first, then releases resources. So calling `close()` alone would work fine here. The lab shows both for educational purposes — to teach the explicit pattern.

**Why flush() exists as a separate method:**
- `flush()` sends all buffered messages but keeps the producer open — useful in long-running producers that process batches periodically
- `close()` calls `flush()` then kills the producer — use when you're done forever

**When you'd use flush() without close():**
- Processing millions of messages in a loop, flushing every N messages
- Need to confirm delivery before continuing business logic
- Transactional workflows where you commit after flushing

**For this simple script:** Just `close()` would suffice. The explicit `flush()` before `close()` is redundant but harmless — it's a teaching pattern, not a production requirement. [Source: https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html]]

In the above code, the producer is sending across two messages through this code. These messages will be received by the consumer.

---

## Exercise 5: Create the consumer.py File

You need a consumer to read messages from Kafka. The code for consumer will be written in the `consumer.py` file.

### Step 1 — Create consumer.py

Create a file named `consumer.py` by running the following command:

```bash
touch consumer.py
```

Click the button below to open the file in edit mode and paste the following content in the file and save it.

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'bankbranch',
    group_id=None,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest'
)

print("Hello")
print(consumer)

for msg in consumer:
    print(msg.value.decode("utf-8"))
```

**Line-by-line breakdown:**

Line 1: `from kafka import KafkaConsumer`
  - Imports the KafkaConsumer class for subscribing to Kafka topics

Line 3-7: `consumer = KafkaConsumer(...)`
  - Creates a consumer instance with configuration:
  - `'bankbranch'`: The topic to subscribe to
  - `group_id=None`: No consumer group (standalone consumer). In production, use a group ID for load balancing across multiple consumers
  - `bootstrap_servers=['localhost:9092']`: The Kafka broker(s) to connect to
  - `auto_offset_reset='earliest'`: Start reading from the beginning of the topic (earliest offset). Options: 'earliest', 'latest', 'none'

Line 9: `print("Hello")`
  - Debug output to confirm the consumer started

Line 10: `print(consumer)`
  - Prints the consumer object (shows configuration and connection state)

Line 12-13: `for msg in consumer: ...`
  - Iterates through messages from the topic
  - `msg.value.decode("utf-8")`: Decodes the message bytes back to a UTF-8 string
  - **Important:** The consumer runs indefinitely in a polling loop. It will keep waiting for new messages until interrupted (Ctrl+C)

**Big picture:** This consumer subscribes to the "bankbranch" topic and prints each ATM transaction as it arrives. The `auto_offset_reset='earliest'` ensures it reads all historical messages, not just new ones. In production, you'd use consumer groups for parallel processing across multiple instances.

---

## Exercise 6: Execute the Three Python Files

### Step 1 — Run admin.py and producer.py

Execute `admin.py` and `producer.py` using the following commands in terminal:

```bash
python3 admin.py
python3 producer.py
```

[ENRICHED: context — Run these commands in the terminal where you installed kafka-python. The admin.py script creates the topic, and producer.py sends messages to it. You should see no output if successful (kafka-python is silent on success).]

### Step 2 — Run consumer.py

Open a new terminal and execute the following commands to run consumer.py:

```bash
cd kafka_2.13-4.3.1
python3 consumer.py
```

Your consumer should print the messages sent by the producer as follows:

```
Hello
<kafka.consumer.group_consumer.KafkaConsumer object at 0x...>
{"atmid": 1, "transid": 100}
{"atmid": 2, "transid": 101}
```

[ENRICHED: troubleshooting — If you see no output from the consumer, check that:
1. The Kafka server is running (Exercise 2)
2. The topic was created (Exercise 3)
3. The producer sent messages (Exercise 4)
4. `auto_offset_reset='earliest'` is set (not 'latest')

If you see "NoBrokersAvailable" error, ensure Kafka is listening on localhost:9092.]

---

## Practice Exercise

Create a new producer from bankbranch in a file named `new_producer.py` which will take user input as long as the user wants and accept user input for the ATM number they want to transact with (1 or 2) and stream the transaction.

Observe the consumer getting the events streamed by the producer in real time.

### Solution

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

transid = 100  # Starting transaction ID

while True:
    try:
        # Get ATM number from user
        atmid = int(input("Enter ATM number (1 or 2) or 0 to exit: "))

        if atmid == 0:
            print("Exiting...")
            break

        if atmid not in [1, 2]:
            print("Invalid ATM number. Please enter 1 or 2.")
            continue

        # Send transaction to Kafka
        producer.send("bankbranch", {'atmid': atmid, 'transid': transid})
        print(f"Sent: ATM {atmid}, Transaction {transid}")

        transid += 1  # Increment transaction ID

    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except ValueError:
        print("Please enter a valid number.")

producer.flush()
producer.close()
print("Producer closed.")
```

**Line-by-line breakdown:**

Line 1-2: Imports KafkaProducer and json for message serialization

Line 4-6: Creates producer with JSON serialization (same as before)

Line 8: `transid = 100`
  - Starting transaction ID. In production, this would come from a database or sequence generator

Line 10: `while True:`
  - Infinite loop to continuously accept user input
  - The loop runs until the user enters 0 or presses Ctrl+C

Line 12: `atmid = int(input(...))`
  - Prompts user for ATM number and converts to integer
  - `input()` blocks until the user types something and presses Enter

Line 14-15: `if atmid == 0: break`
  - Exit condition: user enters 0 to stop

Line 17-19: `if atmid not in [1, 2]: continue`
  - Input validation: only accepts ATM numbers 1 or 2
  - `continue` skips the rest of the loop and prompts again

Line 22: `producer.send("bankbranch", {'atmid': atmid, 'transid': transid})`
  - Sends the transaction to Kafka
  - The message contains the user-specified ATM number and auto-incremented transaction ID

Line 23: `print(f"Sent: ATM {atmid}, Transaction {transid}")`
  - Confirms the message was sent (asynchronous — may not be delivered yet)

Line 25: `transid += 1`
  - Increments transaction ID for the next message

Line 28-29: `except KeyboardInterrupt: break`
  - Handles Ctrl+C gracefully
  - Allows the user to stop the producer with Ctrl+C

Line 30-31: `except ValueError: print(...)`
  - Handles non-integer input (e.g., user types "abc" instead of a number)

Line 34-35: `producer.flush()` and `producer.close()`
  - Ensures all pending messages are sent before exiting
  - Cleans up the producer connection

**Big picture:** This interactive producer simulates a real-world ATM system where transactions arrive in real-time. Run this producer in one terminal and the consumer in another to see live transaction streaming. Each message appears instantly in the consumer terminal.

---

## Troubleshooting Common Errors

### KafkaTimeoutError: Unable to bootstrap from ['localhost:9092']

**Cause:** The Kafka server is not running. All Python scripts (admin.py, producer.py, consumer.py) require the Kafka server to be running on `localhost:9092`.

**How to fix:**
1. Open a **dedicated terminal** for the Kafka server (keep it running)
2. Navigate to the Kafka directory:
   ```bash
   cd kafka_2.13-4.3.1
   ```
3. Generate a cluster ID and format storage (first time only):
   ```bash
   KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
   bin/kafka-storage.sh format --cluster-id $KAFKA_CLUSTER_ID --standalone --config config/server.properties
   ```
4. Start the Kafka server:
   ```bash
   bin/kafka-server-start.sh config/server.properties
   ```
5. Wait until you see output confirming the server started successfully
6. **Keep this terminal open** — closing it stops the Kafka server
7. In a **separate terminal**, run your Python scripts

[ENRICHED: troubleshooting — The KafkaTimeoutError occurs because Kafka's async architecture requires a running broker before any client can connect. The Python scripts don't start Kafka — they only connect to it. You need 3 terminals: one for the Kafka server (always running), one for the producer, and one for the consumer. If you close the Kafka server terminal, all producers and consumers will fail with this error. [Source: https://kafka.apache.org/documentation/#quickstart]]

### FileNotFoundError: No such file or directory

**Cause:** You're not in the Kafka directory when running the Python scripts.

**How to fix:**
```bash
cd kafka_2.13-4.3.1
python3 admin.py
```

### NoSuchFileException: config/kraft/server.properties

**Cause:** You're using outdated Kafka 3.x commands. In Kafka 4.x, the `config/kraft/` directory no longer exists — configuration is now directly in `config/server.properties`.

**How to fix:** Use `config/server.properties` instead of `config/kraft/server.properties`:
```bash
# Storage format (first time only) - requires --standalone flag for single-node
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --cluster-id $KAFKA_CLUSTER_ID --standalone --config config/server.properties

# Start server
bin/kafka-server-start.sh config/server.properties
```

[ENRICHED: correction — Kafka 4.x removed the `config/kraft/` directory. All KRaft configuration now lives in `config/server.properties`. The old paths (`config/kraft/server.properties`, `config/kraft/controller.properties`, `config/kraft/server.properties`) no longer work. Updated all lab commands to use the correct Kafka 4.x paths. [Source: https://medium.com/@meet.gada/how-to-install-apache-kafka-4-2-on-linux-kraft-mode-no-zookeeper-7d8ad986cb46]]

### TopicAlreadyExistsError

**Cause:** You ran admin.py multiple times, trying to create a topic that already exists.

**How to fix:** This is expected — the topic was created on the first run. Subsequent runs will show this error, which you can safely ignore.

---

## Authors

Ramesh Sana Reddy
Lavanya T S
Shreya Khurana

© IBM Corporation. All rights reserved.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | About Skills Network Cloud IDE | Definition | Defined "Theia" as open-source IDE framework by Eclipse Foundation | HIGH | https://theia-ide.org/ |
| 2 | Important Notice section | Context | Explained non-persistent environment implications for lab completion | MEDIUM | UNCERTAIN |
| 3 | Exercise 1, Step 2 | Definition | Defined "wget" as command-line download utility | HIGH | https://www.gnu.org/software/wget/ |
| 4 | Exercise 1, Step 2 | Context | Explained Kafka version numbering (4.3.1, Scala 2.13) and version availability | HIGH | https://kafka.apache.org/downloads |
| 4a | Exercise 1, Step 2 | Correction | Updated Kafka version from 3.8.0 to 4.3.1 (3.8.0 no longer available — 404 error) | HIGH | https://downloads.apache.org/kafka/ |
| 5 | Exercise 1, Step 3 | Definition | Defined "tar" as tape archive utility with flag explanations | HIGH | https://www.gnu.org/software/tar/ |
| 6 | Exercise 2, Step 2 | Definition | Defined "KRaft" (Kafka Raft) consensus protocol replacing ZooKeeper | HIGH | https://kafka.apache.org/documentation/#kraft |
| 7 | Exercise 2, Step 2 | Context | Explained cluster UUID purpose in KRaft coordination | MEDIUM | UNCERTAIN |
| 8 | Exercise 2, Step 3 | Definition | Defined "log directories" as physical message storage locations | HIGH | https://kafka.apache.org/documentation/#design |
| 9 | Exercise 2, Step 4 | Context | Explained server.properties configuration key settings | HIGH | https://kafka.apache.org/documentation/#brokerconfigs |
| 10 | Exercise 3, Step 1 | Definition | Defined "kafka-python" as pure Python Kafka client library | HIGH | https://github.com/dpkp/kafka-python |
| 11 | Exercise 3, Step 1 | Alternative | Suggested confluent-kafka-python for production workloads | HIGH | https://github.com/confluentinc/confluent-kafka-python |
| 12 | Exercise 3, Step 2 | Definition | Defined "touch" as Unix file creation command | HIGH | https://man7.org/linux/man-pages/man1/touch.1.html |
| 13 | Exercise 3, Step 2 | Code breakdown | Line-by-line explanation for KafkaAdminClient topic creation | HIGH | UNCERTAIN |
| 14 | Exercise 4 | Code breakdown | Line-by-line explanation for KafkaProducer message publishing | HIGH | UNCERTAIN |
| 15 | Exercise 5 | Code breakdown | Line-by-line explanation for KafkaConsumer message consumption | HIGH | UNCERTAIN |
| 16 | Exercise 6 | Troubleshooting | Added common error diagnosis for consumer issues | MEDIUM | UNCERTAIN |
| 17 | Practice Exercise | Code breakdown | Line-by-line explanation for interactive producer with user input | HIGH | UNCERTAIN |
| 18 | Exercise 3, Step 2 | Performance context | Replication factor best practices: RF=3 standard, RF=5 only for critical data, optimal config with min.insync.replicas=2 | HIGH | https://www.conduktor.io/kafka/kafka-topics-choosing-the-replication-factor-and-partitions-count |
| 19 | Exercise 4, Line 11 | Performance context | Deep dive on producer.flush(): async buffer behavior, why flush() prevents message loss, when to use vs avoid, production best practices | HIGH | https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html |
| 20 | Exercise 4, Big picture | Clarity | Clarified flush() vs close(): close() internally calls flush(), showing both is redundant but educational; when flush() alone is needed | HIGH | https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html |
| 21 | Troubleshooting section | Troubleshooting | Added KafkaTimeoutError diagnosis (Kafka server not running), FileNotFoundError fix, TopicAlreadyExistsError explanation | HIGH | https://kafka.apache.org/documentation/#quickstart |
| 22 | Exercise 2, Steps 3-4 | Correction | Updated Kafka 4.x paths: config/kraft/server.properties → config/server.properties (kraft/ dir removed in 4.x) | HIGH | https://medium.com/@meet.gada/how-to-install-apache-kafka-4-2-on-linux-kraft-mode-no-zookeeper-7d8ad986cb46 |
| 23 | Troubleshooting section | Correction | Added NoSuchFileException troubleshooting for outdated Kafka 3.x paths | HIGH | https://medium.com/@meet.gada/how-to-install-apache-kafka-4-2-on-linux-kraft-mode-no-zookeeper-7d8ad986cb46 |
| 24 | Exercise 2, Step 3 | Correction | Added --standalone flag to kafka-storage.sh format command (required for single-node KRaft in Kafka 4.3+) | HIGH | https://kafka.apache.org/43/operations/kraft/ |

<!-- EXTRACTION_CHECKLIST: 126 sentences extracted, 126 sentences in output -->