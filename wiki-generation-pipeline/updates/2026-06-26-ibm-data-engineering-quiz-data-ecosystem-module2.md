# Quiz: The Data Engineering Ecosystem

## Overview

This quiz covers the foundational concepts from **Module 2: The Data Engineering Ecosystem**, including data integration tools, data types and file formats, data sources, relational databases, and querying languages.

---

## Questions & Answers

---

### Question 1

**Automated tools, frameworks, and processes for all stages of the data analytics process are part of the Data Engineer's ecosystem. What role do data integration tools play in this ecosystem?**

| Option | Correct? |
|--------|----------|
| Store high-volume day-to-day operational data in data repositories | ❌ |
| Conduct complex data analytics | ❌ |
| **Combine data from multiple sources into a unified view that is accessed by data consumers to query and manipulate data** | ✅ |
| Cover the entire journey of data from source to destination | ❌ |

> **Explanation:** Data integration tools are specifically designed to pull data from disparate sources and consolidate it into a unified, queryable view. This is distinct from data storage (repositories), analytics execution, or end-to-end pipeline orchestration.

---

### Question 2

**Which of these data sources is an example of semi-structured data?**

| Option | Correct? |
|--------|----------|
| Emails | ❌ |
| Documents | ❌ |
| **Network and web logs** | ✅ |
| Social media feeds | ❌ |

> **Explanation:** Semi-structured data has some organizational properties (like tags or key-value pairs) but does not conform to a strict relational schema. Network and web logs contain structured metadata fields (timestamps, IP addresses, status codes) embedded in free-form text, making them semi-structured. Emails and documents are typically unstructured.

---

### Question 3

**Which one of the provided file formats is commonly used by APIs and Web Services to return data?**

| Option | Correct? |
|--------|----------|
| Delimited file | ❌ |
| XLS | ❌ |
| **JSON** | ✅ |
| XML | ❌ |

> **Explanation:** JSON (JavaScript Object Notation) is the dominant format for API and web service responses due to its lightweight syntax, human readability, and native compatibility with web technologies. While XML was historically common in web services (e.g., SOAP), JSON is the modern standard for REST APIs.

---

### Question 4

**What is one example of the relational databases discussed in the video?**

| Option | Correct? |
|--------|----------|
| **SQL Server** | ✅ |
| Flat files | ❌ |
| XML | ❌ |
| Spreadsheet | ❌ |

> **Explanation:** SQL Server (Microsoft SQL Server) is a relational database management system (RDBMS) that organizes data into tables with defined schemas and relationships. Flat files, XML, and spreadsheets are file-based storage formats, not relational database systems.

---

### Question 5

**Which of the following languages is one of the most popular querying languages in use today?**

| Option | Correct? |
|--------|----------|
| R | ❌ |
| Java | ❌ |
| **SQL** | ✅ |
| Python | ❌ |

> **Explanation:** SQL (Structured Query Language) is the standard language for querying and managing relational databases and remains one of the most widely used languages across the entire data ecosystem. While Python and R are popular for data analysis and machine learning, SQL is the primary *querying* language for structured data.

---

## Key Takeaways

- **Data integration tools** unify data from multiple sources into a single view for consumers — they are not storage or analytics engines themselves.
- **Semi-structured data** (e.g., logs, JSON, XML files) sits between structured (tabular) and unstructured (free text, media) data.
- **JSON** is the standard file format returned by modern REST APIs and web services.
- **SQL Server** is an example of an RDBMS; flat files and spreadsheets are not databases.
- **SQL** is the dominant querying language for structured/relational data across virtually all data platforms.
