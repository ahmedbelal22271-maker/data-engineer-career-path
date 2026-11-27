# Coffee Shop Relational Database — Design, ERD & Advanced SQL

A comprehensive relational database design and engineering project modeling enterprise operations for a multi-location coffee shop chain using **Entity-Relationship Diagrams (ERD)**, **PostgreSQL/MySQL DDL scripts**, materialized views, and security role permissions.

---

## 📌 Executive Summary

Retail coffee chains manage high transaction volumes across multiple storefronts, requiring clean relational data models to prevent anomalies and track inventory, sales staff, and customer loyalty. This project implements an end-to-end database design:
1. **Conceptual & Logical Data Modeling**: Analyzes business requirements to draft an Entity-Relationship Diagram (ERD) defining entities (`staff`, `location`, `product`, `sales_transaction`, `customer`).
2. **Schema Generation & Normalization**: Normalizes tables to Third Normal Form (3NF), enforces primary and foreign key constraints, and generates relational DDL scripts (`GeneratedScript.sql`).
3. **Data Ingestion & Integrity**: Ingests realistic operational transaction history (`CoffeeData.sql`).
4. **Database Views & Materialized Views**: Constructs production views (`staff_locations_view`) and materialized views (`product_info_m-view`) to optimize recurring analytical queries without repeated table joins.
5. **Graded Task Submissions**: Step-by-step verification screenshots from Task 1 through Task 10 proving schema creation, constraint validation, view queries, and role assignments.

---

## 📁 Project Structure

```text
c4_coffee_shop_database_final_project/
├── README.md                            # Project documentation & execution guide
├── final project.pdf                    # Official project specification document
├── CoffeeData.sql                       # Complete transactional database dump
├── GeneratedScript.sql                  # Automated relational schema DDL script
├── generated_erd_sql.sql                # SQL DDL generated directly from ERD modeling tool
├── product_info_m-view.csv              # Exported materialized view query output
├── staff_locations_view.csv             # Exported staff locations view output
├── test.py                              # Verification script for database queries
└── Task1.png ... Task10.png             # Graded task verification screenshots
```

---

## 🛠️ Technology Stack

- **Relational DBMS**: PostgreSQL / MySQL
- **Data Modeling**: ERD Diagramming & Relational Schema Normalization (3NF)
- **SQL DDL & DML**: Constraints (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `CHECK`), Views & Materialized Views
- **Python**: Database verification testing
