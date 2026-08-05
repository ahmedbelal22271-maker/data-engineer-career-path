**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 1:** Extract, Transform, Load (ETL) Overview

# Introduction to Data Transformation Techniques

## Learning Objectives

After watching this video, you will be able to name data transformation techniques, compare schema-on-write versus schema-on-read, and list ways information can be lost in transformation.

## Data Transformation Techniques

Data transformation is mainly about formatting the data to suit the application. This can involve many kinds of operations, such as:

### Data Typing

**Data typing**, which involves casting data to appropriate types, such as integer, float, string, object, and category.

[ENRICHED: concrete example — a CSV file stores all values as strings (since CSV is a text format). When loaded into Python/pandas, the column `order_amount` contains strings like `"19.99"` and `"null"`. Data typing involves: (1) casting `order_amount` to `float64` for arithmetic operations, (2) casting `order_date` to `datetime64` for date calculations, (3) casting `country_code` to `category` dtype to reduce memory usage (a column with 5 unique countries stored as strings uses 10× more memory than `category` type). Incorrect typing causes silent errors: if `order_amount` stays as string, sorting produces alphabetical order (`"19.99" > "100.00"` because `"1" > "1"` is false but `"9" > "0"` is true).]

### Data Structuring

**Data structuring**, which includes converting one data format to another, such as JSON, XML, or CSV to database tables.

[ENRICHED: concrete example — a REST API returns nested JSON: `{"user": {"name": "Alice", "orders": [{"id": 1, "amount": 29.99}, {"id": 2, "amount": 45.00}]}}`. To load this into a relational database, the transformation flattens the nested structure into two tables: a `users` table (`id`, `name`) and an `orders` table (`id`, `user_id`, `amount`). The reverse — structuring relational data as JSON — is also common: a database row is serialized into JSON for consumption by a frontend application or a NoSQL document store.] [ENRICHED: definition — JSON, XML, and CSV are semi-structured data, not fully structured. Structured data lives in rigid SQL tables where every row has the same columns. Semi-structured data has organization (keys, hierarchy) but no fixed schema — each JSON object can have different keys. For example: Record 1 is `{"name": "Alice", "age": 30}`, Record 2 is `{"name": "Bob", "hobbies": ["reading"]}`, Record 3 is `{"name": "Charlie", "phone": "+1234567890"}`. In a SQL table, these would require filling unused columns with NULLs. In JSON, each record stores only what it has. Data structuring converts semi-structured data (JSON/XML) into structured data (database tables) by defining a consistent schema and extracting the relevant fields.]

### Anonymizing and Encrypting

As well as **anonymizing and encrypting** transformations to help ensure privacy and security.

[ENRICHED: defined "anonymizing" — the process of removing or obfuscating personally identifiable information (PII) from a dataset so that individuals cannot be re-identified. Techniques include: pseudonymizing names (replacing "John Smith" with "USER_A"), generalizing ages (replacing exact age with age brackets like "30-39"), and k-anonymity (ensuring each record is indistinguishable from at least k-1 other records on quasi-identifiers). Anonymization is required under GDPR for datasets used in analytics or shared with third parties.] [ENRICHED: defined "encrypting" — transforming data using a cryptographic algorithm so that it is unreadable without the decryption key. In-transit encryption (TLS/SSL) protects data moving between systems; at-rest encryption (AES-256) protects data stored on disk. Unlike anonymization, encryption is reversible — the original data can be recovered with the key. Both are complementary: encryption protects data confidentiality; anonymization protects data privacy even if encryption is bypassed.]

### Cleaning

**Cleaning operations** for removing duplicate records, and filling missing values.

[ENRICHED: concrete example — a customer dataset has 50,000 rows but 2,300 are exact duplicates (same `customer_id`, same `email`, same `signup_date` — caused by a bug in the upstream CRM export that ran the same query twice). Deduplication removes the 2,300 duplicates, leaving 47,700 unique records. For missing values: the `phone_number` column has 1,200 null entries. Options: (1) fill with a placeholder like `"N/A"`, (2) fill with the column mode (most common phone area code), (3) leave null if the downstream system handles nulls, or (4) drop the column entirely if it is non-essential. The choice depends on the use case — filling phone numbers with a mode value would be misleading for a contact list, but acceptable for a demographic analysis.]

### Normalizing

**Normalizing data** to ensure units are comparable, for example, using a common currency.

[ENRICHED: concrete example — a global sales dataset contains transactions in USD, EUR, GBP, and JPY. To normalize, each transaction is converted to a common currency (e.g., USD) using the exchange rate at the transaction timestamp. A sale of €100 on 2024-01-15 (rate: 1 EUR = 1.09 USD) becomes $109.00. Without normalization, comparing a €100 sale to a ¥15,000 sale is meaningless. Normalization also applies to units of measurement: converting all weights from pounds to kilograms, all temperatures from Fahrenheit to Celsius, or all timestamps to UTC.]

### Filtering, Sorting, Aggregating, and Binning

**Filtering, sorting, aggregating, and binning operations** for accessing the right data at a suitable level of detail and in a sensible order.

[ENRICHED: defined "binning" — the process of grouping continuous values into discrete bins (intervals). Example: converting individual ages (23, 45, 67, 31, 52) into age groups (18-29, 30-44, 45-59, 60+). Binning is used in histograms, age-based demographic analysis, and feature engineering for machine learning (converting a continuous variable into a categorical one to capture non-linear relationships). Common methods: equal-width bins (fixed interval size), equal-frequency bins (same number of records per bin), and custom bins (domain-specific groupings).]

### Joining or Merging

**Joining or merging disparate data sources.**

[ENRICHED: concrete example — a retailer maintains a `products` table in PostgreSQL (product_id, name, category, price) and an `inventory` table in MongoDB (product_id, warehouse_id, quantity, last_restock_date). The transformation joins these two sources on `product_id`, producing a unified dataset that shows each product's name, price, current stock level, and when it was last restocked. This joined dataset feeds a dashboard that alerts procurement when stock falls below a threshold.]

## Schema-on-Write vs Schema-on-Read

**Schema-on-write** is the conventional approach used in ETL pipelines, where the data must be conformed to a defined schema prior to loading to a destination, such as a relational database. The idea is to have the data consistently structured for stability and for making subsequent queries much faster. But this comes at the cost of limiting the versatility of the data.

[ENRICHED: added specificity — "queries much faster" because schema-on-write allows the database to optimize storage layout at write time: creating indexes on frequently queried columns, partitioning tables by date, and pre-computing materialized views. A query against a schema-on-write database can use these pre-built structures without runtime interpretation. The tradeoff: any schema change (adding a column, changing a data type) requires an ALTER TABLE operation, which may lock the table and take minutes to hours on large datasets. Important clarification: schema-on-write databases (data warehouses) CAN absolutely be SQL queried — that's their primary purpose. The "versatility" limitation is not about whether you can query, but about whether you can query in NEW ways without modifying the pipeline. If the ETL loaded `customer_id, name, email` and you later need `customer_id, name, purchase_history`, you must modify the ETL transformation to include that column, re-run the pipeline, and reload the data. With schema-on-read, you just write a new query against the same raw data that already contains `purchase_history` — no pipeline change needed.]

**Schema-on-read** relates to the modern ELT approach, where the schema is applied to the raw data after reading it from the raw data storage. This approach is versatile since it can obtain multiple views of the same source data using ad hoc schemas. Users potentially have access to more data, since it does not need to go through a rigorous preprocessing step.

[ENRICHED: concrete example — a data lake stores raw JSON event logs in Amazon S3. A data engineer reads the same S3 objects using one schema (extracting `user_id`, `event_type`, `timestamp`) for a user behavior dashboard. A data scientist reads the same objects using a different schema (extracting `device_type`, `screen_resolution`, `battery_level`) for a device analytics model. Neither party needed the other's schema to be defined at write time — the raw data accommodates both views. With schema-on-write (a traditional data warehouse), achieving this would require the ETL pipeline to have pre-defined both columns at load time. If the data scientist's columns weren't in the original ETL transformation, the data simply isn't in the warehouse — the pipeline must be modified, re-tested, and re-run before the scientist can query it.]

[ENRICHED: critical analysis — "why not just make a 200-column warehouse that includes everything?" This is a reasonable question, but a 200-column warehouse breaks down for six concrete reasons: (1) **Unpredictable needs** — new fields appear from new tools/sources that didn't exist when the warehouse was designed; each requires pipeline modification and redeployment. (2) **Source schema drift** — upstream systems rename/add/remove columns without warning, breaking ETL mappings. (3) **Performance degradation** — 200-column tables slow query parsing, increase INSERT I/O, and create lock contention. (4) **NULL explosion** — different sources contribute different columns, leaving most cells NULL for most rows, wasting storage and creating confusion. (5) **Governance chaos** — tracking lineage, permissions, and quality for 200 columns from 15 sources is an administrative nightmare. (6) **Raw data loss** — the 200 columns represent today's understanding; future use cases that derive new fields from raw signals (click sequences → user intent) are impossible if the raw data was discarded. A 200-column warehouse is the worst of both worlds: lake-level storage cost without lake-level flexibility. ELT with a data lake provides cheap raw storage, unlimited query flexibility, and zero pipeline modifications when needs change.]

## Information Loss in Transformation

Whether intentional or accidental, there are many ways in which information can be lost in transformation. We can visualize this loss as follows: Raw data is normally much bigger than transformed data. Since data usually contains noise and redundancy, we can illustrate the information content of data as a proper subset of the data. Correspondingly, we can see that shrinking the data volume can also mean shrinking the information content.

Either way, for ETL processes, any lost information may or may not be recoverable, whereas with ELT, all the original information content is left intact because the data is simply copied over as is.

[ENRICHED: added specificity — "may or may not be recoverable" depends on whether the transformation is lossy or lossless. Lossy transformations permanently discard information (e.g., rounding 3.14159 to 3.14 loses precision that cannot be recovered). Lossless transformations preserve all information (e.g., encoding a string as UTF-8 is reversible). Most ETL transformations are a mix: data typing is lossless (you can cast back), but filtering and aggregation are lossy (discarded rows cannot be recovered unless the raw data is preserved elsewhere).]

### Examples of Information Loss

Examples of ways information can be lost in transformation processes include:

- **Lossy data compression**, for example, converting floating point values to integers, reducing bit rates on audio or video. [ENRICHED: concrete example — a sensor dataset records temperature as `23.4567°C` (float64, 8 bytes). Converting to integer (`23°C`, 4 bytes) discards the fractional precision. For a climate monitoring system, this 0.4567°C loss could mask a subtle warming trend. For a home thermostat, it is negligible. The decision depends on the required precision for the downstream use case.]

- **Filtering**, for example, filtering is usually a temporary selection of a subset of data, but when it is permanent, information can easily be discarded. [ENRICHED: concrete example — a pipeline filters a web traffic log to keep only `200 OK` responses for a performance dashboard. The `404 Not Found` and `500 Internal Server Error` responses are permanently discarded. Months later, the security team wants to analyze 404 patterns to detect a phishing attack — the data is gone. The fix: filter into a separate table or use ELT to keep raw data intact.]

- **Aggregation**, for example, average yearly sales versus daily or monthly average sales. [ENRICHED: added specificity — aggregation reduces cardinality: daily sales (365 data points/year) → monthly sales (12 data points/year) → yearly sales (1 data point/year). At each step, the variance within the period is lost. A retailer with strong holiday seasonality (80% of sales in November-December) appears healthy on a yearly average, but the monthly view reveals that January-October sales are declining — a critical signal lost to aggregation.]

- **Edge computing devices**, for example, false negatives in surveillance devices designed to only stream alarm signals, not the raw data. [ENRICHED: concrete example — here is exactly how this works, step by step:]

**The setup:**

A factory installs 50 security cameras to detect workers not wearing hard hats. Each camera has a small computer (the "edge device") built into it. This computer runs a simple AI model that looks at each video frame and decides: "safe" (everyone has a hard hat) or "violation" (someone is missing one).

**What the camera does with each frame:**

```
Camera sees a frame
        │
        ▼
AI model analyzes it
        │
        ├── "safe" → delete the frame, don't send anything
        │
        └── "violation" → send an alarm to the control room
```

The camera is **throwing away** the video frames it considers "safe." It only keeps and sends the "violation" frames. This saves enormous amounts of storage and network bandwidth — instead of streaming 24/7 video from 50 cameras, it only sends the few frames where something went wrong.

**The problem — a false negative:**

A worker walks under a camera without a hard hat. But the AI model is imperfect — it has a "false negative" (it misses the violation). Here's what happens:

```
Worker without hard hat walks by
        │
        ▼
AI model analyzes the frame
        │
        └── "safe" (WRONG — it missed the violation)
                │
                ▼
        Frame is deleted
        No alarm is sent
        No video is saved
```

**The result:** the violation happened, but there is zero evidence. No alarm was sent. No video was recorded. The raw data (the video frame showing the worker without a hard hat) was deleted by the edge device before anyone could see it.

**If this had been a real accident:**
- The safety investigator has no video to review
- The AI model can't be retrained on this missed case (the training data is gone)
- The factory can't prove compliance or non-compliance to regulators

**What "information loss" means here:**
The edge device performed a transformation (classifying frames as safe/violation). That transformation was wrong (false negative). Because the raw data was discarded during the transformation, the error is permanent and unrecoverable. The information — the video evidence — is lost forever.

**The fix:** store raw video for a short buffer period (e.g., 7 days) alongside the alarm signals. Then if an incident occurs, you can retrieve the raw footage even if the AI model missed it initially.

## Summary

In this video, you learned that data transformation is generally about formatting data to suit the needs of the intended application. Common transformation techniques include typing, structuring, normalizing, aggregating, and cleaning. Schema-on-write is the conventional approach used in ETL pipelines, and schema-on-read relates to the modern ELT approach. Finally, ways of losing information in transformation processes include filtering, aggregation, using edge computing devices, and lossy data compression.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Data typing section | Concrete example | CSV→pandas type casting: order_amount float64, category dtype memory savings, string sort pitfall | HIGH |
| 2 | Data structuring section | Concrete example | Nested JSON→relational tables flattening (users + orders) | HIGH |
| 3 | Anonymizing section | Definition | Defined anonymizing with pseudonymizing, generalization, k-anonymity techniques | HIGH |
| 4 | Encrypting section | Defined in-transit (TLS) vs at-rest (AES-256) encryption, complementary roles | HIGH |
| 5 | Cleaning section | Concrete example | Deduplication (2,300 duplicates from CRM bug) + missing value strategies (4 options) | HIGH |
| 6 | Normalizing section | Concrete example | Multi-currency sales normalization to USD with timestamp-based exchange rates | HIGH |
| 7 | Binning section | Defined binning: equal-width, equal-frequency, custom methods with age group example | HIGH |
| 8 | Joining section | Concrete example | PostgreSQL products + MongoDB inventory join on product_id | HIGH |
| 9 | Schema-on-write paragraph | Added specificity | Explained query speed via indexes, partitioning, materialized views; ALTER TABLE tradeoff | HIGH |
| 10 | Schema-on-read paragraph | Concrete example | S3 JSON logs: data engineer vs data scientist reading same objects with different schemas | HIGH |
| 11 | Information loss paragraph | Added specificity | Distinguished lossy (rounding) vs lossless (UTF-8) transformations | HIGH |
| 12 | Lossy compression row | Concrete example | Sensor float64→integer: climate monitoring vs home thermostat precision requirements | HIGH |
| 13 | Filtering row | Concrete example | Web traffic 200-only filter discards 404/500 security data | HIGH |
| 14 | Aggregation row | Added specificity | Daily→monthly→ yearly: holiday seasonality masking in yearly averages | HIGH |
| 15 | Edge computing row | Concrete example | Factory safety camera false negatives: alarm-only streaming loses raw video evidence | HIGH |

<!-- EXTRACTION_CHECKLIST: 38 sentences extracted, 38 sentences in output -->
