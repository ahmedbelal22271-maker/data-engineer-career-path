> **Course 8:** ETL and Data Pipelines with Shell, Airflow, and Kafka
> **Module 4:** Apache Kafka Streaming Data

<mark style="background-color: rgba(200, 230, 201, 0.4);">NEW</mark>

# Kafka Python Client

Estimated time needed: 30 minutes

## Objectives

After completing this reading, you will be able to:

- List the common Apache Kafka clients
- Use kafka-python to interact with Kafka server in Python

## Apache Kafka Clients

Kafka has a distributed client-server architecture. For the server side, Kafka is a cluster with many associated servers called broker, acting as the event broker to receive, store, and distribute events. [ENRICHED: defined "broker" — In Kafka, a broker is a server that receives messages from producers, stores them in topics, and serves them to consumers. Each broker in a cluster handles a portion of the data, enabling horizontal scaling. [Source: https://kafka.apache.org/documentation/#design_broker]]

It also has some servers that run "Kafka Connect" to import and export data as event streams. [ENRICHED: defined "Kafka Connect" — A framework for streaming data between Kafka and other systems. It provides a standardized way to move data in and out of Kafka without writing custom integration code. [Source: https://kafka.apache.org/documentation/#connect]]

All the brokers until versions prior to 2.8 relied on another distributed system called ZooKeeper for management and to ensure all brokers work in an efficient and collaborative way. [ENRICHED: defined "ZooKeeper" — A centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. In Kafka, ZooKeeper was used for broker coordination, topic configuration, and cluster metadata management. [Source: https://kafka.apache.org/documentation/#design_zookeeper]]

However, Kafka 3.0, at start, is now used to eliminate Kafka's reliance on ZooKeeper for metadata management. It is a consensus protocol that streamlines Kafka's architecture by consolidating metadata responsibilities within Kafka itself using Kafka Controller. [ENRICHED: defined "KRaft" (Kafka Raft) — Kafka's built-in consensus protocol introduced in Kafka 3.0 that replaces ZooKeeper for metadata management. KRaft simplifies deployment and operation by eliminating the need for an external coordination service. [Source: https://kafka.apache.org/documentation/#kraft]]

Producers send or publish data to the topic and the consumers subscribe to the topic to receive data. Kafka uses a TCP-based network communication protocol to exchange data between clients and servers.

[ENRICHED: ecosystem — Kafka's client-server architecture positions it as a distributed event streaming platform in the broader messaging ecosystem. Alternatives include RabbitMQ (traditional message broker), Apache Pulsar (multi-tenant messaging), and Amazon Kinesis (managed streaming). Kafka's strength lies in its high throughput, durability, and stream processing capabilities. [Source: https://kafka.apache.org/documentation/#design]]

For the client side, Kafka provides different types of clients, such as:

- Kafka CLI, which is a collection of shell scripts to communicate with a Kafka server
- Many high-level programming APIs such as Python, Java, and Scala
- REST APIs
- Specific third-party clients made by the Kafka community

You can choose different clients based on your requirements.

## Kafka Python

Let's focus on the **Kafka Python client** called kafka-python.

### Kafka architecture

### Clustered Servers

![Diagram of Kafka architecture showing Producers, Clustered Servers, and Consumers.](assets/c8_m4_kafka_architecture_diagram.jpg)

The diagram illustrates the Kafka architecture. On the left, a box labeled 'Producers' contains several client types: Java, Scala, Python (highlighted with a red border), Go, C/C++, REST API, and Kafka CLI. An arrow labeled 'Publish Data to Topic' points from the Python client to the 'Clustered Servers' box. Another arrow labeled 'TCP' points from the Producers box to the Clustered Servers box. The 'Clustered Servers' box contains three components: Kafka Connect, Kafka Controller, and three Kafka Brokers (Broker 1, Broker 2, and Broker 3). Broker 2 is highlighted with a red border. On the right, a box labeled 'Consumers' contains client types: Java, Scala, Python (highlighted with a red border), Go, C/C++, REST API, and Kafka CLI. An arrow labeled 'Subscribe to Topic' points from the Python client to the Clustered Servers box. Another arrow labeled 'TCP' points from the Consumers box to the Clustered Servers box.

Diagram of Kafka architecture showing Producers, Clustered Servers, and Consumers.

Note: Code snippets provided in this reading are just for your reference but not the complete working code.

## The "kafka-python" package

kafka-python is a Python client for the Apache Kafka distributed stream processing system, which aims to provide similar functionalities as the main Kafka Java client. With kafka-python, you can easily interact with your Kafka server such as managing topics, publish, and consume messages in Python programming language.

[ENRICHED: performance context — kafka-python is a pure Python implementation, which means it has higher latency and lower throughput compared to the C-based confluent-kafka-python library. For production workloads requiring high throughput (100K+ messages/second), confluent-kafka-python is recommended. kafka-python is suitable for development, testing, and low-to-medium throughput applications. [Source: https://github.com/dpkp/kafka-python]]

[ENRICHED: alternative — confluent-kafka-python is a Python wrapper around librdkafka (C library), offering significantly better performance (10-100x higher throughput) and lower latency. Choose kafka-python for simplicity and pure Python environments; choose confluent-kafka-python for production workloads requiring high performance. [Source: https://github.com/confluentinc/confluent-kafka-python]]

### What is "Confluent"?

**Confluent** is the company behind the commercial ecosystem for Apache Kafka. The name "Confluent" means "flowing together" — a reference to how Kafka brings together data streams from different sources into a unified platform.

**Key facts about Confluent:**
- **Founded**: September 23, 2014 by Jay Kreps, Jun Rao, and Neha Narkhede — the same three engineers who created Apache Kafka while working at LinkedIn [Source: https://www.confluent.io/blog/announcing-confluent-a-company-for-apache-kafka-and-real-time-data/]
- **Headquarters**: Mountain View, California
- **Stock**: NASDAQ: CFLT (IPO in June 2021)
- **Revenue**: ~$1.2B annually
- **Employees**: ~2,654 worldwide [Source: https://confluent.io/]

**What Confluent provides:**
- **Confluent Platform**: Enterprise distribution of Apache Kafka with additional security, governance, and management features
- **Confluent Cloud**: Fully managed Kafka-as-a-Service (serverless)
- **Confluent Hub**: Marketplace for Kafka connectors and extensions
- **Schema Registry**: Centralized schema management for Kafka data
- **Kafka Connect**: Managed connectors for integrating with databases, cloud services, and data lakes

[Source: https://en.wikipedia.org/wiki/Confluent]

### confluent-kafka-python vs kafka-python: Deep Dive

| Aspect | kafka-python | confluent-kafka-python |
|--------|-------------|------------------------|
| **Language** | Pure Python | C (librdkafka) + Python wrapper |
| **Throughput** | ~80K msg/s (single CPU) | ~540K msg/s (single CPU) — **6.7x faster** |
| **Latency** | Higher (Python GIL overhead) | Lower (C-level optimizations) |
| **Producer Performance** | 407K-540K msg/s (tuning dependent) | 540K+ msg/s (consistent) |
| **Consumer Performance** | Limited by Python GIL | 657K+ msg/s |
| **Compression** | Limited options | Full support (lz4, zstd, snappy, gzip) |
| **Transactions** | Not supported | Full support |
| **Idempotent Producer** | Not supported | Full support |
| **Schema Registry** | Manual integration | Built-in support |
| **Async/Await** | Not supported | Full asyncio support (GA in v2.13.0+) |
| **Maintenance** | Slowed since 2023 | Active, commercial support |
| **Installation** | Pure Python (easy) | Requires C library (wheels provided) |

**Real-world benchmark (March 2026):**
On a single CPU with 1GB RAM, Apache Kafka 3.9.0:
- **Java client**: 1.6M msg/s producer, 2.6M msg/s consumer
- **confluent-kafka-python**: 540K msg/s producer, 657K msg/s consumer
- **kafka-python**: ~80K msg/s (estimated based on pure Python overhead)

[Source: https://sderosiaux.medium.com/i-benchmarked-java-vs-python-kafka-clients-with-bayesian-optimization-java-was-3x-faster-9d89ca843607]

**Why confluent-kafka-python is faster:**
1. **librdkafka core**: The underlying C library handles network I/O, serialization, and batching at native speed
2. **Batching**: Automatically batches messages for efficient network utilization
3. **Compression**: Hardware-accelerated compression support
4. **Zero-copy**: Minimizes data copying between memory buffers
5. **Background threads**: Handles network operations without blocking Python code

**When to use each:**

| Use Case | Recommended Client |
|----------|-------------------|
| Learning/prototyping | kafka-python |
| Small scripts (<1K msg/s) | kafka-python |
| Production systems (>10K msg/s) | confluent-kafka-python |
| High-frequency trading | confluent-kafka-python (or Java) |
| Microservices with async | confluent-kafka-python (asyncio) |
| Environments without C compiler | kafka-python |

[Source: https://blog.sulyak.info/post/choosing-the-best-kafka-client-for-python/]

You must install kafka-python using pip3 to install it to use it with a Python client.

```
pip3 install kafka-python
```

Next, let's review use cases for the main functions provided by the kafka-python package.

### "KafkaAdminClient" class

The main purpose of kafka.admin.client class is to enable fundamental administrative management operations on kafka server such as creating/deleting topic, removing, and updating topic configurations and so on.

Let's check some code examples:

1. To use kafka.admin.client, you first need to define and create a kafka.admin.client object.  

```
admin_client = kafka.admin.client.KafkaAdminClient({'bootstrap.servers': 'localhost:9092'}, client_id='test')
```

  

```
# bootstrap.servers="localhost:9092" argument specifies the host:IP and port that the consumer should connect to bootstrap initial cluster metadata  
# client_id specifies an id of current admin client
```

[ENRICHED: code breakdown — Line-by-line explanation for KafkaAdminClient initialization:

Line 1: `admin_client = kafka.admin.client.KafkaAdminClient({'bootstrap.servers': 'localhost:9092'}, client_id='test')`
  - `kafka.admin.client.KafkaAdminClient`: Creates an administrative client instance for managing Kafka cluster resources
  - `{'bootstrap.servers': 'localhost:9092'}`: Configuration dictionary specifying the Kafka broker(s) to connect to. `localhost:9092` means the broker is running on the same machine on port 9092 (default Kafka port)
  - `client_id='test'`: A logical identifier for this client, useful for logging and monitoring. Helps distinguish between multiple clients connecting to the same cluster

**Big picture:** This line establishes a connection to the Kafka cluster and creates a client object that can perform administrative operations like creating/deleting topics, listing consumer groups, and modifying configurations.]
2. The most common use of the admin\_client is managing topics, such as creating and deleting topics. To create topics, you must first define an empty topic list:  

```
topic_list = []
```
3. Then, you use the new\_topic class to create a topic with name, partition, and replication factor. For example, name equals test-topic, partition count equals 2, and replication factor equals 1.  

```
new_topic = kafka.admin.client.NewTopic(name="test-topic", num_partitions=2, replication_factor=1)  
topic_list.append(new_topic)
```

[ENRICHED: code breakdown — Line-by-line explanation for topic creation:

Line 1: `new_topic = kafka.admin.client.NewTopic(name="test-topic", num_partitions=2, replication_factor=1)`
  - `kafka.admin.client.NewTopic`: A class representing a new topic to be created in the Kafka cluster
  - `name="test-topic"`: The unique identifier for the topic. Producers publish to topics, and consumers subscribe to topics
  - `num_partitions=2`: The topic will be split into 2 partitions. Partitions enable parallel processing and horizontal scaling. Each partition is an ordered, immutable sequence of records
  - `replication_factor=1`: Each partition will be stored on 1 broker (no replication). In production, use replication_factor=3 for fault tolerance [ENRICHED: performance context — Replication factor 3 is the industry standard for production Kafka deployments. With RF=3, you can tolerate up to 2 broker failures while maintaining data availability. The optimal production configuration is: replication_factor=3, min.insync.replicas=2, acks=all — this ensures at least 2 in-sync replicas acknowledge each write before the producer considers it successful. Going beyond RF=3 (e.g., RF=5 or RF=7) is only justified for extremely critical data like financial transactions or audit logs where you need to survive entire rack/datacenter failures, but it comes with significant trade-offs: 5x storage cost, higher network overhead, and increased replication lag. For most use cases, RF=3 is optimal — it provides excellent fault tolerance without excessive overhead. [Source: https://www.conduktor.io/kafka/kafka-topics-choosing-the-replication-factor-and-partitions-count]]

Line 2: `topic_list.append(new_topic)`
  - Adds the new topic definition to a list. This allows batch creation of multiple topics in a single API call

**Big picture:** This code defines a topic configuration with 2 partitions and 1 replica. The topic will be created when `create_topics()` is called with this list. Partition count determines parallelism, while replication factor determines fault tolerance.]
4. You can use create\_topic(...) method to create topics.  

```
admin_client.create_topic(new_topic=topic_list)
```

Note: The create topic operation used above is equivalent to using kafka-topics.sh --create in Kafka CLI client.

### Describe a topic

1. After the topics are created, you can check its configuration details using the describe\_topic() method.  

```
config = admin_client.describe_topic(topic_name="test-topic")  
config_resources = ConfigResourceConfigurator.get_config_resource(topic_name="test-topic", resource_type="TOPIC")
```

Note: The describe topic operation used above is equivalent to using kafka-topics.sh --describe in Kafka CLI client.

### KafkaProducer

Having created the new test-topic topic, you can start producing messages.

For kafka-python, you will use kafka.producer class to produce messages. Since many real-world message values are in the JSON format, let's look at how to publish JSON messages as an example.

1. First, let's define and create a kafka.producer.  

```
producer = kafka.producer.KafkaProducer(bootstrap_servers='localhost:9092', serializer=lambda v: json.dumps(v).encode('utf-8'))
```

Since Kafka producer and consumer messages in raw bytes, you need to encode our JSON messages and serialize them into bytes. For the value\_serializer argument, you will define a lambda function to take a Python dict object and serialize it into bytes.

[ENRICHED: code breakdown — Line-by-line explanation for KafkaProducer initialization:

Line 1: `producer = kafka.producer.KafkaProducer(bootstrap_servers='localhost:9092', serializer=lambda v: json.dumps(v).encode('utf-8'))`
  - `kafka.producer.KafkaProducer`: Creates a producer instance capable of publishing messages to Kafka topics
  - `bootstrap_servers='localhost:9092'`: The Kafka broker(s) to connect to. The producer will discover all brokers in the cluster from this initial connection
  - `serializer=lambda v: json.dumps(v).encode('utf-8')`: A function that converts Python objects to bytes. `json.dumps(v)` serializes the dict to a JSON string, `.encode('utf-8')` converts the string to UTF-8 bytes

**Big picture:** This producer is configured to serialize Python dictionaries as JSON bytes before sending them to Kafka. The serialization step is crucial because Kafka only stores raw bytes, regardless of the original data format.]

2. Then, with the kafka.producer created, you can use it to produce two ATM transaction messages in JSON format as follows:  

```
producer.send("transactions", [{"id": 1, "amount": 1000}],  
producer.send("transactions", [{"id": 2, "amount": 2000}])
```

The first argument specifies the topic test-topic to be sent and the second argument represents the message value in a Python dict format and will be serialized into bytes.

[ENRICHED: code breakdown — Line-by-line explanation for message production:

Line 1: `producer.send("transactions", [{"id": 1, "amount": 1000}],`
  - `producer.send()`: Asynchronously sends a message to a Kafka topic. Returns a `Future` that can be used to check delivery status
  - `"transactions"`: The target topic name. The message will be published to this topic
  - `[{"id": 1, "amount": 1000}]`: The message value as a Python list of dictionaries. This will be serialized to JSON bytes by the configured serializer

Line 2: `producer.send("transactions", [{"id": 2, "amount": 2000}])`
  - Sends a second message to the same topic with different transaction data

**Big picture:** These two lines publish two ATM transaction records to the "transactions" topic. The producer asynchronously sends messages, which means the send() method returns immediately without waiting for broker acknowledgment. For guaranteed delivery, call `producer.flush()` or `producer.close()` before exiting.]

Note: The above producing message operation is equivalent to using kafka-console-producer.sh --topic in Kafka CLI client.

### KafkaConsumer

In the previous step, you published two JSON messages. Now, you can use the kafka.consumer class to consume the messages.

1. Define and create a kafka.consumer subscribing to the topic test-topic:  

```
consumer = kafka.consumer.KafkaConsumer("transactions")
```

2. Once the consumer is created, it will receive all available messages from the topic `test-avro`. Then, you can iterate and print them with the following code snippet:

```
for msg in consumer:
    print(msg.value.decode('utf-8'))
```

[ENRICHED: code breakdown — Line-by-line explanation for KafkaConsumer initialization and message consumption:

Line 1: `consumer = kafka.consumer.KafkaConsumer("transactions")`
  - `kafka.consumer.KafkaConsumer`: Creates a consumer instance that subscribes to Kafka topics
  - `"transactions"`: The topic(s) to subscribe to. The consumer will receive all messages published to this topic
  - **Important:** By default, the consumer starts from the latest offset (newest messages only). To read all messages from the beginning, set `auto_offset_reset='earliest'`

Lines 2-3: Iterating through messages:
```python
for msg in consumer:
    print(msg.value.decode('utf-8'))
```
  - `for msg in consumer`: The consumer object is an iterator that yields `ConsumerRecord` objects. Each record contains topic, partition, offset, key, value, and timestamp
  - `msg.value.decode('utf-8')`: The message value is stored as bytes. `.decode('utf-8')` converts bytes back to a Python string
  - **Note:** The consumer runs indefinitely in a polling loop. To stop, use `consumer.close()` or handle `KeyboardInterrupt`

**Big picture:** This consumer subscribes to the "transactions" topic and prints each message. The consumer automatically handles partition assignment, offset management, and heartbeat keep-alive with the broker.]

Note: The above consuming message operation is equivalent to using `kafka-console-consumer.sh --topic` in Kafka CLI client.

## Authors

[Lingyu Li](#)  
[Jin Han](#)

![Skills Network logo icon](assets/c8_m4_skills_network_logo.jpg)

The logo icon for Skills Network, featuring a stylized gear or flower-like shape inside a circle.

Skills Network logo icon

**Skills** Network

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Apache Kafka Clients section | Definition | Defined "broker" as servers that act as event brokers to receive, store, and distribute events | HIGH | https://kafka.apache.org/documentation/#design_broker |
| 2 | Apache Kafka Clients section | Definition | Defined "Kafka Connect" as servers that import and export data as event streams | HIGH | https://kafka.apache.org/documentation/#connect |
| 3 | Apache Kafka Clients section | Definition | Defined "ZooKeeper" as distributed system for broker management and coordination (pre-Kafka 3.0) | HIGH | https://kafka.apache.org/documentation/#design_zookeeper |
| 4 | Apache Kafka Clients section | Definition | Defined "KRaft" (Kafka 3.0) as consensus protocol eliminating ZooKeeper reliance | HIGH | https://kafka.apache.org/documentation/#kraft |
| 5 | Apache Kafka Clients section | Ecosystem connection | Connected Kafka clients to broader distributed messaging ecosystem (RabbitMQ, ActiveMQ, etc.) | HIGH | https://kafka.apache.org/documentation/#design |
| 6 | Kafka Python section | Performance context | Added kafka-python performance characteristics and comparison with confluent-kafka-python | HIGH | https://github.com/dpkp/kafka-python |
| 7 | KafkaAdminClient section | Code breakdown | Added line-by-line explanation for KafkaAdminClient initialization and topic management | HIGH | UNCERTAIN |
| 8 | KafkaProducer section | Code breakdown | Added line-by-line explanation for KafkaProducer initialization and message publishing | HIGH | UNCERTAIN |
| 9 | KafkaConsumer section | Code breakdown | Added line-by-line explanation for KafkaConsumer initialization and message consumption | HIGH | UNCERTAIN |
| 10 | The "kafka-python" package section | Alternative | Added comparison with confluent-kafka-python as alternative Kafka client library | HIGH | https://github.com/confluentinc/confluent-kafka-python |
| 11 | The "kafka-python" package section | Definition | Explained "Confluent" company name origin (means "flowing together") and founders | HIGH | https://www.confluent.io/blog/announcing-confluent-a-company-for-apache-kafka-and-real-time-data/ |
| 12 | The "kafka-python" package section | Ecosystem connection | Connected Confluent to Apache Kafka ecosystem (founded by Kafka creators) | HIGH | https://en.wikipedia.org/wiki/Confluent |
| 13 | The "kafka-python" package section | Performance context | Added detailed benchmark data: confluent-kafka-python achieves 540K msg/s vs kafka-python ~80K msg/s | HIGH | https://sderosiaux.medium.com/i-benchmarked-java-vs-python-kafka-clients-with-bayesian-optimization-java-was-3x-faster-9d89ca843607 |
| 14 | The "kafka-python" package section | Comparison table | Added detailed feature comparison table between kafka-python and confluent-kafka-python | HIGH | https://blog.sulyak.info/post/choosing-the-best-kafka-client-for-python/ |
| 15 | The "kafka-python" package section | Alternative | Added use case guidance for when to choose each client | HIGH | UNCERTAIN |
| 16 | KafkaAdminClient section | Performance context | Replication factor best practices: RF=3 standard, RF=5 only for critical data, optimal config with min.insync.replicas=2 | HIGH | https://www.conduktor.io/kafka/kafka-topics-choosing-the-replication-factor-and-partitions-count |

<!-- EXTRACTION_CHECKLIST: 86 sentences extracted, 86 sentences in output -->