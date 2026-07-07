# Big Data Characteristics — Deep Dive

> **Source:** UCSD Big Data Specialization — Course 1, Module 3 (Characteristics of Big Data)

## Overview

The original "Three V's" (Volume, Velocity, Variety) were first articulated by **Doug Laney** in a 2001 META Group research note titled *"3-D Data Management: Controlling Data Volume, Velocity and Variety."* Gartner later acquired META Group and the Three V framework became the most widely cited characterization of Big Data. Modern frameworks extend this to five or more V's. This page provides a detailed examination of each characteristic.

> **Core insight (UCSD):** "A precise specification of 'big' is elusive. What is considered big for one organization may be small for another. What is large-scale today will likely seem small-scale in the near future; petabyte is the new terabyte." Big Data is defined not just by size but by the combination of **scale, distribution, diversity, and timeliness** — its **complexity** matters as much as its volume. [Cross-ref: topics/big_data_foundations.md — What Launched the Big Data Era]

---

## Volume — The Scale Dimension

Volume is the sheer size of data. It originates from large datasets being shared and many small data pieces/events collected over time.

**Data generation per minute (circa 2013-2015 benchmarks):**
- Email: 204 million messages sent
- Facebook: 200,000 photos uploaded, 1.8 million likes generated
- YouTube: 1.3 million videos viewed, 72 hours of video uploaded

**Storage unit progression:**
| Unit | Scale | Reference |
|------|-------|-----------|
| Megabyte (MB) | 10⁶ bytes | ~100 MB = a couple of encyclopedias |
| Gigabyte (GB) | 10⁹ bytes | A DVD is ~5 GB |
| Terabyte (TB) | 10¹² bytes | ~300 hours of good quality video |
| Petabyte (PB) | 10¹⁵ bytes | CERN's LHC generates ~15 PB/year |
| Exabyte (EB) | 10¹⁸ bytes | — |
| Zettabyte (ZB) | 10²¹ bytes | 1 trillion gigabytes |
| Yottabyte (YB) | 10²⁴ bytes | — |
| Ronnabyte (RB) | 10²⁷ bytes | SI official since 2022 |

**Astronomical Scale — Powers of Ten Analogy:**
The UCSD specialization draws a parallel between the Powers of Ten scaling of the universe (from subatomic to cosmic) and the exponential scaling of data sizes:

| Unit | Scale | Visual Analogy |
|------|-------|----------------|
| Megabyte | 10⁶ | Human scale (1 m) |
| Gigabyte | 10⁹ | Earth's diameter (10⁷ m) |
| Terabyte | 10¹² | Earth–Moon distance (10⁸ m) |
| Petabyte | 10¹⁵ | Earth–Sun distance (10¹¹ m) |
| Exabyte | 10¹⁸ | Solar system diameter (10¹³ m) |
| Zettabyte | 10²¹ | Milky Way diameter (10²¹ m) |
| Yottabyte | 10²⁴ | Galaxy cluster scale |
| Brontobyte | 10²⁷ | Observable universe scale |

*Analogy from the Eames "Powers of Ten" (1977) film. The same techniques that work at megabyte scale break down at petabyte or zettabyte scale.*

**Benchmark:** In 2013, Yahoo announced managing 600 PB of data across its Hadoop clusters — illustrating the volume challenge even before the current zettabyte era.

**Challenges of Volume:**
- **Storage** — in-house vs. cloud, cost, infrastructure decisions
- **Retrieval and movement** — networking, bandwidth constraints
- **Processing** — analytical methods that don't scale to massive volumes; memory, processing power, I/O bottlenecks
- **Strategic** — need a holistic strategy for cost-effective large-scale data processing

---

## Velocity — The Speed Dimension

Velocity is the speed at which data accumulates — a continuous process. Near or real-time streaming technologies process information at the speed it is generated.

**Key frameworks for velocity:**
- **Apache Storm** — open-source framework for real-time processing of high-velocity data; complements Hadoop's batch-oriented design
- **Apache Spark Streaming** — micro-batch processing engine for stream workloads
- **Apache Kafka** — distributed event streaming platform for high-throughput data pipelines

**In-situ processing** — computation is brought to where data is generated or stored, rather than moving data to compute resources. Critical for real-time sensor workloads (e.g., aircraft engine monitoring) where data movement latency is unacceptable.

---

## Variety — The Diversity Dimension

Variety is the diversity of data in both type and source. Data arrives along four axes:

1. **Structural** — EKG waveform vs. news article (different organization)
2. **Media** — audio vs. transcript (different modality)
3. **Semantic** — different units, measurement assumptions, or contextual meanings
4. **Availability** — real-time vs. stored, polled vs. pushed

Email is a hybrid entity exhibiting all four axes simultaneously.

---

## Veracity — The Quality Dimension

Veracity is the quality, accuracy, and trustworthiness of data. Core attributes:
- **Consistency** — data means the same thing across all systems
- **Completeness** — no critical fields missing
- **Integrity** — data has not been corrupted
- **Ambiguity** — data is interpretable in only one clear way

**Additional quality factors (UCSD):** Accuracy, trustworthiness/reliability of source, how the data was generated (collection process affects inherent quality), and contextual meaningfulness (whether data is meaningful with respect to the model that analyzes it).

The core challenge: an estimated 80% of data is unstructured, making it inherently harder to validate, categorize, and trust. The principle is **"junk in equals junk out"** — the results of analysis are only as good as the data being analyzed.

**Why veracity degrades at scale:** Unstructured internet content is created without quality controls; high-velocity data leaves little or no time for ETL quality assurance. The faster data must flow, the less time is available to validate it.

### Case Study: Google Flu Trends (2013)

A canonical example of **"big data hubris"** — the assumption that volume alone compensates for quality problems. Google Flu Trends estimated almost **twice as many flu cases** for January 2013 as the CDC reported. The cause: the system relied on search query data without adequately accounting for uncertainties. Heightened media attention to a severe flu season inflated search volumes independently of actual case counts, producing a massive overestimate. The tool was formally discontinued in 2015. [Cross-ref: topics/big_data_foundations.md — Veracity]

### Case Study: Amazon Banana Slicer Reviews

Amazon reviews for a banana slicer illustrate data that looks high-quality (five-star reviews) but carries zero purchasing signal. Reviewers gave satirical five-star ratings ("saved my marriage," "my parole officer recommended it because I'm not allowed around knives") — content that an automated demand-forecasting system would misinterpret, potentially recommending increased inventory based on fake demand signals.

### Data Provenance

Provenance — the documented history of where data came from and how it was transformed — becomes critical as volume and velocity increase. Without provenance, errors cannot be traced back to their source. This is increasingly complex to maintain across multi-step pipelines but essential for veracity management.

---

## Value — The Purpose Dimension

Value is the ability to turn data into something meaningful and actionable. Types of value:
- **Business value** — better decisions, competitive advantage
- **Medical value** — improved patient outcomes, drug discovery
- **Social value** — public policy improvements
- **Personal value** — customer satisfaction

All other V's are properties of the data; value is the *purpose* behind working with it. Without a value objective, the other dimensions are simply challenges without a destination.

### Case Study: Catch the Pink Flamingo

The recurring case study throughout the UCSD specialization: **Eglence Inc.** publishes a multi-user mobile game called *Catch the Pink Flamingo* played by millions worldwide. Players catch special pink flamingos on a world map, form groups, and compete. The game exhibits all five V's:

| V | Manifestation |
|---|---|
| **Volume** | High volumes of player data, game data, and Twitter data |
| **Variety** | Three data source types: mobile app events (machine), Twitter posts (people), registration/stat records (organizational) |
| **Velocity** | Real-time data streams from mobile app, website, and social media |
| **Veracity** | Most users enter inaccurate demographic info during registration |
| **Valence** | Networks of players connected through groups, shared missions, and social media communities |

The Twitter hashtag **#CatchThePinkFlamingo** receives 200,000+ mentions per day worldwide. This scenario recurs throughout the specialization and forms the basis of the Course 6 Capstone Project. [Cross-ref: topics/big_data_specialization_ucsd.md — Course 6 Capstone]

---

## Valence — The Connectedness Dimension

**Origin of the term (chemistry analogy):** In chemistry, atoms have core electrons (inner shells) and valence electrons (outermost shell). Valence electrons have the highest energy level and are responsible for bonding with other atoms — higher valence means greater bonding capacity. Analogously, in Big Data, **Valence** measures how data entities connect and bond with one another.

Valence is the density of connections between data points. Measured as **graph density**: 
```
Valence = (actual connections) / (maximum possible connections)
```
For an undirected graph of n nodes, maximum possible edges = n(n-1)/2. A valence of 1.0 means every possible connection exists; a valence near 0 means sparse connectivity.

**Valence is dynamic** — connectivity increases over time. As more data is collected, connections between data items grow, creating emergent behaviors (new groups, coalitions, community structure shifts) that were not predictable from the initial network state.

As connectivity increases, new challenges arise:
- **Algorithmic inefficiency** on dense graphs — standard graph algorithms (shortest path, community detection) scale poorly as density increases
- **Modeling dynamic change** — connections appear and disappear over time, requiring predictive models of future connectivity
- **Event detection** — local cohesion bursts signal emergent behavior (e.g., a viral trend on Twitter); system-wide polarization can arise from local interactions

**Interaction with other V's:**
- **Volume × Valence:** As data items grow, possible connections grow quadratically — making valence management increasingly complex
- **Velocity × Valence:** Fast-arriving data can rapidly alter connectivity structure, making real-time tracking difficult
- **Variety × Valence:** Connections can span heterogeneous data types, further complicating analysis

---

## The Volume-Velocity-Variety Trilemma

The three original V's create tension: systems optimized for high volume often sacrifice velocity (batch processing). Systems optimized for high velocity often restrict variety (schema-on-write). Systems optimized for high variety may struggle with volume (document stores). The Lambda Architecture (batch + speed layers) and Kappa Architecture (unified streaming) are architectural responses to this trilemma.

[Cross-ref: topics/big_data_foundations.md — 5 V's overview, distributed computing principles]
[Cross-ref: topics/streaming_data_platforms.md — Kafka, Spark Streaming, Kinesis]
