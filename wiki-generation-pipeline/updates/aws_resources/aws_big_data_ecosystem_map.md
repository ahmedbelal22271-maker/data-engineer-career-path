# AWS Big Data Ecosystem — Resource Map

Source: https://aws.amazon.com/what-is/big-data/ (hub page)

## How to Use This Map

This index organizes every resource linked from the AWS "What is Big Data?" hub page and its deeper linked pages. Use it to navigate the AWS big data ecosystem in a structured way — follow parent → child links based on your current learning goal.

Each entry includes:
- **File**: the local markdown copy in this directory
- **URL**: the original AWS page
- **Parent Pages**: which page(s) link to it
- **Child Links**: services/concepts it links to (→ means "links to")
- **Est. Read Time**: based on page length

---

## Section 1: Full Resource Index

| # | Resource | File | URL | Parent Page(s) | Child Links | Est. Read |
|---|----------|------|-----|----------------|-------------|-----------|
| 1 | What is Big Data? (hub) | `01_what_is_big_data.md` | https://aws.amazon.com/what-is/big-data/ | — (entry point) | → Spark, Kafka, Kinesis, Streaming Data, Data Lakes, Security, DoD, Partners | 5 min |
| 2 | Apache Spark | `02_what_is_apache_spark.md` | https://aws.amazon.com/what-is/apache-spark/ | Hub (§ Evolution) | → EMR, Redshift, S3, HDFS, YARN, Apache Mesos, Couchbase, Cassandra, Tez, Presto, Hive, ORC, Parquet, MongoDB, Elasticsearch, EC2 Reserved/Spot | 12 min |
| 3 | Apache Kafka | `03_what_is_apache_kafka.md` | https://aws.amazon.com/what-is/apache-kafka/ | Hub (§ Evolution) | → Amazon MSK, RabbitMQ, MQTT, STOMP, Deploy Kafka on AWS blog | 10 min |
| 4 | Amazon Kinesis | `04_amazon_kinesis.md` | https://aws.amazon.com/kinesis/ | Hub (§ Evolution); Streaming Data (§ AWS Support) | → Data Firehose, Kinesis Data Streams, MSK, S3, Redshift, KCL, Storm, Spark Streaming, IoT, Video Streams | 6 min |
| 5 | What is Streaming Data? | `05_what_is_streaming_data.md` | https://aws.amazon.com/what-is/streaming-data/ | Hub (§ Evolution); Kinesis (§ Use Cases) | → Kinesis, Data Firehose, Kinesis Data Streams, MSK, Redshift, S3, EC2, EMR, KCL, Storm, Spark Streaming, Flume, Kafka | 14 min |
| 6 | Data Lakes & Analytics | `06_data_lakes_and_analytics.md` | https://aws.amazon.com/big-data/datalakes-and-analytics/ | Hub (§ Capabilities); Partners (§ Overview) | → SageMaker, Redshift, EMR, QuickSight, OpenSearch, DataZone, Athena, Glue, MWAA, Kinesis, Data Firehose, MSK, Flink, S3, Clean Rooms, Iceberg, Hive, Parquet, BigQuery, Snowflake, ADLS, GCS | 10 min |
| 7 | AWS Cloud Security | `07_cloud_security.md` | https://aws.amazon.com/security/ | Hub (§ Trusted & Secure); DoD (§ Compliance) | → Security Services, Partner Network, Marketplace, Artifact, ISO 27001, FedRAMP, HIPAA, PCI DSS, NIST Framework | 10 min |
| 8 | DoD SRG Compliance | `08_dod_compliance.md` | https://aws.amazon.com/compliance/dod/ | Hub (§ Trusted & Secure) | → FedRAMP, GovCloud, Artifact, Secret Region, NIST 800-53, LZA on AWS, Well-Architected Framework | 12 min |
| 9 | Partner Solutions | `09_partner_solutions.md` | https://aws.amazon.com/big-data/datalakes-and-analytics/partner-solutions/ | Hub (§ Partners); Data Lakes (§ Partners section) | → Partner Network, Marketplace, Redshift, Partner Solutions Finder | 5 min |
| 10 | What is Edge Computing? | `10_what_is_edge_computing.md` | https://aws.amazon.com/what-is/edge-computing/ | — (standalone; replacement for broken Google Cloud Edge Computing link) | → AI/ML, AWS Edge, Outposts, Storage Gateway, Snow Family, SageMaker Edge, CDN, Manufacturing, Energy, Volkswagen, Hulu, Riot Games | 8 min |

---

## Section 2: Category Clusters

### Cluster A — Core Concepts
These pages explain the fundamental ideas behind big data and streaming.

| File | Topic | Why Read |
|------|-------|----------|
| `01_what_is_big_data.md` | 3 V's (Volume, Variety, Velocity), data lifecycle, analytics types (descriptive/predictive/prescriptive) | Start here — defines the problem space |
| `05_what_is_streaming_data.md` | Streaming characteristics, batch vs streaming, architecture, challenges | Essential for understanding real-time data paradigm |
| `02_what_is_apache_spark.md` | In-memory distributed processing, Spark vs MapReduce, workloads (SQL, ML, Streaming, Graph) | Core processing engine for batch + streaming |
| `03_what_is_apache_kafka.md` | Distributed streaming platform, partitioned log model, Kafka vs RabbitMQ | Standard for event streaming and data pipelines |
| `10_what_is_edge_computing.md` | Edge processing, upstream/downstream apps, latency/security benefits, AWS edge services | Covers edge paradigm — important in modern DE architectures |

### Cluster B — AWS Streaming Services
AWS-native services for collecting, processing, and analyzing streaming data.

| File | Service | What It Does |
|------|---------|-------------|
| `04_amazon_kinesis.md` | Amazon Kinesis | Collect, process, analyze real-time video and data streams |
| → (linked from 04, 05) | Amazon Data Firehose | Load streaming data into S3/Redshift automatically |
| → (linked from 04, 05) | Amazon Kinesis Data Streams | Capture/store TB/hour from hundreds of thousands of sources |
| → (linked from 03, 04, 05, 06) | Amazon MSK | Fully managed Apache Kafka service |

### Cluster C — AWS Compute & Processing
Services for running big data workloads at scale.

| Service | Links Found In | URL |
|---------|----------------|-----|
| Amazon EMR | Spark (AWS offerings), Streaming Data (hybrid), Data Lakes (services) | https://aws.amazon.com/emr/ |
| AWS Glue | Data Lakes (services, multicloud) | https://aws.amazon.com/glue/ |
| Amazon Athena | Data Lakes (services, multicloud) | https://aws.amazon.com/athena/ |
| Amazon MWAA (Airflow) | Data Lakes (services) | https://aws.amazon.com/mwaa/ |
| Amazon Managed Service for Apache Flink | Data Lakes (services) | https://aws.amazon.com/managed-service-apache-flink/ |

### Cluster D — Storage & Warehousing

| Service | Links Found In | URL |
|---------|----------------|-----|
| Amazon S3 | Spark, Kinesis, Streaming Data, Data Lakes | https://aws.amazon.com/s3/ |
| Amazon Redshift | Spark, Kinesis, Streaming Data, Data Lakes, Partners | https://aws.amazon.com/redshift/ |
| Amazon S3 Tables | Data Lakes (services) | https://aws.amazon.com/s3/features/tables/ |

### Cluster E — Analytics & Business Intelligence

| Service | Links Found In | URL |
|---------|----------------|-----|
| Amazon SageMaker | Data Lakes (overview, multicloud) | https://aws.amazon.com/sagemaker/ |
| Amazon QuickSight | Data Lakes (services, customer story) | https://aws.amazon.com/quicksight/ |
| Amazon OpenSearch Service | Data Lakes (services, customer story) | https://aws.amazon.com/opensearch-service/ |

### Cluster F — Governance, Catalog & Collaboration

| Service | Links Found In | URL |
|---------|----------------|-----|
| Amazon DataZone | Data Lakes (services, customer story) | https://aws.amazon.com/datazone/ |
| AWS Clean Rooms | Data Lakes (services) | https://aws.amazon.com/clean-rooms/ |
| SageMaker Catalog | Data Lakes (services) | https://aws.amazon.com/sagemaker/catalog/ |

### Cluster G — Security & Compliance

| Service/Standard | Links Found In | URL |
|------------------|----------------|-----|
| AWS Cloud Security (hub) | Big Data hub, DoD | https://aws.amazon.com/security/ |
| DoD SRG Compliance | Big Data hub | https://aws.amazon.com/compliance/dod/ |
| FedRAMP | Security, DoD | https://aws.amazon.com/compliance/fedramp/ |
| ISO 27001 | Security | https://aws.amazon.com/compliance/iso-27001/ |
| HIPAA | Security | https://aws.amazon.com/compliance/hipaa/ |
| PCI DSS | Security | https://aws.amazon.com/compliance/pci-dss/ |
| AWS Artifact | Security, DoD | https://aws.amazon.com/artifact/ |
| AWS GovCloud (US) | DoD | https://aws.amazon.com/govcloud-us/ |

### Cluster H — Partner Ecosystem

| Resource | Links Found In | URL |
|----------|----------------|-----|
| AWS Partner Network | Big Data hub, Security, Partners | https://aws.amazon.com/partners/ |
| AWS Marketplace | Security, Partners | https://aws.amazon.com/marketplace/ |
| Data & Analytics Competency Partners | Big Data hub | https://aws.amazon.com/big-data/datalakes-and-analytics/partner-solutions/ |

### Cluster I — Open Source / Third-Party (referenced but not AWS)

| Project | Links Found In | URL |
|---------|----------------|-----|
| Apache Hadoop / HDFS | Spark | https://hadoop.apache.org/ |
| Apache Hive | Spark, Data Lakes | https://hive.apache.org/ |
| Apache Parquet | Spark, Data Lakes | https://parquet.apache.org/ |
| Apache ORC | Spark | https://orc.apache.org/ |
| Apache Iceberg | Data Lakes | https://iceberg.apache.org/ |
| Apache Tez | Spark | https://tez.apache.org/ |
| Presto | Spark | https://prestodb.io/ |
| Apache Mesos | Spark | https://mesos.apache.org/ |
| Apache Storm | Kinesis, Streaming Data | https://storm.apache.org/ |
| Apache Flume | Streaming Data | https://flume.apache.org/ |
| Apache Cassandra | Spark | https://cassandra.apache.org/ |
| MongoDB | Spark | https://www.mongodb.com/ |
| Couchbase | Spark | https://www.couchbase.com/ |
| Elasticsearch | Spark | https://www.elastic.co/ |
| RabbitMQ | Kafka | https://www.rabbitmq.com/ |
| MQTT | Kafka | https://mqtt.org/ |
| STOMP | Kafka | https://stomp.github.io/ |
| Google BigQuery | Data Lakes | https://cloud.google.com/bigquery |
| Snowflake | Data Lakes | https://www.snowflake.com/ |
| Azure Data Lake Storage | Data Lakes | https://azure.microsoft.com/en-us/services/storage/data-lake/ |
| Google Cloud Storage | Data Lakes | https://cloud.google.com/storage |

---

## Section 3: Reading Paths

### Path A — Big Data Fundamentals (30 min)
Start here for a broad overview.
1. `01_what_is_big_data.md` (5 min) — the hub
2. `05_what_is_streaming_data.md` (14 min) — streaming paradigm
3. `07_cloud_security.md` (10 min) — security context

### Path B — Processing Engine Deep Dive (35 min)
For engineers who need to understand Spark and Kafka.
1. `02_what_is_apache_spark.md` (12 min) — Spark fundamentals
2. `03_what_is_apache_kafka.md` (10 min) — Kafka fundamentals
3. `04_amazon_kinesis.md` (6 min) — AWS streaming
4. `05_what_is_streaming_data.md` (14 min) — streaming architecture (already read in Path A)

### Path C — AWS Services Landscape (40 min)
For architects evaluating the AWS analytics stack.
1. `06_data_lakes_and_analytics.md` (10 min) — full service catalog
2. `04_amazon_kinesis.md` (6 min) — streaming services
3. `02_what_is_apache_spark.md` (12 min) — Spark on EMR
4. `09_partner_solutions.md` (5 min) — partner ecosystem
5. `07_cloud_security.md` (10 min) — security overview

### Path D — Compliance & Governance (20 min)
For enterprise/government contexts.
1. `07_cloud_security.md` (10 min) — security foundation
2. `08_dod_compliance.md` (12 min) — DoD SRG specifics

### Path E — Edge Computing (10 min)
For understanding edge processing in the data pipeline.
1. `10_what_is_edge_computing.md` (8 min) — edge fundamentals, use cases, AWS edge services

---

## Section 4: Parent → Child Link Graph (text format)

```
What is Big Data? (hub)
├── → Apache Spark
│   ├── → Amazon EMR
│   ├── → Amazon Redshift
│   ├── → Amazon S3
│   ├── → Apache Hadoop (HDFS, YARN)
│   ├── → Apache Mesos
│   └── → Couchbase, Cassandra, MongoDB, Elasticsearch
├── → Apache Kafka
│   ├── → Amazon MSK
│   └── → RabbitMQ
├── → Amazon Kinesis
│   ├── → Amazon Data Firehose
│   ├── → Amazon Kinesis Data Streams
│   └── → Amazon MSK
├── → What is Streaming Data?
│   ├── → Amazon Kinesis (and its sub-services)
│   ├── → Amazon Redshift Streaming Ingestion
│   └── → Apache Storm, Spark Streaming, Flume
├── → Data Lakes & Analytics
│   ├── → Amazon SageMaker
│   ├── → Amazon Redshift, Amazon EMR, AWS Glue
│   ├── → Amazon Athena, Amazon QuickSight
│   ├── → Amazon OpenSearch Service
│   ├── → Amazon DataZone, AWS Clean Rooms
│   └── → Apache Iceberg, Hive, Parquet
├── → AWS Cloud Security
│   └── → FedRAMP, ISO 27001, HIPAA, PCI DSS
├── → DoD SRG Compliance
│   └── → FedRAMP, GovCloud, AWS Artifact
├── → Edge Computing (standalone)
│   ├── → AWS Edge Services
│   ├── → AWS Outposts
│   ├── → AWS Storage Gateway
│   ├── → AWS Snow Family
│   └── → SageMaker Edge Manager
└── → Partner Solutions
    └── → AWS Partner Network, Marketplace
```

---

Created 2026-06-30 from live AWS documentation. URLs verified at time of capture.
