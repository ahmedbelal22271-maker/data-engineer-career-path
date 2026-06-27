# Metadata and Metadata Management

> **LTHP Status:** NEW — Module 2 ecosystem expansion.
> **Source file:** `metadata-management.md` (primary, 138 lines)

## Overview

Metadata is data that provides information about other data. Within databases, data warehousing, business intelligence systems, and data repositories, metadata is what makes data discoverable, governable, and usable at scale. Without it, data assets become siloed, undocumented, and effectively invisible to the people and systems that need them.

---

## Types of Metadata

There are three main types of metadata relevant to data engineering.

### 1. Technical Metadata

Technical metadata defines the data structures in data repositories or platforms from a technical perspective. In a data warehouse, technical metadata includes table-level information (table names, number of columns, number of rows) and data catalogs — an inventory of tables containing the names of each database, every column in each database, every table each column belongs to, and the data type of each column.

> **Note:** For relational databases, technical metadata is typically stored in specialized internal tables called the **System Catalog**.

### 2. Process Metadata

Process metadata describes the processes that operate behind business systems such as data warehouses, accounting systems, or CRM tools. Critical enterprise systems that collect and process data from various sources must be monitored for failures and performance anomalies. Process metadata tracks:

- Process start and end times
- Disk usage
- Data movement (source and destination)
- Number of concurrent users accessing the system

This metadata is invaluable for troubleshooting pipeline failures and optimizing workflows and ad hoc queries.

### 3. Business Metadata

Business metadata is information about data described in readily interpretable, business-friendly terms. It serves users who need to discover and analyze data across and outside the enterprise. Business metadata captures how the data is acquired, what the data is measuring or describing, and the relationships between the data and other data sources.

Business metadata also serves as documentation for the entire data warehouse system, bridging the gap between technical teams and business stakeholders.

---

## Metadata Management

Metadata management involves developing and administering policies and processes to ensure information can be accessed, integrated from various sources, and appropriately shared across the enterprise.

### The Data Catalog

A **Data Catalog** is the critical component of metadata management. It provides a reliable, user-friendly, web-based interface for organizing and searching key data attributes (e.g., `CustomerName`, `ProductType`). The data catalog is central to **Data Governance**, enabling organizations to inventory and efficiently organize their data systems.

### Key Benefits of Metadata Management

- **Enhances data discovery** — users can find relevant data assets quickly
- **Improves repeatability** — processes are documented and reproducible
- **Strengthens governance** — ownership, policies, and accountability are clear
- **Facilitates data access** — reduces friction for both technical and business users

### Data Lineage

Metadata management enables **data lineage** — the ability to track the origin, transformation, and movement of data across systems. Data lineage is essential for:

- Tracing data errors back to their root cause
- Understanding the impact of upstream changes on downstream consumers
- Meeting regulatory and compliance requirements

---

## Data Governance

Metadata management is foundational to data governance. Key focus areas include:

| Focus Area | Description |
|---|---|
| **Availability** | Data is accessible when and where it is needed |
| **Usability** | Data can be effectively understood and used |
| **Consistency** | Data remains consistent across systems and time |
| **Data Integrity** | Data accuracy is maintained throughout its lifecycle |
| **Data Security** | Data is protected from unauthorized access |

Governance processes ensure effective data management, establish accountability for poor data quality, and define how data is used across the organization.

---

## Popular Metadata Management Tools

| Tool | Vendor |
|---|---|
| IBM InfoSphere Information Server | IBM |
| IBM Watson Knowledge Catalog | IBM |
| CA Erwin Data Modeler | Broadcom |
| Oracle Warehouse Builder | Oracle |
| Oracle Enterprise Metadata Management (OEMM) | Oracle |
| SAS Data Integration Server | SAS |
| Talend Data Fabric | Talend |
| Alation Data Catalog | Alation |
| SAP Information Steward | SAP |
| Microsoft Azure Data Catalog | Microsoft |
| Informatica Enterprise Data Catalog | Informatica |
| Adaptive Metadata Manager | Adaptive |
| Unifi Data Catalog | Unifi |
| data.world | data.world |

---

## Summary

| Concept | Key Point |
|---|---|
| Metadata | Data that provides information about other data |
| Technical metadata | Defines data structures; stored in the System Catalog for relational DBs |
| Process metadata | Tracks pipeline execution details; used for monitoring and troubleshooting |
| Business metadata | Describes data in business terms; serves as data warehouse documentation |
| Data Catalog | Central tool for metadata management; enables discovery and governance |
| Data Lineage | Tracks data origin and movement; critical for debugging and compliance |
| Data Governance | Ensures availability, usability, consistency, integrity, and security of data |
