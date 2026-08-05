**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 1:** Extract, Transform, Load (ETL) Overview

# Practice Quiz: ETL and ELT Processes

## Question 1

**ETL process consists of Extract > Transform > Load. Which of these three processes is also known as data wrangling?**

| Option | Correct? |
|--------|----------|
| Data wrangling is a term for another data warehouse process | ✗ |
| **Transform** | **✓ CORRECT** |
| Load | ✗ |
| Extraction | ✗ |

**Answer:** Transform

**Analysis:** Data transformation is also known as data wrangling. From the ETL Fundamentals lesson: "Data transformation, also known as data wrangling, means processing data to make it conform to the requirements of both the target system and the intended use case for the curated data." Wrangling implies the iterative, hands-on work of cleaning, restructuring, and enriching raw data — which is exactly what the Transform step does.

---

## Question 2

**What is the main difference between the ELT and ETL process?**

| Option | Correct? |
|--------|----------|
| Data types | ✗ |
| ETL used primarily for cloud | ✗ |
| ELT is only used for analyzing | ✗ |
| **Order of stages** | **✓ CORRECT** |

**Answer:** Order of stages

**Analysis:** The fundamental difference is the order in which transformation happens relative to loading. ETL = Extract → **Transform** → Load (transform before loading). ELT = Extract → Load → **Transform** (transform after loading). From the Comparing ETL and ELT lesson: "Differences between ETL and ELT, for one thing, the transformations happen in a different order."

---

## Question 3

**Transformations for ETL happen in the data pipeline. Where do transformations happen for ELT?**

| Option | Correct? |
|--------|----------|
| Source environment | ✗ |
| Load process | ✗ |
| Extraction process | ✗ |
| **Destination environment** | **✓ CORRECT** |

**Answer:** Destination environment

**Analysis:** In ELT, raw data is loaded first into the destination (data lake, data warehouse), and transformations happen there afterward. From the Comparing ETL and ELT lesson: "Transformations for ELT are decoupled from the data pipeline and happen in the destination environment at will." The destination (e.g., a data lake or cloud warehouse) has the compute power to run transformations on demand.

---

## Question 4

**Which of the following raw data sources is related to sales?**

| Option | Correct? |
|--------|----------|
| Merchandise data | ✗ |
| Survey data | ✗ |
| Analog data | ✗ |
| **Transactional data** | **✓ CORRECT** |

**Answer:** Transactional data

**Analysis:** Transactional data comes from business, financial, real estate, and point of sale (POS) transactions — these are sales events. From the Data Extraction Techniques lesson: "transactional data from business, financial, real estate, and point of sale or POS transactions." Merchandise data is about products, not the sales themselves. Survey data is about opinions. Analog data is about audio/video formats.

---

## Question 5

**Which of the following data transformation techniques will be suitable for 'unlike' data sources?**

| Option | Correct? |
|--------|----------|
| Filtering, sorting, aggregation | ✗ |
| Cleaning | ✗ |
| Data structuring | ✗ |
| **Joining or merging** | **✓ CORRECT** |

**Answer:** Joining or merging

**Analysis:** "Unlike" data sources means different, unrelated data sources (e.g., a CRM database and an e-commerce platform). The transformation that combines them is joining/merging. From the ETL Fundamentals lesson: "Joining disparate data sources: merging related data." The enrichment gives a concrete example: joining a `customers` table (from a CRM) with an `orders` table (from e-commerce) on `customer_id`. Filtering, cleaning, and structuring operate on a single dataset — only joining combines multiple sources.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | All questions | Source verification | All answers verified against enriched lesson files (c8_m1_etl_fundamentals.md, c8_m1_comparing_etl_and_elt.md, c8_m1_data_extraction_techniques.md, c8_m1_intro_data_transformation_techniques.md) | HIGH |

<!-- EXTRACTION_CHECKLIST: 5 questions extracted, 5 questions in output -->
