# Urban Analytics & Socioeconomic SQL Study — Chicago Open Data Portal

An end-to-end data analytics and advanced SQL project analyzing real-world municipal datasets from the **City of Chicago Data Portal** using **Python**, **SQLAlchemy**, **SQLite**, and **pandas**.

---

## 📌 Executive Summary

Municipal governance requires cross-domain data analysis to allocate educational resources, combat violent crime, and understand socioeconomic hardship. This project integrates three distinct city-wide open datasets:
1. **Chicago Socioeconomic Indicators**: Tracks poverty rate, per-capita income, unemployment, and the composite Hardship Index across 78 Chicago community areas.
2. **Chicago Public Schools Progress Reports**: Measures academic achievement, safety scores, student attendance rates, and collegiate readiness.
3. **Chicago Crime Statistics**: Detailed incident records encompassing crime classifications (theft, narcotics, kidnapping, homicide), location descriptions, and arrest rates.

---

## 📁 Project Contents

```text
c5_databases_and_sql_for_data_science_final_project/
├── README.md                            # Comprehensive project overview & methodology
└── mod5-final-project-v2.ipynb          # Complete interactive Jupyter notebook with executed SQL queries
```

---

## 🛠️ Technology Stack & Analytical Methods

| Tool | Application |
|---|---|
| **SQL Engine** | SQLite / IBM Db2 with `%sql` and `%%sql` Jupyter magic commands |
| **Data Ingestion** | `pandas.read_csv()` loading into relational tables |
| **Advanced SQL** | Subqueries, Multi-table `JOIN`s, Aggregate functions (`AVG`, `COUNT`, `SUM`), Scalar functions, Windowing |
| **Analytical Scope** | Correlating low per-capita income community areas with elevated crime rates and public school safety scores |
