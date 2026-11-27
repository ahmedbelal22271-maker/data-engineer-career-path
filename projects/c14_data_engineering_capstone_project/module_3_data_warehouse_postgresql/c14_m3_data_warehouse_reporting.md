
# Hands-on Lab: Data Warehouse Reporting

**Estimated Study Time:** 248 mins (Deep Comprehension @ 2.5x) | Hands-on Lab Base: 99 mins (Nominal Effort: 30 mins)

> **Course:** [Course 14: Data Engineering Capstone Project](../../../../../index.md)  
> **Module:** [Module 3: Build a Data Warehouse](../../../index.md)  
> **Part:** [Part 2: Data Warehouse Reporting](../../index.md)  
> **Execution Outputs Reference:** [commands_and_outputs.md](<commands_and_outputs.md>)  
> **Database:** Test1 (PostgreSQL)  

![IBM Skills Network Logo](assets/c14_m3_idsn_logo.png)
*IBM Skills Network Educational Platform*

## Estimated time needed: **30** minutes.

## Software Used in this Lab

  

To complete this lab you will utilize the [PostgreSQL Database](https://www.postgresql.org/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDB0110ENSkillsNetwork24601058-2021-01-01) relational database service available as part of IBM Skills Network Labs (SN Labs) Cloud IDE. SN Labs is a virtual lab environment used in this course.

![PostgreSQL Database](assets/c14_m3_postgresql_logo.png)
*PostgreSQL Relational Database Engine*  

## Scenario

You are a data engineer hired by an ecommerce company named SoftCart.com . The company retails download only items like E-Books, Movies, Songs etc. The company has international presence and customers from all over the world. You have designed the schema for the data warehouse in the previous assignment. Data engineering is a team game. Your senior data engineer reviewed your design. Your schema design was improvised to suit the production needs of the company. In this assignment you will generate reports out of the data in the data warehouse.

## Objectives

In this assignment you will:

- Load data into Data Warehouse
- Write aggregation queries
- Create MQTs


# About the dataset

The dataset you would be using in this assignment is not a real life dataset. It was programmatically created for this assignment purpose.

## Prepare the lab environment

Before you start the assignment:

1. Right Click on this [link](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/nm75oOK5n7AGME1F7_OIQg/CREATE-SCRIPT.sql) and save this SQL file in you local system.
    
2. Start PostgreSQL server
    
3. Create a new database Test1
    
4. Create the following tables
    
    - DimDate
    - DimCategory
    - DimCountry
    - FactSales

> After completing each task, save both the executed commands and their corresponding outputs in a text document, or take screenshots—depending on the option you have chosen. This information will be required to answer questions during the final project submission.



# Loading Data

In this exercise you will load the data into the tables. You will load the data provided by the company in csv format.

### Task 1 - Load data into the dimension table DimDate

- Download the data from [this link](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/datawarehousing/data/DimDate.csv)
    
- Load the downloaded data into DimDate table.

```sql
\copy "DimDate" FROM '/mnt/c/Users/marwa/OneDrive/Documents/data engineering/wiki-generation-pipeline/updates/providers/ibm/Data Engineering Capstone Project/modules/module_3_build_a_data_warehouse/part 2/labs/DimDate(3).csv' WITH (FORMAT csv, HEADER true);
```
    
- Write a SQL query to display the first 5 rows of the table.

```sql
SELECT * FROM "DimDate" LIMIT 5;
```
    
- Save the SQL statement you executed and its output in a text document, or take a screenshot of both for future reference.
    

### Task 2 - Load data into the dimension table DimCategory

- Download the data from [this link](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/datawarehousing/DimCategory.csv)
    
- Load the downloaded data into DimCategory table.

```sql
\copy "DimCategory" FROM '/mnt/c/Users/marwa/OneDrive/Documents/data engineering/wiki-generation-pipeline/updates/providers/ibm/Data Engineering Capstone Project/modules/module_3_build_a_data_warehouse/part 2/labs/DimCategory.csv' WITH (FORMAT csv, HEADER true);
```
    
- Write a SQL query to display the first 5 rows of the table.

```sql
SELECT * FROM "DimCategory" LIMIT 5;
```
    
- Save the SQL statement you executed and its output in a text document, or take a screenshot of both for future reference.
    

### Task 3 - Load data into the dimension table DimCountry

- Download the data from [this link](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/datawarehousing/DimCountry.csv)
    
- Load the downloaded data into DimCountry table.

```sql
\copy "DimCountry" FROM '/mnt/c/Users/marwa/OneDrive/Documents/data engineering/wiki-generation-pipeline/updates/providers/ibm/Data Engineering Capstone Project/modules/module_3_build_a_data_warehouse/part 2/labs/DimCountry.csv' WITH (FORMAT csv, HEADER true);
```
    
- Write a SQL query to display the first 5 rows of the table.

```sql
SELECT * FROM "DimCountry" LIMIT 5;
```
    
- Save the SQL statement you executed and its output in a text document, or take a screenshot of both for future reference.
    

### Task 4 - Load data into the fact table FactSales

- Download the data from [this link](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0321EN-SkillsNetwork/datawarehousing/FactSales.csv)
    
- Load this data into FactSales table.

```sql
\copy "FactSales" FROM '/mnt/c/Users/marwa/OneDrive/Documents/data engineering/wiki-generation-pipeline/updates/providers/ibm/Data Engineering Capstone Project/modules/module_3_build_a_data_warehouse/part 2/labs/FactSales(1).csv' WITH (FORMAT csv, HEADER true);
```
    
- Write a SQL query to display the first 5 rows of the table.

```sql
SELECT * FROM "FactSales" LIMIT 5;
```
    
- Save the SQL statement you executed and its output in a text document, or take a screenshot of both for future reference.


# Queries for data analytics

In this exercise you will query the data you have loaded in the previous exercise.

### Task 5 - Create a grouping sets query

- Create a grouping sets query using the columns country, category, totalsales.

```sql
SELECT 
    dc.country, 
    dcat.category, 
    SUM(f.amount) AS totalsales
FROM "FactSales" f
JOIN "DimCountry" dc 
    ON f.countryid = dc.countryid
JOIN "DimCategory" dcat 
    ON f.categoryid = dcat.categoryid
GROUP BY GROUPING SETS (
    (dc.country, dcat.category),
    (dc.country),
    (dcat.category),
    ()
)
ORDER BY dc.country, dcat.category;
```
    
- Save the SQL statement you executed and its output in a text document, or take a screenshot of both for future reference.
    

### Task 6 - Create a rollup query

- Create a rollup query using the columns year, country, and totalsales.

```sql
SELECT 
    dd.year, 
    dc.country, 
    SUM(f.amount) AS totalsales
FROM "FactSales" f
JOIN "DimDate" dd 
    ON f.dateid = dd.dateid
JOIN "DimCountry" dc 
    ON f.countryid = dc.countryid
GROUP BY ROLLUP (
    dd.year, 
    dc.country
)
ORDER BY dd.year, dc.country;
```
    
- Save the SQL statement you executed and its output in a text document, or take a screenshot of both for future reference
    

### Task 7 - Create a cube query

- Create a cube query using the columns year, country, and average sales.

```sql
SELECT 
    dd.year, 
    dc.country, 
    AVG(f.amount) AS averagesales
FROM "FactSales" f
JOIN "DimDate" dd 
    ON f.dateid = dd.dateid
JOIN "DimCountry" dc 
    ON f.countryid = dc.countryid
GROUP BY CUBE (
    dd.year, 
    dc.country
)
ORDER BY dd.year, dc.country;
```
    
- Save the SQL statement you executed and its output in a text document, or take a screenshot of both for future reference.
    

### Task 8 - Create an MQT

- Create an MQT named total_sales_per_country that has the columns country and total_sales.

> **Note on Terminology:** IBM Db2 calls these **MQTs** (Materialized Query Tables). In PostgreSQL, the exact equivalent feature is called a **Materialized View** (`CREATE MATERIALIZED VIEW ...`).

```sql
-- 1. Create the Materialized View (MQT)
CREATE MATERIALIZED VIEW total_sales_per_country (country, total_sales) AS
SELECT 
    dc.country, 
    SUM(f.amount) AS total_sales
FROM "FactSales" f
JOIN "DimCountry" dc 
    ON f.countryid = dc.countryid
GROUP BY dc.country;

-- 2. Query the Materialized View to verify
SELECT * FROM total_sales_per_country;
```
    
- Save the SQL statement you executed and its output in a text document, or take a screenshot of both for future reference
    

End of the assignment.

## Authors

[Niveditha Pandith](https://www.linkedin.com/in/niveditha-pandith-53a057231)

### Other Contributors

Rav Ahuja

## Change Log

|Date (YYYY-MM-DD)|Version|Changed By|Change Description|
|---|---|---|---|
|2022-12-16|0.3|Niveditha Pandith|Converted initial version to Postgres|
|2021-12-12|0.1|Ramesh Sannareddy|Created initial version|
|2022-02-02|0.2|Ramesh Sannareddy|Updated version|

##### Copyright (c) 2022 IBM Corporation. All rights reserved.

---

## Local Setup Reference Commands

### Execute `CREATE_SCRIPT.sql` into `Test1` Database via WSL CLI

```bash
# 1. Create Test1 database (if not created yet)
sudo -u postgres createdb Test1

# 2. Execute CREATE_SCRIPT.sql
sudo -u postgres psql -d Test1 -f "/mnt/c/Users/marwa/OneDrive/Documents/data engineering/wiki-generation-pipeline/updates/providers/ibm/Data Engineering Capstone Project/modules/module_3_build_a_data_warehouse/part 2/labs/CREATE_SCRIPT.sql"

# Alternative using user 'ahmed':
# psql -U ahmed -d Test1 -f "/mnt/c/Users/marwa/OneDrive/Documents/data engineering/wiki-generation-pipeline/updates/providers/ibm/Data Engineering Capstone Project/modules/module_3_build_a_data_warehouse/part 2/labs/CREATE_SCRIPT.sql"

# 3. Verify the tables exist
sudo -u postgres psql -d Test1 -c "\dt"
```