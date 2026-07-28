> **Course 9:** Data Warehouse Fundamentals
> **Module 2:** Designing, Modeling, and Implementing Data Warehouses

# Hands-on Lab: Populating a Data Warehouse using PostgreSQL

<mark>NEW</mark>

## Estimated Time
1 hour

## Purpose of the Lab

The lab is designed to provide hands-on experience in creating and managing a production database using PostgreSQL within the IBM Skills Network Labs (SN Labs) Cloud IDE. You will learn how to launch a PostgreSQL server instance, utilize the pgAdmin graphical user interface (GUI) for database operations, and execute essential tasks like creating a database, designing tables, and loading data. The lab focuses on building a foundation in database management by guiding learners through the process of setting up a 'Production' database and populating it with data following a star schema design.

## Benefits of Learning the Lab

Engaging in this lab offers significant benefits for learners seeking to deepen their understanding of database management systems, particularly PostgreSQL. By working through the lab, you will gain practical skills in SQL, database creation, table design, and data manipulation, which are crucial for roles in data engineering, database administration, and data science. The hands-on approach helps in consolidating knowledge of database schemas and SQL queries, thereby enhancing the learner's ability to manage and analyze data effectively in real-world scenarios.

Additionally, familiarity with tools like pgAdmin and the Cloud IDE environment adds valuable experience to your skill set, preparing you for advanced database projects and tasks.

## Software Used in this Lab

To complete this lab you will utilize the PostgreSQL Database relational database service available as part of IBM Skills Network Labs (SN Labs) Cloud IDE. SN Labs is a virtual lab environment used in this course.

## Database Used in this Lab

Production database is used in this lab.

The production database contains:
- DimCustomer
- DimMonth
- FactBilling

## Objectives

In this lab you will:
- Create production related database and tables in a PostgreSQL instance.
- Populate the production data warehouse by loading the tables from Scripts.

## Lab Structure

In this lab, you will complete several tasks in which you will learn how to create tables and load data in the PostgreSQL database service using the pgAdmin graphical user interface (GUI) tool.

## Data Used in this Lab

The following are the SQL data files used in this lab.

The production database contains:
- DimCustomer
- DimMonth
- FactBilling
- Star Schema

---

## Docker Setup for Local Execution

### Start PostgreSQL Container

```bash
docker run -d \
  --name postgres-dw-lab \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16
```

### Verify Container is Running

```bash
docker ps | grep postgres-dw-lab
```

### Connect to PostgreSQL

```bash
docker exec -it postgres-dw-lab psql -U postgres
```

---

## Task A: Create a Database

First, to create a database on a PostgreSQL server instance, you'll first want to actually launch a PostgreSQL server instance on Cloud IDE and open up the pgAdmin Graphical User Interface.

### Steps (Cloud IDE):

1. Click on the Skills Network extension button on the left side of the window.
2. Open the DATABASES drop down menu.
3. Click on PostgreSQL.
4. Click on the Create button. PostgreSQL may take a few moments to start.

5. Next, open the pgAdmin Graphical User Interface by clicking the pgAdmin launch button in the Cloud IDE interface.

6. Once the pgAdmin GUI opens, click on the Servers tab on the left side of the page. You will be prompted to enter a password.

7. To retrieve your password, click on the PostgreSQL and go to Connection Information tab on the top of the interface.

8. Scroll down to the session password and click on the Copy icon to the right of your password to copy onto your clipboard.

9. Navigate back to the pgAdmin tab and paste in your password, then click OK.

10. You will then be able to access the pgAdmin GUI tool.

11. In the left tree-view, right-click on Databases > Create > Database.

12. In the Database box, type Production as the name for your new database, and then click Save. Proceed to Task B.

### Steps (Local Docker):

```powershell
docker exec -i postgres-dw-lab psql -U postgres -c "CREATE DATABASE production;"
```

---

## Task B: Create Tables

Now, that you have your PostgreSQL service active and have created the Production database using pgAdmin, let's go ahead and create a few tables to populate the database and store the data that we wish to eventually upload into it.

### Steps (Cloud IDE):

1. Click on the Production database and in the top of the page go to Query tool and then click on Open File. Next a new page pops up called Select File. Click on the three dots and choose Upload option as shown in the screenshot.

> **Note:** Ensure that you upload the files to this path: `/var/lib/pgadmin/`

2. In the new blank page that appears drag and drop the star-schema.sql file inside the blank page. Once the star-schema.sql file is successfully loaded, click on the X icon on the right hand side of the page as shown in the screenshot.

3. Once you click on the X icon a new page appears with the file star-schema.sql. Select the star-schema.sql file from the list and click the Select tab.

4. Once the file opens up click on the Run option to execute the star-schema.sql file.

5. Next, right-click on the Production database and click on the Refresh option from the dropdown.

After the database is refreshed the 3 tables (DimCustomer, DimMonth, FactBilling) are created under the Databases > Production > Schemas > Public > Tables.

### Steps (Local Docker):

```powershell
# Copy schema file to container
docker cp star-schema.sql postgres-dw-lab:/tmp/star-schema.sql

# Apply schema
docker exec -i postgres-dw-lab psql -U postgres production -f /tmp/star-schema.sql
```

---

## Task C: Load Tables

1. Click on Query tool and then click Open file and click on the three dot and choose Upload option.

2. In the new blank page that appears drag and drop the DimCustomer.sql file inside the blank page. Once the DimCustomer.sql file is successfully loaded. Click on the small X icon on the right hand side of the page as shown in the screenshot.

3. Once you click on the X icon a new page appears with the file DimCustomer.sql. Select the DimCustomer.sql file from the list and click on Select tab.

4. Once the file opens up, click on the Run option to execute the DimCustomer.sql file.

> **Note:** Repeat the steps as given in Task C to upload the remaining sql files to insert data in DimMonth and FactBilling.

5. Let's run the command below on the PostgreSQL Tool.

```sql
select count(*) from public."DimMonth";
```

You should see an output as seen in the image below.

You are encouraged to run more SQL queries.

### Steps (Local Docker):

```powershell
# Copy data files to container
docker cp DimCustomer.sql postgres-dw-lab:/tmp/DimCustomer.sql
docker cp DimMonth.sql postgres-dw-lab:/tmp/DimMonth.sql
docker cp FactBilling.sql postgres-dw-lab:/tmp/FactBilling.sql

# Load data
docker exec -i postgres-dw-lab psql -U postgres production -f /tmp/DimCustomer.sql
docker exec -i postgres-dw-lab psql -U postgres production -f /tmp/DimMonth.sql
docker exec -i postgres-dw-lab psql -U postgres production -f /tmp/FactBilling.sql

# Verify data loaded
docker exec -i postgres-dw-lab psql -U postgres production -c "SELECT count(*) FROM public.\"DimMonth\";"
```

---

## Practice Exercises

### Problem 1
Using the PostgreSQL tool, find the count of rows in the table FactBilling.

<details>
<summary>Click here for Hint</summary>

Use the SELECT COUNT(*) statement on the FactBilling table.

</details>

<details>
<summary>Click here for Solution</summary>

```sql
SELECT count(*) FROM public."FactBilling";
```

</details>

### Problem 2
Using the PostgreSQL tool, create a simple Materialized view named avg_customer_bill with fields customerid and averagebillamount.

<details>
<summary>Click here for Hint</summary>

Use the CREATE MATERIALIZED VIEW statement with a GROUP BY clause.

</details>

<details>
<summary>Click here for Solution</summary>

```sql
CREATE MATERIALIZED VIEW avg_customer_bill AS
SELECT customerid, AVG(billedamount) AS averagebillamount
FROM public."FactBilling"
GROUP BY customerid;
```

</details>

### Problem 3
Refresh the newly created Materialized views.

<details>
<summary>Click here for Hint</summary>

Use the REFRESH MATERIALIZED VIEW statement.

</details>

<details>
<summary>Click here for Solution</summary>

```sql
REFRESH MATERIALIZED VIEW avg_customer_bill;
```

</details>

### Problem 4
Using the newly created Materialized views find the customers whose average billing is more than 11000.

<details>
<summary>Click here for Hint</summary>

Use a SELECT statement with a WHERE clause on the materialized view.

</details>

<details>
<summary>Click here for Solution</summary>

```sql
SELECT * FROM avg_customer_bill WHERE averagebillamount > 11000;
```

</details>

---

## Congratulations!

You have successfully finished the Populating a Data Warehouse lab.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Lab Overview | Definition | Production database follows star schema design | HIGH | Lab content |
| 2 | Task A | Example | Added Docker commands for local PostgreSQL setup | HIGH | UNCERTAIN |
| 3 | Task C | Example | Added Docker commands for loading data files | HIGH | UNCERTAIN |
| 4 | Practice Exercises | Code | Added SQL solutions for all 4 practice problems | HIGH | Lab content |

---

**Author:** Amrutha Rao
**© IBM Corporation 2022. All rights reserved.**

<!-- EXTRACTION_CHECKLIST: 62 sentences extracted, 62 sentences in output -->
