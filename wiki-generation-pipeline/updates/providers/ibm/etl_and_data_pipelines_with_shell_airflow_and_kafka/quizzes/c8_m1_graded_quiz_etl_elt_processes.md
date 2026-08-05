**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 1:** Extract, Transform, Load (ETL) Overview

# Graded Quiz: ETL and ELT Processes

## Question 1

**ETL process consists of Extract > Transform > Load. Which of the three processes is also known as data wrangling?**

| Option | Correct? |
|--------|----------|
| Load | ✗ |
| **Transform** | **✓ CORRECT** |
| Extraction | ✗ |
| Data wrangling is a term for another data warehouse process | ✗ |

**Answer:** Transform

**Analysis:** Data transformation is also known as data wrangling. From c8_m1_etl_fundamentals.md: "Data transformation, also known as data wrangling, means processing data to make it conform to the requirements of both the target system and the intended use case for the curated data."

---

## Question 2

**The ELT process has no information loss. What is the main reason for this benefit?**

| Option | Correct? |
|--------|----------|
| **Data is acquired and directly loaded, as-is, into its destination environment.** | **✓ CORRECT** |
| Data source integration | ✗ |
| There is a separation between moving and processing data. | ✗ |
| It separates the data pipeline from processing. | ✗ |

**Answer:** Data is acquired and directly loaded, as-is, into its destination environment.

**Analysis:** ELT loads raw data without transforming it first, so nothing is discarded. From c8_m1_intro_data_transformation_techniques.md: "with ELT, all the original information content is left intact because the data is simply copied over as is." The key phrase is "as-is" — no transformation means no information loss.

---

## Question 3

**Which of the following in an ELT process best compares to the "Staging area" in the ETL process?**

| Option | Correct? |
|--------|----------|
| **Data lake in ELT process** | **✓ CORRECT** |
| Database servers | ✗ |
| Transformed data storage | ✗ |
| Storage for source data in the ELT process | ✗ |

**Answer:** Data lake in ELT process

**Analysis:** Both staging areas and data lakes hold raw data temporarily, but differ in accessibility. From c8_m1_comparing_etl_and_elt.md: "the staging area fits the description of a data lake, which is a modern self-serve repository for storing and manipulating raw data." The staging area is engineering-internal; the data lake is shared across the organization.

---

## Question 4

**Which of the following pain points does ELT address?**

| Option | Correct? |
|--------|----------|
| **Challenges imposed by Big Data** | **✓ CORRECT** |
| Request for fixed processes | ✗ |
| Cost-effectiveness | ✗ |
| Transformation in data pipeline | ✗ |

**Answer:** Challenges imposed by Big Data

**Analysis:** ELT was designed to solve big data scalability problems. From c8_m1_comparing_etl_and_elt.md: "The trend is being driven by the pain points that ELT solves, namely, the lengthy time-to-insight, the challenges, for example, scalability imposed by big data, and the conventional siloed nature of data."

---

## Question 5

**There are many techniques for extracting data. What does the choice of technique depend on?**

| Option | Correct? |
|--------|----------|
| Operating system | ✗ |
| Type of client | ✗ |
| Optical or analog | ✗ |
| **Kind of data source and intended use** | **✓ CORRECT** |

**Answer:** Kind of data source and intended use

**Analysis:** Extraction technique is determined by what you're extracting from and why. From c8_m1_data_extraction_techniques.md: "There are many techniques for extracting data, depending on the kind of data source and the intended use of the data."

---

## Question 6

**Extracting data from IoT devices involves large volumes of redundant data. What is used to decrease the data volume of redundant data and only extract features of interest from raw data?**

| Option | Correct? |
|--------|----------|
| **Edge computing** | **✓ CORRECT** |
| APIs | ✗ |
| SQL languages | ✗ |
| Biometric sensors | ✗ |

**Answer:** Edge computing

**Analysis:** Edge computing processes data at the source, reducing what needs to be transmitted. From c8_m1_data_extraction_techniques.md: "Rather than transmitting potentially very large volumes of redundant data from IoT devices, you can use edge computing to reduce that data volume by extracting features of interest from the raw data."

---

## Question 7

**ETL uses the schema-on-write approach. What is the biggest disadvantage of this approach?**

| Option | Correct? |
|--------|----------|
| More data access | ✗ |
| **Limited versatility** | **✓ CORRECT** |
| Stability | ✗ |
| Consistency | ✗ |

**Answer:** Limited versatility

**Analysis:** Schema-on-write locks data into a fixed shape, limiting flexibility. From c8_m1_intro_data_transformation_techniques.md: "Schema-on-write is the conventional approach used in ETL pipelines, where the data must be conformed to a defined schema prior to loading... But this comes at the cost of limiting the versatility of the data."

---

## Question 8

**Why is there no information loss in ELT unlike ETL where there is loss of information?**

| Option | Correct? |
|--------|----------|
| **Because the data is copied as is** | **✓ CORRECT** |
| Because ELT uses edge computing | ✗ |
| Because ELT involves lossy data compression | ✗ |
| Because ETL uses aggregation of data but ELT doesn't | ✗ |

**Answer:** Because the data is copied as is

**Analysis:** ELT preserves raw data by loading it without transformation. From c8_m1_intro_data_transformation_techniques.md: "with ELT, all the original information content is left intact because the data is simply copied over as is."

---

## Question 9

**Which of these is most useful for incremental loading strategy?**

| Option | Correct? |
|--------|----------|
| **Both batch and stream loading** | **✓ CORRECT** |
| File partitioning | ✗ |
| Only batch loading | ✗ |
| Only stream loading | ✗ |

**Answer:** Both batch and stream loading

**Analysis:** Incremental loading encompasses both approaches depending on data volume and velocity. From c8_m1_data_loading_techniques.md: "You can categorize incremental loading into stream loading and batch loading, depending on the volume and velocity of data."

---

## Question 10

**Which of the following loading techniques can split a single file into smaller chunks?**

| Option | Correct? |
|--------|----------|
| Scheduled loading | ✗ |
| Batch loading | ✗ |
| Stream loading | ✗ |
| **Parallel loading** | **✓ CORRECT** |

**Answer:** Parallel loading

**Analysis:** Parallel loading splits data into chunks for simultaneous processing. From c8_m1_data_loading_techniques.md: "Similarly, by splitting a single file into smaller chunks, the chunks can be loaded simultaneously." This is a defining characteristic of parallel loading.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | All questions | Source verification | All 10 answers verified against enriched lesson files | HIGH |

<!-- EXTRACTION_CHECKLIST: 10 questions extracted, 10 questions in output -->
