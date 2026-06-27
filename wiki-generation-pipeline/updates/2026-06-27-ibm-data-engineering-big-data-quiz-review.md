# Quiz Review: Big Data Platforms — Weak Areas

## Overview

This document addresses the specific questions missed during the Big Data Platforms quiz. Each entry restates the question, identifies the correct answer, and explains the concept to close the knowledge gap.

---

## Q1 — What does "Veracity" imply in the context of Big Data?

**Correct Answer:** Accuracy and conformity of data to facts

**Explanation:**
Veracity refers to how trustworthy and reliable the data is. In Big Data contexts, data arrives from many sources and in many formats — not all of it is clean, complete, or accurate. Veracity is the concern of ensuring that the data you're working with actually reflects reality and can be trusted for analysis.

| V | Meaning |
|---|---|
| **Velocity** | The speed at which data is generated and must be processed |
| **Volume** | The sheer scale and amount of data |
| **Variety** | The diversity of data types and sources |
| **Veracity** | The accuracy and conformity of data to facts |
| **Value** | Our ability and need to turn data into meaningful outcomes |

> **Common confusion:** Veracity is easy to mix up with "variety" or "velocity" since all three start with V. Remember: **Veracity = Validity of the data.**

---

## Q3 — What does "Value" imply in the context of Big Data?

**Correct Answer:** Our ability and need to turn data into value

**Explanation:**
Value is the ultimate goal of all Big Data efforts. Having large volumes of fast, varied, and accurate data means nothing if it cannot be transformed into actionable business insights. Value represents the purpose behind collecting and processing Big Data — the return on the investment of storing and engineering all that data.

> **Key distinction from Veracity:** Veracity is about data *quality*; Value is about data *purpose and outcome*.

---

## Q4 — What is one of Apache Spark's key use cases?

**Correct Answer:** Perform complex analytics in real-time

**Explanation:**
Apache Spark is a general-purpose data processing engine built for speed. Unlike Hadoop's MapReduce (which writes intermediate results to disk), Spark processes data **in-memory**, making it orders of magnitude faster for many workloads. This makes it particularly well-suited for:

- **Real-time and streaming analytics**
- Machine learning at scale
- Large-scale data transformation and ETL

The other options map to different tools:

| Option | Actual Tool |
|---|---|
| Consolidate data across the organization | Data integration platforms / ETL tools |
| Scalable and reliable Big Data storage | HDFS (Hadoop Distributed File System) |
| Fast recovery from hardware failures | HDFS (built-in fault tolerance) |

---

## Q5 — Which Big Data tool is used for reading, writing, and managing large dataset files stored in HDFS or Apache HBase?

**Correct Answer:** Hive

**Explanation:**
Apache Hive is a **data warehouse software layer** that sits on top of Hadoop's ecosystem. It is specifically designed for reading, writing, and managing large datasets stored in distributed storage systems like **HDFS** or **Apache HBase**, using a SQL-like query language called HiveQL.

> **Why not Hadoop?** Hadoop (and its HDFS component) provides the *storage infrastructure* — it's where the data lives. Hive is the *interface* for querying and managing that data. They work together but serve different roles.

| Tool | Role |
|---|---|
| **HDFS** | Distributed storage system — where data is physically stored |
| **Hive** | Data warehouse layer — for reading, writing, and querying data in HDFS/HBase |
| **Spark** | Processing engine — for fast, large-scale data computation |
| **Hadoop** | Overarching framework providing distributed storage (HDFS) and processing (MapReduce) |
