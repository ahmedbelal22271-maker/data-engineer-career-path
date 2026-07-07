# Foundations of Big Data

> **LTHP Status:** NEW — Module 2 ecosystem expansion.
> **Source files:** `foundations-big-data.md` (primary, 161 lines), `big-data-summary.md` (summary companion, 59 lines), `big-data-impact-viewpoints.md` (§17 practitioner perspectives, 89 lines)

## Introduction

In the digital world, every interaction leaves a trace. Travel habits, workouts, entertainment choices, and the countless internet-connected devices we interact with daily all generate vast amounts of data. This phenomenon has a name: **Big Data**.

> **Ernst & Young Definition:** "Big Data refers to the dynamic, large and disparate volumes of data being created by people, tools, and machines. It requires new, innovative, and scalable technology to collect, host, and analytically process the vast amount of data gathered in order to derive real-time business insights that relate to consumers, risk, profit, performance, productivity management, and enhanced shareholder value."

Big Data is defined by a common set of characteristics — known as **the V's of Big Data**.

---

## The Five V's of Big Data

### 1. Velocity

**Velocity** is the speed at which data accumulates — a process that never stops. Data is generated extremely fast and continuously. Near or real-time streaming, local, and cloud-based technologies can process information at the speed it is generated. Every 60 seconds, hours of video footage are uploaded to YouTube.

### 2. Volume

**Volume** is the scale of data — the sheer amount of data being stored and growing. Key drivers include the increase in the number of data sources, higher resolution sensors capturing more detail per event, and scalable infrastructure enabling storage of data that previously would have been discarded. With approximately 7 billion people using digital devices, these devices generate approximately **2.5 quintillion bytes of data every day** — equivalent to 10 million Blu-ray DVDs.

### 3. Variety

**Variety** is the diversity of data — in both type and source. This includes structured data (rows and columns in relational databases), unstructured data (tweets, blog posts, images, video, audio), and semi-structured data (JSON, XML, logs). Variety also reflects that data comes from many different origins: internal sources (operational systems, business applications) and external sources (social media, third-party APIs, public datasets).

### 4. Veracity

**Veracity** is the quality, accuracy, and trustworthiness of data — its conformity to facts. Veracity attributes include consistency (data means the same thing across all systems), completeness (no critical fields missing), integrity (data has not been corrupted), and ambiguity (data is interpretable in only one clear way). The core challenge: an estimated **80% of data is unstructured** — making it inherently harder to validate, categorize, and trust.

### 5. Value

**Value** is the ability — and necessity — to turn data into something meaningful and actionable. Value includes business value (better decisions, competitive advantage), medical value (improved patient outcomes, drug discovery), social value (public policy improvements), and personal value (customer satisfaction). The main reason organizations invest in Big Data is to extract value from it. All other V's are properties of the data itself; value is the *purpose* behind working with it.

### The V's in Summary

| V | Definition | Real-World Example |
|---|---|---|
| **Velocity** | Speed of data generation | Hours of YouTube video uploaded every 60 seconds |
| **Volume** | Scale of data stored | 2.5 quintillion bytes generated daily worldwide |
| **Variety** | Diversity of data types and sources | Text, images, video, health data, IoT sensor readings |
| **Veracity** | Quality and accuracy of data | 80% of data is unstructured and must be validated |
| **Value** | Ability to derive insight and benefit | Business intelligence, medical research, recommendations |

---

## Why Conventional Tools Fall Short

The scale of Big Data makes it infeasible to use conventional data analysis tools. A standard relational database or desktop analytics tool cannot store data at petabyte or exabyte scale, process continuous high-velocity streams in real time, or handle the diversity of unstructured and semi-structured data types.

### The Solution: Distributed Computing

Tools such as **Apache Spark**, **Hadoop**, and the broader Hadoop ecosystem provide the ability to extract, load, analyze, and process data across distributed compute resources, overcoming the storage and processing limitations of single-node systems.

---

## How Big Data Changed Data Engineering

> **Source:** `big-data-impact-viewpoints.md` — §17 enrichment with practitioner perspectives.

### A More Diverse and Rich Field

Big Data has made data engineering significantly more diverse. As organizations collect unprecedented amounts of data, the ability to make sense of it and derive actionable insights has become both more relevant and more critical. This shift has driven the emergence of new technologies and products purpose-built for large-scale data, created massive demand for professionals who can design and manage big data systems, and expanded the role of the data engineer beyond traditional database administration.

### The Pre- vs. Post-IoT Shift

Before the rise of IoT and social media, the pathways for ingesting data into a database were narrow and slow — often limited to manual data entry by analysts. Over the past decade, devices and APIs proliferated, with gadgets constantly pushing updates and streaming data to one another. The nature of data itself changed — it became faster, more varied, and far more voluminous. Data ingestion became continuous and automated, rather than batch-driven and manual.

### Traditional RDBMS Hit Their Limits

A critical realization was that RDBMSes are not a one-size-fits-all solution. Database administrators and data engineers discovered this the hard way when trying to scale traditional systems to meet new demands. In response, engineers invented and adopted an entirely new generation of data technologies:

| Technology | Purpose |
|---|---|
| **Google Bigtable** | Wide-column store for large-scale structured data |
| **Apache Cassandra** | Distributed NoSQL database for high availability at scale |
| **Graph-based Databases** | Storing and querying highly connected data |
| **Hadoop** | Distributed storage and processing framework |
| **MapReduce** | Programming model for processing petabytes of data in parallel |

> **Key insight from practitioners:** Data engineers didn't just adopt new tools — they *invented* them. This era marked a turning point where engineers became active contributors to the tooling ecosystem, not just consumers of existing database technology.

### Shifting Attitudes Toward Data Storage

Big Data also changed organizational culture around data retention. Storage is no longer a barrier — disk space has become cheap enough that organizations now store far more data than they historically would have, without the pressure to delete or compress aggressively. "Store everything" has become the default posture, enabled by distributed storage systems and cloud infrastructure.

### Handling Unstructured Data

One of the defining challenges Big Data introduced is the explosion of unstructured data — data that doesn't fit neatly into rows and columns. Unstructured data is typically not handled within traditional relational databases; systems like MongoDB (a document-oriented NoSQL database) are often used instead. The volume of unstructured data now dwarfs structured data in many organizations.

---

## Core Open-Source Big Data Tools

### Apache Hadoop

Hadoop provides distributed storage and processing of large datasets across clusters of computers. Its primary storage component is the **Hadoop Distributed File System (HDFS)** — a storage system purpose-built for Big Data. Data is split across multiple nodes in a cluster, enabling parallel processing and fault tolerance.

### Apache Hive

Hive is a data warehouse software layer built on top of Hadoop for reading, writing, and managing large datasets. It allows analysts and engineers to query large datasets using a SQL-like language (HiveQL), abstracting the complexity of MapReduce and making Big Data more accessible to those familiar with relational query patterns.

### Apache Spark

Spark is a general-purpose data processing engine designed to extract and process large volumes of data. It is significantly faster than Hadoop's MapReduce for many workloads due to in-memory processing. Spark supports batch processing, streaming, machine learning, and graph processing within a single unified engine.

---

## Summary and Key Takeaways

- **Big Data** refers to dynamic, large, and disparate volumes of data generated by people, tools, and machines — requiring new, scalable technology to process and derive value from.
- The **Five V's** define Big Data: Velocity (speed), Volume (scale), Variety (diversity), Veracity (quality), and Value (purpose).
- **80% of data is unstructured** — making veracity one of the most pressing challenges in big data analytics.
- **2.5 quintillion bytes** of data are generated every day by the world's digital devices.
- Conventional analysis tools cannot operate at big data scale. **Distributed computing tools** — primarily **Apache Hadoop** and **Apache Spark** — are the foundation of modern big data processing.
- The rise of IoT and social media fundamentally changed how, how fast, and how much data is generated.
- Storage cost is no longer a meaningful constraint — organizations now default to storing more data, not less.
- The ultimate goal of all Big Data work is **Value** — transforming raw data into insights that benefit businesses, individuals, and society.

---

## UCSD Big Data Specialization — Supplementary Concepts

### What Launched the Big Data Era

Two converging opportunities launched the Big Data era: a **growing torrent of data** (McKinsey 2013 identified data science as the #1 catalyst for economic growth) and **cloud computing** — on-demand computing anytime, anywhere, removing the barrier of owned infrastructure. Global data grows ~40% per year while IT spending grows only ~5% per year.

### The Sixth V — Valence

Valence is the **connectedness of data** — the density of connections between data points, analogous to valence electrons in chemistry. It is measured as graph density: the ratio of actual connections to possible connections. As connectivity increases over time, new challenges arise: algorithmic inefficiency on dense graphs, modeling dynamic change (connections appear and disappear), and event detection (local cohesion bursts signal emergent behavior — e.g., a viral trend on Twitter).

### In-Situ Processing

Traditional RDBMS moves data to compute resources. **In-situ processing** reverses this: computation is brought to where the data is generated or stored. This reduces data movement latency and is critical for real-time sensor workloads (e.g., aircraft engine monitoring at 40,000 feet). It enables real-time actions — not just monitoring, but immediate response. This requires an organizational culture shift toward real-time action orientation and scalable computing infrastructure.

### Key Frameworks for Velocity — Storm

Apache **Storm** is an open-source framework for real-time processing of high-velocity data, complementing Hadoop's batch-oriented design. Unlike Hadoop (optimized for volume), Storm handles data generated at fast rates and can integrate with any database or storage technology.

### SCADA Systems

SCADA (Supervisory Control and Data Acquisition) is an industrial control system for remote monitoring and control of physical processes. It spans multiple geographic sites and sensor types, enabling real-time action definition for waste reduction and efficiency improvement. Applied in manufacturing, power generation, water treatment, pipelines, smart buildings, and HVAC systems.

### Data Variety Deep Dive

Data arrives along four axes of variety: **structural** (EKG waveform vs. news article — different organization), **media** (audio vs. transcript — different modality), **semantic** (different units, measurement assumptions, or contextual meanings), and **availability** (real-time vs. stored, polled vs. pushed). Email is a hybrid entity exhibiting all four axes simultaneously.

### Applications of Big Data — UCSD Practitioner Perspectives

> **Source:** UCSD Course 1, Module 2 — Applications of Big Data

**Personalized Marketing & Recommendation Engines:** Amazon, Walmart, and Target use individual consumer data (purchase, search, viewing, location history) to tailor product displays and communications. Amazon personalizes based on previously viewed items; Netflix recommends shows based on viewing history.

**Sentiment Analysis (Opinion Mining):** Companies apply NLP to product reviews and social media feeds to classify sentiment as positive, negative, or neutral. The Meltwater/Danone case study demonstrates this for brand reputation: Meltwater helped Danone monitor social media during a marketing campaign and provided early warning of a reputational crisis (the 2013 European horsemeat scandal), enabling Danone to reassure customers before the news broke in UK press. Twitter feed analysis is regularly used by news channels during elections to gauge public opinion.

**Mobile Advertising & Location-Based Ads:** Platforms use GPS sensors in mobile devices to deliver real-time, location-based advertisements and discounts. Example: a Home Depot scenario where a recent home buyer receives mobile coupons about paint and hardware when near a store location, leveraging integrated consumer data, purchase history, and geolocation.

**Smart Cities:** An interconnected mesh of sensors implanted across cities generates real-time data enabling better service quality, reduced pollution, optimized traffic flow, and energy savings. San Diego is presented as a prototype digital city, generating data from traffic sensors, satellites, and camera networks for wildfire response, traffic management, and energy efficiency. [Cross-ref: topics/data_sources.md — machine-generated, human-generated, organizational data]

**Biomedical Big Data & Genomics:** Genomics is one of the fastest-growing big data types. Storage demand for sequence data is projected to reach 2–40 exabytes by 2025, equivalent to or exceeding YouTube's annual storage demand. Precision medicine integrates sensor data (fitness devices like FitBit producing several GB/day), organizational data (NCBI, Gene Ontology, UMLS knowledge-bases), and people-generated data (mobile health apps, Twitter, blogs, online support groups) to enable individualized treatment. [Cross-ref: topics/big_data_specialization_ucsd.md — Course 1 Module 2]

### Machine-Generated Data — Scale and Characteristics

> **Source:** UCSD Course 1, Module 2 — Machine-Generated Data

Machine-generated data is the **largest and most complex** source of big data. A Boeing 787 produces **0.5 TB per flight** — almost every part continuously updates both flight and ground teams. The Large Hadron Collider generates **40 TB per second** during experiments.

**Three properties of smart devices:**
1. **Connect** — can connect to other devices or networks
2. **Execute & Collect** — autonomously execute services and collect data
3. **Environmental Awareness** — have some knowledge of their environment

The interconnection of smart devices defines the **Internet of Things (IoT)** — spanning home, car, office, city, rural areas, sky, and ocean. Activity trackers (tracking distance, calorie consumption, heartbeat, sleep quality) enable new approaches to patient intervention via personalized medicine.

### Organization-Generated Data — Structured but Siloed

> **Source:** UCSD Course 1, Module 2 — Organization-Generated Data

Organizational data includes commercial transactions, credit card records, government records, e-commerce data, banking/stock records, medical records, sensor data, and clicks. It is highly structured, stored in RDBMS, and queried via SQL.

**The "Structured Data" Continuum** (from UCSD lecture): Structured data exists on a spectrum from human-readable raw formats (CSV, XML) through semantic key-value interchange formats (JSON, RSS, SOAP, ReST) to machine-level binary interfaces (ABI, I/O). This reinforces that "structured" is not binary.

**The silo problem:** Data is traditionally captured at department level without shared infrastructure or cross-organizational access policy, producing outdated, unsynchronized, and invisible datasets. Cloud-based solutions are the leading approach to breaking silos.

### WIFIRE Project — Wildfire Analytics Cyberinfrastructure

> **Source:** UCSD Course 1, Module 2 — WIFIRE Project

The WIFIRE (Workflows Integrating Collaborative Hazard Sciences) project at the San Diego Supercomputer Center (SDSC) builds an integrated system for wildfire analysis by combining satellite and remote sensor data with computational techniques. Key components:
- **Firemap** — operational web tool for fire behavior modeling and forecasting
- **WIFIRE Edge** — middleware integrating disparate edge sensing products
- **WXmap** — integrated weather data tool for fire risk prediction
- **BurnPro3D** — 3D modeling for planning prescribed burns

The motivating event was the May 2014 San Diego County fires: 14 fires burned 26,000 acres with over $60M in damage and 1 fatality. Wildfire management requires integrating sensor/satellite data, institutional data (fire perimeter maps, fuel maps), and public social media data (Twitter) simultaneously in real time — a big data integration challenge. [Cross-ref: topics/data_integration_platforms.md — data integration process and WIFIRE]
