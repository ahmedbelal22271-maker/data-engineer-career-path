> **Course 9:** Data Warehouse Fundamentals
> **Module 2:** Designing, Modeling, and Implementing Data Warehouses

# Hands-on Lab: Verifying Data Quality for a Data Warehouse

<mark>NEW</mark>

## Estimated Time
30 minutes

## Purpose of the Lab

The primary purpose of this lab is to instruct participants on the process of conducting thorough data quality checks in a data warehousing environment. It focuses on using a Python-based framework within a PostgreSQL database to validate data integrity. Key areas of emphasis include identifying null values, duplicates, and invalid entries, as well as verifying data ranges. The lab aims to equip learners with the necessary skills to set up and utilize a testing framework for data validation, ensuring data accuracy and consistency.

## Benefits of Learning the Lab

Engaging in this lab offers several benefits, particularly in enhancing one's capabilities in data management and quality assurance. Learners will gain hands-on experience in implementing automated data quality checks, a skill crucial for maintaining the reliability of data in real-world applications. This proficiency is especially beneficial for professionals working with large datasets, as it ensures the integrity of data used for analysis and decision-making. Moreover, understanding these concepts is essential for anyone aspiring to specialize in data science, database administration, or any field that relies heavily on accurate and reliable data.

## Objectives

In this lab, you will:
- Check Null values
- Check Duplicate values
- Check Min Max
- Check Invalid values
- Generate a report on data quality

---

## Prerequisites

### Docker Setup for PostgreSQL

This lab runs PostgreSQL in a Docker container. You should already have the PostgreSQL Docker image:

```bash
# Check existing images
docker images | grep postgres

# You should see:
# postgres    latest    650MB
# postgres    16        642MB
```

### Start PostgreSQL Container

```bash
# Start a PostgreSQL container with the lab database
docker run -d \
  --name postgres-dw-lab \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16

# Verify it's running
docker ps | grep postgres-dw-lab
```

### Connect to PostgreSQL

```bash
# Connect using psql
docker exec -it postgres-dw-lab psql -U postgres

# Or from host (if psql is installed)
psql -h localhost -U postgres -p 5432
```

> **Note:** All supporting files (schema SQL, Python scripts) are in the `assets/` subdirectory. See `assets/README_LOCAL_SETUP.md` for detailed local setup instructions.

---

## Exercise 1: Set Up the Staging Area

### Step 1: Start the PostgreSQL Server

The PostgreSQL server is already running in your Docker container.

### Step 2: Create the Database on the Data Warehouse

Using the `createdb` command of the PostgreSQL server, we can directly create the database from the terminal.

First, set your PostgreSQL password for authentication:

```bash
export PGPASSWORD=postgres
```

Now, create a database named `billingDW`:

```bash
createdb -h localhost -U postgres -p 5432 billingDW
```

In the above command:
- `-h` mentions that the database server is accessible using the hostname "localhost"
- `-U` mentions that we are using the user name postgres to log into the database
- `-p` mentions that the database server is running on port number 5432

### Step 3: Download the Schema .sql File

The commands to create the schema are available in the file below:

```
https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0260EN-SkillsNetwork/labs/Working%20with%20Facts%20and%20Dimension%20Tables/star-schema.sql
```

Download the file by running the command below:

```bash
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0260EN-SkillsNetwork/labs/Working%20with%20Facts%20and%20Dimension%20Tables/star-schema.sql
```

### Step 4: Create the Schema

Run the command below to create the schema in the `billingDW` database:

```bash
psql -h localhost -U postgres -p 5432 billingDW < star-schema.sql
```

---

## Exercise 2: Set Up the Testing Framework

You can perform most of the data quality checks by manually running SQL queries on the data warehouse. However, it is a good idea to automate these checks using custom programs or tools. Automation helps you to easily:
- Create new tests
- Run tests
- Schedule tests

We will be using a Python-based framework to run the data quality tests.

### Step 1: Download the Framework

Run the commands below to download the framework:

```bash
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0260EN-SkillsNetwork/labs/Verifying%20Data%20Quality%20for%20a%20Data%20Warehouse/dataqualitychecks.py

wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/HB0XK4MDrGwigMmVPmPoeQ/dbconnect.py

wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0260EN-SkillsNetwork/labs/Verifying%20Data%20Quality%20for%20a%20Data%20Warehouse/mytests.py

wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/saTxV8y9Kt-e8Zxe29M0TA/generate-data-quality-report.py
```

### Step 2: Install the Python Driver for PostgreSQL

```bash
python3 -m pip install psycopg2
```

### Step 3: Update Password and Host in `dbconnect.py`

Open `dbconnect.py` and make these changes:

1. Replace `<replace this with your postgres password>` with your actual PostgreSQL password (line 3)
2. Change `host = "postgres"` to `host = "localhost"` (line 9) for local Docker usage

Also update the same values in `generate-data-quality-report.py` (line 15 for password, line 19 for host).

### Step 4: Test Database Connectivity

Now we need to check:
- If the PostgreSQL Python driver is installed properly
- If PostgreSQL server is up and running
- If our micro framework can connect to the database

Run the command below:

```bash
python3 dbconnect.py
```

If all goes well, you should see a message: `Successfully connected to database`.

The command also disconnects from the server with a message: `Connection closed`.

---

## Exercise 3: Create a Sample Data Quality Report

Run the command below to install pandas:

```bash
python3 -m pip install pandas tabulate
```

Run the command below to generate a sample data quality report:

```bash
python3 generate-data-quality-report.py
```

You should see a list of tests that were run and their status.

---

## Exercise 4: Explore the Data Quality Tests

Open the file `mytests.py` in the editor. The file contains all the data quality tests.

It provides a quick and easy way to author and run new data quality tests. The testing framework provides the following tests:

| Test Function | Description |
|---------------|-------------|
| `check_for_nulls` | Checks for nulls in a column |
| `check_for_min_max` | Checks if values in a column are within a range of min and max values |
| `check_for_valid_values` | Checks for any invalid values in a column |
| `check_for_duplicates` | Checks for duplicates in a column |

Each test can be authored by specifying a minimum of 4 parameters:

| Parameter | Description |
|-----------|-------------|
| `testname` | The human readable name of the test for reporting purposes |
| `test` | The actual test name that the testing micro framework provides |
| `table` | The table name on which the test is to be performed |
| `column` | The column name on which the test is to be performed |

---

## Exercise 5: Check for Nulls

Let us now see what a `check_for_nulls` test looks like.

Here is a sample `check_for_nulls` test:

```python
test1 = {
    "testname": "Check for nulls",
    "test": check_for_nulls,
    "column": "monthid",
    "table": "DimMonth"
}
```

All tests must be named as `test` followed by a unique number to identify the test.

Let us now create a new `check_for_nulls` test and run it. The test below checks if there are any null values in the column `year` in the table `DimMonth`. The test fails if nulls exist.

Copy and paste the code below at the end of `mytests.py` file:

```python
test5 = {
    "testname": "Check for nulls",
    "test": check_for_nulls,
    "column": "year",
    "table": "DimMonth"
}
```

Save the file and run the command below to generate the new data quality report:

```bash
python3 generate-data-quality-report.py
```

---

## Exercise 6: Check for Min Max Range

Let us now see what a `check_for_min_max` test looks like.

Here is a sample `check_for_min_max` test:

```python
test2 = {
    "testname": "Check for min and max",
    "test": check_for_min_max,
    "column": "monthid",
    "table": "DimMonth",
    "minimum": 1,
    "maximum": 12
}
```

In addition to the usual fields, you have two more fields here:
- `minimum` is the lowest valid value for this column (Example: 1 in case of month number)
- `maximum` is the highest valid value for this column (Example: 12 in case of month number)

Let us now create a new `check_for_min_max` test and run it. The test below checks for minimum of 1 and maximum of 4 in the column `quarter` in the table `DimMonth`. The test fails if there are any values less than minimum or more than maximum.

Copy and paste the code below at the end of `mytests.py` file:

```python
test6 = {
    "testname": "Check for min and max",
    "test": check_for_min_max,
    "column": "quarter",
    "table": "DimMonth",
    "minimum": 1,
    "maximum": 4
}
```

Save the file and run the command below to generate the new data quality report:

```bash
python3 generate-data-quality-report.py
```

---

## Exercise 7: Check for Any Invalid Entries

Let us now see what a `check_for_valid_values` test looks like.

Here is a sample `check_for_valid_values` test:

```python
test3 = {
    "testname": "Check for valid values",
    "test": check_for_valid_values,
    "column": "category",
    "table": "DimCustomer",
    "valid_values": {'Individual', 'Company'}
}
```

In addition to the usual fields, you have an additional field here:
- Use the field `valid_values` to mention what are the valid values for this column.

Let us now create a new `check_for_valid_values` test and run it. The test below checks for valid values in the column `quartername` in the table `DimMonth`. The valid values are Q1, Q2, Q3, Q4. The test fails if there are any values that are not in the valid set.

Copy and paste the code below at the end of `mytests.py` file:

```python
test7 = {
    "testname": "Check for valid values",
    "test": check_for_valid_values,
    "column": "quartername",
    "table": "DimMonth",
    "valid_values": {'Q1', 'Q2', 'Q3', 'Q4'}
}
```

Save the file and run the command below to generate the new data quality report:

```bash
python3 generate-data-quality-report.py
```

---

## Exercise 8: Check for Duplicate Entries

Let us now see what a `check_for_duplicates` test looks like.

Here is a sample `check_for_duplicates` test:

```python
test4 = {
    "testname": "Check for duplicates",
    "test": check_for_duplicates,
    "column": "monthid",
    "table": "DimMonth"
}
```

Let us now create a new `check_for_duplicates` test and run it. The test below checks for any duplicate values in the column `customerid` in the table `DimCustomer`. The test fails if duplicates exist.

Copy and paste the code below at the end of `mytests.py` file:

```python
test8 = {
    "testname": "Check for duplicates",
    "test": check_for_duplicates,
    "column": "customerid",
    "table": "DimCustomer"
}
```

Save the file and run the command below to generate the new data quality report:

```bash
python3 generate-data-quality-report.py
```

---

## Practice Exercises

### Problem 1
Create a `check_for_nulls` test on column `billedamount` in the table `FactBilling`.

<details>
<summary>Click here for Hint</summary>

```python
test9 = {
    "testname": "Check for nulls in billedamount",
    "test": check_for_nulls,
    "column": "billedamount",
    "table": "FactBilling"
}
```

</details>

<details>
<summary>Click here for Solution</summary>

```python
test9 = {
    "testname": "Check for nulls in billedamount",
    "test": check_for_nulls,
    "column": "billedamount",
    "table": "FactBilling"
}
```

</details>

### Problem 2
Create a `check_for_duplicates` test on column `billid` in the table `FactBilling`.

<details>
<summary>Click here for Hint</summary>

```python
test10 = {
    "testname": "Check for duplicates in billid",
    "test": check_for_duplicates,
    "column": "billid",
    "table": "FactBilling"
}
```

</details>

<details>
<summary>Click here for Solution</summary>

```python
test10 = {
    "testname": "Check for duplicates in billid",
    "test": check_for_duplicates,
    "column": "billid",
    "table": "FactBilling"
}
```

</details>

### Problem 3
Create a `check_for_valid_values` test on column `quarter` in the table `DimMonth`. The valid values are 1, 2, 3, 4.

<details>
<summary>Click here for Hint</summary>

```python
test11 = {
    "testname": "Check for valid quarter values",
    "test": check_for_valid_values,
    "column": "quarter",
    "table": "DimMonth",
    "valid_values": {1, 2, 3, 4}
}
```

</details>

<details>
<summary>Click here for Solution</summary>

```python
test11 = {
    "testname": "Check for valid quarter values",
    "test": check_for_valid_values,
    "column": "quarter",
    "table": "DimMonth",
    "valid_values": {1, 2, 3, 4}
}
```

</details>

---

## Congratulations!

You have successfully finished this lab.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Lab Overview | Definition | Data quality checks validate data integrity in warehouses | HIGH | Lab content |
| 2 | Testing Framework | Ecosystem | Python-based framework automates data quality tests | HIGH | Lab content |
| 3 | Docker Setup | Example | Added Docker commands for local PostgreSQL setup | HIGH | UNCERTAIN |

---

**Authors:** Ramesh Sannareddy
**Other Contributors:** Rav Ahuja
**© IBM Corporation. All rights reserved.**

<!-- EXTRACTION_CHECKLIST: 86 sentences extracted, 86 sentences in output -->
