# Retail Sales Data Warehouse — Star Schema Design & Implementation

A practical data warehousing project designing and deploying a multi-tier star schema warehouse for an e-commerce electronics retailer using **PostgreSQL** in **Docker**, CSV staging, dimension loading, and fact table aggregations.

---

## 📌 Executive Summary

Modern retail organizations require centralized data warehouses to monitor sales performance across customer demographics, product categories, and temporal periods. This project designs and populates a containerized analytical warehouse:
1. **Star Schema Dimensional Design**: Designs dimension tables (`DimDate`, `DimProduct`, `DimCustomerSegment`) with surrogate primary keys and a centralized fact table (`FactSales`) recording transaction revenue and unit volume.
2. **Containerized Infrastructure**: Runs PostgreSQL using Docker Compose (`docker-compose.yml`) for reproducible, isolated database environments.
3. **Data Staging & Bulk Ingestion**: Ingests dimensional datasets (`DimDate.csv`, `DimProduct.csv`, `DimCustomerSegment.csv`) and fact records (`FactSales.csv`) into PostgreSQL.
4. **Graded Task Evidence**: Verifies table schemas, row counts, and data loading via terminal screenshots (Task 9 through Task 12).

---

## 📁 Project Structure

```text
c9_data_warehouse_fundamentals_practice_project/
├── README.md                                                   # Project documentation
├── docker-compose.yml                                          # PostgreSQL container definition
├── c9_m3_practice_project_designing_implementing_data_warehouse.md # Lab manual
├── DimDate.csv                                                 # Date dimension dataset
├── DimProduct.csv                                              # Product dimension dataset
├── DimCustomerSegment.csv                                      # Customer segment dimension
├── FactSales.csv                                               # Sales transactions fact table
└── 9-DimDate.png ... 12-FactSales.png                           # Verification screenshots
```

---

## 🛠️ Technology Stack

- **Data Warehouse Engine**: PostgreSQL 13+
- **Containerization**: Docker & Docker Compose
- **Design Pattern**: Kimball Star Schema (Fact and Dimension Tables)
