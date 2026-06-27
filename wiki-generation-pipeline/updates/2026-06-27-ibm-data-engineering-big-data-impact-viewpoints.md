# Viewpoints: Impact of Big Data on Data Engineering

## Overview

This lesson captures perspectives from practicing data professionals on how Big Data has fundamentally reshaped the field of data engineering — from the tools engineers use, to the skills they need, to the sheer scale and variety of data they must handle.

---

## The Four Vs of Big Data

Big Data is commonly defined through four core characteristics:

| Characteristic | Description |
|---|---|
| **Velocity** | The speed at which data is generated and must be processed |
| **Veracity** | The trustworthiness and accuracy of the data |
| **Volume** | The sheer amount of data being produced and stored |
| **Variety** | The diversity of data types and sources (structured, unstructured, semi-structured) |

These four dimensions collectively distinguish Big Data from traditional data workloads and have driven the need for entirely new engineering approaches.

---

## How Big Data Changed Data Engineering

### A More Diverse and Rich Field

Big Data has made data engineering significantly more diverse. As organizations collect unprecedented amounts of data, the ability to make sense of it and derive actionable insights has become both more relevant and more critical. This shift has:

- Driven the emergence of new technologies and products purpose-built for large-scale data
- Created massive demand for professionals who can design, build, and manage big data systems
- Expanded the role of the data engineer beyond traditional database administration

### The Pre- vs. Post-IoT Shift

Before the rise of IoT (Internet of Things) and social media, the pathways for ingesting data into a database were narrow and slow — often limited to manual data entry by analysts.

Over the past decade, the landscape changed dramatically:

- **Devices and APIs proliferated**, with gadgets constantly pushing updates and streaming data to one another
- **The nature of data itself changed** — it became faster, more varied, and far more voluminous
- **Data ingestion became continuous and automated**, rather than batch-driven and manual

### Traditional RDBMS Hit Their Limits

A critical realization for the field was that **Relational Database Management Systems (RDBMSes) are not a one-size-fits-all solution**. Database administrators and data engineers discovered this the hard way when trying to scale traditional systems to meet new demands.

In response, data engineers invented and adopted an entirely new generation of data technologies:

| Technology | Purpose |
|---|---|
| **Google Bigtable** | Wide-column store for large-scale structured data |
| **Apache Cassandra** | Distributed NoSQL database for high availability at scale |
| **Graph-based Databases** | Storing and querying highly connected data |
| **Hadoop** | Distributed storage and processing framework |
| **MapReduce** | Programming model for processing petabytes of data in parallel |

> **Key insight:** Data engineers didn't just adopt new tools — they *invented* them. This era marked a turning point where engineers became active contributors to the tooling ecosystem, not just consumers of existing database technology.

---

## Shifting Attitudes Toward Data Storage

Big Data also changed organizational culture around data retention:

- **Storage is no longer a barrier.** Disk space has become cheap enough that organizations now store far more data than they historically would have, without the pressure to delete or compress aggressively.
- **"Store everything" has become the default posture**, enabled by distributed storage systems and cloud infrastructure.
- This shift is one of the most tangible outcomes of the Big Data era — the accumulation of data that can later be mined for insights, even if its value isn't immediately obvious.

---

## Handling Unstructured Data

One of the defining challenges Big Data introduced is the explosion of **unstructured data** — data that doesn't fit neatly into rows and columns:

- Unstructured data is typically *not* handled within traditional relational databases
- When stored in a database context, systems like **MongoDB** (a document-oriented NoSQL database) are often used
- The volume of unstructured data (text, images, logs, social media content, sensor readings) now dwarfs structured data in many organizations

---

## Key Takeaways

- Big Data is defined by the **four Vs**: velocity, veracity, volume, and variety.
- The rise of IoT and social media fundamentally changed how, how fast, and how much data is generated.
- Traditional RDBMSes were insufficient for Big Data workloads, driving engineers to invent and adopt new distributed systems (Cassandra, Hadoop, BigTable, etc.).
- Storage cost is no longer a meaningful constraint — organizations now default to storing more data, not less.
- Unstructured data has become a dominant data type, requiring specialized tools like MongoDB.
- Big Data created an entirely new demand for data engineering professionals skilled in large-scale, distributed systems.
