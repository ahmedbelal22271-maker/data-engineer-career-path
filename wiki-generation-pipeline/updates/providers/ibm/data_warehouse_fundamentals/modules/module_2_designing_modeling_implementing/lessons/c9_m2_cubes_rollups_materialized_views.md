> **Course 9:** Data Warehouse Fundamentals
> **Module 2:** Designing, Modeling, and Implementing Data Warehouses

# Cubes, Rollups, and Materialized Views and Tables

## Learning Objectives

After watching this video, you will be able to:

- Relate what a data cube is in terms of star schema.
- Discuss the terms slice, dice, drill up or down, roll up, and pivot in terms of data cubes.
- Describe what a materialized view is.
- Recall two use cases for materialized views.

---

## Why Data Cubes Exist: The Problem They Solve

<mark style="background-color: rgba(200, 230, 201, 0.4);">Before diving into what data cubes are, it's crucial to understand why they were invented in the first place. The concept emerged from a fundamental limitation in traditional relational databases when it comes to business analysis.</mark>

<mark style="background-color: rgba(200, 230, 201, 0.4);">**The Core Problem:** Business questions are inherently multidimensional. A sales manager doesn't just ask "What were total sales?" They ask "What were total sales **for** Product X **in** Region Y **during** Quarter Z?" This requires analyzing data across multiple dimensions simultaneously.</mark>

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Traditional Relational Database Limitation:** In a standard relational database, data is stored in flat, two-dimensional tables. While you can write SQL queries with multiple GROUP BY clauses to analyze across dimensions, these queries become exponentially complex and slow as you add more dimensions. For example, analyzing sales across just 3 dimensions (product, region, time) with a GROUP BY ROLLUP requires computing 2^3 = 8 different aggregation levels. With 6 dimensions, that's 2^6 = 64 different GROUP BY operations, each requiring a full table scan.</mark>

<mark style="background-color: rgba(200, 230, 201, 0.4);">**The Performance Bottleneck:** As data volumes grow into terabytes or petabytes, these complex analytical queries become impractically slow. Business analysts need interactive, sub-second responses to explore data from different perspectives, but relational databases are optimized for transactional operations (OLTP), not complex analytical workloads (OLAP).</mark>

<mark style="background-color: rgba(200, 230, 201, 0.4);">**The Solution: Data Cubes:** Data cubes solve this by pre-computing and storing aggregated results across multiple dimension combinations. Instead of computing aggregations on-the-fly during each query, the cube operator (introduced by Jim Gray et al. in 1995) generates multidimensional summaries during data loading. When an analyst asks "What were total sales for Product X in Region Y during Quarter Z?" the answer can be retrieved from pre-calculated results rather than scanning the entire fact table.</mark>

[ENRICHED: historical context — The data cube operator was formally defined in Jim Gray et al.'s 1995 paper "Data Cube: A Relational Aggregation Operator Generalizing Group-By, Cross-Tab, and Sub-Totals." This paper introduced the CUBE BY SQL extension, which revolutionized how multidimensional analysis could be performed on relational data. [Source: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-22.pdf]]

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Why This Matters for Data Warehousing:** Data warehouses are specifically designed for analytical workloads. They store historical, integrated data from across the organization specifically to support complex queries. Data cubes are a natural extension of this architecture—they take the star or snowflake schema from the data warehouse and create a pre-computed, multidimensional structure optimized for fast interactive analysis.</mark>

[ENRICHED: ecosystem — Data cubes are the core technology behind OLAP (Online Analytical Processing) systems. They enable the five key OLAP operations: drill down (viewing more detailed data), roll up (viewing summarized data), slice (selecting a single value from one dimension), dice (selecting subsets from multiple dimensions), and pivot (rotating the view). These operations allow business users to explore data interactively without writing complex SQL. [Source: https://www.ibm.com/think/topics/olap]]

<mark style="background-color: rgba(200, 230, 201, 0.4);">**The Trade-off (Theory vs. Practice):** The theoretical concept of a data cube is to pre-compute ALL possible dimension combinations for instant query responses. However, this full materialization is computationally prohibitive for high-dimensional data. The trade-off is between query performance (more pre-computation = faster queries) and storage/computation costs (more pre-computation = more storage and longer loading times). This is why practical implementations use selective strategies rather than computing everything.</mark>

<mark style="background-color: rgba(200, 230, 201, 0.4);">**How Data Cubes Are Actually Built: The Practical Reality:** You're right to question this—computing every possible combination of dimensions is indeed computationally expensive. For a data cube with *n* dimensions, there are 2^n possible aggregation combinations (called cuboids). With just 10 dimensions, that's 1,024 different cuboids. With 20 dimensions, it's over 1 million. So how do real systems handle this? The answer is they don't compute everything—they use selective strategies.</mark>

[ENRICHED: practical implementation — Real-world data cube implementations never compute the full cube for high-dimensional data. Instead, they use selective materialization strategies that balance query performance against storage and computation costs. The three main approaches are: (1) full materialization for small dimension sets, (2) partial materialization using intelligent selection algorithms, and (3) on-demand computation with caching. [Source: https://cse.buffalo.edu/adblab/people/zzhao35/teaching/cse707_fall21/datacube.pdf]]

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Strategy 1: Iceberg Cubes (Selective Computation):** Instead of computing all aggregations, Iceberg cubes only compute those that meet a minimum support threshold. For example, you might only compute aggregations where the count is at least 100 transactions. This dramatically reduces the computation by pruning rare or uninteresting combinations early. The BUC (Bottom-Up Cube) algorithm builds cubes from single dimensions upward, allowing it to prune branches that don't meet the threshold before computing expensive multi-dimensional combinations.</mark>

[ENRICHED: algorithm — The BUC (Bottom-Up Cube) algorithm computes Iceberg cubes by starting with single-dimension aggregations and progressively building up to higher-dimensional combinations. If a single-dimension aggregation doesn't meet the minimum support threshold, all combinations containing that dimension are pruned. This is similar to the Apriori algorithm for association rules. [Source: https://sigmodrecord.org/publications/sigmodRecord/9906/Bottom-up%20computation%20of%20sparse%20and%20Iceberg%20CUBE.pdf]]

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Strategy 2: Cube Shells (Partial Dimension Coverage):** For high-dimensional data (e.g., 50 dimensions), systems compute only "cube shells"—aggregations up to a certain dimensionality. For example, you might compute all 1-, 2-, 3-, and 4-dimensional aggregations but not 5-dimensional or higher. This provides good query flexibility for most analytical scenarios while keeping computation manageable. Most business questions involve exploring 2-5 dimensions at a time, so cube shells cover the majority of use cases.</mark>

[ENRICHED: optimization — Cube shell computation is particularly effective because most OLAP queries operate on only a small number of dimensions simultaneously. Even in a 60-dimensional data cube, analysts typically examine 3-5 dimensions at a time. Computing all cuboids with 3 or fewer dimensions requires only C(60,1) + C(60,2) + C(60,3) = 35,550 cuboids instead of the full 2^60 ≈ 10^18 cuboids. [Source: https://www.vldb.org/conf/2003/papers/S15P02.pdf]]

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Strategy 3: Intelligent View Selection (Greedy Algorithms):** When you can't compute everything, greedy algorithms select the most valuable views to materialize based on query patterns, data distribution, and storage constraints. These algorithms model the cube as a lattice where some views can be computed from others. They then select views that minimize total query cost while staying within storage budgets. The Mervyn's department store chain, for example, pre-computed 2,400 summary tables to optimize their most common queries.</mark>

[ENRICHED: real-world example — The paper "Implementing Data Cubes Efficiently" describes how the Mervyn's department store chain optimized their data warehouse with 2,400 pre-computed summary tables. Using greedy algorithms to select which views to materialize, they achieved dramatic query performance improvements while managing storage costs. This demonstrates that practical cube implementations are highly selective. [Source: https://cse.buffalo.edu/adblab/people/zzhao35/teaching/cse707_fall21/datacube.pdf]]

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Strategy 4: Parallel and Distributed Computation:** Modern systems use parallel algorithms to distribute cube computation across multiple processors or nodes. The PnP (Pipe 'n Prune) algorithm, for example, achieves near-linear speedup on clusters of 32 processors by overlapping computation with disk I/O and balancing workloads. This makes even large iceberg cubes feasible to compute within acceptable time windows.</mark>

[ENRICHED: performance — Parallel cube computation algorithms like PnP scale well because cube computation is embarrassingly parallel—different cuboids can be computed independently. On an 8-node cluster, researchers achieved an 82% reduction in computation time for partial data cubes. External memory implementations show only slight performance degradation when data exceeds main memory. [Source: https://web.cs.dal.ca/~arc/publications/2-28/paper.pdf]]

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Strategy 5: Lazy Computation with Materialized Views:** In modern data warehouses, the trend is toward materialized views rather than full cubes. Materialized views allow you to pre-compute specific, frequently-asked queries (like "total sales by region by quarter") without committing to all possible combinations. The database optimizer can then use these materialized views to accelerate similar queries, providing a flexible middle ground between full pre-computation and pure on-demand calculation.</mark>

---

## Data Cubes

Let's use an example to illustrate the concept of a data cube. Here is a cube generated from an imaginary star schema for a Sales OLAP (online analytical processing system).

[ENRICHED: definition — **OLAP (Online Analytical Processing)** is a category of software tools that enable users to interactively analyze multidimensional data from multiple perspectives. OLAP supports operations like drilling down, rolling up, slicing, dicing, and pivoting. The term was coined in E.F. Codd's 1993 paper "Providing OLAP to User-Analysts." [Source: https://clickhouse.com/resources/engineering/olap-operations]]

[ENRICHED: definition — **Data cube** is a multidimensional representation of data where dimensions (e.g., time, product, region) define the axes and measures (e.g., sales revenue) populate the cells. A data cube with *n* dimensions is an *n*-dimensional hypercube. [Source: https://theintactone.com/2026/03/03/olap-operations-roll-up-drill-down-slice-dice-pivot/]]

The coordinates of the cube are defined by a set of dimensions, which are selected from the star schema. In this illustration, we are only showing three dimensions, but data cubes can have many dimensions. We have the Product categories corresponding to the items sold, the State or Province the items were sold from, and the Year these products were sold in.

The cells of the cube are defined by a fact of interest from the schema, which could be something like "total sales in thousands of dollars." Here the "243" indicates "243 thousand dollars" for some given Product, State, and Year combination.

There are many operations you can perform on data cubes, such as slicing, dicing, drilling up and down, pivoting, and rolling up. Let's go over some examples of these operations, starting with slicing.

---

## OLAP Cube Operations

### Slicing

Slicing a data cube involves selecting a single member from a dimension, which yields a data cube that has one dimension less than the original.

For example, you can slice this sales cube by selecting only the year 2018 from the year dimension, allowing you to analyze sales totals for all sales states and all products for the year 2018.

[ENRICHED: example — In SQL, slicing corresponds to a WHERE clause filtering on a single dimension value: `SELECT product, state, SUM(sales) FROM sales_cube WHERE year = 2018 GROUP BY product, state;` This produces a 2D "slice" of the original 3D cube. [Source: https://clickhouse.com/resources/engineering/olap-operations]]

<mark style="background-color: rgba(200, 230, 201, 0.4);">**How to Visualize This:** You're correct—a data cube is essentially a collection of pre-computed GROUP BY results stored in a multidimensional structure. Think of it like a spreadsheet on steroids. Imagine a 3D cube where each axis represents a dimension, and each cell contains the aggregated value for that combination:</mark>

```
SALES CUBE (3D)
                Year
                ↑
                |
                |      ┌─────────────────┐
                |     /│                /│
                |    / │   Sales $     / │
                |   /  │   by Product │  │
                |  /   │   by State   │  │
                | /    │   by Year    │  │
                |/     │              │  │
    Product ────┼──────┼──────────────┼──┼──→ State
                │      │              │  │
                │      └─────────────────┘
                │     /
                │    /
                │   /
                │  /
                │ /
                │/
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**The Key Insight:** The cube doesn't store raw data—it stores pre-computed aggregations. Each cell might contain `SUM(sales)` for that specific Product + State + Year combination. The "magic" is that all the GROUP BY combinations are already calculated: by product alone, by state alone, by year alone, by product+state, by product+year, by state+year, and by all three.</mark>

<mark style="background-color: rgba(200, 230, 201, 0.4);">**What Slicing Does:** When you slice by Year=2018, you're essentially asking for a 2D cross-section of that 3D cube—you get all the Product+State aggregations for 2018 only. It's like cutting a layer off the cube and looking at it flat:</mark>

```
SLICE: Year = 2018

         Product
           ↑
           │
           │   ┌─────────────────┐
           │   │  T-Shirts │ Jeans │
           │   │     45    │   67  │
           │   │─────────────────│
           │   │  Gloves   │ Hats  │
           │   │     23    │   12  │
           │   └─────────────────┘
           │         → State
           │    NY    FL    CA
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**The Physical Reality:** In actual database implementations, this "cube" is often stored as materialized summary tables. For example, you might have separate tables like `sales_by_product_state_year`, `sales_by_product_state`, `sales_by_product`, etc. The cube structure is a logical concept—physically, it's multiple summary tables that the OLAP engine navigates efficiently.</mark>

### Dicing

Similarly, dicing a cube involves selecting a subset of values from a dimension, effectively shrinking it.

For example, you can dice this sales cube by selecting only "Gloves", "T-shirts", and "Jeans" from the Product-Type dimension, allowing you to restrict your view to just those product types.

[ENRICHED: distinction — Slice selects a single value from ONE dimension (reduces by one axis). Dice selects multiple values from TWO or MORE dimensions (creates a smaller sub-cube). Both map to SQL WHERE clauses; the distinction is the number of predicates. [Source: https://clickhouse.com/resources/engineering/olap-operations]]

### Drill Down and Drill Up

<mark style="background-color: rgba(200, 230, 201, 0.4);">**The Concept:** Dimensions often have hierarchies—levels of detail from coarse to fine. Drill down and drill up let you navigate these hierarchies without writing new queries. Think of it like zooming in and out on a map.</mark>

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Dimension Hierarchies:** Here are common examples of hierarchies in business dimensions:</mark>

```
PRODUCT HIERARCHY:
Category → Subcategory → Product Name
Clothing → T-Shirts → Classic T-Shirt
         → Jeans → Slim Fit Jeans
         → Gloves → Leather Gloves

TIME HIERARCHY:
Year → Quarter → Month → Day
2018 → Q1 → January → Jan 1
              → February → Feb 1
              → March → Mar 1
        → Q2 → April → ...
              → May → ...
              → June → ...

LOCATION HIERARCHY:
Country → State → City
USA → New York → New York City
    → California → Los Angeles
    → Florida → Miami
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Drill Down (Zoom In):** Moving from summarized data to more detailed data. You're asking: "Show me the breakdown of this summary."</mark>

```
BEFORE DRILL DOWN (Level 1: Category):
┌─────────────────────────────────────────┐
│ Product Category │ Total Sales │
├─────────────────────────────────────────┤
│ Clothing         │   $45,000   │
│ Electronics      │   $67,000   │
│ Home & Garden    │   $23,000   │
└─────────────────────────────────────────┘

DRILL DOWN on "Clothing" (Level 2: Subcategory):
┌─────────────────────────────────────────┐
│ Product Subcategory │ Total Sales │
├─────────────────────────────────────────┤
│ T-Shirts            │   $18,000   │
│ Jeans               │   $15,000   │
│ Gloves              │   $12,000   │
└─────────────────────────────────────────┘

DRILL DOWN on "T-Shirts" (Level 3: Product Name):
┌─────────────────────────────────────────┐
│ Product Name        │ Total Sales │
├─────────────────────────────────────────┤
│ Classic T-Shirt     │    $7,000   │
│ Slim Fit T-Shirt    │    $6,500   │
│ Regular Fit T-Shirt │    $4,500   │
└─────────────────────────────────────────┘
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Drill Up (Zoom Out):** Moving from detailed data back to summarized data. You're asking: "Show me the bigger picture."</mark>

```
DRILL UP from "Classic T-Shirt" back to Category level:
┌─────────────────────────────────────────┐
│ Product Category │ Total Sales │
├─────────────────────────────────────────┤
│ Clothing         │   $45,000   │  ← Back to the top
│ Electronics      │   $67,000   │
│ Home & Garden    │   $23,000   │
└─────────────────────────────────────────┘
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Why This Matters:** An analyst might see that "Clothing" sales are down 10% this quarter. They drill down to see which subcategory is causing the problem. They discover "T-Shirts" are down 25%. They drill down further and find "Slim Fit T-Shirts" are down 40%. The root cause is identified in three clicks, no SQL required.</mark>

[ENRICHED: definition — **Drill down** moves from summarized, high-level data to more detailed, granular information by descending a dimension hierarchy (e.g., Category → Subcategory → Product Name). **Drill up** (or roll up) is the inverse: climbing up the hierarchy to aggregate detail into summaries. In snowflake schemas, these hierarchies are explicitly modeled in separate dimension tables. [Source: https://theintactone.com/2026/03/03/olap-operations-roll-up-drill-down-slice-dice-pivot/]]

[ENRICHED: example — In SQL, drill down corresponds to changing the GROUP BY clause to include a more granular column. For example, `SELECT category, SUM(sales) FROM sales GROUP BY category` (drill up level) vs. `SELECT subcategory, SUM(sales) FROM sales WHERE category = 'Clothing' GROUP BY subcategory` (drill down one level). The OLAP engine handles this navigation automatically. [Source: https://clickhouse.com/resources/engineering/olap-operations]]

### Pivoting

Pivoting data cubes is straightforward. It involves a rotation of the data cube.

In this case, the year and product dimensions have been interchanged, while the State dimension has been fixed "as is."

Pivoting doesn't change its information content; it just changes the point of view you may choose to analyze it from.

### Rolling Up

<mark style="background-color: rgba(200, 230, 201, 0.4);">**The Concept:** Rolling up means summarizing data by collapsing one or more dimensions. You're asking: "Give me totals across these categories instead of individual rows." It's like taking detailed data and grouping it into broader buckets.</mark>

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Step-by-Step Example:** Let's see exactly what happens when you roll up. Start with this raw sales data:</mark>

```
SOURCE DATA: sales_fact table
┌─────┬─────────────┬───────┬────────────┐
│ Row │ Product     │ State │ Sales ($)  │
├─────┼─────────────┼───────┼────────────┤
│  1  │ T-Shirt     │ NY    │    100     │
│  2  │ T-Shirt     │ FL    │    150     │
│  3  │ T-Shirt     │ CA    │    200     │
│  4  │ Jeans       │ NY    │    300     │
│  5  │ Jeans       │ FL    │    250     │
│  6  │ Jeans       │ CA    │    350     │
│  7  │ Gloves      │ NY    │     50     │
│  8  │ Gloves      │ FL    │     75     │
│  9  │ Gloves      │ CA    │    100     │
└─────┴─────────────┴───────┴────────────┘
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**The SQL Query:** Let's roll up by Product to see total sales per product (collapsing the State dimension):</mark>

```sql
-- Roll up: collapse State dimension, sum sales per Product
SELECT product, SUM(sales_amount) AS total_sales
FROM sales_fact
GROUP BY product;
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Resulting Table After Roll Up:** The State dimension is gone—each row now represents a summary across all states:</mark>

```
RESULT AFTER ROLL UP (by Product):
┌─────────────┬─────────────┬─────────────────────────────────┐
│ Product     │ Total Sales │ How it was calculated           │
├─────────────┼─────────────┼─────────────────────────────────┤
│ T-Shirt     │     450     │ 100 + 150 + 200 (NY+FL+CA)     │
│ Jeans       │     900     │ 300 + 250 + 350 (NY+FL+CA)     │
│ Gloves      │     225     │  50 +  75 + 100 (NY+FL+CA)     │
└─────────────┴─────────────┴─────────────────────────────────┘

Note: 9 rows collapsed to 3 rows. State dimension is removed.
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Multi-Dimensional Roll Up with ROLLUP Keyword:** The GROUP BY ROLLUP operator generates subtotals at ALL levels automatically:</mark>

```sql
-- Full roll-up: generate all aggregation levels
SELECT product, state, SUM(sales_amount) AS total_sales
FROM sales_fact
GROUP BY ROLLUP(product, state);
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Resulting Table with All Roll-Up Levels:** This produces multiple summary levels in one result:</mark>

```
RESULT WITH ROLLUP(product, state):
┌─────┬─────────────┬───────┬────────────┬──────────────────────────┐
│ Row │ Product     │ State │ Total Sales│ Level                    │
├─────┼─────────────┼───────┼────────────┼──────────────────────────┤
│  1  │ T-Shirt     │ NY    │    100     │ Detail (product+state)   │
│  2  │ T-Shirt     │ FL    │    150     │ Detail (product+state)   │
│  3  │ T-Shirt     │ CA    │    200     │ Detail (product+state)   │
│  4  │ Jeans       │ NY    │    300     │ Detail (product+state)   │
│  5  │ Jeans       │ FL    │    250     │ Detail (product+state)   │
│  6  │ Jeans       │ CA    │    350     │ Detail (product+state)   │
│  7  │ Gloves      │ NY    │     50     │ Detail (product+state)   │
│  8  │ Gloves      │ FL    │     75     │ Detail (product+state)   │
│  9  │ Gloves      │ CA    │    100     │ Detail (product+state)   │
├─────┼─────────────┼───────┼────────────┼──────────────────────────┤
│ 10  │ T-Shirt     │ NULL  │    450     │ Product subtotal         │
│ 11  │ Jeans       │ NULL  │    900     │ Product subtotal         │
│ 12  │ Gloves      │ NULL  │    225     │ Product subtotal         │
├─────┼─────────────┼───────┼────────────┼──────────────────────────┤
│ 13  │ NULL        │ NY    │    450     │ State subtotal           │
│ 14  │ NULL        │ FL    │    475     │ State subtotal           │
│ 15  │ NULL        │ CA    │    650     │ State subtotal           │
├─────┼─────────────┼───────┼────────────┼──────────────────────────┤
│ 16  │ NULL        │ NULL  │   1,575    │ Grand total              │
└─────┴─────────────┴───────┴────────────┴──────────────────────────┘

NULL values indicate "ALL" values for that dimension (rolled up).
```

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Reading the Result:** 
- Rows 1-9: Original detail rows (Product + State combinations)
- Rows 10-12: Product subtotals (State collapsed to NULL) — "Total T-Shirt sales across all states"
- Rows 13-15: State subtotals (Product collapsed to NULL) — "Total NY sales across all products"
- Row 16: Grand total (both dimensions collapsed) — "Total sales across everything"</mark>

<mark style="background-color: rgba(200, 230, 201, 0.4);">**Why This Matters:** Instead of running 4 separate queries (by product, by state, grand total, plus the detail), you get ALL aggregation levels in one query. The OLAP engine pre-computes these levels so they're instantly available.</mark>

[ENRICHED: performance context — In modern columnar databases (Snowflake, BigQuery, ClickHouse), roll-up operations execute as SQL GROUP BY with ROLLUP or CUBE extensions. These are processed natively without requiring pre-built cube structures. The SQL:1999 standard formalized the ROLLUP keyword for hierarchical aggregation. [Source: https://clickhouse.com/resources/engineering/olap-operations]]

```sql
-- Example: Roll-up aggregation across dimensions
SELECT product, state, SUM(sales_amount) AS total_sales
FROM sales_fact
GROUP BY ROLLUP(product, state);
```

**Line-by-line breakdown:**
- `SELECT product, state, SUM(sales_amount) AS total_sales` — Selects the dimension columns and computes the sum of sales as the measure
- `FROM sales_fact` — Queries the fact table containing sales transactions
- `GROUP BY ROLLUP(product, state)` — Generates subtotals at multiple levels: (product, state), (product) only, (state) only, and grand total

---

## Materialized Views

A "materialized view" is essentially a local, read-only copy, or snapshot, of the results of a query.

They can be used to replicate data, for example to be used in a staging database as part of an ETL process, or to precompute and cache expensive queries, such as joins or aggregations, for use in data analytics environments.

Materialized views also have options for automatically refreshing the data, thus keeping your query up-to-date. Because materialized views can be queried, you can safely work with them without worrying about affecting the source database.

[ENRICHED: definition — A **materialized view** physically stores the result set of a query on disk, unlike a regular view which is a virtual definition that executes the underlying query each time it is accessed. Materialized views provide major performance gains for expensive computations but introduce a freshness trade-off since the data is a snapshot. [Source: https://www.epsio.io/blog/database-materialized-view-vs-regular-view]]

[ENRICHED: ecosystem — Materialized views are widely used in OLAP systems, data marts, and ETL pipelines as precomputed intermediates for dashboards or batch analytics. They complement (but do not replace) indexing strategies and query optimization. Modern alternatives include cube layers (e.g., Apache Druid, ClickHouse aggregating merge tree) and incremental view maintenance (e.g., Epsio). [Source: https://www.epsio.io/blog/database-materialized-view-vs-regular-view]]

### Refresh Options

Materialized Views can be set up to have different refresh options, such as:

- **Never:** They are only populated when created, which is useful if the data seldom changes.
- **Upon request:** Manually refresh, for example, after changes to the data have been made, or scheduled refresh, for example, after daily data loads.
- **Immediately:** Automatically refresh after every statement.

[ENRICHED: ecosystem — Oracle supports fast (incremental) refresh using Materialized View Logs that track changes on base tables. PostgreSQL only supports complete refresh (full recomputation) since version 9.3 — there is no built-in fast refresh. IBM Db2 calls materialized views MQTs (Materialized Query Tables) and supports both immediate and deferred refresh with integrity checking. [Source: https://www.cybrosys.com/research-and-development/postgres/why-postgresql-has-no-fast-materialized-view-refresh]]

---

## Creating Materialized Views: Database Examples

### Oracle

Let's look at an example. Here is how you might create a materialized view in Oracle using SQL statements.

- Start by creating and naming a "materialized view" object called "My underscore Mat underscore View"
- Specify the refresh type as fast, which means "incrementally refresh the data"
- Specify today as the start date, and
- Refresh the view every day
- The final statement selects all data from my underscore table underscore name

### PostgreSQL

Here is how you might create a materialized view in PostgreSQL to replicate a table.

- Start by creating a "materialized view" object called "My underscore Mat underscore View"
- Specify some parameters
- Specify the source tablespace, say "tablespace underscore name", and
- Select all rows and columns from "table underscore name."

In PostgreSQL you can only refresh materialized views manually, using the "refresh material view" command.

```sql
-- PostgreSQL: Create a materialized view
CREATE MATERIALIZED VIEW my_mat_view AS
SELECT * FROM source_table;

-- Refresh manually (full recomputation)
REFRESH MATERIALIZED VIEW my_mat_view;

-- Refresh without blocking concurrent reads (requires UNIQUE index)
REFRESH MATERIALIZED VIEW CONCURRENTLY my_mat_view;
```

**Line-by-line breakdown:**
- `CREATE MATERIALIZED VIEW my_mat_view AS` — Creates a physical snapshot of the query result, stored on disk
- `SELECT * FROM source_table` — The query whose results are materialized
- `REFRESH MATERIALIZED VIEW my_mat_view` — Recomputes the entire view from scratch (PostgreSQL has no built-in fast/incremental refresh)
- `REFRESH MATERIALIZED VIEW CONCURRENTLY my_mat_view` — Allows concurrent reads during refresh but requires a UNIQUE index on the view

### IBM Db2 (MQTs)

In Db2, materialized views are called MQTs, which stands for "materialized query tables."

Here's an example, from IBM's online documentation, of creating a system-maintained "immediate refresh" MQT.

- The table, which is named "emp," is based on the underlying tables: "Employee" and "Department" from the "Sample" database.
- The table will be created according to the query formed by these SQL statements, which selects columns from both tables.
- The "data initially deferred" clause means that data will not be inserted into the table as part of the "create table" statement, while the "refresh immediate" clause specifies that the query should refresh automatically.
- The "immediate checked" clause specifies that the data is to be checked against the MQT's defining query and refreshed.

Lastly, the "not incremental" clause specifies that integrity checking is to be done on the whole table. A query executed against the "emp" materialized query table shows that it is fully populated with data.

[ENRICHED: performance context — Db2's query optimizer automatically considers MQTs when rewriting queries. If a query's results match an MQT's definition, the optimizer transparently redirects the query to the MQT instead of recomputing from base tables, providing 10x+ speedups without application changes. [Source: https://www.postgresql.org/message-id/AANLkTim68kC3dkioiUp_jy=6koUBPHM0-C=_2-Kr4ogX@mail.gmail.com]]

---

## Summary

In this video, you learned that:

- A data cube represents a star or snowflake schema's dimensions as coordinates, plus a fact from the schema to populate its cells with values.
- Many operations can be applied to data cubes, such as: drilling down into hierarchical dimensions, slicing, dicing, and rolling up.
- Materialized views can be used to replicate data or to precompute expensive queries.
- And finally, modern enterprise data warehouse tools, such as Oracle and Db2, allow you to automatically keep your materialized views up-to-date.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Why Data Cubes Exist | Historical context | Data cube operator defined by Jim Gray et al. in 1995 paper | HIGH | https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-22.pdf |
| 2 | Why Data Cubes Exist | Ecosystem | Data cubes as core OLAP technology enabling drill down, roll up, slice, dice, pivot | HIGH | https://www.ibm.com/think/topics/olap |
| 3 | Data Cubes | Definition | Defined "OLAP (Online Analytical Processing)" | HIGH | https://clickhouse.com/resources/engineering/olap-operations |
| 4 | Data Cubes | Definition | Defined "Data cube" as n-dimensional hypercube | HIGH | https://theintactone.com/2026/03/03/olap-operations-roll-up-drill-down-slice-dice-pivot/ |
| 5 | Slicing | Example | SQL example of slice operation with WHERE clause | HIGH | https://clickhouse.com/resources/engineering/olap-operations |
| 6 | Dicing vs Slicing | Distinction | Clarified slice (1 dimension) vs dice (2+ dimensions) | HIGH | https://clickhouse.com/resources/engineering/olap-operations |
| 7 | Drill Down/Up | Definition | Defined drill down and drill up with hierarchy example | HIGH | https://theintactone.com/2026/03/03/olap-operations-roll-up-drill-down-slice-dice-pivot/ |
| 8 | Rolling Up | Performance | Modern columnar DB roll-up via GROUP BY ROLLUP/CUBE, SQL:1999 standard | HIGH | https://clickhouse.com/resources/engineering/olap-operations |
| 9 | Materialized Views | Definition | Defined materialized view vs regular view (physical vs virtual) | HIGH | https://www.epsio.io/blog/database-materialized-view-vs-regular-view |
| 10 | Materialized Views | Ecosystem | Positioning in OLAP/data marts/ETL; alternatives: Druid, Epsio | HIGH | https://www.epsio.io/blog/database-materialized-view-vs-regular-view |
| 11 | Refresh Options | Ecosystem | Oracle fast refresh (MV Logs), PostgreSQL complete-only, Db2 MQTs | HIGH | https://www.cybrosys.com/research-and-development/postgres/why-postgresql-has-no-fast-materialized-view-refresh |
| 12 | PostgreSQL | Code breakdown | Line-by-line PostgreSQL MV create and refresh syntax | HIGH | https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html |
| 13 | Db2 MQTs | Performance | Db2 optimizer transparently redirects queries to matching MQTs for 10x+ speedup | HIGH | https://www.postgresql.org/message-id/AANLkTim68kC3dkioiUp_jy=6koUBPHM0-C=_2-Kr4ogX@mail.gmail.com |
| 14 | How Cubes Are Built | Practical implementation | Three main strategies: full, partial, on-demand with caching | HIGH | https://cse.buffalo.edu/adblab/people/zzhao35/teaching/cse707_fall21/datacube.pdf |
| 15 | How Cubes Are Built | Algorithm | BUC algorithm for Iceberg cubes with Apriori-style pruning | HIGH | https://sigmodrecord.org/publications/sigmodRecord/9906/Bottom-up%20computation%20of%20sparse%20and%20Iceberg%20CUBE.pdf |
| 16 | How Cubes Are Built | Optimization | Cube shells: compute only up to m-dimensional cuboids in n-D cube | HIGH | https://www.vldb.org/conf/2003/papers/S15P02.pdf |
| 17 | How Cubes Are Built | Real-world example | Mervyn's 2,400 pre-computed summary tables with greedy selection | HIGH | https://cse.buffalo.edu/adblab/people/zzhao35/teaching/cse707_fall21/datacube.pdf |
| 18 | How Cubes Are Built | Performance | Parallel PnP algorithm: 82% reduction, linear speedup on 8-node cluster | HIGH | https://web.cs.dal.ca/~arc/publications/2-28/paper.pdf |
| 19 | Slicing | Visualization | Text-based 3D cube and 2D slice diagrams with practical explanation | HIGH | UNCERTAIN |
| 20 | Drill Down/Up | Visualization | Concrete hierarchy examples and drill down/up tables | HIGH | UNCERTAIN |
| 21 | Drill Down/Up | Example | SQL examples showing drill down vs drill up queries | HIGH | https://clickhouse.com/resources/engineering/olap-operations |
| 22 | Rolling Up | Visualization | Complete source data, SQL, and multi-level result table with NULL=NULL explanation | HIGH | UNCERTAIN |

<!-- EXTRACTION_CHECKLIST: 120 sentences extracted, 120 sentences in output -->
