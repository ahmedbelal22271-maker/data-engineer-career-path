# Multi-Source Data Aggregator — World Bank & Public APIs

A practical data ingestion and integration project combining tabular CSV datasets and RESTful JSON APIs to produce unified statistical reports using **Python**, **pandas**, and **Requests**.

---

## 📌 Executive Summary

Real-world data pipelines must ingest from disparate sources with varying latency, schemas, and formats. This project demonstrates end-to-end data aggregation:
1. **CSV Data Extraction**: Ingests World Bank macro-economic indicators from local CSV storage, parses data types, handles null values, and melts wide-format year columns into tidy format.
2. **REST API Ingestion**: Issues authenticated HTTP GET requests to public REST endpoints, extracts dynamic JSON responses, and normalizes nested objects using `pd.json_normalize()`.
3. **Data Integration & Cleaning**: Merges heterogeneous feeds on standard ISO country codes, cleans anomalies, and harmonizes timestamps.
4. **Descriptive Analytics & Summary Reporting**: Computes multi-dimensional aggregations, correlation coefficients, and exports structured CSV summaries.

---

## 📁 Project Structure

```text
course2-data-aggregator/
├── README.md                            # Project overview & execution instructions
├── data-aggregator.ipynb                # Complete interactive analysis notebook
└── world_bank_folder/                   # Raw World Bank indicator datasets
```

---

## 🛠️ Technology Stack

- **Python 3.10+**
- **pandas** (DataFrames, reshaping, melting, groupby aggregations)
- **requests** (REST API querying & JSON parsing)
- **Jupyter Notebook** (Interactive reporting)
