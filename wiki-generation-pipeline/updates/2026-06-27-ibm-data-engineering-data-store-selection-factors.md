# Module 3: Data Engineering Lifecycle — Factors for Selecting and Designing Data Stores

## Overview

A **data store** (or data repository) is any system used to collect, organize, and isolate data for business operations, reporting, or analysis. It may take the form of a database, data warehouse, data mart, big data store, or data lake.

## Five Primary Factors

| Factor | Key Questions |
|---|---|
| **1. Type of Data** | Structured → RDBMS; Semi/unstructured → NoSQL. Match the database model to how data is *accessed*, not just how it is *structured*. |
| **2. Volume of Data** | Large raw/unstructured → Data Lake; High-volume + high-velocity → Big Data Repository (distributed, parallel processing). |
| **3. Intended Use of Data** | OLTP (normalize, fast read/write) vs OLAP (denormalize, complex queries). Drives scalability and normalization decisions. |
| **4. Storage Considerations** | Performance (throughput/latency), Availability, Integrity, Recoverability — all must be explicitly designed for. |
| **5. Privacy, Security & Governance** | Layered security (access control, multizone encryption, data management, monitoring). Regulations: GDPR, CCPA, HIPAA. |

## NoSQL Sub-Types

| Type | Best For | Avoid When |
|---|---|---|
| Key-Value | Fast lookups, caching | Complex queries needed |
| Document | Flexible, nested data | Complex multi-operation transactions |
| Column | Large-scale analytical reads | Frequent updates to individual records |
| Graph | Connected, relationship-heavy data | High-volume transactional analytics |

## Key Takeaways

- **Structured data → RDBMS; Semi/unstructured data → NoSQL**
- Data lakes for raw, schema-less volumes; big data stores for distributed high-velocity workloads
- OLTP: normalize; OLAP: denormalize
- Performance, availability, integrity, recoverability are core storage properties
- Privacy/security must be built in from the start, not retrofitted
