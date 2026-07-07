# Big Data Processing Tools: Hadoop, HDFS, Hive, and Spark

> **LTHP Status:** NEW — Module 2 ecosystem expansion.
> **Source file:** `big-data-tools-hadoop-spark.md` (primary, 225 lines)

## Introduction

Big Data processing technologies provide ways to work with large sets of structured, semi-structured, and unstructured data so that value can be derived from them. This page covers three core open-source technologies in the Big Data ecosystem:

| Tool | Role in One Line |
|---|---|
| **Apache Hadoop** | Collection of tools for distributed storage and processing of big data |
| **Apache HDFS** | The storage layer of Hadoop — partitions and replicates files across a cluster |
| **Apache Hive** | Data warehouse built on Hadoop, enabling SQL-based querying of big data |
| **Apache Spark** | Distributed analytics engine for real-time and complex data processing |

---

## Apache Hadoop

### What It Is

**Hadoop** is a Java-based, open-source framework that allows distributed storage and processing of large datasets across clusters of computers.

Key terminology: a **node** is a single computer in the cluster; a **cluster** is a collection of nodes working together. Hadoop can scale from a single node to any number of nodes, each contributing local storage and computation.

### Core Characteristics

- **Reliable** — built-in fault tolerance and data replication
- **Scalable** — grows horizontally by adding nodes, not by upgrading single machines
- **Cost-effective** — runs on commodity hardware; no format requirements for stored data

### What You Can Do with Hadoop

| Capability | Description |
|---|---|
| **Incorporate emerging formats** | Streaming audio, video, social media sentiment, clickstream data — formats not traditionally supported in data warehouses |
| **Self-service access** | Provides real-time, self-service data access for all stakeholders |
| **Cost optimization** | Consolidate enterprise data and move cold data (infrequently accessed) off expensive warehouse systems onto Hadoop |

> **Cold data** = data that is not in frequent use. Moving it to Hadoop reduces costs without sacrificing availability.

---

## HDFS — Hadoop Distributed File System

### What It Is

**HDFS** is the storage system for big data that runs on multiple pieces of commodity hardware connected through a network. It solves the problem of storing files too large for any single machine by splitting them into blocks and distributing those blocks across the cluster.

### How HDFS Stores Data

A large file (e.g., a US phonebook) is split into blocks — names A–H on Server 1, I–Q on Server 2, R–Z on Server 3. To reconstruct the full file, a program assembles the blocks from every server. HDFS also replicates each block onto two additional servers by default, so if one server fails, the data is still available.

### Key HDFS Concepts

| Concept | Description |
|---|---|
| **Block splitting** | Large files are partitioned into blocks distributed across multiple nodes, enabling parallel access |
| **Parallel computation** | Because data lives on each node, computation runs locally on that node — no data transfer needed |
| **Replication** | Each block is replicated across additional nodes (default: 2 replicas) to prevent data loss |
| **Data locality** | Moving computation to the node where data resides, rather than moving data to computation — minimizes network congestion |

### HDFS Benefits

Fast hardware failure recovery with built-in fault detection, streaming data access supporting high throughput rates, massive scale to hundreds of nodes in a single cluster, portability across hardware platforms and operating systems, and fault tolerance through replication.

---

## Apache Hive

### What It Is

**Hive** is an open-source data warehouse software for reading, writing, and managing large dataset files stored in HDFS or other storage systems such as Apache HBase. Hive enables data warehouse-style analytics on top of Hadoop by providing SQL-like access to big data (HiveQL) — making it accessible to analysts and engineers who already know SQL.

### How Hive Works

A user submits a SQL query to Hive, which translates it into MapReduce jobs that run against HDFS/HBase data storage, then returns the results.

### Strengths

- SQL interface — easy access to big data without writing low-level MapReduce code
- ETL, reporting, and data analysis — well-suited for batch-oriented warehousing tasks
- Reads from HDFS and HBase — works natively within the Hadoop ecosystem

### Limitations

| Limitation | Reason |
|---|---|
| **High query latency** | Hadoop is designed for long sequential scans; not suitable for fast response times |
| **Not suitable for OLTP** | Hive is read-based and performs poorly with high-write transaction processing |

> **When to use Hive:** Batch analytics, ETL pipelines, reporting over historical data — not for real-time or transactional workloads.

---

## Apache Spark

### What It Is

**Spark** is a general-purpose distributed data processing engine designed to extract and process large volumes of data for a wide range of applications — from interactive analytics to machine learning.

### What Sets Spark Apart: In-Memory Processing

Traditional Hadoop MapReduce reads data from disk, processes it, writes it back to disk, and repeats. Spark keeps data in memory between processing steps, eliminating the repeated disk read/write cycles. This makes Spark dramatically faster for iterative workloads like machine learning.

### Use Cases

| Use Case | Description |
|---|---|
| **Interactive Analytics** | Fast, ad hoc queries over large datasets with near-real-time response |
| **Stream Processing** | Processing continuous data streams in real time |
| **Machine Learning** | Iterative algorithms that benefit from in-memory data persistence |
| **Data Integration** | Combining and reconciling data from heterogeneous sources |
| **ETL** | Transforming and loading large volumes of data at speed |

Spark provides interfaces for all major data programming languages: Java, Scala, Python, R, and SQL. It can run on its own standalone clustering technology, on top of Hadoop using HDFS for storage, or access data from HDFS, Hive, and a wide variety of other data sources.

---

## Hadoop vs. Hive vs. Spark — At a Glance

| Dimension | Hadoop | HDFS | Hive | Spark |
|---|---|---|---|---|
| **Primary role** | Distributed processing framework | Distributed file storage | SQL data warehouse on Hadoop | In-memory analytics engine |
| **Processing model** | Batch (MapReduce) | Storage only | Batch (via MapReduce) | Batch + real-time streaming |
| **Query interface** | Java/MapReduce | N/A | SQL (HiveQL) | Java, Scala, Python, R, SQL |
| **Latency** | High | N/A | High | Low (in-memory) |
| **Write support** | Yes | Yes | Limited (read-based) | Yes |
| **Best for** | Large-scale batch processing | Storing big data reliably | Warehousing, ETL, reporting | Real-time analytics, ML, ETL |
| **Runs on top of** | Commodity hardware | Commodity hardware | Hadoop / HDFS | Hadoop, HDFS, standalone |

---

## UCSD Big Data Specialization — Hadoop Ecosystem Content

> **Source:** UCSD Course 1, Module 6 — Systems: Getting Started with Hadoop

### The 4 W's and an H of Hadoop

The UCSD specialization frames Hadoop around five questions:
- **What's** in the ecosystem? — HDFS, YARN, MapReduce, Hive, Pig, HBase, ZooKeeper, and more
- **Why** is it beneficial? — scalability on commodity hardware, fault tolerance, variety of data types
- **Where** is it used? — web analytics, log processing, recommendation systems, scientific computing
- **Who** uses it? — Yahoo (created it in 2005), Facebook, LinkedIn, eBay, Netflix, and thousands of enterprises
- **How** do these tools work? — distributed storage + distributed processing + coordination services

### ZooKeeper vs YARN (UCSD Q&A)

A common source of confusion in the Hadoop ecosystem:

| Aspect | YARN | ZooKeeper |
|--------|------|-----------|
| **Role** | Resource management and job scheduling | Distributed coordination service |
| **What it does** | Allocates CPU/memory containers to run jobs | Provides leader election, distributed locks, configuration |
| **Who uses it** | MapReduce, Spark, Giraph submit resource requests | HBase, Kafka (pre-KRaft), Hadoop HA Namenode |
| **Key abstraction** | Container (slice of node resources) | znode (hierarchical key-value node) |
| **Failure handling** | Restarts failed tasks in new containers | Leader election replaces failed coordinator |

**Short version:** YARN decides who gets compute resources to run a job; ZooKeeper helps distributed services coordinate state and agree on leadership.

### MapReduce — The Pasta Sauce Analogy

UCSD uses a cooking analogy to explain MapReduce: you are cooking pasta for colleagues with four friends (compute nodes). Raw vegetables = input data. Each friend chops a random mix of vegetables, measures weight per type, and generates `<key, value>` pairs (MAP phase — e.g., `<tomatoes, 5 lbs>`, `<onions, 10 lbs>`). You assign kitchen areas per vegetable type; friends group bowls of the same type together (SHUFFLE phase). Finally, friends combine same-type bowls into one big bowl with total weight (REDUCE phase — e.g., `<onions, 33.4 lbs>`). You, as coordinator, are the Master node. This scales as more friends join — demonstrating horizontal scalability. [Cross-ref: topics/hadoop_ecosystem.md — MapReduce; topics/cloud_computing_and_distributed_systems.md — MapReduce]

### When to Reconsider Hadoop

Hadoop is a good fit for: large-scale data volume growth, quick access to archival data, multiple applications over the same data store, and high volume/variety workloads. Hadoop is generally **not the best fit** for:

1. **Small datasets** — if data fits on a single machine, Hadoop overhead (cluster setup, HDFS latency) outweighs benefits
2. **Advanced algorithms requiring specific hardware** — e.g., GPU-accelerated deep learning (TensorFlow/PyTorch)
3. **Task-level parallelism** — Hadoop is optimized for data parallelism (same function across many data partitions), not running many different functions simultaneously
4. **Replacing existing databases** — Hadoop complements databases but is not optimized for fast random access or OLTP (HDFS blocks are 128 MB — reading one record may require reading an entire block)
5. **Highly coupled algorithms** — algorithms with tight synchronization between steps conflict with MapReduce's independent task execution

### Pre-Built Hadoop Images

To accelerate getting started, companies provide **pre-built Hadoop images** (VM images with OS + Hadoop stack pre-installed):

- **Cloudera** — used in the UCSD course; provides pre-assembled stacks
- **Hortonworks** — provided stacks for Mac and Windows (merged with Cloudera in 2019)
- **Cloud deployment:** Images can run on IaaS (AWS, Azure, GCP), combining pre-built convenience with cloud elasticity

This avoids the hours-to-days effort of manually installing and configuring HDFS, YARN, Hive, Pig, ZooKeeper, and dependencies. [Cross-ref: topics/cloud_computing_and_distributed_systems.md — IaaS and commodity clusters]

---

## Summary and Key Takeaways

- **Apache Hadoop** is the foundational open-source framework for distributed big data storage and processing across clusters of commodity hardware.
- **HDFS** is Hadoop's storage layer — it splits large files into blocks, distributes them across nodes, replicates them for fault tolerance, and uses data locality to minimize network overhead.
- **Apache Hive** provides a SQL interface on top of Hadoop for data warehouse tasks like ETL and reporting — but is not suitable for low-latency or high-write transactional workloads.
- **Apache Spark** is a general-purpose, in-memory distributed analytics engine — dramatically faster than MapReduce for iterative and real-time workloads, supporting streaming, ML, ETL, and interactive analytics.
- Spark's key differentiator is in-memory processing — avoiding repeated disk I/O between steps, making it the tool of choice for real-time analytics and machine learning at scale.
