# Cloud Computing and Distributed Systems for Big Data

> **Source:** UCSD Big Data Specialization — Course 1, Modules 2, 5, 6

## Overview

Cloud computing and distributed systems are the infrastructure foundation of Big Data. Cloud computing provides on-demand access to compute and storage without owning physical hardware. Distributed systems enable data processing across clusters of commodity hardware.

---

## Cloud Computing as a Big Data Enabler

Two converging opportunities launched the Big Data era: a **growing torrent of data** and **cloud computing** — on-demand computing anytime, anywhere, removing the barrier of owned infrastructure. Global data grows ~40% per year while IT spending grows only ~5% per year.

### Elasticity — The Defining Feature of Cloud Computing

A key distinction between cloud and traditional IT: **elasticity** — the ability to dynamically scale resources up or down on demand. In traditional IT, infrastructure is provisioned for peak capacity and sits idle at other times. Cloud computing aligns cost with actual usage, analogous to a utility meter.

**IaaS/PaaS/SaaS — the rental car analogy (UCSD):**
- **IaaS** — renting a car and driving it yourself (you control the infrastructure)
- **PaaS** — hiring a limousine with a driver (you control the application, not the platform)
- **SaaS** — taking a taxi (you just use the service)
- **Data as a Service (DaaS)** — a bus (standardized data delivery to many consumers)

### Cloud Service Models

| Model | Description | Examples |
|-------|-------------|----------|
| **IaaS** (Infrastructure as a Service) | Virtualized compute, storage, networking | AWS EC2, Google Compute Engine, Azure VMs |
| **PaaS** (Platform as a Service) | Managed runtime for applications | Google App Engine, AWS Elastic Beanstalk, Heroku |
| **SaaS** (Software as a Service) | Ready-to-use applications | Gmail, Salesforce, Office 365 |

### Deployment Models

- **Public cloud** — shared infrastructure over the internet (AWS, Azure, GCP)
- **Private cloud** — dedicated infrastructure for a single organization
- **Hybrid cloud** — combination of public and private, with orchestration between them
- **Multi-cloud** — using multiple public cloud providers simultaneously

---

## Distributed File Systems

### Commodity Cluster Architecture

> **Source:** UCSD Course 1, Module 5 — Distributed Systems Foundations

Big data systems run on **commodity clusters** — racks of low-cost, standard servers (typically 32–64 GB RAM, 4–8 TB disk per node). These clusters assume **regular failure** as a design constraint: in a cluster of 10,000 nodes, approximately 10–50 nodes fail per day. The distributed system must handle failures transparently.

**Data parallelism:** A single logical operation (e.g., counting word frequencies in 10 TB of text) is split into many tasks executed simultaneously across nodes. Each task processes a subset of the data using the same instruction or function. This contrasts with **task parallelism**, where different operations run on different data.

**Rack awareness:** Network topology matters — data transfer between nodes on the same rack (via a top-of-rack switch) is faster and cheaper than transfers across racks. HDFS and YARN optimize for locality: they first attempt to place computation on the same node as the data, then within the same rack, and only as a last resort across racks.

### From Single Drive to Distributed Storage

A **file system** manages how the operating system stores and retrieves files on disk. When data exceeds a single machine's capacity, a **distributed file system** partitions and replicates data across multiple computers connected through a network.

**Why distributed file systems matter for big data:**
- **Scalability** — add more nodes to increase capacity (horizontal scaling)
- **Fault tolerance** — data replication means node failures don't cause data loss
- **Data locality** — computation can run on nodes that already hold the data ("move computation to data, not data to computation")
- **High concurrency** — multiple readers can be served from different replicas simultaneously

### Key Design Principle: Move Computation, Not Data

Traditional RDBMS moves data to compute resources. Distributed file systems reverse this: computation is shipped to where the data resides. This is the foundation of the MapReduce programming model.

### Read Scalability Through Replication

Replication serves dual purposes: (1) fault tolerance — multiple copies prevent data loss, and (2) read scalability — multiple readers can access different replicas simultaneously.

**Tradeoff:** A replication factor of 3 means ~3x raw storage overhead. 1 PB of logical data consumes ~3 PB of disk.

### Write-Once, Append-Only Pattern

Big data systems typically use an immutable data pattern: data is written once and updates are recorded as new data appended over time. The current state is derived by combining original data with subsequent updates. This avoids the hard distributed-systems problem of synchronizing in-place updates across replicas.

---

## Hadoop Distributed File System (HDFS)

HDFS is the storage foundation of the Hadoop ecosystem. It has shown production scalability up to **200 petabytes** in a single cluster of **4,500 servers** with close to a billion files and blocks.

### Architecture

| Component | Role | Details |
|-----------|------|---------|
| **NameNode** | Metadata manager | Records file names, directory hierarchy, block locations. Usually one per cluster (single point of failure — HDFS High Availability adds a standby) |
| **DataNode** | Block storage | Runs on each cluster node, stores file blocks, listens for NameNode commands |

**Analogy:** The NameNode is like a library's card catalog — it tells you which shelf holds which book. DataNodes are the actual shelves.

### Key Parameters

- **Default block size:** 64 MB (Hadoop 1.x) / 128 MB (Hadoop 2.x+)
- **Default replication factor:** 3 (configurable per file, directory, or globally)
- **Typical file size:** gigabytes to terabytes

### Data Types Supported

HDFS handles text files (line-by-line or token-by-token), geospatial data (vectors or rasters), genomics data (FASTA/FASTQ formats), and any custom format via input/output format specifications.

---

## Hadoop Ecosystem: YARN and MapReduce

### YARN — Resource Management

YARN (Yet Another Resource Negotiator) manages cluster resources, scheduling computational workloads. It decouples resource management from data processing, allowing multiple processing engines (MapReduce, Spark, Hive) to share the same cluster.

**Hadoop 1.0 → Hadoop 2.0 Evolution (UCSD):** In Hadoop 1.0, MapReduce handled both resource management and data processing in a single monolithic system. Hadoop 2.0 introduced YARN as a separate resource management layer, enabling non-MapReduce workloads (Spark, Hive, HBase) to run on the same cluster. The simple YARN Architecture: a **ResourceManager** (global scheduler) per cluster, a **NodeManager** per node (manages containers), and an **ApplicationMaster** per job (coordinates execution).

### MapReduce — Parallel Programming Model

MapReduce processes large datasets in two phases:
1. **Map** — filter and transform data in parallel across nodes
2. **Reduce** — aggregate and summarize the mapped results

This model automatically handles parallelization, distribution, fault tolerance, and load balancing.

[Cross-ref: topics/hadoop_ecosystem.md — Hadoop, HDFS, MapReduce, YARN overview]
[Cross-ref: topics/big_data_foundations.md — 5 V's, distributed computing foundations]
[Cross-ref: topics/big_data_characteristics_deep_dive.md — Volume challenges, in-situ processing]
