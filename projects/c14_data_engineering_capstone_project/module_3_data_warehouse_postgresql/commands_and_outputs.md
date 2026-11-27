# Hands-on Lab: Data Warehouse Analytics Queries and Execution Outputs

**Estimated Study Time:** 55 mins (Deep Comprehension @ 2.5x) | Hands-on Lab Base: 22 mins (Nominal Effort: 30 mins)

> **Associated Lab Guide:** [c14_m3_data_warehouse_reporting.md](<c14_m3_data_warehouse_reporting.md>)  
> **Course:** [Course 14: Data Engineering Capstone Project](../../../../../index.md)  
> **Module:** [Module 3: Build a Data Warehouse](../../../index.md)  
> **Part:** [Part 2: Data Warehouse Reporting](../../index.md)  
> **Database:** `Test1` (PostgreSQL)  

---

## Overview

This document records the executed OLAP analytical queries and verbatim terminal outputs produced during **Task 5 through Task 8** of the Data Warehouse Reporting lab for the SoftCart e-commerce platform.

---

## Task 5: Create a Grouping Sets Query

Execute a `GROUPING SETS` query using the dimensions `country` and `category` alongside aggregated `totalsales` from `FactSales`.

### SQL Query
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

### Execution Output
```text
country                       |                      category                      | totalsales
----------------------------------------------------+----------------------------------------------------+------------
 Argentina                                          | Books                                              |    4285010
 Argentina                                          | Electronics                                        |    4338757
 Argentina                                          | Software                                           |    4292153
 Argentina                                          | Sports                                             |    4450354
 Argentina                                          | Toys                                               |    4389307
 Argentina                                          |                                                    |   21755581
 Australia                                          | Books                                              |    4340188
 Australia                                          | Electronics                                        |    4194740
 Australia                                          | Software                                           |    4410360
 Australia                                          | Sports                                             |    4201103
 Australia                                          | Toys                                               |    4375613
 Australia                                          |                                                    |   21522004
 Austria                                            | Books                                              |    4326948
 Austria                                            | Electronics                                        |    4217401
 Austria                                            | Software                                           |    4277079
 Austria                                            | Sports                                             |    4322907
 Austria                                            | Toys                                               |    4221391
 Austria                                            |                                                    |   21365726
 Azerbaijan                                         | Books                                              |    4286053
 Azerbaijan                                         | Electronics                                        |    4244146
 Azerbaijan                                         | Software                                           |    4295528
 Azerbaijan                                         | Sports                                             |    4279866
 Azerbaijan                                         | Toys                                               |    4220173
 Azerbaijan                                         |                                                    |   21325766
 Belgium                                            | Books                                              |    4320892
 Belgium                                            | Electronics                                        |    4272771
 Belgium                                            | Software                                           |    4304601
 Belgium                                            | Sports                                             |    4283485
 Belgium                                            | Toys                                               |    4316500
 Belgium                                            |                                                    |   21498249
 Brazil                                             | Books                                              |    4221036
 Brazil                                             | Electronics                                        |    4326684
 Brazil                                             | Software                                           |    4264671
 Brazil                                             | Sports                                             |    4257976
 Brazil                                             | Toys                                               |    4280404
 Brazil                                             |                                                    |   21350771
 Bulgaria                                           | Books                                              |    4227020
 Bulgaria                                           | Electronics                                        |    4259350
```

---

## Task 6: Create a Rollup Query

Execute a hierarchical `ROLLUP` query using the temporal dimension `year` and geographical dimension `country` with aggregated `totalsales`.

### SQL Query
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

### Execution Output
```text
year |                      country                       | totalsales
------+----------------------------------------------------+------------
 2019 | Argentina                                          |    7163167
 2019 | Australia                                          |    7259016
 2019 | Austria                                            |    7320233
 2019 | Azerbaijan                                         |    7097729
 2019 | Belgium                                            |    7093441
 2019 | Brazil                                             |    7116253
 2019 | Bulgaria                                           |    7312912
 2019 | Canada                                             |    7158271
 2019 | Cyprus                                             |    7250287
 2019 | Czech Republic                                     |    7087032
 2019 | Denmark                                            |    6955746
 2019 | Egypt                                              |    7169300
 2019 | Estonia                                            |    7193792
 2019 | Finland                                            |    7064381
 2019 | France                                             |    7077076
 2019 | Germany                                            |    7056510
 2019 | Greece                                             |    7208571
 2019 | Hungary                                            |    6922795
 2019 | India                                              |    7210119
 2019 | Indonesia                                          |    7316521
 2019 | Ireland                                            |    6886406
 2019 | Israel                                             |    7158364
 2019 | Italy                                              |    7310397
:
```

---

## Task 7: Create a Cube Query

Execute a multidimensional `CUBE` query using `year` and `country` calculating average sales (`averagesales`).

### SQL Query
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

### Execution Output
```text
year |                      country                       |     averagesales
------+----------------------------------------------------+-----------------------
 2019 | Argentina                                          | 4017.4800897363993270
 2019 | Australia                                          | 4066.6756302521008403
 2019 | Austria                                            | 4078.1242339832869081
 2019 | Azerbaijan                                         | 3967.4281721632196758
 2019 | Belgium                                            | 3978.3740886146943354
 2019 | Brazil                                             | 4025.0299773755656109
 2019 | Bulgaria                                           | 4087.7093348239239799
 2019 | Canada                                             | 4005.7476217123670957
 2019 | Cyprus                                             | 4045.9190848214285714
 2019 | Czech Republic                                     | 3979.2431218416619876
 2019 | Denmark                                            | 3909.9190556492411467
 2019 | Egypt                                              | 4014.1657334826427772
 2019 | Estonia                                            | 4021.1246506428172163
 2019 | Finland                                            | 3957.6364145658263305
 2019 | France                                             | 3960.3111359820928931
 2019 | Germany                                            | 3946.5939597315436242
 2019 | Greece                                             | 4045.2138047138047138
 2019 | Hungary                                            | 3882.6668536174985979
 2019 | India                                              | 4050.6286516853932584
 2019 | Indonesia                                          | 4062.4769572459744586
 2019 | Ireland                                            | 3868.7674157303370787
 2019 | Israel                                             | 4019.2947782144862437
 2019 | Italy                                              | 4086.3035215204024595
 2019 | Japan                                              | 3991.0339454646633278
 2019 | Jordan                                             | 3967.7225661226786719
 2019 | Malaysia                                           | 4053.2417088251826869
 2019 | Mexico                                             | 4022.0276056338028169
 2019 | Netherlands                                        | 3928.5738255033557047
 2019 | New Zealand                                        | 4018.1849547511312217
 2019 | Norway                                             | 4045.9837625979843225
 2019 | Oman                                               | 3944.8878873239436620
 2019 | Peru                                               | 4008.7938547486033520
 2019 | Philippines                                        | 4009.1907158836689038
 2019 | Poland                                             | 4039.2245357343837929
 2019 | Portugal                                           | 4053.7745208568207441
 2019 | Qatar                                              | 3982.8494983277591973
 2019 | Russia                                             | 4030.8080581980973699
 2019 | Saudi Arabia                                       | 4049.7827547592385218
:
```

---

## Task 8: Create and Query a Materialized Query Table (MQT / Materialized View)

Create a materialized view `total_sales_per_country` precomputing total sales per country to accelerate recurring dashboard and analytical queries.

### SQL Query
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

### Execution Output
```text
country                       | total_sales
----------------------------------------------------+-------------
 Argentina                                          |    21755581
 Australia                                          |    21522004
 Austria                                            |    21365726
 Azerbaijan                                         |    21325766
 Belgium                                            |    21498249
 Brazil                                             |    21350771
 Bulgaria                                           |    21410716
 Canada                                             |    21575438
 Cyprus                                             |    21500526
 Czech Republic                                     |    21334142
 Denmark                                            |    21331097
 Egypt                                              |    21379967
 Estonia                                            |    21493054
 Finland                                            |    21336188
 France                                             |    21341055
 Germany                                            |    21301931
 Greece                                             |    21412393
 Hungary                                            |    21338015
 India                                              |    21330883
 Indonesia                                          |    21498960
 Ireland                                            |    21095982
 Israel                                             |    21581548
 Italy                                              |    21844913
 Japan                                              |    21765341
 Jordan                                             |    21429604
 Malaysia                                           |    21452597
 Mexico                                             |    21455404
 Netherlands                                        |    21383019
 New Zealand                                        |    21329461
 Norway                                             |    21544439
 Oman                                               |    21433121
 Peru                                               |    21704462
 Philippines                                        |    21651762
 Poland                                             |    21845131
 Portugal                                           |    21554611
 Qatar                                              |    21473762
 Russia                                             |    21738876
 Saudi Arabia                                       |    21326437
:
```
