> **Course 9:** Data Warehouse Fundamentals
> **Module 1:** An Introduction to Data Warehouses, Data Marts, and Data Lakes

# Practice Quiz: An Introduction to Data Warehouses, Data Marts, and Data Lakes

<mark style="background-color: rgba(200, 230, 201, 0.4);">NEW</mark>

**Type:** Practice Quiz
**Time:** 10 min
**Due:** Jul 27, 11:59 PM EEST
**Attempts:** Unlimited

---

## Question 1

**What is a data mart?**

| Option | Correct? |
|--------|----------|
| Data warehouse | ✗ |
| Pool of raw data | ✗ |
| Data Lake | ✗ |
| **Isolated part of the larger enterprise data warehouse** | **✓ CORRECT** |

**Answer:** Isolated part of the larger enterprise data warehouse

[ENRICHED: analysis — A data mart is defined in c9_m1_data_marts_overview.md as "an isolated part of the larger enterprise data warehouse that is specifically built to serve a particular business function, purpose, or community of users." The other options are incorrect: a "data warehouse" is the larger system from which a data mart is derived; a "pool of raw data" describes a data lake; and a "data lake" is a storage repository for raw, unprocessed data in its native format — not a subset of a warehouse. Data marts are purpose-built for specific departments (finance, marketing, sales) and contain only the relevant data for that team, making them smaller, faster, and more focused than the full enterprise data warehouse.]

---

## Question 2

**What do data warehouse systems support? (Select 3 correct answers.)**

| Option | Correct? |
|--------|----------|
| **Application of artificial intelligence** | **✓ CORRECT** |
| **Data mining** | **✓ CORRECT** |
| Data cleansing | ✗ |
| **Application of machine learning** | **✓ CORRECT** |

**Answer:** Application of artificial intelligence, Data mining, Application of machine learning

[ENRICHED: analysis — According to c9_m1_data_warehouse_overview.md: "Data warehouse systems support data mining, including the application of artificial intelligence and machine learning." Data cleansing is NOT a capability of the warehouse itself — it is part of the ETL (Extract, Transform, Load) process that occurs BEFORE data is loaded into the warehouse. Data cleansing happens in the staging area during the transform phase, not as an analytical function of the warehouse system. The warehouse's role is to store already-cleaned data and enable analytics on it.]

---

## Question 3

**Select the answer that describes cloud-based data warehouses.**

| Option | Correct? |
|--------|----------|
| **Cloud-based data warehouses offer scalability, pay-per-use economics and optionally, as fully managed services.** | **✓ CORRECT** |
| Cloud-based data warehouses require the same investment as an appliance-based data warehouse. | ✗ |
| Cloud-based data warehouses require more management than on-premises data warehouses. | ✗ |
| Cloud-based data warehouses exist as pre-integrated bundles of hardware and software that provide high performance for workloads and low maintenance overhead. | ✗ |

**Answer:** Cloud-based data warehouses offer scalability, pay-per-use economics and optionally, as fully managed services.

[ENRICHED: analysis — From c9_m1_data_warehouse_overview.md: "Cloud Data Warehouses, frequently called CDWs, have gained popularity, where organizations don't purchase hardware or install warehousing software... organizations access data warehouses as a scalable, pay-as-you-go service." From c9_m1_popular_data_warehouse_systems.md: cloud deployments offer "the benefits of cloud scalability and pay-per-use economics, and in many cases, deliver their data warehouses as fully managed services." The other options are incorrect: cloud warehouses are typically cheaper than appliance-based warehouses (no upfront hardware investment); they require LESS management than on-premises (fully managed means no patching, no hardware maintenance); and the description of "pre-integrated bundles of hardware and software" defines an appliance-based warehouse, not a cloud-based one.]

---

## Question 4

**Which industries use data warehouses?**

| Option | Correct? |
|--------|----------|
| **Almost every industry** | **✓ CORRECT** |
| Some industries | ✗ |
| Only the IT industry | ✗ |
| None of the above | ✗ |

**Answer:** Almost every industry

[ENRICHED: analysis — From c9_m1_data_warehouse_overview.md: "Data warehouses are a part of almost every industry, including e-commerce, transportation, medical, banking and fin-tech, social media, and governments." This broad adoption exists because virtually every industry generates data that needs to be analyzed for decision-making, reporting, and compliance. The examples listed span healthcare, finance, retail, logistics, government, and technology — demonstrating that data warehousing is not limited to any single sector.]

---

## Question 5

**Which statement best defines a data lake?**

| Option | Correct? |
|--------|----------|
| A storage repository that stores data processed for a specific need | ✗ |
| An isolated part of the larger enterprise data warehouse that is specifically built to serve a particular business function | ✗ |
| **A pool of raw data** | **✓ CORRECT** |
| None of the above | ✗ |

**Answer:** A pool of raw data

[ENRICHED: analysis — From c9_m1_data_lakes_overview.md: "a data lake is a pool of raw data where each data element is given a unique identifier and is tagged with metatags for further use." The other options are incorrect: "A storage repository that stores data processed for a specific need" describes a data warehouse (which stores transformed, curated data for specific use cases); "An isolated part of the larger enterprise data warehouse that is specifically built to serve a particular business function" is the exact definition of a data mart. A data lake's defining characteristic is that it stores data in its raw, native format without requiring predefined schemas or transformation before storage.]

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Question 1 | Analysis | Explained why each incorrect option is wrong with definitions from enriched lesson files | HIGH | c9_m1_data_marts_overview.md |
| 2 | Question 2 | Analysis | Distinguished warehouse analytics capabilities from ETL data cleansing process | HIGH | c9_m1_data_warehouse_overview.md |
| 3 | Question 3 | Analysis | Contrasted cloud vs appliance vs on-premises warehouse characteristics | HIGH | c9_m1_data_warehouse_overview.md, c9_m1_popular_data_warehouse_systems.md |
| 4 | Question 4 | Analysis | Listed specific industries from enriched content as evidence | HIGH | c9_m1_data_warehouse_overview.md |
| 5 | Question 5 | Analysis | Mapped each incorrect option to the correct term (warehouse, data mart) | HIGH | c9_m1_data_lakes_overview.md |

<!-- EXTRACTION_CHECKLIST: 5 questions, 5 answers verified against enriched MD files -->
