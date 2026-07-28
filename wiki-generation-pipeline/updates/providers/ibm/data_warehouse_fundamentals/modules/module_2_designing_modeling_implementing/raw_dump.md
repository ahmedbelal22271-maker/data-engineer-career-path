IBM
×
0:00 / 5:31
Overview of Data Warehouse Architectures

Dive deeper on this topic
Transcript
​
Interactive Transcript - Enable basic transcript mode by pressing the escape key

You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key
​Welcome to “Data Warehouse Architecture Overview.” ​After watching this video, you will be able to: ​List use cases that drive data warehouse design considerations. ​Describe a general data warehousing architecture and list its component layers. ​Distinguish between general and reference enterprise data warehouse architecture and ​Describe reference architectures for two enterprise data warehouse platforms. ​The details of the architecture of a data warehouse depend on the intended usage of ​the platform. ​Requirements can include ​report generation and dashboarding, ​exploratory data analysis, ​automation and machine learning, and ​self-serve analytics. ​Let’s start by considering a general architectural model for an Enterprise Data Warehouse, or ​EDW, platform, which companies can adapt for their analytics requirements. 
​In this architecture, you can have various layers or components, including: ​Data sources, such as flat files, databases, and existing operational systems, ​an ETL layer for extracting, transforming, and loading data, ​optional staging and sandbox areas for holding data and developing workflows, ​an enterprise data warehouse repository, ​sometimes, data marts, which are known as a “hub and spoke” architecture when multiple ​data marts are involved, and an analytics layer and business intelligence tools. ​Data warehouses also enforce security for incoming data and data passing through to ​further stages and users throughout the network. ​Enterprise data warehouse vendors often create proprietary reference architecture and implement ​template data warehousing solutions that are variations on this general architectural model. ​A data warehousing platform is a complex environment with lots of moving parts. ​Thus, interoperability among components is vital. ​Vendor-specific reference architecture typically incorporates tools and products from the vendor’s ​ecosystem that work well together. ​Next, let’s check out IBM-specific reference data warehouse architecture. 
​Each layer of the architecture performs a specific function: ​The data acquisition layer consists of components to acquire raw data from source systems, such ​as human resources, finance, and billing departments. ​The data integration layer, essentially a staging area, has components for extracting ​the data, transforming it, and loading it into the data repository layer. ​It also houses administration tools and central metadata. ​The data repository layer stores the integrated data, typically employing a relational model. ​The analytics layer often stores data in a cube format to make it easier for users to ​analyze it. ​And, the final presentation layer incorporates applications that provide access for different ​sets of users, such as marketing analysts, users, and agents. ​Applications consume the data through web pages and portals defined in the reporting ​tool or through web services. 
​IBM reference architecture is supported and extended using several products from the IBM ​InfoSphere suite. ​IBM InfoSphere DataStage is a scalable ETL platform that delivers near real-time integration ​of all data types, on-premises, and in cloud environments. ​IBM InfoSphere MetaData Workbench provides end-to-end data flow reporting and impacts ​analysis of information assets in an environment that allows organizations to share easily, ​locate, and retrieve information from these systems. ​Use the built-in data flow reporting capabilities to monitor how IBM InfoSphere DataStage moves ​and transforms your data. ​IBM InfoSphere QualityStage, designed to support your data quality and information governance ​initiatives, enables you to investigate, cleanse, and manage your data. ​This solution helps you create and maintain consistent views of key entities, including ​customers, vendors, locations, and products. ​IBM Db2 Warehouse is a family of highly performant, scalable, and reliable data management products ​that manage both structured and unstructured data across on-premises and cloud environments. 
​And finally, IBM Cognos Analytics is an advanced business intelligence platform that generates reports, ​scoreboards, and dashboards, performs exploratory data analysis, and even curates and joins ​your data using multiple sources. ​In this video, you learned that: ​An architectural model for a general data warehousing platform includes data sources, ​ETL pipelines, optional staging and sandbox areas, an enterprise data warehouse repository, ​optional data marts, and analytics and business intelligence tools. ​Companies can modify general enterprise data warehouse architecture to suit their analytics ​requirements. ​Vendors offer proprietary reference architecture based on the general model, which they test ​for interoperability among components. ​An IBM enterprise data warehouse solution combines InfoSphere with Db2 Warehouse and ​Cognos Analytics. 
IBM 0:00 / 5:31 Overview of Data Warehouse Architectures Dive deeper on this topic Transcript ​ Interactive Transcript - Enable basic transcript mode by pressing the escape key You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key ​Welcome to “Data Warehouse Architecture Overview.” ​After watching this video, you will be able to: ​List use cases that drive data warehouse design considerations. ​Describe a general data warehousing architecture and list its component layers. ​Distinguish between general and reference enterprise data warehouse architecture and ​Describe reference architectures for two enterprise data warehouse platforms. ​The details of the architecture of a data warehouse depend on the intended usage of ​the platform. ​Requirements can include ​report generation and dashboarding, ​exploratory data analysis, ​automation and machine learning, and ​self-serve analytics. ​Let’s start by considering a general architectural model for an Enterprise Data Warehouse, or ​EDW, platform, which companies can adapt for their analytics requirements. ​In this architecture, you can have various layers or components, including: ​Data sources, such as flat files, databases, and existing operational systems, ​an ETL layer for extracting, transforming, and loading data, ​optional staging and sandbox areas for holding data and developing workflows, ​an enterprise data warehouse repository, ​sometimes, data marts, which are known as a “hub and spoke” architecture when multiple ​data marts are involved, and an analytics layer and business intelligence tools. ​Data warehouses also enforce security for incoming data and data passing through to ​further stages and users throughout the network. ​Enterprise data warehouse vendors often create proprietary reference architecture and implement ​template data warehousing solutions that are variations on this general architectural model. ​A data warehousing platform is a complex environment with lots of moving parts. ​Thus, interoperability among components is vital. ​Vendor-specific reference architecture typically incorporates tools and products from the vendor’s ​ecosystem that work well together. ​Next, let’s check out IBM-specific reference data warehouse architecture. ​Each layer of the architecture performs a specific function: ​The data acquisition layer consists of components to acquire raw data from source systems, such ​as human resources, finance, and billing departments. ​The data integration layer, essentially a staging area, has components for extracting ​the data, transforming it, and loading it into the data repository layer. ​It also houses administration tools and central metadata. ​The data repository layer stores the integrated data, typically employing a relational model. ​The analytics layer often stores data in a cube format to make it easier for users to ​analyze it. ​And, the final presentation layer incorporates applications that provide access for different ​sets of users, such as marketing analysts, users, and agents. ​Applications consume the data through web pages and portals defined in the reporting ​tool or through web services. ​IBM reference architecture is supported and extended using several products from the IBM ​InfoSphere suite. ​IBM InfoSphere DataStage is a scalable ETL platform that delivers near real-time integration ​of all data types, on-premises, and in cloud environments. ​IBM InfoSphere MetaData Workbench provides end-to-end data flow reporting and impacts ​analysis of information assets in an environment that allows organizations to share easily, ​locate, and retrieve information from these systems. ​Use the built-in data flow reporting capabilities to monitor how IBM InfoSphere DataStage moves ​and transforms your data. ​IBM InfoSphere QualityStage, designed to support your data quality and information governance ​initiatives, enables you to investigate, cleanse, and manage your data. ​This solution helps you create and maintain consistent views of key entities, including ​customers, vendors, locations, and products. ​IBM Db2 Warehouse is a family of highly performant, scalable, and reliable data management products ​that manage both structured and unstructured data across on-premises and cloud environments. ​And finally, IBM Cognos Analytics is an advanced business intelligence platform that generates reports, ​scoreboards, and dashboards, performs exploratory data analysis, and even curates and joins ​your data using multiple sources. ​In this video, you learned that: ​An architectural model for a general data warehousing platform includes data sources, ​ETL pipelines, optional staging and sandbox areas, an enterprise data warehouse repository, ​optional data marts, and analytics and business intelligence tools. ​Companies can modify general enterprise data warehouse architecture to suit their analytics ​requirements. ​Vendors offer proprietary reference architecture based on the general model, which they test ​for interoperability among components. ​An IBM enterprise data warehouse solution combines InfoSphere with Db2 Warehouse and ​Cognos Analytics. : Added to Selection. Press [CTRL + S] to save as a note : Added to Selection. Press [CTRL + S] to save as a note




IBM
×
0:04 / 7:36
Cubes, Rollups, and Materialized Views and Tables

Dive deeper on this topic
Transcript
​
Interactive Transcript - Enable basic transcript mode by pressing the escape key

You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key
​Welcome to Cubes, Rollups, and Materialized Views and Tables. ​After watching this video, you will be able to: ​Relate what a data cube is in terms of star schema. ​Discuss the terms slice, dice, drill up or down, roll up, and pivot in terms of data ​cubes. ​Describe what a materialized view is. ​And, recall two use cases for materialized views. ​Let’s use an example to illustrate the concept of a data cube. ​Here is a cube generated from an imaginary star schema for a Sales OLAP (online analytical ​processing system). 
​The coordinates of the cube are defined by a set of dimensions, which are selected from ​the star schema. ​In this illustration, we are only showing three dimensions, but data cubes can have ​many dimensions. ​We have the Product categories corresponding to the items sold, the State or Province the ​items were sold from, and the Year these products were sold in. ​The cells of the cube are defined by a fact of interest from the schema, which could be ​something like “total sales in thousands of dollars.” ​Here the “243” indicates “243 thousand dollars” for some given Product, State, ​and Year combination. ​There are many operations you can perform on data cubes, such as slicing, dicing, drilling ​up and down, pivoting, and rolling up. ​Let’s go over some examples of these operations, starting with slicing. 
​Slicing a data cube involves selecting a single member from a dimension, which yields a data ​cube that has one dimension less than the original. ​For example, you can slice this sales cube by selecting only the year 2018 from the year ​dimension, allowing you to analyze sales totals for all sales states and all products for ​the year 2018. ​Similarly, dicing a cube involves selecting a subset of values from a dimension, effectively ​shrinking it. ​For example, you can dice this sales cube by selecting only “Gloves”, “T-shirts”, ​and “Jeans” from the Product-Type dimension, allowing you to restrict your view to just ​those product types. ​In snowflake schema, you will find hierarchies, or subcategories within some of your dimensions ​that you can drill into. ​Thus, for example, you can “drill down” into a particular member of the “Product ​category” dimension, such as “T-shirts,” resulting in this view, which may include ​more specific “product groups” such as “Classic,” “Slim fit,” and “Regular ​fit.” ​Drilling up is just the reverse process, which would take you back to the original data cube. 
​Pivoting data cubes is straightforward. ​It involves a rotation of the data cube. ​In this case, the year and product dimensions have been interchanged, while the State dimension ​has been fixed "as is." ​Pivoting doesn’t change its information content; it just changes the point of view ​you may choose to analyze it from. ​Rolling up means summarizing along a dimension. ​You can roll up a dimension by applying aggregations, such as ​COUNT, MIN, MAX, SUM, and AVERAGE. ​For example, you could calculate the average selling price of Classic, Slim fit, and Regular ​fit T-shirts by summing horizontally over the three US states and dividing by three. 
​A “materialized view” is essentially a local, read-only copy, or snapshot, of the ​results of a query. ​They can be used to replicate data, for example to be used in a staging database as part of ​an ETL process, or to precompute and cache expensive queries, such as joins or aggregations, ​for use in data analytics environments. ​Materialized views also have options for automatically refreshing the data, thus keeping your query ​up-to-date. ​Because materialized views can be queried, you can safely work with them without worrying ​about affecting the source database. ​Materialized Views can be set up to have different refresh options, such as: ​Never: they are only populated when created, which is useful if the data seldom changes. ​Upon request: manually refresh, for example, after changes to the data have been made, ​or scheduled refresh, for example, after daily data loads. ​Immediately: automatically refresh after every statement. 
​Let’s look at an example. ​Here is how you might create a materialized view in Oracle using SQL statements. ​Start by creating and naming a “materialized view” object called “My underscore Mat ​underscore View”, ​Specify the refresh type as fast, which means “incrementally refresh the data”. ​Specify today as the start date, and ​Refresh the view every day. ​The final statement selects all data from my underscore table underscore name. ​Here is how you might create a materialized view in PostgreSQL to replicate a table. ​Start by creating a “materialized view” object called “My underscore Mat underscore ​View”, ​Specify some parameters, ​Specify the source tablespace, say “tablespace underscore name”, and ​Select all rows and columns from “table underscore name.” 
​In PostgreSQL you can only refresh materialized views manually, using the “refresh material ​view” command. ​In Db2, materialized views are called MQTs, which stands for "materialized query tables." ​Here’s an example, from IBM’s online documentation, of creating a system-maintained “immediate ​refresh” MQT. ​The table, which is named “emp,” is based on the underlying tables: “Employee” and ​“Department” from the “Sample” database. ​The table will be created according to the query formed by these SQL statements, which ​selects columns from both tables. ​The “data initially deferred” clause means that data will not be inserted into the table ​as part of the “create table” statement, while the “refresh immediate” clause specifies ​that the query should refresh automatically. ​The “immediate checked” clause specifies that the data is to be checked against the ​MQT’s defining query and refreshed. 
​Lastly, the “not incremental” clause specifies that integrity checking is to be done on the ​whole table. ​A query executed against the “emp” materialized query table shows that it is fully populated ​with data. ​In this video, you learned that: ​A data cube represents a star or snowflake schema’s dimensions as coordinates, plus ​a fact from the schema to populate its cells with values. ​Many operations can be applied to data cubes, such as: drilling down into hierarchical dimensions, ​slicing, dicing, and rolling up. ​Materialized views can be used to replicate data or to precompute expensive queries. ​And finally, modern enterprise data warehouse tools, such Oracle and Db2, allow you to automatically ​keep your material views up-to-date. 
IBM 0:04 / 7:36 Cubes, Rollups, and Materialized Views and Tables Dive deeper on this topic Transcript ​ Interactive Transcript - Enable basic transcript mode by pressing the escape key You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key ​Welcome to Cubes, Rollups, and Materialized Views and Tables. ​After watching this video, you will be able to: ​Relate what a data cube is in terms of star schema. ​Discuss the terms slice, dice, drill up or down, roll up, and pivot in terms of data ​cubes. ​Describe what a materialized view is. ​And, recall two use cases for materialized views. ​Let’s use an example to illustrate the concept of a data cube. ​Here is a cube generated from an imaginary star schema for a Sales OLAP (online analytical ​processing system). ​The coordinates of the cube are defined by a set of dimensions, which are selected from ​the star schema. ​In this illustration, we are only showing three dimensions, but data cubes can have ​many dimensions. ​We have the Product categories corresponding to the items sold, the State or Province the ​items were sold from, and the Year these products were sold in. ​The cells of the cube are defined by a fact of interest from the schema, which could be ​something like “total sales in thousands of dollars.” ​Here the “243” indicates “243 thousand dollars” for some given Product, State, ​and Year combination. ​There are many operations you can perform on data cubes, such as slicing, dicing, drilling ​up and down, pivoting, and rolling up. ​Let’s go over some examples of these operations, starting with slicing. ​Slicing a data cube involves selecting a single member from a dimension, which yields a data ​cube that has one dimension less than the original. ​For example, you can slice this sales cube by selecting only the year 2018 from the year ​dimension, allowing you to analyze sales totals for all sales states and all products for ​the year 2018. ​Similarly, dicing a cube involves selecting a subset of values from a dimension, effectively ​shrinking it. ​For example, you can dice this sales cube by selecting only “Gloves”, “T-shirts”, ​and “Jeans” from the Product-Type dimension, allowing you to restrict your view to just ​those product types. ​In snowflake schema, you will find hierarchies, or subcategories within some of your dimensions ​that you can drill into. ​Thus, for example, you can “drill down” into a particular member of the “Product ​category” dimension, such as “T-shirts,” resulting in this view, which may include ​more specific “product groups” such as “Classic,” “Slim fit,” and “Regular ​fit.” ​Drilling up is just the reverse process, which would take you back to the original data cube. ​Pivoting data cubes is straightforward. ​It involves a rotation of the data cube. ​In this case, the year and product dimensions have been interchanged, while the State dimension ​has been fixed "as is." ​Pivoting doesn’t change its information content; it just changes the point of view ​you may choose to analyze it from. ​Rolling up means summarizing along a dimension. ​You can roll up a dimension by applying aggregations, such as ​COUNT, MIN, MAX, SUM, and AVERAGE. ​For example, you could calculate the average selling price of Classic, Slim fit, and Regular ​fit T-shirts by summing horizontally over the three US states and dividing by three. ​A “materialized view” is essentially a local, read-only copy, or snapshot, of the ​results of a query. ​They can be used to replicate data, for example to be used in a staging database as part of ​an ETL process, or to precompute and cache expensive queries, such as joins or aggregations, ​for use in data analytics environments. ​Materialized views also have options for automatically refreshing the data, thus keeping your query ​up-to-date. ​Because materialized views can be queried, you can safely work with them without worrying ​about affecting the source database. ​Materialized Views can be set up to have different refresh options, such as: ​Never: they are only populated when created, which is useful if the data seldom changes. ​Upon request: manually refresh, for example, after changes to the data have been made, ​or scheduled refresh, for example, after daily data loads. ​Immediately: automatically refresh after every statement. ​Let’s look at an example. ​Here is how you might create a materialized view in Oracle using SQL statements. ​Start by creating and naming a “materialized view” object called “My underscore Mat ​underscore View”, ​Specify the refresh type as fast, which means “incrementally refresh the data”. ​Specify today as the start date, and ​Refresh the view every day. ​The final statement selects all data from my underscore table underscore name. ​Here is how you might create a materialized view in PostgreSQL to replicate a table. ​Start by creating a “materialized view” object called “My underscore Mat underscore ​View”, ​Specify some parameters, ​Specify the source tablespace, say “tablespace underscore name”, and ​Select all rows and columns from “table underscore name.” ​In PostgreSQL you can only refresh materialized views manually, using the “refresh material ​view” command. ​In Db2, materialized views are called MQTs, which stands for "materialized query tables." ​Here’s an example, from IBM’s online documentation, of creating a system-maintained “immediate ​refresh” MQT. ​The table, which is named “emp,” is based on the underlying tables: “Employee” and ​“Department” from the “Sample” database. ​The table will be created according to the query formed by these SQL statements, which ​selects columns from both tables. ​The “data initially deferred” clause means that data will not be inserted into the table ​as part of the “create table” statement, while the “refresh immediate” clause specifies ​that the query should refresh automatically. ​The “immediate checked” clause specifies that the data is to be checked against the ​MQT’s defining query and refreshed. ​Lastly, the “not incremental” clause specifies that integrity checking is to be done on the ​whole table. ​A query executed against the “emp” materialized query table shows that it is fully populated ​with data. ​In this video, you learned that: ​A data cube represents a star or snowflake schema’s dimensions as coordinates, plus ​a fact from the schema to populate its cells with values. ​Many operations can be applied to data cubes, such as: drilling down into hierarchical dimensions, ​slicing, dicing, and rolling up. ​Materialized views can be used to replicate data or to precompute expensive queries. ​And finally, modern enterprise data warehouse tools, such Oracle and Db2, allow you to automatically ​keep your material views up-to-date. : Added to Selection. Press [CTRL + S] to save as a note



IBM
Grouping Sets in SQL
0:02/2:45

The GROUPING SETS clause is used in conjunction with the GROUP BY clause to allow you to easily summarize data by aggregating a fact over as many dimensions as you like.  
SQL GROUP BY clause 

Recall that the SQL GROUP BY clause allows you to summarize an aggregation such as SUM or AVG over the distinct members, or groups, of a categorical variable or dimension. 

You can extend the functionality of the GROUP BY clause using SQL clauses such as CUBE and ROLLUP to select multiple dimensions and create multi-dimensional summaries. These two clauses also generate grand totals, like a report you might see in a spreadsheet application or an accounting style sheet. Just like CUBE and ROLLUP, the SQL GROUPING SETS clause allows you to aggregate data over multiple dimensions but does not generate grand totals. 
Examples 

Let’s start with an example of a regular GROUP BY aggregation and then compare the result to that of using the GROUPING SETS clause. We’ll use data from a fictional company called Shiny Auto Sales. The schema for the company’s warehouse is displayed in the entity-relationship diagram in Figure 1. 

Fig. 1. Entity-relationship diagram for a “sales” star schema based on the fictional “Shiny Auto Sales” company. 

We’ll work with a convenient materialized view of a completely denormalized fact table from the sales star schema, called DNsales, which looks like the following: 

This DNsales table was created by joining all the dimension tables to the central fact table and selecting only the columns which are displayed. Each record in DNsales contains details for an individual sales transaction. 
Example 1 

Consider the following SQL code which invokes GROUP BY on the auto class dimension to summarize total sales of new autos by auto class. 

The result looks like this: 
Example 2 

Now suppose you want to generate a similar view, but you also want to include the total sales by salesperson. You can use the GROUPING SETS clause to access both the auto class and salesperson dimensions in the same query. Here is the SQL code you can use to summarize total sales of new autos, both by auto class and by salesperson, all in one expression: 

Here is the query result. Notice that the first four rows are identical to the result of Example 1, while the next 5 rows are what you would get by substituting salespersonname for autoclassname in Example 1. 

Essentially, applying GROUPING SETS to the two dimensions, salespersonname and autoclassname, provides the same result that you would get by appending the two individual results of applying GROUP BY to each dimension separately as in Example 1. 












IBM
×
0:02 / 6:57
Data Modeling using Star and Snowflake Schemas

Dive deeper on this topic
Transcript
​
Interactive Transcript - Enable basic transcript mode by pressing the escape key

You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key
​Welcome to Data Modeling Using Star and Snowflake Schemas. ​After watching this video, you will be able to: ​Describe star schema modeling in terms of facts and dimensions. ​Describe snowflake schema as an extension of Star schema. ​Distinguish star from snowflake schema in terms of normalization. ​Recall that a fact table contains foreign keys ​that refer to the primary keys of dimension tables. ​The idea of a star schema is based on the way a set of dimension tables can be visualized, ​or modeled, as radiating from a central fact table, linked by these keys. ​A star schema is thus a graph, whose nodes are fact and dimension tables, ​and whose edges are the relations between those tables. 
​Star schemas are commonly used to develop specialized data warehouses called “data marts.” ​Snowflake schemas are a generalization of star ​schemas and can be seen as normalized star schemas. ​Normalization means separating the levels or hierarchies of a ​dimension table into separate child tables. ​A schema need not be fully normalized to be considered a snowflake, ​so long as at least one of its dimensions has its levels separated. ​Let’s look at some general principles you need ​to consider when designing a data model for a star schema. ​The first step involves selecting a business process as the basis for what you want to model. ​You might be interested in processes such as sales, manufacturing, or supply chain logistics. 
​In step two, you need to choose a granularity, ​which is the level of detail that you need to capture. ​Are you interested in coarse-grained information such as annual regional sales numbers? ​Or, maybe you want to drill down into monthly sales performance by salesperson. ​Next in the process, you need to identify the dimensions. ​These may include attributes such as the date and time, and names of people, places, and things. ​The final consideration in designing star schemas is to identify the facts. ​These are the things being measured in the business process. 
​Let’s apply these considerations to a scenario. ​Imagine, for example, that you are a data engineer helping to ​lay out the data ops for a new store called “A to Z Discount Warehouse.” ​They would like you to develop a data plan to capture everyday POS, ​or point-of-sales transactions that happen at the ​till, where customers have their items scanned and pay for them. ​Thus, “point-of-sale transactions” is the business process that you want to model. ​The finest granularity you can expect to capture from POS transactions comes from the individual ​line items, which is included in the detailed information you can see on a typical store receipt. ​This is precisely what “A to Z” is interested in capturing. ​The next step in the process is to identify the dimensions. 
​These include attributes such as the date and time of the purchase, ​the store name, the products purchased, and the cashier who processed the items. ​You might add other dimensions, like “payment method,” whether the ​line item is a return or a purchase, and perhaps a “customer membership number.” ​Now it’s time to consider the facts. ​Thus, you identify facts such as the amount for each item’s price, ​the quantity of each product sold, any discounts applied to the sale, and the sales tax applied. ​Other facts to consider include environmental fees, or deposit fees for returnable containers. ​Now you are ready to start building your star schema for “A to Z Discount Warehouse.” ​At the center of your star schema sits a “point-of-sales fact table,” ​which contains a unique ID, called “P O S ID,” for each line item in the transaction, ​plus the following facts, or measures: the amount of the transaction in dollars, ​the quantity, or number of items involved, the sales tax, and any discount applied. 
​There may be other facts to include, but these can be added later as you discover them. ​Each line item from a sales transaction has many dimensions associated with it. ​You include them as foreign keys in your fact table, ​or as links to the primary keys of your dimension tables. ​For example, the name of the store at which the item was sold is kept in a dimension table ​called “store,” which is identified in the fact-table by the value of ​the foreign “Store ID” key, which is the primary key for the Store table. ​Product information is stored in the Product table, ​which is uniquely identified by the “ProductID” key. ​Similarly, the date of the transaction is keyed by the “Date ID,” ​which cashier entered the transaction is keyed by the “Cashier ID,” ​and which member was involved is indicated by the “Member ID.” ​This illustrates what a star schema might look like. 
​Let’s see how you can use normalization to extend your star schema to a snowflake schema. ​Starting with your star schema, you can extract some of the details of the dimension tables ​into their own separate dimension tables, creating a hierarchy of tables. ​A separate city table can be used to record which city the store is in, ​while a foreign ‘city id’ key would be included in the ‘Store’ table to maintain the link. ​You might also have tables and keys for the city’s state or province, ​and a pre-defined sales region for the store, and for which country the store resides in. ​We’ve left out the associated keys for simplicity. ​We can continue to normalize other dimensions, like the product’s brand, ​and a “product category” that it belongs to, ​the day of week and the month corresponding to the date, plus the quarter, and so on. ​This normalized version of the star schema is called a snowflake schema, ​due to its multiple layers of branching which resembles a snowflake pattern. 
​Much like how pointers are used to point to memory locations ​in computing, normalization reduces the memory footprint of the data. ​In this video, you learned that: ​Facts and dimension tables, together with foreign and primary keys, ​are used to form star and snowflake modeling schemas. ​Design considerations for data modeling with star schema ​include identifying a business process, its granularity, and its facts and dimensions. ​Snowflake schemas can be described as normalized star schemas, where ​normalization involves separating dimension tables into individual tables ​defined by levels or hierarchies of the parent dimension and reduces storage footprint. 
IBM 0:00 / 6:57 Data Modeling using Star and Snowflake Schemas Dive deeper on this topic Transcript ​ Interactive Transcript - Enable basic transcript mode by pressing the escape key You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key ​Welcome to Data Modeling Using Star and Snowflake Schemas. ​After watching this video, you will be able to: ​Describe star schema modeling in terms of facts and dimensions. ​Describe snowflake schema as an extension of Star schema. ​Distinguish star from snowflake schema in terms of normalization. ​Recall that a fact table contains foreign keys ​that refer to the primary keys of dimension tables. ​The idea of a star schema is based on the way a set of dimension tables can be visualized, ​or modeled, as radiating from a central fact table, linked by these keys. ​A star schema is thus a graph, whose nodes are fact and dimension tables, ​and whose edges are the relations between those tables. ​Star schemas are commonly used to develop specialized data warehouses called “data marts.” ​Snowflake schemas are a generalization of star ​schemas and can be seen as normalized star schemas. ​Normalization means separating the levels or hierarchies of a ​dimension table into separate child tables. ​A schema need not be fully normalized to be considered a snowflake, ​so long as at least one of its dimensions has its levels separated. ​Let’s look at some general principles you need ​to consider when designing a data model for a star schema. ​The first step involves selecting a business process as the basis for what you want to model. ​You might be interested in processes such as sales, manufacturing, or supply chain logistics. ​In step two, you need to choose a granularity, ​which is the level of detail that you need to capture. ​Are you interested in coarse-grained information such as annual regional sales numbers? ​Or, maybe you want to drill down into monthly sales performance by salesperson. ​Next in the process, you need to identify the dimensions. ​These may include attributes such as the date and time, and names of people, places, and things. ​The final consideration in designing star schemas is to identify the facts. ​These are the things being measured in the business process. ​Let’s apply these considerations to a scenario. ​Imagine, for example, that you are a data engineer helping to ​lay out the data ops for a new store called “A to Z Discount Warehouse.” ​They would like you to develop a data plan to capture everyday POS, ​or point-of-sales transactions that happen at the ​till, where customers have their items scanned and pay for them. ​Thus, “point-of-sale transactions” is the business process that you want to model. ​The finest granularity you can expect to capture from POS transactions comes from the individual ​line items, which is included in the detailed information you can see on a typical store receipt. ​This is precisely what “A to Z” is interested in capturing. ​The next step in the process is to identify the dimensions. ​These include attributes such as the date and time of the purchase, ​the store name, the products purchased, and the cashier who processed the items. ​You might add other dimensions, like “payment method,” whether the ​line item is a return or a purchase, and perhaps a “customer membership number.” ​Now it’s time to consider the facts. ​Thus, you identify facts such as the amount for each item’s price, ​the quantity of each product sold, any discounts applied to the sale, and the sales tax applied. ​Other facts to consider include environmental fees, or deposit fees for returnable containers. ​Now you are ready to start building your star schema for “A to Z Discount Warehouse.” ​At the center of your star schema sits a “point-of-sales fact table,” ​which contains a unique ID, called “P O S ID,” for each line item in the transaction, ​plus the following facts, or measures: the amount of the transaction in dollars, ​the quantity, or number of items involved, the sales tax, and any discount applied. ​There may be other facts to include, but these can be added later as you discover them. ​Each line item from a sales transaction has many dimensions associated with it. ​You include them as foreign keys in your fact table, ​or as links to the primary keys of your dimension tables. ​For example, the name of the store at which the item was sold is kept in a dimension table ​called “store,” which is identified in the fact-table by the value of ​the foreign “Store ID” key, which is the primary key for the Store table. ​Product information is stored in the Product table, ​which is uniquely identified by the “ProductID” key. ​Similarly, the date of the transaction is keyed by the “Date ID,” ​which cashier entered the transaction is keyed by the “Cashier ID,” ​and which member was involved is indicated by the “Member ID.” ​This illustrates what a star schema might look like. ​Let’s see how you can use normalization to extend your star schema to a snowflake schema. ​Starting with your star schema, you can extract some of the details of the dimension tables ​into their own separate dimension tables, creating a hierarchy of tables. ​A separate city table can be used to record which city the store is in, ​while a foreign ‘city id’ key would be included in the ‘Store’ table to maintain the link. ​You might also have tables and keys for the city’s state or province, ​and a pre-defined sales region for the store, and for which country the store resides in. ​We’ve left out the associated keys for simplicity. ​We can continue to normalize other dimensions, like the product’s brand, ​and a “product category” that it belongs to, ​the day of week and the month corresponding to the date, plus the quarter, and so on. ​This normalized version of the star schema is called a snowflake schema, ​due to its multiple layers of branching which resembles a snowflake pattern. ​Much like how pointers are used to point to memory locations ​in computing, normalization reduces the memory footprint of the data. ​In this video, you learned that: ​Facts and dimension tables, together with foreign and primary keys, ​are used to form star and snowflake modeling schemas. ​Design considerations for data modeling with star schema ​include identifying a business process, its granularity, and its facts and dimensions. ​Snowflake schemas can be described as normalized star schemas, where ​normalization involves separating dimension tables into individual tables ​defined by levels or hierarchies of the parent dimension and reduces storage footprint. : Added to Selection. Press [CTRL + S] to save as a note












IBM
Data Warehousing with Star and Snowflake schemas
0:01/8:07
Why do we use these schemas, and how do they differ?


Star schemas are optimized for reads and are widely used for designing data marts, whereas snowflake schemas are optimized for writes and are widely used for transactional data warehousing. A star schema is a special case of a snowflake schema in which all hierarchical dimensions have been denormalized, or flattened.

Attribute 
	

Star schema 
	

Snowflake schema 

Read speed 
	

Fast 
	

Moderate 

Write speed 
	

Moderate 
	

Fast 

Storage space 
	

Moderate to high 
	

Low to moderate 

Data integrity risk 
	

Low to moderate  
	

Low  

Query complexity  
	

Simple to moderate 
	

Moderate to complex 

Schema complexity 
	

Simple to moderate 
	

Moderate to complex 

Dimension hierarchies 
	

Denormalized single tables 
	

Normalized over multiple tables 

Joins per dimension hierarchy 
	

One  
	

One per level  

Ideal use 
	

OLAP systems, Data Marts 
	

OLTP systems 


Table 1. A comparison of star and snowflake schema attributes. 
Normalization reduces redundancy

Both star and snowflake schemas benefit from the application of normalization. “Normalization reduces redundancy” is an idiom that points to a key advantage leveraged by both schemas.
 
Normalizing a table means to create, for each dimension:

    A surrogate key to replace the natural key, that is, the unique values of the given column, and 

    A lookup table to store the surrogate and natural key pairs.

Each surrogate key’s values are repeated exactly as many times within the normalized table as the natural key was before moving the natural key to its new lookup table. Thus, you did nothing to reduce the redundancy of the original table. 

However, dimensions typically contain groups of items that appear frequently, such as a “city name” or “product category”. Since you only need one instance from each group to build your lookup table, your lookup table will have many fewer rows than your fact table. If there are child dimensions involved, then the lookup table may still have some redundancy in the child dimension columns. In other words, if you have a hierarchical dimension, such as “Country”, “State”, and “City”, you can repeat the process on each level to further reduce the redundancy.

Notice that further normalizing your hierarchical dimensions has no effect on the size or content of your fact table - star and snowflake schema data models share identical fact tables.

Normalization reduces data size


When you normalize a table, you typically reduce its data size, because in the process you likely replace expensive data types, such as strings, with much smaller integer types. But to preserve the information content, you also need to create a new lookup table that contains the original objects.
 
The question is, does this new table use less storage than the savings you just gained in the normalized table?

For small data, this question is probably not worth considering, but for big data, or just data that is growing rapidly, the answer is yes, it is inevitable. Indeed, your fact table will grow much more quickly than your dimension tables, so normalizing your fact table, at least to the minimum degree of a star schema is likely warranted. Now the question is about which is better – star or snowflake?


Comparing benefits: snowflake vs. star data warehouses



The snowflake, being completely normalized, offers the least redundancy and the smallest storage footprint. If the data ever changes, this minimal redundancy means the snowflaked data needs to be changed in fewer places than would be required for a star schema. In other words, writes are faster, and changes are easier to implement.
 
However, due to the additional joins required in querying the data, the snowflake design can have an adverse impact on read speeds. By denormalizing to a star schema, you can boost your query efficiency.

You can also choose a middle path in designing your data warehouse. You could opt for a partially normalized schema. You could deploy a snowflake schema as your basis and create views or even materialized views of denormalized data. You could for example simulate a star schema on top of a snowflake schema. At the cost of some additional complexity, you can select from the best of both worlds to craft an optimal solution to meet your requirements.

Practical differences



Most queries you apply to the dataset, regardless of your schema choice, go through the fact table. Your fact table serves as a portal to your dimension tables.

The main practical difference between star and snowflake schema from the perspective of an analyst has to do with querying the data. You need more joins for a snowflake schema to gain access to the deeper levels of the hierarchical dimensions, which can reduce query performance over a star schema. Thus, data analysts and data scientists tend to prefer the simpler star schema.
 
Snowflake schemas are generally good for designing data warehouses and in particular, transaction processing systems, while star schemas are better for serving data marts, or data warehouses that have simple fact-dimension relationships. For example, suppose you have point-of-sale records accumulating in an Online Transaction Processing System (OLTP) which are copied as a daily batch ETL process to one or more Online Analytics Processing (OLAP) systems where subsequent analysis of large volumes of historical data is carried out. The OLTP source might use a snowflake schema to optimize performance for frequent writes, while the OLAP system uses a star schema to optimize for frequent reads. The ETL pipeline that moves the data between systems includes a denormalization step which collapses each hierarchy of dimension tables into a unified parent dimension table.


Too much of a good thing?



There is always a tradeoff between storage and compute that should factor into your data warehouse design choices. For example, do your end-users or applications need to have precomputed, stored dimensions such as ‘day of week’, ‘month of year’, or ‘quarter’ of the year? Columns or tables which are rarely required are occupying otherwise usable disk space. It might be better to compute such dimensions within your SQL statements only when they are needed. For example, given a star schema with a date dimension table, you could apply the SQL ‘MONTH’ function as MONTH(dim_date.date_column) on demand instead of joining the precomputed month column from the MONTH table in a snowflake schema.



Scenario

Suppose you are handed a small sample of data from a very large dataset in the form of a table by your client who would like you to take a look at the data and consider potential schemas for a data warehouse based on the sample. Putting aside gathering specific requirements for the moment, you start by exploring the table and find that there are exactly two types of columns in the dataset - facts and dimensions. There are no foreign keys although there is an index. You think of this table as being a completely denormalized, or flattened dataset.
 
You also notice that amongst the dimensions are columns with relatively expensive data types in terms of storage size, such as strings for names of people and places.

At this stage you already know you could equally well apply either a star or snowflake schema to the dataset, thereby normalizing to the degree you wish. Whether you choose star or snowflake, the total data size of the central fact table will be dramatically reduced. This is because instead of using dimensions directly in the main fact table, you use surrogate keys, which are typically integers; and you move the natural dimensions to their own tables or hierarchy of tables which are referenced by the surrogate keys. Even a 32-bit integer is small compared to say a 10-character string (8 X 10 = 80 bits).
 
Now it’s a matter of gathering requirements and finding some optimal normalization scheme for your schema.


 













IBM
×
0:01 / 4:48
Staging Areas for Data Warehouses

Dive deeper on this topic
Transcript
​
Interactive Transcript - Enable basic transcript mode by pressing the escape key

You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key
​Welcome to Staging Areas for Data Warehouses. ​After watching this video, you will be able to: ​Describe what a data warehouse staging area is. ​Describe why a staging area may be used. ​Relate how a staging area is used as a first step for integrating data sources. ​What is a data warehouse staging area? ​You can think of a staging area as an intermediate storage area that is used for ETL processing. ​Thus, staging areas act as a bridge between data sources and the target ​data warehouses, data marts, or other data repos. 
​They are often transient, meaning that they are erased after successfully running ETL workflows. ​However, many architectures hold data for archival or troubleshooting purposes. ​They are also useful for monitoring and optimizing your ETL workflows. ​Staging areas can be implemented in many ways, including: ​simple flat files, such as csv files, stored in a directory, ​and managed using tools such as Bash or Python, or ​a set of SQL tables in a relational database such as Db2, or ​a self-contained database instance within a data ​warehousing or business intelligence platform such as Cognos Analytics. ​Let’s explore an example use case, to illustrate a possible architecture for a Data Warehouse ​containing a Staging Area, which in turn includes an associated Staging Database. ​Imagine the enterprise would like to create a dedicated ​“Cost Accounting” Online Analytical Processing system. ​The required data is managed in separate Online Transaction Processing Systems within ​the enterprise, from the Payroll, Sales, and Purchasing departments. 
​From these siloed systems, the data is extracted to individual Staging Tables, ​which are created in the Staging Database. ​Data from these tables is then transformed in the ​Staging Area using SQL to conform it to the requirements of the Cost Accounting system. ​The conformed tables can now be integrated, or joined, into a single table. ​The final phase is the loading phase, ​where the data is loaded into the target cost-accounting system. ​A staging area can have many functions. ​Some typical ones include: ​Integration: Indeed, one of the primary functions performed by ​a staging area is consolidation of data from multiple source systems. ​Change detection: Staging areas can be set up to manage extraction of new ​and modified data as needed. 
​Scheduling: Individual tasks within an ETL workflow can be scheduled to run ​in a specific sequence, concurrently, and at certain times. ​There’s also: ​Data cleansing and validation. For example, you can handle missing values and duplicated records. ​Aggregating data: You can use the staging area to summarize data. ​For example, daily sales data can be aggregated into weekly, ​monthly, or annual averages, prior to loading into a reporting system. ​Normalizing data: To enforce consistency of data types, or names of categories such as ​country and state codes in place of mixed naming conventions such as “Mont,” “MA,” or “Montana.” ​A staging area is a separate location, where data from source systems is extracted to. 
​The extraction step therefore decouples operations such as ​validation, cleansing and other processes from the source environment. ​This helps to minimize any risk of corrupting source-data systems, ​and simplifies ETL workflow construction, operation, and maintenance. ​If any of the extracted data becomes corrupted somehow, you can easily recover. ​In this video, you learned that: ​A staging area acts as a bridge between data sources and the target system and are ​mainly used to integrate disparate data sources in data warehouses. ​Staging areas can be implemented quite simply as a set of flat files ​in a directory and managed with scripts, or as tables in a database. ​Staging areas decouple data processing from the source systems ​and thus help minimize risk of data corruption. ​Although they are often transient, ​staging areas can be held for archiving or troubleshooting purposes. 







IBM
×
0:02 / 7:35
Verify Data Quality

Dive deeper on this topic
Transcript
​
Interactive Transcript - Enable basic transcript mode by pressing the escape key

You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key
​Welcome to “Verifying Data Quality.” ​After watching this video, you will be able to: ​Define data quality verification. ​Identify why organizations verify data. ​List examples of data quality concerns. ​Outline a process for handling bad data. ​Data verification includes checking your data for: ​Accuracy⏤ Is your data correct? ​Completeness⏤Is there missing data? 
​Consistency⏤ Are fields consistently entered? and, ​Currency⏤Is your data up to date? ​Data verification is about managing data quality and enhancing its reliability. ​High-quality data enables successful integration of related data and its complex relationships. ​Data verification also provides you with a complete and connected view of your organization, ​data that is ready for advanced analysis, statistical modeling and machine learning, ​and ultimately, more confidence in your insights and decision-making. ​Unfortunately, data quality is not a top concern among the daily chaos of running ​a company. ​According to Harvard Business Review, IBM’s 2016 estimate of the yearly cost of poor ​data quality, in the US alone, was over 3 trillion dollars. 
​Let’s identify data quality concerns that organizations contend with. ​The first is accuracy. ​Accuracy includes ensuring a match between source data and destination data. ​How can accuracy become an issue? ​Data migrating from source systems often contains duplicated records. ​When users enter data manually, typos can find their way into the data records, yielding ​out-of-range values, outliers, and spelling mistakes. ​Sometimes large chunks of data become misaligned, causing data corruption. 
​For example, a CSV file might contain a legitimate comma, which the new system can misinterpret ​as a column separator. ​Another data quality concern is completeness. ​Data is incomplete when the business finds missing values, such as voids or nulls in ​fields that should be populated, or haphazard use of placeholders such as “9 9 9” or ​“minus 1” to indicate a missing value. ​Entire records can also be missing due to upstream system failures. ​Consistency is another important data quality concern. ​Are there deviations from standard terminology? ​Are dates entered consistently? 
​For example, year-month-day and month-day-year formats are incompatible. ​Is data entered consistently? For example, Mr. John Doe and John Doe might refer to the ​same person in the real world, but the system will see them as distinct. ​Are the units consistent? For example, you are expecting ”kilograms,” but you might ​have entries based on “pounds,” or you are expecting 'dollar amounts,” but you ​might have entries based on “thousands of dollars.” ​Lastly, currency is an ongoing data quality concern for most businesses. 
​Currency is about ensuring your data remains up to date. ​For example, you might have dimension tables that contain customer addresses, some of which ​might be outdated. ​In the US, you could check these against a change-of-address database and update your ​table as required. Another currency concern would be name changes as customers can change ​their names for various reasons. ​Determining how to resolve and prevent bad data can be a complex and iterative process. ​First, you’ll implement rules to detect bad data. ​Then you’ll apply those rules to capture and quarantine any bad data. 
​You might need to report any bad data and share the findings with the appropriate domain ​experts. ​You and your team can investigate the root cause of each problem, searching for clues ​upstream in the data lineage. Once you diagnose each problem, you can begin ​correcting the issues. ​Ultimately, you want to automate the entire data cleaning workflow as much as possible. ​For example, you need to validate the quality of data in the staging area before loading ​the data into a data warehouse for analytics. ​You determine that data from certain data sources consistently has data quality issues ​including: ​Missing data, ​Duplicate values, ​Out-of-range values, and ​Invalid values. ​Here’s how an organization might manage and resolve these issues. 
​First, write SQL queries to detect these issues and test for them. ​Next, address some of the quality issues that you’ve repeatedly identified by creating ​rules for treating them, such as removing rows that have out-of-range values. ​Create a script that runs queries to detect data quality issues that happen during the ​nightly loads to the data warehouse. ​This script applies corrective measures and transformations for some of these known issues. ​Next, create a second script that automates the script you created in step 3. ​After the data is extracted from the various data sources, this script automatically runs ​the prior script’s SQL data validation queries every night in the staging area. ​The script you created in step 3 generates a report of any remaining issues that could ​not be automatically resolved. The administrator can review this report and address the unresolved ​issues. 
​Some of the leading vendors and their tools for data quality solutions include: ​IBM InfoSphere Server for Data Quality, ​Informatica Data Quality, ​SAP Data Quality Management, ​SAS Data Quality, ​Talend Open Studio for Data Quality, ​Precisely Spectrum Quality, ​Microsoft Data Quality Services, ​Oracle Enterprise Data Quality, ​And an open-source tool called OpenRefine. ​Each of these solutions has its own strengths. Let's look at one of these solutions. ​The “IBM InfoSphere Information Server for Data Quality” is an example of a product ​that can help you perform data verification in a unified environment. ​“InfoSphere Information Server for Data Quality” enables you to continuously monitor ​the quality of your data, and keep your data clean on an ongoing basis, helping you turn ​your data into trusted information. ​In addition, the “IBM InfoSphere Information Server for Data Quality” comes with built-in, ​end-to-end data quality tools to: ​Help you understand your data and its relationships. ​Monitor and analyze data quality continuously. 
​Clean, standardize, and match data; and ​Maintain data lineage, which is the history of the data’s origin and what happened to ​the data along the way. ​In this video, you learned that: ​Data verification includes checking your data for accuracy, completeness, consistency, and ​currency. ​Data verification is about managing data quality, enhancing data reliability, and maximizing ​data value. ​Determining how to resolve and prevent bad data can be a complex and iterative process. ​Enterprise-grade tools such as “IBM InfoSphere Information Server for Data Quality” can ​help you perform data verification in a unified environment. 







IBM
×
0:00 / 8:22
Populating a Data Warehouse

Dive deeper on this topic
Transcript
​
Interactive Transcript - Enable basic transcript mode by pressing the escape key

You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key
​Welcome to “Populating a Data Warehouse.” ​After watching this video, you will be able to: ​Describe populating a data warehouse as an ongoing process. ​List the main steps for populating a data warehouse. ​List methods for change detection and incremental loading. ​Manually create and populate tables for a sales star schema. ​Recall the periodic maintenance required to keep your data warehouse running smoothly. ​Populating the enterprise data warehouse is an ongoing process. 
​You have an initial load followed by periodic incremental loads. For example, you may load ​new data every day or every week. ​Rarely, a full refresh may be required in case of major schema changes or catastrophic ​failures. ​Generally, fact tables are dynamic and require frequent updating while dimension tables don’t ​change often. ​For example, lists of cities or stores are quite static, but sales happen every day. ​Many tools are available to automate the ongoing process of keeping your data warehouse current. ​Databases like Db2 have a Load utility that is faster than inserting a row at a time, ​and ​loading your Warehouse can also be a part of your ETL data pipeline that is automated ​using tools like Apache Airflow and Apache Kafka. 
​You can also write your own scripts, combining lower-level tools like Bash, Python, and SQL, ​to build your data pipeline and schedule it with cron. ​And InfoSphere DataStage allows you to compile and run jobs to load your data. ​Before populating your data warehouse, ensure that: ​Your schema has already been modeled. ​Your data has been staged in tables or files. ​And, you have mechanisms for verifying the data quality. ​Now you are ready to set up your data warehouse and implement the initial load. ​You first instantiate the data warehouse and its schema, then create the production tables. 
​Next, establish relationships between your fact and dimension tables, ​and finally, load your transformed and cleaned data into them from your staging tables or ​files. ​Now that you’ve gone through the initial load, it’s time to set up ongoing data loads. ​You can automate subsequent incremental loads using a script as part of your ETL data pipeline. ​You can also schedule your incremental loads to occur daily or weekly, depending on your ​needs. ​You will also need to include some logic to determine what data is new or updated in your ​staging area. ​Normally, you detect changes in the source system itself. ​Many relational database management systems have mechanisms for identifying any new, changed, ​or deleted records since a given date. 
​You might also have access to timestamps that identify both when the data was first written ​and the date it might have been modified. ​Some systems might be less accommodating and you might need to load the entire source ​to your ETL pipeline for subsequent brute-force comparison to the target, which is fine if ​the source data isn’t too large. ​Data warehouses need periodic maintenance, usually monthly or yearly, to archive data ​that is not likely to be used. ​You can script both the deletion of older data and its archiving to slower, less costly ​storage. ​Let’s illustrate the process with a simplified example of manually populating a data warehouse ​with a star schema called ‘sales.’ We’ll assume that you’ve already instantiated ​the data warehouse and the ‘sales’ schema. ​Here’s a sample of some auto sales transaction data from a fictional company called Shiny ​Auto Sales. 
​You can see several foreign key columns, such as ​“sales ID,” which is a sequential key identifying the sales invoice number, ​“emp no,” which is the employee number, and ​“class ID,” which encodes the type of car sold, such as “small SUV.” ​Each of these keys represents a dimension that points to a corresponding dimension table ​in the star schema. ​The “date” column is a dimension that indicates the sale date. ​The “amount” column is the sales amount, which happens to be the fact of interest. ​This table is already close to the form of a fact table. The only exception is the date ​column, which is not yet represented by a foreign “date ID” key. ​Let’s use PSQL, the terminal-based front end for PostGreSQL, to illustrate how you ​can create your dimension tables using the salesperson dimension as an example. 
​Use the CREATE TABLE clause to create the “DimSalesPerson” table with the “sales” ​schema, along with ​“SalesPersonID” as a serial primary key, ​“SalespersonAltID”, as the salesperson’s employee number, ​and finally, a column for the salesperson’s name. ​Now you can start populating the “DimSalesPerson” table, row by row. ​You use an “insert into” clause on the “sales dot DimSalesPerson” table, ​specifying the “SalesPersonAltID” and “SalesPersonName” columns, ​and begin inserting values such as employee number 680, “Cadillac Jack.” ​You would similarly create and populate tables for the remaining dimensions. ​You can enter the SQL statement: ​“SELECT star FROM sales dot dim salesperson LIMIT 5” to view your salesperson dimension ​table, ​and see that everything seems to be correctly populated, such as record 1, employee number ​617, and salesperson name “Go-cart Joe.” ​Now it’s time to create your sales fact table, using “CREATE TABLE” with “sales ​dot FactAutoSales” as the table name, ​“TransactionID“ as the primary key, with “big serial” type and the various ​foreign keys, such as “SalesID” and “AutoClassID”, ​and finally the fact of interest, “amount” as type “money.” ​Next, you proceed with setting up the relations between the fact and dimension tables of the ​sales schema. 
​For example, you can apply the ALTER TABLE statement and the ADD CONSTRAINT clause to ​the “sales dot FactAutoSales” fact table to add “KVAutoClassID” as a foreign key relating ​“AutoClassID” to the same column name in the “sales dot DimAutoCategory” table ​using the REFERENCES clause. ​You would then use the same method to set up the relations for the remaining dimension ​tables. ​After defining all the tables and setting up the corresponding relations, it’s finally ​time to start populating your fact table using the sales data that you started with. ​You can use the INSERT INTO statement on “sales dot FactAutoSales,” specifying the column ​names “SalesID,” "Amount," “SalesPersonID,” “AutoClassID,” and “SalesDateKey,” and entering rows ​of values such as 1629, 42000, 2, 1, and 4, which you would obtain using the auto sales ​data. ​You can view the auto sales fact table by entering the SQL statement “select star" ​from “sales dot FactAutoSales Limit 5” to display its first 5 rows. ​Here you see the dollar amounts for individual auto sales, the primary key called “transactionID,” ​and the remaining columns, which are the foreign keys that you set up. ​In this video, you learned that: ​Populating an enterprise data warehouse includes initial creation of fact and dimension tables ​and their relations and loading of clean data into tables. 
​Populating the enterprise data warehouse is an ongoing process that starts with an initial ​load, followed by periodic incremental loads. ​Fact tables are dynamic and require frequent updating while dimension tables are more static ​and don’t change often. ​And you can automate incremental loading and periodic maintenance of your data warehouse ​using scripting or built-for-purpose data pipeline tools. 














IBM
×
0:36 / 8:44
Querying the Data

Dive deeper on this topic
Transcript
​
Interactive Transcript - Enable basic transcript mode by pressing the escape key

You may navigate through the transcript using tab. To save a note for a section of text press CTRL + S. To expand your selection you may use CTRL + arrow key. You may contract your selection using shift + CTRL + arrow key. For screen readers that are incompatible with using arrow keys for shortcuts, you can replace them with the H J K L keys. Some screen readers may require using CTRL in conjunction with the alt key
​Welcome to "Querying the Data." ​After watching this video, you will be able to: ​Interpret an entity-relationship diagram, or ERD, for a star schema and use the relations ​between tables to set up queries. ​Create a materialized view by denormalizing, or joining tables from, a star schema. ​Apply the CUBE and ROLLUP options in a GROUP BY clause to generate commonly requested total ​and subtotal summaries. ​CUBE and ROLLUP operations generate the kinds of summaries that management often requests. ​These summaries are much easier to implement than the multiple SQL queries that are otherwise ​required. ​Materialized views conveniently enable you to create a stored table you so can refresh ​on a schedule or on-demand. 
​When the a view is complex, requested frequently, or is run on large data sets, consider materializing ​the view to help reduce the load on the database. ​Because the data is precomputed, querying materialized views can be much faster than ​querying the underlying tables. ​Combining cubes or rollups with materialized views can enhance performance. You can even ​follow up by materializing the cube or rollup. ​Consider the following scenario: ​You have the task of creating some live summary tables for reporting January sales by salesperson ​and automobile type for ShinyAutoSales. ​Begin by understanding the existing star schema in their data warehouse, called "sasDW," based ​on PostgreSQL. ​Then explore relevant ShinyAutoSales data by querying the tables from the "sales" star ​schema in the sasDW warehouse. 
​After exploring the schema, you decide to create a materialized view as a staging table. ​Creating the view as a staging table provides you with the data you need while minimizing ​your impact on the database. ​You can incrementally refresh the data at will during off-peak hours. ​You start a PostgreSQL session and generate an entity relationship diagram, or ERD, which ​represents the "Sales" star schema implemented within the ShinyAutoSales data warehouse, ​"sasDW." ​Then, you locate the central fact table named "fact auto sales." ​This table contains the "amount" column, which is the measure you need. ​You also spot the three foreign keys in the sales fact table: "sales date key," "auto ​class ID," and "salesperson ID." 
​These keys link respectively to: ​The "Date dimension table," which contains dates and related values such as the day of ​the week, month name, and quarter. ​The "Auto category dimension table," which includes the "auto class name," and the Boolean ​"is new" column, and finally, ​the "Salesperson dimension table," which contains the "salesperson's name." ​In this example, you are using PostgreSQL. Let's assume you already started up the terminal-based ​front-end to PostgreSQL, "P S Q L," and connected to the "S A S D W" data warehouse. ​Notice the command prompt contains the name of the data warehouse you are connected to, ​"S A S D W." ​Starting with the auto sales fact table, you'll enter the SQL statement "select star from ​sales dot fact auto sales limit 10" to display its first 10 rows. ​Here, you see the dollar amounts for individual auto sales, but the remaining columns are ​primary and foreign keys, which don't have any direct meaning for you yet. 
​However, you notice that the sales ID values are sequential, but the numbering starts at ​1,629 instead of 1. ​That's because ShinyAutoSales has provided you with access to a windowed subset of their ​data. ​Next, you query the auto category dimension table. ​Now, you can see meaningful names for various automobile classes, such as truck and compact ​SUVs. ​You notice duplicate entries for the truck class and wonder why they exist. ​When you look more closely, you realize the duplicate entries exist because of the distinct ​subclasses for new and used trucks. ​Similarly, you generate a view for the salesperson dimension table and find eight distinct salesperson ​names, including "Gocart Joe" and "Jane Honda." So far, so good! 
​Finally, you view the date dimension table. ​You notice the dates only go back to January 1, 2021. ​Your contact at Shiny Auto Sales informs you that she will provide you with more data later ​and that for now, you can work with a smaller data set while you develop your queries. ​The date table contains potentially useful date elements such as the day of the week, ​month name, and quarter name. ​At this stage, it would be more convenient to have a table of data that contains the ​dimensions you need with human interpretable columns, rather than just keys. ​Essentially, you want to create a denormalized view of the data by joining the dimensions ​back to the fact of interest. ​You proceed by selecting the "date," "auto class name," "is new," "salesperson name," ​and "amount" columns from their tables, and joining each dimension onto the "amount" fact ​using an inner join on the corresponding keys. 
​Next, why not capture the view as a materialized view called "Denormalized sales" or "D N sales" ​for short? ​Then you can reuse the materialized view for different queries without having to recreate ​your work. ​You accomplish this task using the clause "CREATE MATERIALIZED VIEW D N sales AS," followed ​by the same query you used to generate the denormalized view. ​Type "Select star from D N sales, LIMIT 10" to display your resulting materialized view. ​Now you have a tidy, human-readable, time-series of sales data available for further analysis. ​For example, you can see that "Cadillac Jack” sold a new midsize SUV on January 5 for $26,500. ​Next, you want to apply CUBE and ROLLUP operations to your denormalized, materialized view. 
​Let's see the CUBE results. ​Here, you select the "auto class name," "salesperson name," and the "sum of the sales amounts" ​from "D N sales," where "is new" is set to "true." ​Finally, group the generated cube by the "auto class name" and "salesperson name." ​The output looks like this: ​The first row has no entries in the dimensions columns, which means 'all.' Thus, the value ​of $366,076 represents the total sales for all new cars. ​The next block of records has both dimension columns populated. So, for instance, ​you can read the total sales of new midsize SUVs by "Gocart Joe,” which is $32,099. 
​Similarly, the last two blocks summarize "new auto sales" by class, and by salesperson. ​Next, you apply a ROLLUP instead of a CUBE operation. You decide to keep the query the ​same as the previous query, except that you replace CUBE with ROLLUP. ​Here's what the resulting view looks like now. ​You have five fewer rows with the ROLLUP result than CUBE, resulting in 13 rows instead of ​18 rows. ​The only difference in this result is that you don't have the "total sale amounts by ​salesperson" summary. ​While CUBE generates all possible permutations of the "GROUP BY" columns, ROLLUP only looks ​at the single permutation defined by the columns' order listed in the ROLLUP call. 
​In this video, you learned that: ​CUBE and ROLLUP summaries on materialized views provide powerful capabilities for quickly ​querying and analyzing data in data warehouses. ​CUBE and ROLLUP operations generate the kinds of summaries grouped by dimensions that ​management often requests. ​You can denormalize star schemas using joins to bring together human-interpretable facts ​and dimensions in a single materialized view. ​You can create staging tables from materialized views, which you can incrementally refresh ​during off-peak hours. 
IBM 0:33 / 8:44 Querying the Data Dive deeper on this topic : Added to Selection. Press [CTRL + S] to save as a note















IBM
Module 2 Summary: Designing, Modeling and Implementing Data Warehouses
0:00/0:27

Now you can identify some of the differences between general data warehouse architecture and reference data warehouse architecture. You now know how to use facts and dimension tables when designing a data warehouse. You can now apply CUBE and ROLLUP functions to speed the retrieval of aggregated data using materialized views.  And you can identify when an organization benefits by using staging areas for data storage and retrieval.

