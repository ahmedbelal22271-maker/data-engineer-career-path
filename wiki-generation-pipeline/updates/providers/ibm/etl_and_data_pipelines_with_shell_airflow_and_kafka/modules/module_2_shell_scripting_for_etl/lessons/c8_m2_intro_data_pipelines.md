**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 2:** Shell Scripting for ETL

# Introduction to Data Pipelines

## Learning Objectives

After watching this video, you will be able to:
- define what a pipeline is,
- describe data pipeline performance in terms of latency and throughput, and
- give examples of data pipeline use cases.

## What is a Pipeline?

The concept of a pipeline applies broadly to any set of processes that are connected to each other sequentially. This means that the output of one process is passed along as input to the next process in a chain.

[ENRICHED: concrete example — the video's analogy of friends passing boxes, mapped to real data work:

**The analogy:** 5 friends stand in a line. Friend 1 picks up a box, passes it to Friend 2, who passes it to Friend 3, and so on until Friend 5 puts it down. Each friend does ONE thing: receive → pass. The work is distributed across the chain.

**But what does this have to do with data?** Here is where the analogy clicks — replace "friends" with "scripts" and "boxes" with "data files":

**Scenario: You're a data engineer at an e-commerce company. Every night at 2 AM, you need to:**
1. Pull yesterday's sales from the database
2. Clean the data (remove duplicates, fix formatting)
3. Calculate totals per product
4. Load the results into a dashboard

**Without a pipeline (one big script):**

```bash
# one giant script doing everything
python3 -c "
import psycopg2, pandas as pd
conn = psycopg2.connect(...)
df = pd.read_sql('SELECT * FROM sales WHERE date = yesterday', conn)
df = df.drop_duplicates()
df['amount'] = df['amount'].astype(float)
df['tax'] = df['amount'] * 0.08
df['total'] = df['amount'] + df['tax']
totals = df.groupby('product').sum()
totals.to_sql('daily_summary', conn)
"
```

This works, but: if step 3 (tax calculation) breaks, you have to debug the ENTIRE script. If you want to change how duplicates are removed, you're editing the same file that handles database connections. Everything is tangled together.

**With a pipeline (each step is a separate script, connected by files):**

```bash
# STAGE 1: Extract — read raw data, save to file
python3 extract.py > raw_sales.csv

# STAGE 2: Transform — clean the data
python3 clean.py raw_sales.csv > clean_sales.csv

# STAGE 3: Transform — calculate totals
python3 calculate.py clean_sales.csv > daily_summary.csv

# STAGE 4: Load — push to database
python3 load.py daily_summary.csv
```

Now map this to the friends-passing-boxes analogy:

```
[raw_sales.csv]                                    [database]
       ↓                                               ↑
   extract.py ──→ clean.py ──→ calculate.py ──→ load.py
   (Friend 1)    (Friend 2)    (Friend 3)     (Friend 4)
   "pick up")     "clean")      "calculate")   "put down")
```

| Friends Analogy | Real Pipeline Equivalent | What It Does |
|----------------|--------------------------|--------------|
| F1 picks up box | `extract.py` reads database | Gets the raw data |
| F1 passes to F2 | Output saved as `raw_sales.csv` | Data moves to next stage |
| F2 receives & cleans | `clean.py` removes duplicates | Transforms the data |
| F2 passes to F3 | Output saved as `clean_sales.csv` | Clean data moves on |
| F3 calculates totals | `calculate.py` aggregates | Another transformation |
| F3 passes to F4 | Output saved as `daily_summary.csv` | Ready for loading |
| F4 puts box down | `load.py` writes to database | Final destination |

**Why is this better than one big script?**

| Problem | One Big Script | Pipeline |
|---------|---------------|----------|
| Tax calculation bug in step 3 | Debug the entire 50-line script | Open `calculate.py` only — 5 lines |
| Need to change database connection | Edit the same file as business logic | Edit `extract.py` and `load.py` only |
| Step 2 is slow, need to optimize | Untangle cleaning logic from everything else | Optimize `clean.py` independently |
| Want to run step 3 repeatedly during testing | Re-run the whole script (wastes time running extract every time) | Run `python3 calculate.py clean_sales.csv` directly |
| New team member joins | "Here's a 200-line script, good luck" | "Each file does one thing, read them in order" |

**The core principle:** Each friend (script) does ONE job well. The boxes (data files) between them are the connections. You can swap out any friend without rebuilding the whole chain. That's why pipelines exist — they make data work **modular, debuggable, and maintainable**.]  

For example, one way to move boxes from one place to another is to have a chain of friends, each passing the boxes one by one up the line to the nearest friend. Each friend is a processor whose function is identical, get a box, pass a box. Mass production is similar, but transformations may differ from stage to stage.

[ENRICHED: added specificity — the distinction between the "box passing" pipeline and "mass production" pipeline is important:

In box passing, every stage does the **same thing** (pass the box). In mass production (and most real data pipelines), each stage does something **different**.

The reason this matters: if every stage did the same thing, you wouldn't need a pipeline — you could just use one stage. The power of a pipeline comes from **specialization**. Each stage is optimized for one transformation.

**Real ETL pipeline example — processing web server logs:**

```
Raw log file (10 GB)
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: EXTRACT                                                │
│ Script: extract.py                                              │
│ Input:  /var/log/apache2/access.log                             │
│ Output: /tmp/raw_events.csv                                     │
│ What it does: Parses raw log lines into structured CSV rows     │
│ Time: 2 minutes                                                  │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼  [raw_events.csv — 10 GB of structured rows]
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: FILTER                                                 │
│ Script: filter.py                                               │
│ Input:  /tmp/raw_events.csv                                     │
│ Output: /tmp/filtered_events.csv                                │
│ What it does: Remove bots, health checks, static assets         │
│ Time: 30 seconds                                                 │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼  [filtered_events.csv — 2 GB after filtering]
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: TRANSFORM                                              │
│ Script: transform.py                                            │
│ Input:  /tmp/filtered_events.csv                                │
│ Output: /tmp/page_views.csv                                     │
│ What it does: Group by page, count views, compute avg duration  │
│ Time: 1 minute                                                   │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼  [page_views.csv — 50 MB aggregated data]
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: LOAD                                                   │
│ Script: load.py                                                 │
│ Input:  /tmp/page_views.csv                                     │
│ Output: PostgreSQL table `analytics.page_views`                 │
│ What it does: UPSERT into warehouse, update dashboard           │
│ Time: 15 seconds                                                 │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
Dashboard shows fresh data every night at 2 AM
```

**Why not do this in one script?** Because each stage has different failure modes and different skill requirements:
- Extract: needs to handle messy log formats (regex expertise)
- Filter: needs business logic knowledge (what counts as a "real" visit?)
- Transform: needs SQL/pandas skills (aggregation logic)
- Load: needs database admin knowledge (index management, conflict resolution)

A data engineer who's great at regex might be weak at SQL. By splitting into a pipeline, different people can own different stages. And when the transform step breaks at 3 AM, you only need to understand 20 lines of `transform.py`, not 500 lines of a monolith.]

## Data Pipelines

Data pipelines are pipelines that specifically move or modify data. The purpose of a data pipeline is to move data from one place or form to another. A data pipeline is a system which extracts data and passes it along to optional transformation stages for final loading.

[ENRICHED: defined "data pipeline" — a coordinated sequence of automated processes that move data from source systems through transformation steps to a destination. The pipeline abstracts the complexity: instead of manually extracting data, cleaning it, and loading it, you define the pipeline once and it runs automatically on a schedule or in response to events. The "optional transformation stages" phrase is important — not all data pipelines transform data. A simple backup pipeline might just copy data from System A to System B with no transformation at all.]

[ENRICHED: clarified concept — pipeline flexibility and what a pipeline actually includes:

**How flexible is a pipeline definition?**

The core principle: **pipelines are modular by design.** Each stage is an independent unit that can be modified, replaced, or removed without rebuilding the entire system. This is the fundamental advantage over a monolithic script.

**Concrete example — the e-commerce pipeline from the friends analogy:**

```bash
# Current pipeline: 4 stages
extract.py → clean.py → calculate.py → load.py
```

**Scenario: Business wants to add a "fraud check" step between calculate and load:**

| Approach | What you do | Risk |
|----------|------------|------|
| **Monolith** | Edit the 50-line script, insert fraud check logic in the middle, hope nothing breaks | HIGH — one bug breaks everything |
| **Pipeline** | Create `fraud_check.py`, add one line: `fraud_check.py daily_summary.csv > verified.csv`, update `load.py` to read from `verified.csv` | LOW — only 2 files touched |

**Scenario: Transform step is slow, need to parallelize:**

| Approach | What you do | Risk |
|----------|------------|------|
| **Monolith** | Rewrite the entire script to add multiprocessing | HIGH —重构 entire codebase |
| **Pipeline** | Replace `clean.py` with `clean_parallel.py` that uses 4 workers | LOW — one file swapped |

**Scenario: Migration from on-prem to cloud:**

| Approach | What you do | Risk |
|----------|------------|------|
| **Monolith** | Rewrite everything for cloud APIs | HIGH — complete rewrite |
| **Pipeline** | Replace `extract.py` (read from on-prem DB) with `extract_s3.py` (read from S3) | LOW — one stage changed |

**The flexibility spectrum:**

```
SIMPLE                                              COMPLEX
  │                                                    │
  ▼                                                    ▼
cp -r /data/ /backup/     →     Airflow DAG with 20 tasks,
(1 command, 0 flexibility       Spark transformations,
 needed — just works)           Kafka streaming, monitoring,
                                alerting, auto-scaling
```

The simpler the pipeline, the less flexibility you need (and have). A `cp -r` backup has no stages to swap. But as pipelines grow (more stages, more data, more teams), modularity becomes critical.

**What a pipeline REALLY includes (beyond ETL):**

A production data pipeline is not just Extract → Transform → Load. It includes the **control plane** — the operational machinery that keeps it running:

| Component | What It Does | Without It |
|-----------|-------------|------------|
| **Extraction** | Read data from sources | No data enters the pipeline |
| **Ingestion** | Bring data into the pipeline environment | Data sits in source, unusable |
| **Transformation** (optional) | Clean, reshape, enrich | Raw data lands as-is |
| **Loading** | Write to destination | Data never reaches warehouse |
| **Scheduling/Triggering** | Define when jobs run | Pipeline never executes |
| **Monitoring** | Track health, performance, errors | Silent failures — broken pipeline undetected |
| **Logging** | Record all events | Can't debug when things go wrong |
| **Alerting** | Notify on failures | No one knows until someone reports bad data |
| **Error Handling** | Catch and recover from failures | One bad record crashes the entire pipeline |
| **Parallelization** | Split work across workers | Bottleneck stages slow everything |
| **I/O Buffers** | Smooth flow between stages of different speed | Fast stages idle waiting for slow stages |
| **Maintenance & Optimization** | Fix issues, tune performance | Pipeline degrades over time |

**Real-world example — what happens when you skip the control plane:**

```
NAIVE PIPELINE (just ETL):
extract.py → transform.py → load.py

What happens at 3 AM when the source database is down?
→ extract.py crashes
→ transform.py never runs
→ load.py never runs
→ Dashboard shows yesterday's data
→ Nobody knows until the marketing team complains at 9 AM

PRODUCTION PIPELINE (ETL + control plane):
┌─────────────────────────────────────────────────┐
│ SCHEDULE: Airflow DAG, runs at 2 AM daily       │
│                                                  │
│ extract.py ──→ transform.py ──→ load.py         │
│     │              │                │            │
│     ▼              ▼                ▼            │
│  LOG: "Extract     LOG: "Transform   LOG: "Load  │
│  started"          started"          started"    │
│     │              │                │            │
│     ▼              ▼                ▼            │
│  MONITOR: Track    MONITOR: Track   MONITOR:     │
│  latency, errors   latency, errors  latency,     │
│                                     errors        │
│     │              │                │            │
│     ▼              ▼                ▼            │
│  ALERT: If extract fails, page on-call engineer  │
│  ALERT: If latency > 5 min, notify Slack channel │
│  ALERT: If error rate > 1%, halt pipeline        │
└─────────────────────────────────────────────────┘

What happens at 3 AM when the source database is down?
→ Airflow retries extract.py 3 times (exponential backoff)
→ After 3 failures, Airflow marks task as FAILED
→ Airflow sends Slack alert: "Pipeline sales_nightly_load FAILED"
→ On-call engineer gets paged, investigates
→ Dashboard shows "Data as of Jul 22" (not stale data pretending to be fresh)
→ Engineer fixes issue, manually triggers pipeline re-run
→ Pipeline succeeds on retry
```

**The key insight:** The pipeline definition is the *entire system* — not just the data flow stages. When someone says "our pipeline," they mean: the extraction logic, transformation logic, loading logic, AND the scheduling, monitoring, alerting, error handling, and optimization that keeps it running. The ETL stages are the *what*; the control plane is the *how it stays alive*.]

This includes low-level hardware architectures, but our focus here is on data pipelines as architectures driven by software processes such as commands, programs, and processing threads.

[ENRICHED: defined "processing threads" — a thread is the smallest unit of execution within a process. Modern CPUs can run multiple threads simultaneously (multi-threading), allowing a data pipeline to process multiple data packets in parallel. For example, a pipeline might use one thread to extract data from a database while another thread transforms previously extracted data. This is the software-level equivalent of the physical pipeline analogy: multiple "workers" (threads) handling different packets at different stages simultaneously.]

The simple bash pipe command in Linux can be used as the glue that connects such processes together.

[ENRICHED: concrete example — the bash pipe (`|`) connects commands sequentially, where the output of one command becomes the input of the next: `cat sales.csv | grep "2024" | awk '{print $3}' | sort | uniq -c`. This pipeline: (1) `cat` reads the file, (2) `grep` filters to 2024 records, (3) `awk` extracts the third column, (4) `sort` orders the values, (5) `uniq -c` counts unique values. Each command is a stage; the pipe `|` is the connection. The data flows as text through each stage, being transformed at each step. This is the simplest form of a data pipeline — and it demonstrates the core principle: small, focused tools connected sequentially to accomplish complex data processing.]

## Data Packets

We can think of data flowing through the pipeline in the form of data packets. A term which we will use to broadly refer to units of data. Packets can range in size from a single record or event to large collections of data.

[ENRICHED: added specificity — the concept of "data packets" is abstract and flexible by design. In different contexts, a "packet" might be: a single row in a database (one customer record), a single event (one click on a website), a batch of records (all transactions from yesterday), or a large file (a 10 GB CSV). The pipeline doesn't care about the packet size — it processes whatever it receives. This abstraction allows the same pipeline architecture to handle both real-time streaming (small packets, one event at a time) and batch processing (large packets, millions of records at once).]

Here we have data packets queued for ingestion to the pipeline. The length of the data pipeline represents the time it takes for a single packet to traverse the pipeline. The arrows between packets represent the throughput delays or the times between successive packet arrivals.

[ENRICHED: added specificity — this visual representation is key to understanding pipeline performance. Imagine a queue of packets waiting to enter the pipeline:

```
PACKET QUEUE:  [P1] [P2] [P3] [P4] [P5]
                    ↓
              ┌─────────────────────────────┐
              │  PIPELINE                    │
              │  ┌─────┐  ┌─────┐  ┌─────┐  │
              │  │ S1  │→ │ S2  │→ │ S3  │  │
              │  └─────┘  └─────┘  └─────┘  │
              └─────────────────────────────┘
                    ↓
              OUTPUT: [P1] [P2] [P3] ...

Latency = time for ONE packet to go through ALL stages
Throughput = how many packets come out per unit time
```

The "length" of the pipeline (visually, how long the box is) represents latency — how long it takes a single packet to traverse all stages. The "arrows between packets" represent throughput delays — the gaps between when successive packets exit the pipeline.]

## Performance Considerations

You have just been introduced to two key performance considerations regarding data pipelines.

### Latency

The first is latency, which is the total time it takes for a single packet of data to pass through the pipeline. Equivalently, latency is the sum of the individual time spent during each processing stage within the pipeline. Thus, overall latency is limited by the slowest process in the pipeline.

[ENRICHED: concrete example — a data pipeline with three stages:

| Stage | Processing Time |
|-------|----------------|
| Extract (read from database) | 2 seconds |
| Transform (clean + join) | 8 seconds |
| Load (write to warehouse) | 3 seconds |

Latency = 2 + 8 + 3 = **13 seconds** per packet.

The Transform stage is the bottleneck — it takes 8 seconds, while the other stages take 2 and 3 seconds. Even if you speed up Extract to 0.5 seconds, latency drops to only 0.5 + 8 + 3 = 11.5 seconds. To meaningfully reduce latency, you must speed up the SLOWEST stage (Transform). This is known as **Amdahl's Law** in computing: the overall speedup is limited by the slowest component.]

For example, no matter how fast your internet service is, the time it takes to load a web page will be decided by the server speed.

[ENRICHED: added specificity — this is a real-world latency example. Your internet connection might deliver data at 1 Gbps (low latency on your end), but if the web server takes 3 seconds to generate the page, your total latency is at least 3 seconds. The server is the bottleneck. The same applies to data pipelines: if one stage is slow, the entire pipeline is slow — regardless of how fast the other stages are.]

### Throughput

The second performance consideration is called throughput. It refers to how much data can be fed through the pipeline per unit of time. Processing larger packets per unit of time increases throughput.

[ENRICHED: concrete example — using the same three-stage pipeline:

| Stage | Processing Time |
|-------|----------------|
| Extract | 2 seconds |
| Transform | 8 seconds |
| Load | 3 seconds |

**Without pipelining (sequential):**
- Packet 1: Extract (2s) → Transform (8s) → Load (3s) = 13s
- Packet 2: waits for Packet 1 to finish, then starts = 13s more
- Throughput: 1 packet every 13 seconds = **~4.6 packets/minute**

**With pipelining (overlapping):**
- Time 0-2s: Packet 1 in Extract
- Time 2-10s: Packet 1 in Transform, Packet 2 in Extract
- Time 10-13s: Packet 1 in Load, Packet 2 in Transform, Packet 3 in Extract
- After pipeline fills: one packet exits every 8 seconds (the bottleneck stage)
- Throughput: 1 packet every 8 seconds = **~7.5 packets/minute**

Pipelining increases throughput from ~4.6 to ~7.5 packets/minute — a **63% improvement** — without making any single stage faster. The improvement comes from overlapping the stages so no stage sits idle.]

[ENRICHED: clarified concept — latency and throughput are independent metrics. A common confusion is thinking that high throughput implies low latency, or that high latency implies low throughput. Neither is true. They measure different things:

- **Latency** = time for ONE unit to travel from start to finish. It answers: "How long does a single unit wait?"
- **Throughput** = rate of output (units ÷ time). It answers: "How many units come out per second?"

**They can move independently:**

| Scenario | Latency | Throughput | Key comparison |
|----------|---------|------------|----------------|
| 10 slow stages, pipelined | 1,000s | 0.01 units/sec | Baseline — many stages, pipelined |
| 1 slow stage, no pipeline | 100s | 0.01 units/sec | Same throughput, 10× lower latency |
| 10 slow stages, NOT pipelined | 1,000s | 0.001 units/sec | Same latency as row 1, 10× lower throughput |
| Batch of 1M units, 100s | 100s | 10,000 units/sec | High latency AND high throughput simultaneously |

**Detailed walkthrough of each scenario:**

---

**Scenario 1: 10 slow stages, pipelined**

Setup: 10 stages, each takes 100 seconds. Units enter one at a time, overlapping across stages.

**First — what do the 10 stages actually DO?**

Each stage is a separate script that performs one transformation on the data. Imagine you're processing web server logs — every day,1 million log records arrive, and you need to turn them into a dashboard-ready summary.

| Stage | Script | What it does to the data | Input | Output |
|-------|--------|--------------------------|-------|--------|
| S1 | `read_logs.sh` | Read raw log file from disk | `/var/log/access.log` (10 GB) | `raw.csv` (10 GB) |
| S2 | `parse.sh` | Parse each log line into structured fields | `raw.csv` (messy text) | `parsed.csv` (structured rows) |
| S3 | `filter_bots.sh` | Remove bot/crawler traffic | `parsed.csv` (all traffic) | `human_only.csv` (6 GB, 40% removed) |
| S4 | `extract_ip.sh` | Pull IP address from each record | `human_only.csv` | `with_ip.csv` |
| S5 | `geo_lookup.sh` | Look up country/city from IP | `with_ip.csv` | `with_geo.csv` |
| S6 | `parse_agent.sh` | Extract browser + OS from user-agent string | `with_geo.csv` | `with_browser.csv` |
| S7 | `sessionize.sh` | Group events into user sessions (30 min timeout) | `with_browser.csv` | `sessions.csv` |
| S8 | `count_views.sh` | Count page views per session | `sessions.csv` | `page_views.csv` |
| S9 | `join_users.sh` | Join with user database to get demographics | `page_views.csv` | `final.csv` |
| S10 | `write_db.sh` | Write results to PostgreSQL | `final.csv` | `analytics.page_views` table |

**Each stage takes 100 seconds** because it's processing1 million records. The total pipeline takes 10 × 100 = 1,000 seconds per batch.

---

**What happens to Unit 1 (the first batch of1M records):**

```
Time:     0    100   200   300   ...   900   1000
S1:      [U1]  idle  idle  idle  ...   idle  idle
          ↓
       U1 is raw log text, becomes raw.csv
          ↓
S2:      idle  [U1]  idle  idle  ...   idle  idle
               ↓
            U1 is raw.csv, becomes parsed.csv (structured)
               ↓
S3:      idle  idle  [U1]  idle  ...   idle  idle
                    ↓
                 U1 is parsed.csv, becomes human_only.csv (bots removed)
                    ↓
...
S10:     idle  idle  idle  idle  ...   [U1]  idle
                                       ↓
                                    U1 is final.csv, written to database
                                       ↓
                                    DASHBOARD UPDATED ✓
```

**Latency = 1,000 seconds.** The first batch entered at t=0, reached the dashboard at t=1000.

---

**Now watch what happens with MULTIPLE units (this is where pipelining kicks in):**

The key: **S1 doesn't wait for U1 to finish the entire pipeline.** The moment S1 finishes reading U1's logs (at t=100), it immediately starts reading U2's logs. Meanwhile, S2 starts parsing U1. Both stages are working simultaneously — on DIFFERENT batches.

```
Time:      0       100      200      300      ...    900     1000    1100
         ┌────────┬────────┬────────┬────────┬─────┬────────┬────────┬────────┐
S1:      │ U1     │ U2     │ U3     │ U4     │ ... │ U10    │ idle   │ idle   │
         │ read   │ read   │ read   │ read   │     │ read   │        │        │
         │ logs   │ logs   │ logs   │ logs   │     │ logs   │        │        │
         ├────────┼────────┼────────┼────────┼─────┼────────┼────────┼────────┤
S2:      │ idle   │ U1     │ U2     │ U3     │ ... │ U9     │ U10    │ idle   │
         │        │ parse  │ parse  │ parse  │     │ parse  │ parse  │        │
         │        │ logs   │ logs   │ logs   │     │ logs   │ logs   │        │
         ├────────┼────────┼────────┼────────┼─────┼────────┼────────┼────────┤
S3:      │ idle   │ idle   │ U1     │ U2     │ ... │ U8     │ U9     │ U10    │
         │        │        │ filter │ filter │     │ filter │ filter │ filter │
         │        │        │ bots   │ bots   │     │ bots   │ bots   │ bots   │
         ├────────┼────────┼────────┼────────┼─────┼────────┼────────┼────────┤
S4:      │ idle   │ idle   │ idle   │ U1     │ ... │ U7     │ U8     │ U9     │
         │        │        │        │ extract│     │ extract│ extract│ extract│
         │        │        │        │ IP     │     │ IP     │ IP     │ IP     │
         ├────────┼────────┼────────┼────────┼─────┼────────┼────────┼────────┤
S5:      │ idle   │ idle   │ idle   │ idle   │ ... │ U6     │ U7     │ U8     │
         │        │        │        │        │     │ geo    │ geo    │ geo    │
         │        │        │        │        │     │ lookup │ lookup │ lookup │
         ├────────┼────────┼────────┼────────┼─────┼────────┼────────┼────────┤
S6:      │ idle   │ idle   │ idle   │ idle   │ ... │ U5     │ U6     │ U7     │
         │        │        │        │        │     │ parse  │ parse  │ parse  │
         │        │        │        │        │     │ agent  │ agent  │ agent  │
         ├────────┼────────┼────────┼────────┼─────┼────────┼────────┼────────┤
S7:      │ idle   │ idle   │ idle   │ idle   │ ... │ U4     │ U5     │ U6     │
         │        │        │        │        │     │ session│ session│ session│
         ├────────┼────────┼────────┼────────┼─────┼────────┼────────┼────────┤
S8:      │ idle   │ idle   │ idle   │ idle   │ ... │ U3     │ U4     │ U5     │
         │        │        │        │        │     │ count  │ count  │ count  │
         │        │        │        │        │     │ views  │ views  │ views  │
         ├────────┼────────┼────────┼────────┼─────┼────────┼────────┼────────┤
S9:      │ idle   │ idle   │ idle   │ idle   │ ... │ U2     │ U3     │ U4     │
         │        │        │        │        │     │ join   │ join   │ join   │
         │        │        │        │        │     │ users  │ users  │ users  │
         ├────────┼────────┼────────┼────────┼─────┼────────┼────────┼────────┤
S10:     │ idle   │ idle   │ idle   │ idle   │ ... │ U1     │ U2     │ U3     │
         │        │        │        │        │     │ write  │ write  │ write  │
         │        │        │        │        │     │ to DB  │ to DB  │ to DB  │
         └────────┴────────┴────────┴────────┴─────┴────────┴────────┴────────┘
                                         OUTPUT:         →U1→   →U2→   →U3→
                                        dashboard      updated updated updated
                                                         t=1000  t=1100  t=1200
```

**Reading the diagram — trace U2 through the pipeline:**
- t=0-100: U2 doesn't exist yet. S1 is reading U1's logs.
- t=100-200: S1 finishes U1, starts reading U2's logs. S2 starts parsing U1.
- t=200-300: S1 finishes U2, starts reading U3. S2 finishes parsing U1, starts parsing U2. S3 starts filtering U1's bots.
- ...
- t=1000-1100: S10 writes U2 to database. Dashboard updated.

**Reading the diagram — trace what happens at t=500 (middle of the pipeline):**
- S1 is reading U5's logs (just started)
- S2 is parsing U4's logs
- S3 is filtering bots from U3
- S4 is extracting IPs from U2
- S5 is doing geo-lookup on U1
- S6-S10: idle (U1 hasn't reached them yet, earlier units already passed)

**Five different batches, at five different stages of processing, all happening simultaneously.** That's pipelining.

---

**After the pipeline fills (t=900+), the steady state:**

```
Every 100 seconds:
- S1 finishes reading a batch → passes to S2 → starts next batch
- S2 finishes parsing a batch → passes to S3 → starts next batch
- ...
- S10 finishes writing a batch → dashboard updated → starts next batch

One batch exits every 100 seconds.
Throughput = 1 batch / 100 sec = 0.01 batches/sec = 36 batches/hour.
```

**Key insight:** Even though each batch sits inside for 1,000 seconds (latency), the pipeline outputs batches at a steady rate of one every 100 seconds (throughput). Latency is high. Throughput is moderate. They coexist — because multiple batches are being processed simultaneously at different stages.

---

**Scenario 2: 1 slow stage, no pipeline**

Setup: 1 stage, takes 100 seconds. No pipelining — one unit at a time.

```
[U1] → [S1] → [OUT]
       100s

[U1] enters t=0, exits t=100
[U2] enters t=100, exits t=200
[U3] enters t=200, exits t=300
```
**Latency = 100 seconds.** Much faster per unit than Scenario 1.
**Throughput = 1 unit / 100 sec = 0.01 units/sec.**

Now compare with Scenario 1:
- Scenario 1: **1,000s** latency, **0.01** units/sec throughput
- Scenario 2: **100s** latency, **0.01** units/sec throughput

**Same throughput (0.01 units/sec), but Scenario 2 is 10× lower latency.** The difference? Scenario 1 has 10 stages (each unit passes through 10 transformations). Scenario 2 has 1 stage (one transformation). Pipelining makes Scenario 1's throughput competitive despite having 10× more stages, but it can't reduce the per-unit latency — that's determined by how many stages a unit must traverse.

---

**Scenario 3: 10 slow stages, NOT pipelined**

Setup: Same as Scenario 1, but no overlapping — Unit 2 waits for Unit 1 to fully exit before entering.

**The core concept: what happens to each stage when it's NOT working on the current unit?**

In **pipelined** mode: When S1 finishes with U1 and passes it to S2, S1 doesn't sit idle — it immediately grabs U2 and starts working on it. Every stage is always busy.

In **non-pipelined** mode: When S1 finishes with U1 and passes it to S2, S1 sits idle. It waits until U1 has fully exited the pipeline (passed through all 10 stages) before it's allowed to grab U2. Every stage is idle 90% of the time.

**Concrete analogy — restaurant kitchen with 3 stations:**

Imagine a restaurant with 3 stations:
- **Station 1 (S1):** Prep — chop vegetables (takes 5 min)
- **Station 2 (S2):** Cook — fry the dish (takes 5 min)
- **Station 3 (S3):** Plate — arrange and serve (takes 5 min)

3 customers order meals (U1, U2, U3). Each meal takes 15 min total (5+5+5).

**Non-pipelined (the "wait for everyone" approach):**

```
Time:    0-5     5-10    10-15   15-20   20-25   25-30   30-35   35-40   40-45
S1:     [U1]     idle    idle    [U2]    idle    idle    [U3]    idle    idle
S2:     idle    [U1]    idle     idle   [U2]    idle     idle   [U3]    idle
S3:     idle     idle    [U1]    idle    idle   [U2]    idle    idle   [U3]
         ↑                            ↑                              ↑
      U1 served                   U2 served                      U3 served
      t=15                        t=30                           t=45
```

What happens step by step:
- t=0-5: S1 preps U1. S2 and S3 idle (nowhere to cook/plate yet).
- t=5-10: S1 passes U1 to S2. S2 cooks U1. **S1 sits idle** (not allowed to start U2).
- t=10-15: S2 passes U1 to S3. S3 plates U1. **S1 and S2 sit idle.**
- t=15: U1 is served. NOW S1 can start U2.
- t=15-20: S1 preps U2. S2 and S3 idle again.
- ...pattern repeats...

**Latency = 15 min** (each meal takes 15 min to make).
**Throughput = 1 meal / 15 min = 4 meals/hour.**

Notice: S1 is busy only 5 out of every 15 minutes (33% utilization). S2 is busy 5 out of 15 (33%). S3 is busy 5 out of 15 (33%). **Two-thirds of the time, the kitchen is idle.**

---

**Pipelined (the "overlap everything" approach):**

```
Time:    0-5     5-10    10-15   15-20   20-25   25-30   30-35
S1:     [U1]    [U2]    [U3]     idle    idle    idle    idle
S2:     idle    [U1]    [U2]    [U3]    idle    idle    idle
S3:     idle     idle    [U1]    [U2]    [U3]   idle    idle
                        ↑       ↑       ↑
                     U1 served U2 served U3 served
                     t=15     t=20     t=25
```

What happens step by step:
- t=0-5: S1 preps U1. S2 and S3 idle.
- t=5-10: S1 passes U1 to S2, **and immediately starts prepping U2**. S2 cooks U1. S3 still idle.
- t=10-15: S2 passes U1 to S3, **and immediately starts cooking U2**. S1 preps U3. S3 plates U1.
- t=15: U1 is served. But U2 is already cooking (started at t=10), and U3 is already prepping (started at t=10).
- t=15-20: S3 plates U2. S2 cooks U3. S1 idle (no more orders).
- t=20: U2 served.
- t=25: U3 served.

**Latency = 15 min** (same — each meal still takes 15 min).
**Throughput = 3 meals / 25 min ≈ 7.2 meals/hour.** (vs 4 meals/hour non-pipelined)

**Why the difference?** Look at S2's row:
- Non-pipelined: S2 works t=5-10, then idle t=10-25 (15 min idle)
- Pipelined: S2 works t=5-10, t=10-15, t=15-20 (almost no idle time)

Pipelining keeps S2 busy by feeding it U2 immediately after U1, instead of making it wait for U1 to be fully served.

---

**Now apply this to 10 stages:**

| | Pipelined (Scenario 1) | Non-pipelined (Scenario 3) |
|---|---|---|
| S1 busy with U2 at t=100? | Yes — starts U2 immediately | No — S1 idle until t=1000 |
| S2 busy with U2 at t=200? | Yes — starts U2 at t=200 | No — S2 idle until t=1000 |
| Stage utilization | ~100% after pipeline fills | ~10% (each stage busy 100s out of 1000s) |
| U2 enters pipeline | t=100 | t=1000 |
| U2 exits pipeline | t=1100 | t=2000 |
| Throughput | 1 unit / 100 sec | 1 unit / 1000 sec |

**The key insight:** Pipelining doesn't make any single stage faster. It eliminates the idle time between stages. In non-pipelined mode, S2 waits idle for 900 seconds while U1 traverses S3-S10. In pipelined mode, S2 starts working on U2 the moment it finishes U1. That idle time is pure waste — pipelining recovers it.

Pipelining doesn't change latency. It changes throughput by keeping stages busy.

---

**Scenario 4: Batch of 1M units, 100 seconds**

Setup: Process 1,000,000 records as one big batch. The batch takes 100 seconds to go through the pipeline.

```
[1M records] → [Pipeline] → [1M records]
                 100s

Single record enters at t=0, exits at t=100
BUT: the other 999,999 records are in the pipeline simultaneously
```

**Latency = 100 seconds** (one unit's journey through the pipeline).
**Throughput = 1,000,000 units / 100 sec = 10,000 units/sec.**

This is the scenario that surprises people: **high latency AND high throughput at the same time.**

Why? Because the 1M records aren't processed one at a time. They're processed as a batch — all 1M records flow through each stage together. Stage 1 reads all 1M records (takes 30s), passes all 1M to Stage 2, which transforms all 1M (takes 50s), passes all 1M to Stage 3, which loads all 1M (takes 20s).

The single-record latency is 100 seconds. But the system output 1M records in those 100 seconds. The throughput is enormous because the work is parallelized across the batch.

**Real-world analogy:** A restaurant kitchen. One dish takes 20 minutes to prepare (latency). But the kitchen serves 200 dishes per hour (throughput). The high throughput doesn't reduce the 20-minute wait for your specific dish — it comes from the kitchen handling many orders simultaneously.

---

**The key insight:** Throughput measures how fast the pipeline produces output *regardless of how long each unit was inside*. Latency measures how long *one specific unit* was delayed. You can have a pipeline where every unit sits inside for 10 minutes (high latency) but one unit exits every millisecond (high throughput). The units are queuing inside the pipeline, overlapping their processing — that's what pipelining gives you.]

Coming back to our example of having a chain of friends passing boxes from one to another, we can see in the right image within limits, that passing bigger boxes can increase productivity.

[ENRICHED: added specificity — "passing bigger boxes" means increasing the packet size. If each friend spends roughly the same time picking up and passing a box regardless of its size, then larger boxes mean more content per pass. Example: if it takes 2 seconds to pass a small box (1 item) or a large box (10 items), the large box gives you 10× the throughput for the same time cost. In data terms: processing a batch of 10,000 records often takes only slightly more time than processing 1,000 records, because the overhead (connection setup, schema parsing, disk I/O) is fixed. This is why batch processing is more efficient than processing records one at a time — you amortize the fixed costs across more records. However, there are limits: eventually the box is too heavy to pass quickly, or the batch is too large to fit in memory.]

## Use Cases

Let's list a few of the applications of data pipelines from the multitude of use cases.

The simplest pipeline has no transformations and is used as file backups, integrating disparate raw data sources into a data lake, moving transactional records to a data warehouse, streaming data from IoT devices to make information available in the form of dashboards or learning systems, preparing raw data for machine learning development or production, and message sending and receiving, such as with email, SMS, or online video meetings.

[ENRICHED: concrete examples for each use case:]

| Use Case | What Happens | Transformation? | Example |
|----------|-------------|-----------------|---------|
| **File backups** | Copy files from one location to another | None | `cp -r /data/ /backup/` — simple copy, no transformation |
| **Integrating raw data sources into a data lake** | Collect raw data from multiple sources into one repository | Minimal (format conversion) | Pulling CSVs from FTP, JSON from APIs, and logs from servers into S3 buckets |
| **Moving transactional records to a data warehouse** | Extract from OLTP, transform for analytics, load into OLAP | Yes (full ETL) | Nightly batch: extract yesterday's orders, clean and aggregate, load into Redshift |
| **Streaming IoT data to dashboards** | Real-time flow from sensors to visualization | Yes (filtering, aggregation) | Temperature sensors → Kafka → Flink aggregation → Grafana dashboard |
| **Preparing raw data for ML** | Extract, clean, engineer features, split into train/test | Yes (heavy transformation) | Customer data → clean NULLs → compute features (avg_order_value, tenure) → save as Parquet for model training |
| **Message sending/receiving** | Route messages between senders and recipients | Minimal (routing, formatting) | Email: compose → SMTP server → recipient's inbox. Video meeting: capture audio/video → encode → stream to participants |

[ENRICHED: ecosystem — the simplest pipeline (file backup) is a **data movement** pipeline with no transformation. The most complex (ML feature engineering) is a full **ETL/ELT** pipeline with multiple transformation stages. The spectrum from simple to complex maps directly to the tools required: simple pipelines can use cron + bash scripts; complex pipelines need orchestration tools like Apache Airflow, stream processing frameworks like Kafka + Flink, and feature stores like Feast or Tecton.]

## Summary

In this video, you learned that:
- the purpose of a data pipeline is to move data from one place or form to another,
- we can visualize data flowing through a pipeline as a series of data packets flowing in and out, one by one,
- latency and throughput are key design considerations for data pipelines, and
- use cases for data pipelines are many and range from simple copy and paste like data backups to online video meetings.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Pipeline concept | Concrete example | Friends-passing-boxes analogy mapped to real scripts: e-commerce scenario, monolith vs pipeline comparison, 5-row table showing modularity benefits | HIGH |
| 2 | Pipeline concept | Added specificity | Mass production distinction: real 4-stage ETL pipeline (Extract→Filter→Transform→Load) processing web server logs, with file I/O at each stage and specialization rationale | HIGH |
| 3 | Data pipelines | Definition | Defined data pipeline as coordinated sequence of automated processes | HIGH |
| 4 | Data pipelines | Added specificity | Explained "optional transformation stages" — not all pipelines transform | HIGH |
| 5 | Software processes | Definition | Defined "processing threads" as smallest execution units, multi-threading for parallel packet processing | HIGH |
| 6 | Bash pipe | Concrete example | 5-command bash pipeline: cat → grep → awk → sort → uniq -c | HIGH |
| 7 | Data packets | Added specificity | Packet size flexibility: single row, single event, batch, or large file | HIGH |
| 8 | Pipeline visualization | Added specificity | ASCII diagram of packet queue + pipeline stages + latency/throughput definitions | HIGH |
| 9 | Latency | Concrete example | 3-stage pipeline: Extract(2s) + Transform(8s) + Load(3s) = 13s latency, bottleneck analysis, Amdahl's Law reference | HIGH |
| 10 | Latency | Concrete example | Internet/server latency example — server speed as bottleneck | HIGH |
| 11 | Throughput | Concrete example | Same pipeline: sequential (4.6 pkt/min) vs pipelined (7.5 pkt/min) = 63% improvement | HIGH |
| 12 | Throughput | Clarified concept | Latency and throughput are independent metrics — 10-stage web analytics pipeline with concrete roles per stage (read logs → parse → filter bots → extract IP → geo lookup → parse agent → sessionize → count views → join users → write DB), detailed pipelining diagram showing 5 batches at 5 stages simultaneously, steady-state throughput explanation | HIGH |
| 13 | Throughput | Added specificity | "Bigger boxes" = batch size efficiency, fixed overhead amortization, memory limits | HIGH |
| 14 | Use cases | Concrete examples | 6-row table mapping each use case to what happens, transformation level, and real example | HIGH |
| 15 | Use cases | Ecosystem | Mapped simple→complex pipeline spectrum to tools (cron/bash → Airflow/Kafka/Feature stores) | HIGH |
| 16 | Data pipelines | Clarified concept | Pipeline flexibility: modular design enables swapping stages, adding steps, migrating to cloud without full rewrite; 3 scenarios (add fraud check, parallelize transform, migrate to cloud) with monolith vs pipeline risk comparison | HIGH |
| 17 | Data pipelines | Added specificity | Pipeline components beyond ETL: 12-row table covering extraction, ingestion, transformation, loading, scheduling, monitoring, logging, alerting, error handling, parallelization, I/O buffers, maintenance; naive vs production pipeline comparison showing control plane in action | HIGH |
| 18 | Data pipelines | Ecosystem | Connected pipeline components to Airflow (scheduling/monitoring), Kafka (buffering), cloud services (managed control plane); explained that "our pipeline" means the entire system, not just ETL stages | HIGH |

<!-- EXTRACTION_CHECKLIST: 24 sentences extracted, 24 sentences in output -->
