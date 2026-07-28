> **Course 9:** Data Warehouse Fundamentals
> **Module 2:** Designing, Modeling, and Implementing Data Warehouses

# Hands-on Lab: Querying the Data Warehouse (Cubes, Rollups, Grouping Sets and Materialized Views)

<mark>NEW</mark>

## Estimated Time
30 minutes

## Purpose of the Lab

The purpose of this lab is to provide hands-on experience in advanced SQL query techniques using PostgreSQL in a Cloud IDE environment. The lab focuses on teaching how to create grouping sets, rollups, and cubes for data aggregation and summarization, as well as how to implement and utilize Materialized Query Tables (Materialized views) for efficient data querying. These skills are essential for managing and analyzing large datasets, particularly in data warehousing and business intelligence contexts.

## Benefits of Learning the Lab

By completing this lab, you will gain valuable insights into the practical application of complex SQL queries and data manipulation techniques. The knowledge of grouping sets, rollups, and cubes will enable learners to effectively summarize and analyze data, which is crucial in making informed business decisions. Understanding and implementing Materialized views provides an efficient way to handle large-scale data by reducing the computational load during frequent query executions. These skills are highly beneficial for careers in data analysis, database administration, and business intelligence, enhancing your ability to manage and analyze data in real-world scenarios.

## Objectives

In this lab you will learn how to create:
- Grouping sets
- Rollup
- Cube
- Materialized views

---

## Prerequisites

**This lab requires that you complete the previous lab Populate a Data Warehouse.**

If you have not finished the Populate a Data Warehouse Lab yet, please finish it before you continue.

You need the `billingdw` database with tables: DimCustomer, DimMonth, FactBilling.

---

## Key Concepts

`GROUPING SETS`, `CUBE`, and `ROLLUP` allow us to easily create subtotals and grand totals in a variety of ways. All these operators are used along with the `GROUP BY` operator.

- **GROUPING SETS** operator allows us to group data in a number of different ways in a single SELECT statement.
- **ROLLUP** operator is used to create subtotals and grand totals for a set of columns.
- **CUBE** operator creates subtotals for all possible combinations of the columns specified.

---

## Exercise 1: Launch PostgreSQL and Open pgAdmin

See the previous lab for detailed instructions on connecting to your PostgreSQL instance.

---

## Exercise 2: Write a query using grouping sets

To create a grouping set using the three columns `year`, `quartername`, and `sum(billedamount)`, run the SQL statement below:

```sql
SELECT year, quartername, SUM(billedamount) AS totalbilledamount
FROM "FactBilling"
LEFT JOIN "DimCustomer"
    ON "FactBilling".customerid = "DimCustomer".customerid
LEFT JOIN "DimMonth"
    ON "FactBilling".monthid = "DimMonth".monthid
GROUP BY grouping sets(year, quartername)
ORDER BY year, quartername;
```

The partial output can be seen in the image below.

---

## Exercise 3: Write a query using rollup

To create a rollup using the three columns `year`, `category`, and `sum(billedamount)`, run the SQL statement below:

```sql
SELECT year, category, SUM(billedamount) AS totalbilledamount
FROM "FactBilling"
LEFT JOIN "DimCustomer"
    ON "FactBilling".customerid = "DimCustomer".customerid
LEFT JOIN "DimMonth"
    ON "FactBilling".monthid = "DimMonth".monthid
GROUP BY rollup(year, category)
ORDER BY year, category;
```

The partial output can be seen in the image below.

---

## Exercise 4: Write a query using cube

To create a cube using the three columns labeled `year`, `category`, and `sum(billedamount)`, run the SQL statement below:

```sql
SELECT year, category, SUM(billedamount) AS totalbilledamount
FROM "FactBilling"
LEFT JOIN "DimCustomer"
    ON "FactBilling".customerid = "DimCustomer".customerid
LEFT JOIN "DimMonth"
    ON "FactBilling".monthid = "DimMonth".monthid
GROUP BY cube(year, category)
ORDER BY year, category;
```

The partial output can be seen in the image below.

---

## Exercise 5: Create a Materialized Query Table (Materialized views)

In pgAdmin we can implement materialized views using Materialized Query Tables.

### Step 1: Create the Materialized views

Execute the SQL statement below to create a materialized view named `countrystats`:

```sql
CREATE MATERIALIZED VIEW countrystats (country, year, totalbilledamount) AS
SELECT country, year, SUM(billedamount)
FROM "FactBilling"
LEFT JOIN "DimCustomer"
    ON "FactBilling".customerid = "DimCustomer".customerid
LEFT JOIN "DimMonth"
    ON "FactBilling".monthid = "DimMonth".monthid
GROUP BY country, year;
```

The above command creates a materialized view named `countrystats` that has 3 columns:
- Country
- Year
- totalbilledamount

### Step 2: Populate/refresh data into the Materialized views

Execute the SQL statement below to populate the materialized view `countrystats`:

```sql
REFRESH MATERIALIZED VIEW countrystats;
```

The command above populates the materialized view with relevant data.

### Step 3: Query the Materialized views

Once a materialized view is refreshed, you can query it. Execute the SQL statement below to query the materialized view `countrystats`:

```sql
SELECT * FROM countrystats;
```

---

## Practice Exercises

### Problem 1
Create a grouping set for the columns `year`, `quartername`, `sum(billedamount)`.

<details>
<summary>Click here for Hint</summary>

Use GROUPING SETS with year and quartername.

</details>

<details>
<summary>Click here for Solution</summary>

```sql
SELECT year, quartername, SUM(billedamount) AS totalbilledamount
FROM "FactBilling"
LEFT JOIN "DimCustomer"
    ON "FactBilling".customerid = "DimCustomer".customerid
LEFT JOIN "DimMonth"
    ON "FactBilling".monthid = "DimMonth".monthid
GROUP BY grouping sets(year, quartername)
ORDER BY year, quartername;
```

</details>

### Problem 2
Create a rollup for the columns `country`, `category`, `sum(billedamount)`.

<details>
<summary>Click here for Hint</summary>

Use ROLLUP with country and category.

</details>

<details>
<summary>Click here for Solution</summary>

```sql
SELECT country, category, SUM(billedamount) AS totalbilledamount
FROM "FactBilling"
LEFT JOIN "DimCustomer"
    ON "FactBilling".customerid = "DimCustomer".customerid
LEFT JOIN "DimMonth"
    ON "FactBilling".monthid = "DimMonth".monthid
GROUP BY rollup(country, category)
ORDER BY country, category;
```

</details>

### Problem 3
Create a cube for the columns `year`, `country`, `category`, `sum(billedamount)`.

<details>
<summary>Click here for Hint</summary>

Use CUBE with year, country, and category.

</details>

<details>
<summary>Click here for Solution</summary>

```sql
SELECT year, country, category, SUM(billedamount) AS totalbilledamount
FROM "FactBilling"
LEFT JOIN "DimCustomer"
    ON "FactBilling".customerid = "DimCustomer".customerid
LEFT JOIN "DimMonth"
    ON "FactBilling".monthid = "DimMonth".monthid
GROUP BY cube(year, country, category)
ORDER BY year, country, category;
```

</details>

### Problem 4
Create a materialized view named `average_billamount` with columns `year`, `quarter`, `category`, `country`, `average_bill_amount`.

<details>
<summary>Click here for Hint</summary>

Use CREATE MATERIALIZED VIEW with AVG() function.

</details>

<details>
<summary>Click here for Solution</summary>

```sql
CREATE MATERIALIZED VIEW average_billamount (year, quarter, category, country, average_bill_amount) AS
SELECT year, quarter, category, country, AVG(billedamount)
FROM "FactBilling"
LEFT JOIN "DimCustomer"
    ON "FactBilling".customerid = "DimCustomer".customerid
LEFT JOIN "DimMonth"
    ON "FactBilling".monthid = "DimMonth".monthid
GROUP BY year, quarter, category, country;
```

</details>

---

## Congratulations!

You have successfully finished the Querying the Data Warehouse (Cubes, Rollups, Grouping Sets and Materialized Views) lab.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Key Concepts | Definition | GROUPING SETS, ROLLUP, CUBE for aggregation | HIGH | Lab content |
| 2 | Exercise 2 | Code | Grouping sets query with year and quartername | HIGH | Lab content |
| 3 | Exercise 3 | Code | Rollup query with year and category | HIGH | Lab content |
| 4 | Exercise 4 | Code | Cube query with year and category | HIGH | Lab content |
| 5 | Exercise 5 | Code | Materialized view creation and refresh | HIGH | Lab content |

---

**Author:** Amrutha Rao
**© IBM Corporation. All rights reserved.**

<!-- EXTRACTION_CHECKLIST: 48 sentences extracted, 48 sentences in output -->
