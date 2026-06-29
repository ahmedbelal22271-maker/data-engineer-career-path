# IBM Data Engineering Professional Certificate — Full Learning Plan

**Target total:** ~262h (IBM track) + ~554h (supplements) + ~123h (post-track enhancements) = ~939h all-inclusive; realistically ~400–550h following the IBM track with selective supplements  
**Format:** 16 IBM courses in official order → 9 post-track enhancement modules (A-I) → Appendices (certs + playlist index)  
**Use it as a menu:** Follow the IBM courses sequentially for the most structured path. Add supplements based on your weak areas. Complete Post-Track Enhancements after Course 16 for topics IBM doesn't cover (Hive/Impala, Apache Ranger/Atlas, dbt, UCSD Big Data Specialization electives).

---

## 📝 Changelog
- v1 — Original: 300-hour Big Data plan (Samsung Innovation Campus replacement)
- v2 — 2026-06: Added **Module 0** (DE Foundations), **Module 12** (Pipeline Orchestration & Transformation), **Module 13** (Modern Data Platforms), **Module 14** (AI-Ready Data Engineering), **Appendix A** (8 Free End-to-End Projects), **Appendix B** (2026 Certification Roadmap). Total plan expanded to ~420h.
- v3 — 2026-06: Integrated Mahmoud Mohsen's [Big-Data Analytics YouTube playlist](https://www.youtube.com/playlist?list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI) (20 videos) across 6 modules. Added **Appendix C** (full playlist index). ~7h of additional video content.
- v4 — 2026-06-25: Integrated **[IBM Data Engineering Professional Certificate](https://www.coursera.org/professional-certificates/ibm-data-engineer)** (16 Coursera courses) across the plan. IBM courses prioritized at the start of each relevant module. ~233h of IBM content integrated.
- v5.0 — 2026-06-25: Restructured plan around **IBM Data Engineering Professional Certificate** (16-course spine). All existing resources preserved as supplements or post-track enhancements. New section format introduced. Career Ladder, Certification Roadmap, and Mohsen Playlist Index updated to reference IBM Course numbers. Affected: entire plan structure.
- v5.1 — 2026-06-25: Integrated **"بالعربي Big Data"** channel by Ahmed Sami ([@bigdata4756](https://www.youtube.com/@bigdata4756)) — 16 Arabic-language videos/series (+~61h supplement content) mapped to Courses 2, 5, 6, and 12. New Appendix B subsection added. 2 video IDs confirmed via oEmbed; remaining links point to channel page (search-engine-returned IDs failed oEmbed verification — noted transparently in Appendix B). Hour Summary updated: Foundations block 50h→96h, Big Data block 112h→127h, totals 689h→750h.
- v6.0 — 2026-06-25: Added **Minimum Viable Path** (MVP) section (~200h fast-track for beginners or career-switchers). Added **self-assessment gates** after Courses 7, 9, 12, and 14. Fixed **week-by-week schedule** to show IBM-only vs IBM+core-supplements pacing columns. Added **dimensional modeling supplement** (Course 9). Surfaced **Docker/Compose** as an earlier supplement (Course 6). Added **Confluent Schema Registry / Avro** supplement (Course 8). Added **GCP BigQuery** supplement (Course 9). Clarified Ahmed Sami SQL supplement as an *alternative* to Mode, not additive (Course 5).
- v7.0 — 2026-06-25: Split all supplement tables into Tier 1 (must-watch) and Tier 2 (optional) across all 16 IBM course sections. Added portfolio project ideas table (2–3 projects) to each course section.
- v7.1 — 2026-06-26: Integrated 7 practitioner tips from IBM Data Engineering Viewpoints: Skills and Qualities to Be a Data Engineer. 0 new resource rows, 7 workflow callouts, 0 inline notes added across 5 sections (How to Read, Courses 1, 5, 6, 8, and 16).
- v7.2 — 2026-06-26: Integrated 3 items from UCSD Big Data Specialization (Coursera page). 3 new resource rows, 0 callouts, 0 inline notes, 0 restructures. Coursera-first ordering enforced across 2 modules. Weekly schedule blocks added in 2 modules (Courses 12 and 14). UCSD Courses 1, 2, 4 already present — skipped. New rows: UCSD Course 3 (Big Data Integration and Processing, 17h) and Course 5 (Graph Analytics for Big Data, 12h) added to Course 12 Tier 2; UCSD Course 6 (Big Data Capstone, 22h) added to Course 14 Tier 2.
- v8.0 — 2026-06-27: Integrated 4 items from Claude-curated resources + wiki gap analysis. 3 new post-track enhancements (E: Data Lakehouse Architecture ~10h, F: Data Architecture Patterns ~10h, G: Data Cataloging & Discovery ~10h). 1 new Tier 2 row in Enhancement C (DataKitchen Data Observability Certification ~10h + data contracts supplements ~2h). Coursera-first enforced in 3 new modules. Enhancement C total 17h→27h. Post-track total 49h→89h. Full plan total 801h→841h. Brain verification: APPROVED.
- v9.0 — 2026-06-27: Integrated 9 items from DataTalks.Club DE Zoomcamp repo audit by Claude. 4 new supplement rows in Course 8 (dlt ingestion +4h, Terraform GCP +5h, PyFlink/Spark Streaming +8h, RisingWave +3h). 1 new row in Course 9 (BigQuery ML + cost optimization, +8h). 1 new row in Course 12 (Dataproc + Spark-to-BigQuery, +8h). 1 new row in Enhancement C (Kestra alternative orchestration, +4h). 2 new enhancements (H: Bruin Unified Platform ~5h, I: Capstone Pipeline Project ~25h). Full plan total 841h→910h. Brain verification: APPROVED.
- v10.0 — 2026-06-29: Integrated 5 items from first full wiki-to-plan sync (51 files scanned, 5 actionable). 2 inline notes added: Big Data Five V's framework + "store everything" philosophy (Course 12), column-oriented storage explanation (Course 11). 1 combined career insight callout in Course 16 synthesizing 3 viewpoint files (career path diversity, DBA→DE transition, hiring manager 4-layer evaluation framework). 10 SUPPLEMENT files recognized as already-covered. Full plan total unchanged at ~910h. Brain verification: APPROVED.
- v10.1 — 2026-06-29: Integrated 2 actionable items from wiki-to-plan sync (7 new files after wiki pipeline rebuild). 2 practitioner callouts added: Jupyter best practices (Course 2) and diagnostic troubleshooting patterns (Course 7). 5 new files recognized as already-covered. 7 legacy files marked REMOVED (replaced by consolidated versions). Full plan total unchanged at ~910h. Brain verification: APPROVED.
- v10.2 — 2026-06-30: Corrected 3 UCSD Big Data Specialization course hours (Course 1: 6h→18h, Course 2: 8h→15h, Course 4: 10h→20h) after Coursera quiz cross-reference. Updated section totals (Course 1: 24h→36h, Course 12: 134h→141h, Course 13: 58h→68h) and master total 910h→939h. No new resources added.

---

## How to read the tables

> 💡 **Practitioner tip (IBM Data Engineering Viewpoints):** Before any tool or technology, ask yourself whether you genuinely love working with data. Practitioners are unanimous: indifference to the subject matter is not sustainable in a field this detailed and fast-moving. Passion for data is what carries you through the complexity.

- **Free** = no cost at all. **Free-audit** = free if you skip the graded certificate. **Paid** = flagged only when no adequate free substitute exists.
- Hours are realistic *active* study/lab hours, not video runtime.
- Resource order within each supplement table = recommended order, not interchangeable alternatives (unless marked "OR").
- Links were verified at the time this plan was written; if a link breaks, search the resource name directly.

---

## Career Ladder at a Glance

> Source: Sumit Gupta's "Data Engineering" infographic (2025)

| Level | Core Skills | This Plan's Coverage |
|---|---|---|
| **Beginner** | SQL, Python, Linux, Databases | Courses 1–7 |
| **Junior** | ETL/ELT, Data Warehousing, APIs, Git, Scheduling | Courses 8–9 |
| **Mid-Level** | Airflow, dbt, Spark/Kafka, Cloud Storage, Data Modeling | Courses 8, 12 + Enhancement C |
| **Senior** | Distributed Systems, Cloud Architecture, Streaming, Governance, Optimization | Courses 11–12 + Enhancements A–B |
| **Modern AI-Ready** | Vector DBs, RAG Pipelines, Feature Stores, LLM Data Workflows, Data Quality | Course 15 |

---

## 🚀 Minimum Viable Path (MVP) — ~200h Fast-Track

> **Who this is for:** Career-switchers, bootcamp graduates, or anyone who wants to land a junior DE role without committing to the full 750h plan upfront. This is a curated subset — not a shortcut, but a focused entry point.
>
> **Rule:** Follow the IBM courses below in order. Skip all supplements except the ones marked ⭐ (highest ROI). After landing your first role, return to the full plan to fill gaps.

### MVP Course Sequence

| # | Course | IBM Hours | ⭐ One Must-Do Supplement | Supplement Hours | MVP Total |
|---|---|---|---|---|---|
| 1 | Introduction to Data Engineering | 14h | AWS "What Is Big Data?" explainer | 1h | ~15h |
| 2 | Python for Data Science, AI & Development | 24h | Real Python free tutorials (file I/O, requests, pandas) | 4h | ~28h |
| 3 | Python Project for Data Engineering | 10h | *(self-contained — no supplement needed)* | — | ~10h |
| 4 | Introduction to Relational Databases | 16h | PostgreSQL official tutorial (install + DDL/DML practice) | 2h | ~18h |
| 5 | Databases and SQL for Data Science with Python | 18h | Mode SQL Tutorial (Basic + Intermediate tracks only) | 4h | ~22h |
| 6 | Linux Commands and Shell Scripting | 17h | Linux Journey (command line + permissions modules) | 2h | ~19h |
| 8 | ETL and Data Pipelines with Shell, Airflow and Kafka | 18h | Confluent Developer "Kafka 101" (first 4 modules) | 3h | ~21h |
| 9 | Getting Started with Data Warehousing and BI Analytics | 10h | dbt Learn "Fundamentals" course | 5h | ~15h |
| 12 | Introduction to Big Data with Spark and Hadoop | 20h | freeCodeCamp PySpark Tutorial (YouTube) | 6h | ~26h |
| 14 | Data Engineering Capstone Project | 18h | *(build your own end-to-end project — see project list)* | — | ~18h |

**MVP Total: ~192h** (IBM: ~165h + supplements: ~27h)

### What the MVP covers and omits

| ✅ Covered in MVP | ❌ Skipped (return to full plan later) |
|---|---|
| Python scripting for data tasks | DBA & security depth (Courses 7, Enhancement B) |
| SQL — querying, joins, views, stored procedures | NoSQL databases (Course 11) |
| Linux, Bash, cron scheduling | Machine learning with Spark (Course 13) |
| ETL pipelines with Airflow + Kafka basics | GenAI / RAG pipelines (Course 15) |
| Core data warehousing concepts + dbt intro | Hive/Impala/Pig (Enhancement A) |
| Hadoop + Spark fundamentals | Data governance (Ranger/Atlas) |
| End-to-end capstone project | Advanced dbt, data contracts (Enhancement C) |

### After the MVP: what to do next

1. **Apply for jobs now.** Junior DE roles typically require exactly these skills.
2. **Return to Courses 7, 10, 11, 13** — prioritize based on the job description you're targeting.
3. **Add Course 15 (GenAI)** if your target company uses LLM-driven data pipelines.
4. **Work through the Enhancements** once you're on the job and have context for why they matter.

> **Note:** Courses 7 (DBA), 10 (BI), 11 (NoSQL), 13 (ML), 15 (GenAI), and 16 (Career) are skipped in the MVP because they either deepen existing skills (7, 10), are specializations (11, 13, 15), or are better done with real-world context (16). Course 16's mock interviews can be done in parallel with job applications at any point.

---

## ── IBM DATA ENGINEERING PROFESSIONAL CERTIFICATE ──────────────

> 🎓 **[IBM Data Engineering Professional Certificate](https://www.coursera.org/professional-certificates/ibm-data-engineer)** — 16 courses · ~262h · Beginner level · IBM Skills Network Team, Romeo Kienzler, Joseph Santarcangelo
>
> The IBM track is the **primary spine** of this plan. Every course below is followed by supplementary free resources that reinforce or extend the IBM material. Complete the IBM course first, then work through supplements based on your confidence level.

---

## IBM Track — Course 1: Introduction to Data Engineering (~36h total)

> 🎓 **Primary:** [Introduction to Data Engineering](https://www.coursera.org/learn/introduction-to-data-engineering) — DE lifecycle, data repositories, data pipelines, Big Data engines, data security, governance, and compliance | ~14h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Coursera — "Introduction to Big Data" (UCSD, Big Data Specialization, Course 1)](https://www.coursera.org/learn/big-data-introduction) | MOOC, audit mode | 18 | Free-audit |
| [AWS — "What Is Big Data?"](https://aws.amazon.com/what-is/big-data/) explainer page | Official docs | 1 | Free |
| [Martin Kleppmann's site](https://martin.kleppmann.com/) — free blog posts/talks related to *Designing Data-Intensive Applications* (concepts only) | Free blog/author site | 1 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [GitHub — AlessandroCorradini/University-of-California-San-Diego-Big-Data-Specialization](https://github.com/AlessandroCorradini/University-of-California-San-Diego-Big-Data-Specialization) — use to cross-check your own work | Repo/reference | 1 | Free |
| [Google Cloud — "What Is Edge Computing?"](https://cloud.google.com/learn/what-is-edge-computing) overview | Official docs | 1 | Free |

**Combined total: ~36h | IBM: 14h | Tier 1 supplements: 20h | Tier 2 supplements: 2h**

> 💡 **Practitioner tip (IBM Data Engineering Viewpoints):** Focus on the theory beneath the tools. How data is structured, how it flows, and how storage and retrieval trade-offs work remain stable even as frameworks come and go. Engineers who understand the fundamentals can learn any new tool quickly; engineers who only know specific tools are stranded when those tools are replaced.

### 💼 Portfolio Project Ideas (Course 1)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| DE Landscape Reference Map | 🟢 Beginner | Markdown / GitHub Pages | Demonstrates ability to synthesize the data engineering ecosystem into a structured reference document, mapping tools to pipeline stages. |
| Data Pipeline Architecture Diagram | 🟢 Beginner | draw.io / Mermaid (GitHub-rendered) | Demonstrates ability to design and communicate a conceptual end-to-end data pipeline covering ingestion, storage, transformation, and serving layers. |
| Big Data Use-Case Analysis Report | 🟡 Intermediate | Markdown / Jupyter Notebook | Demonstrates ability to evaluate real-world datasets for Big Data characteristics (volume, velocity, variety) and recommend appropriate architectural patterns. |

---

## IBM Track — Course 2: Python for Data Science, AI & Development (~39h total)

> 🎓 **Primary:** [Python for Data Science, AI & Development](https://www.coursera.org/learn/python-for-applied-data-science-ai) — Python syntax, data types, data structures, pandas, NumPy, REST APIs, web scraping with BeautifulSoup | ~24h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [freeCodeCamp — "Python for Everybody" (full course, YouTube)](https://www.youtube.com/watch?v=8DvywoWv6fI) | YouTube | 8 | Free |
| [Real Python — "Python for Data Engineering" tutorials](https://realpython.com/) (free articles: file I/O, requests, pandas basics) | Free articles | 4 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Mahmoud Mohsen — Python series (playlist vids 9–13)](https://www.youtube.com/playlist?list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI) — tightly scoped to data-oriented Python; use alongside or instead of the freeCodeCamp course above if you want a shorter path focused on NumPy/pandas: [#9 Basics 1](https://www.youtube.com/watch?v=joztCLdwdnQ&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=9) · [#10 Basics 2](https://www.youtube.com/watch?v=Erpsy8RJ9ms&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=10) · [#11 NumPy](https://www.youtube.com/watch?v=gcVHEjSBB8I&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=11) · [#12 Pandas 1](https://www.youtube.com/watch?v=TFo7ZkFIPCA&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=12) · [#13 Pandas 2](https://www.youtube.com/watch?v=neh_0SiPuJI&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=13) | YouTube series | 3 | Free |
| [بالعربي Big Data — Python Foundations](https://www.youtube.com/@bigdata4756) — full beginner-to-intermediate Python series in Arabic; two long-form sessions covering syntax, data structures, NumPy, pandas, and data analysis workflows: [Python - The Basics - Part 1 / جحر السوعبان](https://www.youtube.com/@bigdata4756) (~6h) · [Python - The Basics - Part 2 / السوعبان صديقي](https://www.youtube.com/watch?v=mlbe7Vxr7yA) (~2h36min) — watch alongside or instead of the freeCodeCamp course for a focused Arabic-language path | YouTube series (Arabic) | 10.5h | Free |

**Combined total: ~39h | IBM: 24h | Tier 1 supplements: 12h | Tier 2 supplements: 13.5h**

> 💡 **Practitioner tip (Jupyter best practices):** Use markdown cells liberally to document your reasoning — a notebook should tell a story, not just show code. Keep each code cell focused on a single logical step. Restart the kernel and run all cells periodically to verify your notebook runs end-to-end before sharing. Track notebook files with git from day one.

### 💼 Portfolio Project Ideas (Course 2)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| Public REST API Collector | 🟢 Beginner | Python, requests, pandas, CSV/JSON | Demonstrates ability to extract data from a public REST API, normalize nested JSON responses, and write structured output to disk. |
| Wikipedia Table Scraper & Cleaner | 🟡 Intermediate | Python, BeautifulSoup, pandas, GitHub | Demonstrates ability to scrape tabular data from HTML pages, handle encoding edge cases, and produce a clean, analysis-ready dataset. |
| Multi-Source Data Aggregator | 🟡 Intermediate | Python, pandas, NumPy, Jupyter Notebook | Demonstrates ability to ingest, merge, and summarize data from multiple public sources (CSV + API) into a single analytical output with descriptive statistics. |

---

## IBM Track — Course 3: Python Project for Data Engineering (~10h total)

> 🎓 **Primary:** [Python Project for Data Engineering](https://www.coursera.org/learn/python-project-for-data-engineering) — hands-on ETL project: webscraping + API extraction + data transformation using Python and Jupyter | ~10h | Free-audit

> No additional supplements needed — IBM course is self-contained for this topic.

> ⚡ *All resources in this section are Tier 1 — essential.*

**Combined total: ~10h | IBM: 10h | Tier 1 supplements: 0h | Tier 2 supplements: 0h**

### 💼 Portfolio Project Ideas (Course 3)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| Country GDP ETL Pipeline | 🟢 Beginner | Python, BeautifulSoup, pandas, SQLite | Demonstrates ability to build a complete extract-transform-load pipeline that scrapes a public data source, applies transformations, and persists results to a local database. |

---

## IBM Track — Course 4: Introduction to Relational Databases (~21h total)

> 🎓 **Primary:** [Introduction to Relational Databases (RDBMS)](https://www.coursera.org/learn/introduction-to-relational-databases) — data models, ER diagrams, relational schemas, MySQL, PostgreSQL, IBM DB2 | ~16h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [PostgreSQL — official tutorial](https://www.postgresql.org/docs/current/tutorial.html) — install locally, practice DDL/DML | Official docs | 2 | Free |
| [SQLZoo](https://sqlzoo.net/) — hands-on SQL exercises in the browser | Free interactive | 3 | Free |

**Combined total: ~21h | IBM: 16h | Tier 1 supplements: 5h | Tier 2 supplements: 0h**

> ⚡ *All resources in this section are Tier 1 — essential.*

### 💼 Portfolio Project Ideas (Course 4)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| Normalized E-Commerce Schema | 🟢 Beginner | PostgreSQL, DDL SQL, ER diagram (draw.io) | Demonstrates ability to design a fully normalized relational schema with primary keys, foreign keys, and indexes for a realistic business domain. |
| Library Management System DB | 🟡 Intermediate | PostgreSQL, stored procedures, views | Demonstrates ability to implement referential integrity constraints, multi-table views, and stored procedures that enforce business logic at the database layer. |
| Schema Migration Script Suite | 🟡 Intermediate | PostgreSQL, Bash, SQL migration scripts | Demonstrates ability to version-control database schemas and produce repeatable, idempotent migration scripts suitable for CI/CD pipelines. |

---

## IBM Track — Course 5: Databases and SQL for Data Science with Python (~37h total)

> 🎓 **Primary:** [Databases and SQL for Data Science with Python](https://www.coursera.org/learn/sql-data-science) — SQL DDL/DML, joins, views, stored procedures, transactions, Jupyter integration | ~18h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Mode — free interactive SQL tutorial](https://mode.com/sql-tutorial/) (Basic, Intermediate, Advanced tracks — all free) — also useful as a refresher before distributed SQL engines later in the track | Free interactive | 6 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [بالعربي Big Data — SQL for Data Analysis](https://www.youtube.com/@bigdata4756) — 10h 20min Arabic-language end-to-end SQL course: "شاهد كيف أصبح الفيل والدرفيل أصدقاء" — covers SQL foundations through analytical queries. **Use this OR Mode above — not both.** Pick Mode if you prefer English + interactive exercises; pick this if you prefer a video-based Arabic walkthrough. | YouTube series (Arabic) — OR Mode above | 13h | Free |

**Combined total: ~37h | IBM: 18h | Tier 1 supplements: 6h | Tier 2 supplements: 13h**

> 💡 **Practitioner tip (IBM Data Engineering Viewpoints):** SQL is the single most universally cited technical skill across every DE specialization and industry. It is not just a query language — it is how you interact with, validate, and manipulate data at every stage of the pipeline. Invest deeply here; no other skill pays off as consistently.

### 💼 Portfolio Project Ideas (Course 5)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| SQL Analytics Notebook — Chicago Crime Data | 🟢 Beginner | Python, ibm_db / psycopg2, Jupyter Notebook | Demonstrates ability to query a public dataset with complex joins, window functions, and aggregations, then present findings in a reproducible Jupyter notebook. |
| Stored Procedure ETL Layer | 🟡 Intermediate | PostgreSQL, SQL, Python | Demonstrates ability to encapsulate multi-step data transformation logic in stored procedures and invoke them programmatically from a Python pipeline. |
| SQL Query Performance Benchmarker | 🔴 Advanced | PostgreSQL, EXPLAIN ANALYZE, Python, pandas | Demonstrates ability to profile and optimize SQL queries using execution plans, index strategies, and rewriting techniques — and document improvements with before/after benchmarks. |

---

## IBM Track — Course 6: Hands-on Introduction to Linux Commands and Shell Scripting (~24h total)

> 🎓 **Primary:** [Hands-on Introduction to Linux Commands and Shell Scripting](https://www.coursera.org/learn/hands-on-introduction-to-linux-commands-and-shell-scripting) — Linux architecture, Bash shell, file management, scripting, cron jobs, networking | ~17h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Linux Journey](https://linuxjourney.com/) — interactive Linux fundamentals (command line, permissions, scripting) | Free interactive | 4 | Free |
| [Docker — "Get Started" official tutorial](https://docs.docker.com/get-started/) (Parts 1–5: containers, images, volumes, networking) + [Docker Compose overview](https://docs.docker.com/compose/) — **do this now, not later**: Airflow (Course 8), Kafka, and Spark all run via Docker Compose in practice. Installing it here means you arrive at those courses ready to run real environments. ~4h total. | Official docs + hands-on | 4 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [GitHub — "Introduction to Git and GitHub" (Google, via Coursera, audit mode)](https://www.coursera.org/learn/introduction-git-github) | MOOC, audit mode | 3 | Free-audit |
| [بالعربي Big Data — Linux, Git & Dev Tools](https://www.youtube.com/@bigdata4756) — three deep-dive Arabic-language series directly supporting this course: [Linux for Data Engineers / البطريق العضاض يعظ](https://www.youtube.com/@bigdata4756) (11h 25min) · [Git and GitHub / شخبط وانت متطمن](https://www.youtube.com/@bigdata4756) (~6h) · [Visual Studio Code / هنشخبط الكود على إيه؟](https://www.youtube.com/watch?v=DsJOSKyxqMc) (~57min) — use Linux series alongside Course 6, Git series alongside the Google Git course, VS Code as a one-session setup walkthrough | YouTube series (Arabic) | 23h | Free |

**Combined total: ~24h | IBM: 17h | Tier 1 supplements: 8h | Tier 2 supplements: 26h**

> 💡 **Practitioner tip (IBM Data Engineering Viewpoints):** Automation is one of the most valuable skills in today's DE landscape. Modern data teams run on fast turnaround expectations — scripting repetitive tasks, building CI/CD pipelines for data workflows, and managing infrastructure as code are what separate a productive DE from one who is constantly firefighting.

### 💼 Portfolio Project Ideas (Course 6)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| Automated Data Backup Script | 🟢 Beginner | Bash, cron, Linux | Demonstrates ability to write production-grade shell scripts with error handling, logging, and scheduled execution via cron for automated data operations. |
| Dockerized ETL Environment | 🟡 Intermediate | Docker, Docker Compose, Bash, Python | Demonstrates ability to containerize a Python ETL script with all dependencies, orchestrated via Docker Compose, ensuring reproducible execution across environments. |
| Git-Versioned Pipeline Repository | 🟡 Intermediate | Git, GitHub, Bash, Python | Demonstrates ability to manage a data pipeline project with proper branching strategy, commit conventions, and a CI-ready repository structure. |

---

## IBM Track — Course 7: Relational Database Administration (~28h total)

> 🎓 **Primary:** [Relational Database Administration (DBA)](https://www.coursera.org/learn/relational-database-administration) — backup/restore, user roles & permissions, performance monitoring, troubleshooting, automation | ~21h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [MIT Kerberos — official documentation](https://web.mit.edu/kerberos/) — concepts and protocol overview | Official docs | 4 | Free |
| [Cloudera documentation hub](https://docs.cloudera.com/) — security architecture concepts | Free vendor docs | 3 | Free |

**Combined total: ~28h | IBM: 21h | Tier 1 supplements: 7h | Tier 2 supplements: 0h**

> ⚡ *All resources in this section are Tier 1 — essential.*

> 💡 **Practitioner tip (Performance troubleshooting):** When diagnosing pipeline or query issues, follow a pattern-based approach: slow queries almost always trace to missing indexes or inefficient joins — check the query plan first. Pipeline failures during ingestion are usually schema drift or data quality issues at the source. Memory errors point to insufficient resources or data skew. For data inconsistencies, implement idempotent writes and checkpointing. These diagnostic patterns apply across databases, warehouses, and streaming systems alike.

> ### 🎯 Self-Assessment Gate — Foundations (after Course 7)
> Before moving to Course 8, you should be able to:
> - [ ] Write a Python script that reads a CSV, transforms it, and loads it into a PostgreSQL table
> - [ ] Explain the difference between a primary key, foreign key, and index — and create all three in SQL
> - [ ] Write a Bash script with a loop, conditional, and cron-scheduled run
> - [ ] Explain what a database transaction is and what ACID means
> - [ ] Run `docker ps`, `docker run`, `docker-compose up` without looking them up
>
> If you can't do all five confidently, revisit the supplement resources before continuing. Courses 8+ assume this foundation.

### 💼 Portfolio Project Ideas (Course 7)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| PostgreSQL Backup & Recovery Runbook | 🟢 Beginner | PostgreSQL, Bash, pg_dump / pg_restore | Demonstrates ability to design and execute a backup/restore strategy with documented recovery procedures and automated scheduling. |
| Role-Based Access Control Implementation | 🟡 Intermediate | PostgreSQL, SQL (GRANT/REVOKE), documentation | Demonstrates ability to implement least-privilege RBAC for a multi-user database environment, with an auditable permissions matrix. |
| Performance Monitoring Dashboard Script | 🔴 Advanced | PostgreSQL, Python, psycopg2, pg_stat_* views | Demonstrates ability to query PostgreSQL system catalogs, identify slow queries and lock contention, and produce a diagnostic report — a core DBA skill in production environments. |

---

## IBM Track — Course 8: ETL and Data Pipelines with Shell, Airflow and Kafka (~71h total)

> 🎓 **Primary:** [ETL and Data Pipelines with Shell, Airflow and Kafka](https://www.coursera.org/learn/etl-and-data-pipelines-shell-airflow-kafka) — ETL vs ELT patterns, batch vs concurrent execution, Bash/Python ETL workflows, Apache Airflow DAGs, Apache Kafka streaming pipelines, data pipeline components | ~18h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

*Ingestion & streaming tools (extend the Kafka/Airflow foundation):*

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Confluent Developer — "Kafka 101" course hub](https://developer.confluent.io/courses/apache-kafka/events/) | Official vendor course | 8 | Free |
| [Apache Airflow — official documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html) — Core Concepts, Tutorial, DAG authoring guides | Official docs | 6 | Free |
| [Confluent — Schema Registry documentation](https://docs.confluent.io/platform/current/schema-registry/index.html) + [Apache Avro specification](https://avro.apache.org/docs/) — **essential for production Kafka work**: without schema enforcement, consumers break silently when producers change message format. Read the Schema Registry "Getting Started" guide + the Avro spec overview (~2h); then the [Confluent "Schema Registry" free course](https://developer.confluent.io/courses/schema-registry/key-concepts/) (~1h). | Official docs + vendor course | 3 | Free |

> 💡 **Practitioner tip (IBM Data Engineering Viewpoints):** Design every ETL transformation to be idempotent, testable, and maintainable from the first iteration — not as a refactor later. A pipeline that produces the same result on repeated runs and can be unit-tested in isolation will save you far more time in production than any performance optimization.

| **Project checkpoint:** Build a NiFi or Kafka pipeline that ingests a public streaming dataset into a topic, then consume and write to local/S3-compatible storage | Hands-on project | 2 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Coursera — "Process Real-Time Data with Spark Streams"](https://www.coursera.org/learn/process-real-time-data-with-spark-streams) — Spark Structured Streaming with Kafka integration, event-time watermarks, Delta Lake sinks, end-to-end pipeline deployment | MOOC, audit mode | 8 | Free |
| [DataTalks.Club — Data Engineering Zoomcamp (GitHub repo), Module 2: Workflow Orchestration with Airflow](https://github.com/DataTalksClub/data-engineering-zoomcamp) | Free course module | 6 | Free |
| [Astronomer — "Intro to Apache Airflow" free course](https://academy.astronomer.io/astronomer-certification-apache-airflow-fundamentals-preparation) | Official vendor course | 4 | Free |
| [freeCodeCamp — "Data Loading with Python and AI" (YouTube)](https://www.youtube.com/watch?v=T23Bs75F7ZQ) — dlt-based declarative Python ingestion: @dlt.resource, @dlt.source, REST pagination, incremental loading, schema inference, write dispositions, deployment to Airflow/Dagster/GitHub Actions; co-created by dlt founder Adrian Brudaru and DataTalks.Club's Alexey Grigorev | YouTube | 4 | Free |
| [Coursera — "Getting Started with Terraform for Google Cloud"](https://www.coursera.org/learn/getting-started-with-terraform-for-google-cloud) — HCL syntax, GCP provider, GCS buckets, BigQuery datasets, variables, modules; Google Cloud–authored | MOOC, audit mode | 5 | Free |
| [RisingWave — official tutorials](https://risingwave.com/learn/) + [DE Zoomcamp 2025 RisingWave workshop](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/cohorts/2025/workshops) — SQL-native stream processing: CREATE SOURCE over Kafka, CREATE MATERIALIZED VIEW for real-time aggregations, stream-stream joins, deduplication via standard PostgreSQL-compatible SQL | Official docs + workshop | 3 | Free |
| [DataTalks.Club — Data Engineering Zoomcamp (GitHub repo, Module 6: Streaming with Kafka)](https://github.com/DataTalksClub/data-engineering-zoomcamp) | Free course module | 6 | Free |
| [Apache NiFi — documentation hub](https://nifi.apache.org/documentation.html) + in-app templates | Official docs | 4 | Free |
| [Apache Flume — User Guide](https://flume.apache.org/FlumeUserGuide.html) | Official docs | 2 | Free |
| [Apache Sqoop — User Guide](https://sqoop.apache.org/docs/1.4.7/SqoopUserGuide.html) | Official docs | 2 | Free |
| [Apache Flink — official documentation](https://nightlies.apache.org/flink/flink-docs-stable/) (DataStream API / Getting Started) — supplement the Spark Streaming course above with Flink's alternative stream-processing model; focus on PyFlink Table API for portability | Official docs | 4 | Free |
| [Spark — Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html) — reference companion to the Coursera course above | Official docs | 2 | Free |
| **Project checkpoint:** Build an Airflow DAG + dbt project: ingest NYC Taxi or a public REST API → raw layer in Postgres/BigQuery → dbt transformations → dbt tests → a final analytical model. Version-control everything in GitHub. | Hands-on project | 4 | Free |

> **Tool choice note:** Airflow is the industry standard for orchestration. Alternatives (Prefect, Dagster, Mage, Kestra) are worth knowing exist — [Prefect documentation](https://docs.prefect.io/), [Dagster documentation](https://docs.dagster.io/), and [Kestra Academy](https://academy.kestra.io/) are all free. Kestra's YAML-first declarative paradigm is a fundamentally different approach from Python-DAG frameworks; see Enhancement C for a dedicated Kestra orientation. Do not split time across all of them during your first pass.

**Combined total: ~91h | IBM: 18h | Tier 1 supplements: 19h | Tier 2 supplements: 54h**

### 💼 Portfolio Project Ideas (Course 8)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| Airflow-Orchestrated Batch ETL | 🟡 Intermediate | Python, Apache Airflow, PostgreSQL, Docker Compose | Demonstrates ability to design and deploy a multi-task Airflow DAG with retry logic, dependency management, and scheduled batch ingestion from a public API into a relational database. |
| Real-Time Kafka Streaming Pipeline | 🟡 Intermediate | Apache Kafka, Python (confluent-kafka), Avro, Schema Registry | Demonstrates ability to build a producer-consumer streaming pipeline with Avro-serialized messages and Schema Registry enforcement, simulating a real-time data feed. |
| End-to-End ELT Pipeline with dbt | 🔴 Advanced | Airflow, dbt, PostgreSQL / BigQuery, GitHub Actions | Demonstrates ability to implement a full ELT workflow where Airflow orchestrates ingestion and dbt handles all transformation logic, tests, and documentation in a version-controlled repo. |

---

## IBM Track — Course 9: Data Warehouse Fundamentals (~46h total)

> 🎓 **Primary:** [Data Warehouse Fundamentals](https://www.coursera.org/learn/data-warehouse-fundamentals) — data warehouse design and population, CUBE/ROLLUP/materialized views, star & snowflake schemas, IBM Cognos Analytics dashboards | ~16h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

*Platform Decision Framework — pick one cloud + one data platform and go deep before diversifying:*

| Platform | Best When | Free Learning Path |
|---|---|---|
| **AWS** | Broadest ecosystem, S3 data lakes, max market demand | [AWS Skill Builder free tier](https://skillbuilder.aws/) + [freeCodeCamp AWS YouTube](https://www.youtube.com/@freecodecamp) |
| **Azure** | Enterprise/Microsoft ecosystem, Power BI integration, AD auth | [Microsoft Learn — free paths](https://learn.microsoft.com/en-us/training/) |
| **GCP** | Strong analytics + ML (BigQuery, Vertex AI) | [Google Cloud Skills Boost free credits](https://www.cloudskillsboost.google/) |
| **Databricks** | Spark-heavy roles, unified lakehouse, Delta Lake | [Databricks Community Edition](https://community.cloud.databricks.com/) + [Databricks Academy free](https://www.databricks.com/learn/training/home) |
| **Snowflake** | Data warehousing, data sharing, high-performance SQL | [Snowflake free trial + Hands-On Essentials](https://www.snowflake.com/en/data-cloud/overview/hands-on-essentials/) |

> **Starter recommendation:** If you want big-tech/startup jobs → **AWS + Databricks**. Enterprise targets → **Azure + Snowflake**. Analytics/ML-heavy → **GCP + BigQuery**. Pick one cloud + one data platform and go deep before diversifying.

*Data warehousing & cloud platform deep dives:*

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [dbt Learn — "Dimensional Modeling" free course](https://courses.getdbt.com/courses/dimensional-modeling) — **fills a genuine gap**: IBM Course 9 covers star/snowflake schemas briefly, but this course goes deep on Kimball methodology, slowly changing dimensions (SCD Type 1/2/3), fact vs dimension table design, and surrogate keys. Essential for DE interviews. ~3h. | Official vendor course | 3 | Free |
| [DataTalks.Club — Data Engineering Zoomcamp, Data Warehousing & Analytics Engineering modules](https://github.com/DataTalksClub/data-engineering-zoomcamp) | Free course module | 8 | Free |
| [Google Cloud Skills Boost — "BigQuery for Data Analysts" learning path](https://www.cloudskillsboost.google/paths/402) — **add this regardless of your cloud preference**: BigQuery's SQL dialect, partitioning, clustering, and job-based pricing model are common interview topics and appear in many public DE project walkthroughs. Free credits cover the labs. | Official vendor course | 5 | Free (with free credits) |
| [Coursera — "Google BigQuery for Data and ML Engineers" (Pearson)](https://www.coursera.org/learn/pearson-google-bigquery-for-data-and-ml-engineers-video-course-rbgah) — BigQuery architecture, partitioning/clustering cost optimization, CREATE MODEL/ML.EVALUATE/ML.PREDICT, generative AI integration; by Dan Sullivan, Google Cloud certified architect | MOOC, audit mode | 8 | Free-audit |
| **Project checkpoint:** Pick one platform (Snowflake or BigQuery). Ingest the dataset from your Course 8 dbt project into it; write and optimize 5 analytical queries; document your platform choice rationale vs the alternatives in a short README. | Hands-on project | 3 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Snowflake — "Hands-On Essentials: Data Warehouse" (free badge course)](https://www.snowflake.com/en/data-cloud/overview/hands-on-essentials/) | Official vendor course | 5 | Free |
| [Databricks — "Lakehouse Fundamentals" free learning path](https://www.databricks.com/learn/training/lakehouse-fundamentals) + Community Edition labs | Official vendor course | 5 | Free |
| [AWS Skill Builder — "Data Engineering on AWS" free modules](https://skillbuilder.aws/) | Official vendor course | 4 | Free |
| [Kimball Group — free design tips archive](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/) — reference companion to the dbt course above; classic design patterns (conformed dimensions, junk dimensions, degenerate dimensions) | Free reference | 2 | Free |

**Combined total: ~51h | IBM: 16h | Tier 1 supplements: 19h | Tier 2 supplements: 16h**

> ### 🎯 Self-Assessment Gate — Core DE (after Course 9)
> Before moving to Course 10, you should be able to:
> - [ ] Explain the difference between a star schema and a snowflake schema — and when you'd choose each
> - [ ] Describe what a slowly changing dimension (SCD Type 2) is and implement one in SQL
> - [ ] Write an Airflow DAG that runs on a schedule, handles failures with retries, and sends an alert on error
> - [ ] Explain what a Kafka consumer group is and why it matters for parallelism
> - [ ] Produce and consume Avro-serialized messages using Confluent Schema Registry
>
> If you can't do all five, revisit the relevant supplement sections before continuing.

### 💼 Portfolio Project Ideas (Course 9)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| Star Schema Data Warehouse (BigQuery) | 🟡 Intermediate | BigQuery, dbt, SQL, Kimball modeling | Demonstrates ability to design and populate a star-schema data warehouse with fact and dimension tables, implementing SCD Type 2 for a slowly changing dimension. |
| Snowflake Analytics Layer | 🟡 Intermediate | Snowflake, SQL, dbt, GitHub | Demonstrates ability to provision a Snowflake environment, load raw data, and build a documented, tested dbt transformation layer with at least one materialized view. |
| Cross-Platform DW Benchmark | 🔴 Advanced | BigQuery + Snowflake, Python, dbt | Demonstrates ability to deploy the same dimensional model across two cloud warehouses, benchmark query performance, and produce a documented cost/performance comparison. |

---

## IBM Track — Course 10: BI Dashboards with IBM Cognos Analytics and Google Looker (~28h total)

> 🎓 **Primary:** [BI Dashboards with IBM Cognos Analytics and Google Looker](https://www.coursera.org/learn/bi-dashboards-with-ibm-cognos-analytics-and-google-looker) — IBM Cognos Analytics, Google Looker Studio, interactive dashboards, data visualization best practices | ~12h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Microsoft Learn — "Get started with Power BI" learning path](https://learn.microsoft.com/en-us/training/powerplatform/power-bi) | Official vendor course | 6 | Free |
| [Mahmoud Mohsen — #19 Data Visualization and Case Studies](https://www.youtube.com/watch?v=Lo2Byt-V_jQ&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=19) — works through end-to-end case studies tying visualization back to the Big Data pipeline; watch before building the project checkpoint below | YouTube | 1 | Free |
| **Project checkpoint:** Build one Jupyter-notebook visualization report and one Power BI dashboard summarizing Course 13 ML results | Hands-on project | 1 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Jupyter — official documentation](https://docs.jupyter.org/en/latest/) | Official docs | 3 | Free |
| [Guy in a Cube (YouTube channel)](https://www.youtube.com/@GuyInACube) — Power BI tips/tutorials | YouTube channel | 3 | Free |
| [Apache Hue — official site/live demo](https://gethue.com/) | Official docs/live demo | 2 | Free |

**Combined total: ~28h | IBM: 12h | Tier 1 supplements: 8h | Tier 2 supplements: 8h**

### 💼 Portfolio Project Ideas (Course 10)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| Google Looker Studio Public Dataset Dashboard | 🟢 Beginner | Google Looker Studio, BigQuery (free tier) | Demonstrates ability to connect a cloud data source to a BI tool and build an interactive, shareable dashboard with filters, drill-downs, and clear data storytelling. |
| Power BI Report from PostgreSQL | 🟡 Intermediate | Power BI Desktop, PostgreSQL, DAX | Demonstrates ability to model relationships in Power BI, author DAX measures, and publish a report that communicates pipeline output to a non-technical audience. |
| Automated Jupyter Report with nbconvert | 🟡 Intermediate | Python, Jupyter Notebook, matplotlib / plotly, Airflow | Demonstrates ability to schedule and auto-export a parameterized Jupyter notebook as an HTML report via an Airflow DAG — a common lightweight reporting pattern in DE teams. |

---

## IBM Track — Course 11: Introduction to NoSQL Databases (~50h total)

> 🎓 **Primary:** [Introduction to NoSQL Databases](https://www.coursera.org/learn/introduction-to-nosql-databases) — four NoSQL categories, MongoDB CRUD, Cassandra keyspace/table operations, IBM Cloudant | ~18h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Mahmoud Mohsen — MongoDB series (playlist vids 4–7)](https://www.youtube.com/playlist?list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI) — watch before the MongoDB University course as a quick conceptual primer: [#4 MongoDB vs RDBMS](https://www.youtube.com/watch?v=8CJbtQd8qRg&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=4) (17 min) · [#5 Operations 1](https://www.youtube.com/watch?v=uk08KAZaE2k&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=5) (31 min) · [#6 Operations 2](https://www.youtube.com/watch?v=2bhJkI6oW9I&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=6) (34 min) · [#7 MapReduce & Relations](https://www.youtube.com/watch?v=TcjxLAXodyU&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=7) (34 min) | YouTube series | 2 | Free |
| [MongoDB University — M001 "MongoDB Basics"](https://learn.mongodb.com/) | Official vendor course | 8 | Free |
| **Project checkpoint:** Model the same dataset in Cassandra, MongoDB, and HBase; compare query performance/design tradeoffs in a short writeup | Hands-on project | 6 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [DataStax Academy](https://academy.datastax.com/) + [Apache Cassandra — official documentation](https://cassandra.apache.org/doc/latest/) | Official vendor course + docs | 8 | Free |
| [Apache HBase — Reference Guide](https://hbase.apache.org/book.html) — schema design, region servers | Official docs | 6 | Free |
| [AWS — Amazon S3 documentation](https://aws.amazon.com/s3/) | Official docs | 2 | Free |

> 💡 **Wiki integration — How column-oriented storage works (and why it matters):** Cassandra and HBase are *column-oriented* databases, meaning they store data one column at a time on disk rather than one row at a time. In a row-oriented DB (PostgreSQL), a single disk read fetches all columns for a set of rows — ideal for OLTP (many columns, few rows). In a column-oriented DB, a disk read fetches one column's values across many rows — ideal for analytical queries that scan large ranges but access few columns. For Cassandra specifically: each partition key maps to a row, and within that row, column names are sorted. This design makes Cassandra excel at high-write, time-series workloads where queries always include the partition key. Understanding this storage layout difference is essential for schema design — creating a good Cassandra model requires thinking backward from your query patterns to your partition key strategy.

**Combined total: ~50h | IBM: 18h | Tier 1 supplements: 16h | Tier 2 supplements: 16h**

### 💼 Portfolio Project Ideas (Course 11)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| MongoDB Product Catalog API | 🟡 Intermediate | Python, pymongo, MongoDB (Docker), FastAPI | Demonstrates ability to design a document-oriented schema for hierarchical product data and expose it via a REST API, highlighting the tradeoffs vs a relational model. |
| Cassandra Time-Series Event Store | 🟡 Intermediate | Apache Cassandra (Docker), Python, cassandra-driver | Demonstrates ability to model high-write time-series data in Cassandra with an appropriate partition key strategy and benchmark write/read throughput. |
| Multi-Store Data Access Layer | 🔴 Advanced | Python, MongoDB, Cassandra, PostgreSQL, Docker Compose | Demonstrates ability to architect a polyglot persistence layer that routes reads and writes to the appropriate store based on access pattern — a common senior DE design decision. |

---

## IBM Track — Course 12: Introduction to Big Data with Spark and Hadoop (~119h total)

> 🎓 **Primary:** [Introduction to Big Data with Spark and Hadoop](https://www.coursera.org/learn/introduction-to-big-data-with-spark-hadoop) — Hadoop architecture, HDFS, Hive, HBase, Spark fundamentals, RDDs, DataFrames, SparkSQL, Docker/Kubernetes deployment | ~20h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

*Big Data concepts & theory:*

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Mahmoud Mohsen — Big Data concepts series (playlist vids 1–3)](https://www.youtube.com/playlist?list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI) — Arabic-language lectures with clear diagrams; excellent visual companion: [#1 Data Model](https://www.youtube.com/watch?v=AKSYxxDczEw&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=1) (31 min) · [#2 Distributed File System / GFS](https://www.youtube.com/watch?v=zAkMFWYnFHA&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=2) (30 min) · [#3 MapReduce](https://www.youtube.com/watch?v=NpQ-zwZPXaw&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=3) (34 min) | YouTube series | 2 | Free |

*Hadoop & HDFS supplements:*

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Apache Hadoop — official documentation](https://hadoop.apache.org/docs/stable/) — "Single Cluster Setup," HDFS Architecture, YARN Architecture guides | Official docs | 5 | Free |
| [Mahmoud Mohsen — #8 Hadoop Distributed File System](https://www.youtube.com/watch?v=4DuFZNVE090&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=8) (43 min) — use as a visual walkthrough of HDFS internals alongside the official Apache docs; covers NameNode/DataNode architecture with worked diagrams | YouTube | 1 | Free |
| [Apache Spark — official documentation hub](https://spark.apache.org/docs/latest/) — Quick Start, RDD Programming Guide, Spark SQL/DataFrame Guide, Structured Streaming Guide | Official docs | 12 | Free |
| [freeCodeCamp.org — "PySpark Tutorial" (YouTube)](https://www.youtube.com/watch?v=_C8kWso4ne4) | YouTube | 6 | Free |
| **Project checkpoint:** Re-implement 3+ Course 8 pipeline/query exercises using Spark DataFrames; add one Structured Streaming job consuming from a Course 8 Kafka topic | Hands-on project | 4 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Coursera — "Big Data Modeling and Management Systems" (UCSD, Course 2)](https://www.coursera.org/learn/big-data-management) | MOOC, audit mode | 15 | Free-audit |
| [Coursera — "Big Data Integration and Processing" (UCSD, Big Data Specialization, Course 3)](https://www.coursera.org/learn/big-data-integration-processing) — hands-on Spark, MongoDB, and Hadoop integration for large-scale analytical pipelines; extends Course 12 IBM content with practical retrieval and processing patterns | MOOC, audit mode | 17 | Free-audit |
| [Coursera — "Graph Analytics for Big Data" (UCSD, Big Data Specialization, Course 5)](https://www.coursera.org/learn/big-data-graph-analytics) — graph data modeling, Neo4j, and Spark GraphX; builds graph analysis skills directly applicable to network-structured datasets and graph-based ML features | MOOC, audit mode | 12 | Free-audit |
| [Coursera — "Building Batch Data Pipelines on Google Cloud" (GCP Data Engineer Cert, Course 2)](https://www.coursera.org/professional-certificates/gcp-data-engineering) — Dataproc cluster provisioning, Spark-BigQuery connector, Dataproc Serverless, Spark/Hive jobs on GCP, Cloud Composer orchestration | MOOC, audit mode | 15 | Free-audit |
| [AWS EMR — "Getting Started" guide](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html) (small cluster, terminate promptly to stay in free tier) | Official vendor labs | 4 | Free (within limits) |
| [Microsoft Learn — Azure HDInsight "Get Started" tutorial](https://learn.microsoft.com/en-us/azure/hdinsight/hdinsight-hadoop-linux-tutorial-get-started) | Official vendor labs | 3 | Free (within limits) |
| [بالعربي Big Data — Hadoop Ecosystem & Docker/Kubernetes](https://www.youtube.com/@bigdata4756) — hands-on Arabic-language series covering every layer of the Hadoop stack plus containerized deployment: [What is Big Data? / أيه هي البيج داتا؟](https://www.youtube.com/@bigdata4756) (~9min) · Installing Hadoop Parts 1–4 / يلا نسطّب هادووب (~39min+17min+17min+17min) · [MapReduce / خطط واختصر](https://www.youtube.com/@bigdata4756) (~27min) · [HDFS / غرائب وعجائب هادووب](https://www.youtube.com/@bigdata4756) (~28min) · [YARN / توزيع الأرزاق](https://www.youtube.com/@bigdata4756) (~28min) · [Hadoop I/O / الملفات المفعوصة](https://www.youtube.com/@bigdata4756) (~21min) · [Docker and Kubernetes / العلبة دي فيها سوعبان](https://www.youtube.com/@bigdata4756) (~10h) — use Hadoop sub-series alongside the Apache docs; Docker/Kubernetes series teaches containerised cluster deployment directly relevant to this course | YouTube series (Arabic) | 15h | Free |
| [UC Berkeley — "Big Data Analysis with Apache Spark" (BerkeleyX CS105x), via Class Central](https://www.classcentral.com/course/edx-big-data-analysis-with-apache-spark-3026) | University MOOC, audit mode | 15 | Free-audit |
| [Databricks — free training home](https://www.databricks.com/learn/training/home) — self-paced "Apache Spark Programming" introductory modules | Official vendor course | 8 | Free |
| [Mahmoud Mohsen — Spark series (playlist vids 17–18)](https://www.youtube.com/playlist?list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI) — concise lecture-style intro to Spark concepts; use as a warmup before the Databricks hands-on labs: [#17 Introduction & RDDs](https://www.youtube.com/watch?v=tejR_7HgXcc&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=17) (55 min) · [#18 DataFrames, MLlib & Streaming](https://www.youtube.com/watch?v=mp7LFZFfDAU&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=18) (55 min) | YouTube series | 2 | Free |

> 💡 **Wiki integration — Big Data's Five V's Framework:** Before diving into Hadoop/Spark internals, internalize the Five V's that define Big Data: **Volume** (scale — TB/PB+), **Velocity** (speed — real-time vs batch), **Variety** (diversity — structured, semi-structured, unstructured), **Veracity** (quality — trustworthiness of data), **Value** (business outcome — the ultimate measure). Practitioners emphasize that a dataset is only "Big Data" when traditional RDBMS approaches break down on at least 2–3 of these dimensions. The field itself was born because engineers embraced a "store everything" philosophy — keep raw data indefinitely rather than pre-aggregating, because you don't yet know which questions you'll ask. This shift from schema-on-write (traditional DB) to schema-on-read (Hadoop/Spark) is the conceptual foundation beneath every tool in this course.

**Combined total: ~141h | IBM: 20h | Tier 1 supplements: 30h | Tier 2 supplements: 91h**

> ### 🎯 Self-Assessment Gate — Big Data (after Course 12)
> Before moving to Course 13, you should be able to:
> - [ ] Explain HDFS block replication — what happens when a DataNode goes down?
> - [ ] Write a PySpark job that reads a Parquet file, filters rows, aggregates by a column, and writes output back to disk
> - [ ] Explain the difference between RDDs, DataFrames, and Datasets in Spark
> - [ ] Run a multi-container Spark cluster locally using Docker Compose
> - [ ] Describe in one sentence the difference between Lambda and Kappa architectures
>
> If you can't do all five, revisit the Spark documentation and Databricks free labs before continuing.

### 💼 Portfolio Project Ideas (Course 12)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| PySpark Batch Processing Pipeline | 🟡 Intermediate | PySpark, HDFS (Docker), Parquet, GitHub | Demonstrates ability to ingest a large public dataset into HDFS, process it with PySpark DataFrames (filter, aggregate, join), and write optimized Parquet output. |
| Structured Streaming Kafka-to-Parquet Job | 🟡 Intermediate | PySpark Structured Streaming, Kafka, Docker Compose | Demonstrates ability to consume a live Kafka stream with PySpark, apply windowed aggregations, and write micro-batch results to partitioned Parquet files. |
| Docker Compose Spark Cluster | 🔴 Advanced | Docker Compose, Apache Spark (multi-node), PySpark | Demonstrates ability to provision and operate a multi-node Spark cluster locally, submit jobs from a driver container, and diagnose performance using the Spark UI. |

---

## IBM Track — Course 13: Machine Learning with Apache Spark (~68h total)

> 🎓 **Primary:** [Machine Learning with Apache Spark](https://www.coursera.org/learn/machine-learning-with-apache-spark) — ML role in data engineering, Spark ML pipelines, regression, classification, clustering with SparkML, generative AI concepts, model persistence | ~16h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Apache Spark — MLlib Programming Guide](https://spark.apache.org/docs/latest/ml-guide.html) | Official docs | 10 | Free |
| [Google — Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) | Official vendor course | 8 | Free |
| [Mahmoud Mohsen — Data Analysis series (playlist vids 14–16)](https://www.youtube.com/playlist?list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI) — algorithm intuition lectures; useful before implementing the same algorithms in Spark MLlib: [#14 Intro to AI & Regression](https://www.youtube.com/watch?v=OdB_oiXMk8A&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=14) (47 min) · [#15 Classification Algorithms](https://www.youtube.com/watch?v=error0K9BSE&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=15) (53 min) · [#16 Clustering & Deep Learning](https://www.youtube.com/watch?v=N0xFjJv5GSc&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=16) (39 min) | YouTube series | 2 | Free |
| **Project checkpoint:** Full Spark MLlib pipeline (feature engineering → train/test split → model → evaluation) for classification + clustering on a public Kaggle dataset | Hands-on project | 6 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Coursera — "Machine Learning With Big Data" (UCSD, Big Data Specialization, Course 4)](https://www.coursera.org/learn/big-data-machine-learning) | MOOC, audit mode | 20 | Free-audit |
| [Kaggle Learn](https://www.kaggle.com/learn) — "Intro to Machine Learning" + "Intermediate Machine Learning" micro-courses | Free interactive | 6 | Free |

> Note: the UCSD Big Data Specialization's machine-learning course is officially Course 4 ("Machine Learning With Big Data") in the six-course sequence.

**Combined total: ~68h | IBM: 16h | Tier 1 supplements: 26h | Tier 2 supplements: 26h**

### 💼 Portfolio Project Ideas (Course 13)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| SparkML Classification Pipeline | 🟡 Intermediate | PySpark MLlib, Jupyter Notebook, Kaggle dataset | Demonstrates ability to build a reproducible Spark ML pipeline with feature engineering, cross-validation, and model evaluation metrics — ready for integration into a data product. |
| Model Persistence & Batch Scoring Job | 🟡 Intermediate | PySpark MLlib, HDFS / local FS, Airflow | Demonstrates ability to train, persist, and reload a SparkML model for scheduled batch scoring, wiring the scoring job into an Airflow DAG. |
| Spark ML vs scikit-learn Benchmark | 🔴 Advanced | PySpark MLlib, scikit-learn, Python, Jupyter | Demonstrates ability to implement the same ML workflow at two scales, compare accuracy and runtime, and articulate when Spark ML is — and isn't — the right choice. |

---

## IBM Track — Course 14: Data Engineering Capstone Project (~43h total)

> 🎓 **Primary:** [Data Engineering Capstone Project](https://www.coursera.org/learn/data-enginering-capstone-project) — end-to-end project: RDBMS, NoSQL (MongoDB), Apache Spark, data warehousing, ETL pipelines, and BI dashboards | ~18h | Free-audit

**Capstone alignment — how the IBM capstone maps to the skills you built:**

1. **Courses 4–5 (RDBMS & SQL):** Design a relational database for a real-world scenario.
2. **Course 11 (NoSQL):** Build and query NoSQL data stores.
3. **Course 12 (Big Data):** Stand up a Hadoop cluster, load data into HDFS, run a Spark job.
4. **Courses 8–9 (ETL & DW):** Build an ETL pipeline into a data warehouse.
5. **Course 10 (BI):** Create dashboards visualizing your pipeline output.
6. **Course 13 (ML):** Train a Spark ML model on your processed data.
7. **Courses 1–3 (Foundations):** Apply Python scripting, API integration, and DE lifecycle thinking throughout.
8. **Full integration:** Airflow orchestration → cloud warehouse → Spark ML → RAG bot → dashboard — this is portfolio-level work.

**Additional capstone inspiration — free end-to-end project walkthroughs:**

| # | Project | Focus Area | Link |
|---|---|---|---|
| 1 | End To End Big Data Engineering Project With Azure | Azure, ADF, ADLS, Databricks | [YouTube](https://lnkd.in/gykp5HNy) |
| 2 | Apache Spark End-To-End Project — Apple Data Analysis | Spark, PySpark, data analysis | [YouTube](https://lnkd.in/gBcDNUDK) |
| 3 | Apache Spark End to End Project — Customer and Sales | Spark DataFrames, SQL | [YouTube](https://lnkd.in/gjZ8vuxA) |
| 4 | Olympic Data Analytics — Azure End-To-End Project | Azure Synapse, ADF, Power BI | [YouTube](https://lnkd.in/gb_gwT3R) |
| 5 | IRCTC Real Time Data Pipeline — Complete DE Project | Kafka, streaming, real-time | [YouTube](https://lnkd.in/g34szQAV) |
| 6 | Azure Data Engineer End to End Project | Azure full stack | [YouTube](https://lnkd.in/gsPWybWw) |
| 7 | Snowflake Real Cricket Analytics Use Case | Snowflake, data warehousing | [YouTube](https://lnkd.in/gE-qnnrD) |
| 8 | End to End Azure Data Engineering Project | Azure, orchestration | [YouTube](https://lnkd.in/gMM2MDcz) |

**When to use these:** Projects 2–3 → after Course 12 (Spark). Projects 1, 4, 6, 8 → after Course 9 (Azure/cloud). Project 5 → after Course 8 (Kafka). Project 7 → after Course 9 (Snowflake).

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|---|
| [Coursera — "Big Data - Capstone Project" (UCSD, Big Data Specialization, Course 6)](https://www.coursera.org/learn/big-data-capstone-project) — five-week end-to-end big data project using Splunk, KNIME, Spark MLlib, and Gephi; complements the IBM capstone by providing a second full-cycle project narrative for your portfolio | MOOC, audit mode | 22 | Free-audit |

**Combined total: ~43h | IBM: 18h | Tier 1 supplements: 3h | Tier 2 supplements: 22h**

> ⚡ *All resources in this section are Tier 1 — essential.*

> ### 🎯 Self-Assessment Gate — Portfolio Readiness (after Course 14)
> Before applying to jobs or moving to Courses 15–16, your capstone project should:
> - [ ] Have a public GitHub repository with a clear README explaining the problem, architecture, and how to run it
> - [ ] Include at least one Airflow DAG orchestrating the pipeline end-to-end
> - [ ] Demonstrate both a relational and a NoSQL data store in use
> - [ ] Include a Spark processing step (not just SQL)
> - [ ] Have a dashboard or query output that a non-technical person could understand
>
> This is your portfolio. A strong capstone project is more valuable than any certification at the junior DE level.

### 💼 Portfolio Project Ideas (Course 14)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| Full-Stack DE Capstone — E-Commerce Analytics | 🔴 Advanced | PostgreSQL, MongoDB, Airflow, Spark, Snowflake, Power BI, Docker Compose | Demonstrates ability to architect and deliver a complete data engineering system — from ingestion through transformation, warehousing, and visualization — integrating all skills from Courses 1–13 into a single production-grade GitHub repository. |

---

## IBM Track — Course 15: Generative AI: Elevate your Data Engineering Career (~95h total)

> 🎓 **Primary:** [Generative AI: Elevate your Data Engineering Career](https://www.coursera.org/learn/generative-ai-elevate-your-data-engineering-career) — GenAI for data generation, augmentation, anonymization, ETL processes, warehouse schema design, and infrastructure setup; practical labs + real-world case studies | ~13h | Free-audit

**Supplementary resources — study these alongside or immediately after the IBM course above:**

*GenAI fundamentals & prompting:*

**🔴 Tier 1 — Must-Watch / Must-Read**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [DeepLearning.AI — "ChatGPT Prompt Engineering for Developers"](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) | MOOC | 2 | Free |
| [Google Cloud Skills Boost — "Introduction to Generative AI" learning path](https://www.cloudskillsboost.google/paths/118) | Official vendor course | 4 | Free |
| [DataTalks.Club — LLM Zoomcamp (GitHub repo + self-paced YouTube playlist)](https://github.com/DataTalksClub/llm-zoomcamp) — covers RAG, embeddings, vector/hybrid search, evaluation, monitoring, agents | Free cohort-based course, self-paced option | 20 | Free |
| [LangChain RAG tutorial](https://python.langchain.com/docs/tutorials/rag/) OR [LlamaIndex documentation](https://docs.llamaindex.ai/en/stable/) (pick one) | Official docs | 3 | Free |
| **Capstone:** Build a RAG Q&A bot over a public dataset (e.g., Wikipedia subset or your own course notes), store embeddings in a free vector store (Chroma/FAISS, self-hosted), serve via a simple API | Hands-on project | 3 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Anthropic — Prompt Engineering documentation](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) | Official docs | 3 | Free |
| [AWS — Amazon Bedrock product/getting-started page](https://aws.amazon.com/bedrock/) + [AWS Skill Builder](https://skillbuilder.aws/) free-tier Bedrock labs | Official vendor labs | 5 | Free (AWS free tier) |
| [Microsoft Learn — "Develop Generative AI apps with Azure OpenAI Service"](https://learn.microsoft.com/en-us/training/paths/develop-ai-solutions-azure-openai/) | Official docs/labs | 4 | Free |
| [Google — "Responsible AI Practices"](https://ai.google/responsibility/responsible-ai-practices/) | Official docs | 2 | Free |
| [Hugging Face — NLP Course](https://huggingface.co/learn/nlp-course) (embeddings/transformers chapters) | Official free course | 4 | Free |
| [Pinecone Learning Center](https://www.pinecone.io/learn/) — Vector Search & Embeddings guides | Vendor docs/tutorials | 3 | Free |
| [Apache Ranger documentation](https://ranger.apache.org/) — policy/governance model overview | Official docs | 2 | Free |
| [Feast — open-source feature store documentation](https://docs.feast.dev/) + "Getting Started" quickstart | Official docs | 4 | Free |
| [Hopsworks — "Feature Store for ML" free course](https://www.hopsworks.ai/feature-store) | Official vendor course | 3 | Free |
| [Weaviate — "Zero to MVP" learning path](https://weaviate.io/developers/weaviate/quickstart) | Official docs | 3 | Free |
| [pgvector — GitHub README + PostgreSQL extension docs](https://github.com/pgvector/pgvector) — vector search inside Postgres, no external service needed | Official docs | 2 | Free |
| [Great Expectations — open-source data quality](https://docs.greatexpectations.io/docs/) — full "Getting Started" + integration with Airflow | Official docs | 4 | Free |
| [freeCodeCamp — "Data Quality & Observability" (search YouTube for recent tutorials)](https://www.youtube.com/@freecodecamp) | YouTube | 2 | Free |
| [LlamaIndex — "Building Production RAG Systems" guide](https://docs.llamaindex.ai/en/stable/optimizing/production_rag/) — engineering the data pipeline behind RAG, not just the prompting layer | Official docs | 3 | Free |
| [MLflow — official documentation](https://mlflow.org/docs/latest/index.html) — experiment tracking, model registry (prompt versioning analogue) | Official docs | 2 | Free |
| **Project checkpoint:** Extend your RAG bot: add a feature store that preprocesses and registers document metadata as features; add a Great Expectations suite that validates incoming data before embedding; document your data quality strategy in a README. | Hands-on project | 4 | Free |

> **Connection to other courses:** The RAG capstone's vector store (Chroma/FAISS) is your prototyping layer. Weaviate/pgvector above is the production layer. Course 8's Airflow DAGs can orchestrate the embedding refresh pipeline. Course 9's Snowflake/BigQuery can back your feature store.

**Combined total: ~95h | IBM: 13h | Tier 1 supplements: 32h | Tier 2 supplements: 50h**

### 💼 Portfolio Project Ideas (Course 15)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| RAG Q&A Bot over Public Dataset | 🟡 Intermediate | Python, LangChain / LlamaIndex, FAISS / Chroma, FastAPI | Demonstrates ability to build a retrieval-augmented generation pipeline that indexes a document corpus into a vector store and serves semantically accurate answers via an API endpoint. |
| Airflow-Orchestrated Embedding Refresh Pipeline | 🔴 Advanced | Airflow, Python, pgvector / Chroma, Great Expectations | Demonstrates ability to operationalize a RAG system with scheduled embedding refresh, automated data quality validation before indexing, and lineage-aware pipeline orchestration. |
| Synthetic Data Generator for ML Training | 🟡 Intermediate | Python, OpenAI / local LLM (Ollama), pandas, PostgreSQL | Demonstrates ability to use an LLM to generate domain-specific synthetic training data, validate its statistical properties, and load it into a structured store for downstream model use. |

---

## IBM Track — Course 16: Data Engineering Career Guide and Interview Preparation (~11h total)

> 🎓 **Primary:** [Data Engineering Career Guide and Interview Preparation](https://www.coursera.org/learn/data-engineering-career-guide-and-interview-preparation) — role of a data engineer, career paths, job search strategies, resume/portfolio building, interview types, mock interviews, professional presentation | ~11h | Free-audit

> No additional supplements needed — IBM course is self-contained for this topic. Use the Certification Roadmap in Appendix A to plan your next credential, and the capstone projects from Course 14 to build your portfolio.

> ⚡ *All resources in this section are Tier 1 — essential.*

**Combined total: ~11h | IBM: 11h | Tier 1 supplements: 0h | Tier 2 supplements: 0h**

> 💡 **Practitioner tip (IBM Data Engineering Viewpoints):** There is no single universal technical stack. The specific tools you need depend on the industry — retail favors Kafka and Cassandra for 24/7 pipelines; healthcare demands compliance-first design with HL7/FHIR; social media requires petabyte-scale streaming; finance needs low-latency, governance-heavy pipelines. Build the universal foundation first, then specialize based on the industry you're targeting.

> 💡 **Practitioner tip (IBM Data Engineering Viewpoints):** Soft skills are the real differentiator — multiple practitioners independently cite them as more important than any specific tool. Communication (explaining trade-offs to management, understanding what analysts need), curiosity (asking why the data should look a certain way), and detail orientation (no unchecked edge cases in a pipeline) are what separate effective DEs from technically skilled ones.

> 💡 **Wiki practitioner insight — paths into DE are non-linear:** Practitioners unanimously agree there is no single path into data engineering. DEs come from DBA, software engineering, analytics, and even completely non-technical backgrounds who learned to code on the job. What they share is genuine curiosity about data — not a specific degree or previous title. One hiring manager's framework evaluates candidates on four layers: (1) **Fundamentals** — SQL, data modeling, pipeline principles; (2) **Tools** — depth in the stack relevant to the role; (3) **Architecture thinking** — ability to design trade-offs, not just build features; (4) **Soft skills** — communication, curiosity, attention to detail. Junior candidates are weighted heavily on (1) and (4); senior candidates must demonstrate all four. Build the fundamentals first — the specific tools will change, but the patterns stay.

### 💼 Portfolio Project Ideas (Course 16)

| Project | Difficulty | Stack | Demonstrates |
|---|---|---|---|
| DE Portfolio Website | 🟢 Beginner | GitHub Pages / Netlify, Markdown / HTML | Demonstrates ability to present a professional data engineering portfolio — linking all capstone projects, certifications, and a skills matrix — as a recruiter-facing artifact that complements a resume. |

---

## ── POST-TRACK ENHANCEMENTS ────────────────────────────────────

> These modules cover topics the IBM track does not address. Complete them after finishing all 16 IBM courses.

---

## Enhancement A — Big Data Analytics at Scale (~23h)

> **Gap filled:** The IBM track covers data warehousing (Course 9) and Spark SQL (Course 12) but does not teach Hive/Impala/Pig or Lambda vs Kappa architecture — tools and patterns still common in Hadoop-based enterprise environments.

**Topics:** Apache Hive (DDL/DML, partitioning, bucketing), Apache Impala, Apache Pig, Lambda vs Kappa streaming architectures.

**Learning objective:** Write and optimize HiveQL queries against partitioned tables, explain Hive vs Impala tradeoffs, and diagram a Lambda vs a Kappa architecture for the same use case.

| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Apache Hive — Language Manual](https://cwiki.apache.org/confluence/display/Hive/LanguageManual) (DDL/DML, partitioning, bucketing) | Official docs | 8 | Free |
| [Apache Impala — official documentation](https://impala.apache.org/impala-docs.html) | Official docs | 5 | Free |
| [Apache Pig — official documentation](https://pig.apache.org/docs/latest/start.html) | Official docs | 3 | Free |
| [Jay Kreps — "Questioning the Lambda Architecture" (O'Reilly Radar)](https://www.oreilly.com/radar/questioning-the-lambda-architecture/) + Confluent Kappa blog posts | Free articles | 2 | Free |
| **Project checkpoint:** Load NYC Taxi or NOAA weather data into Hive-style partitioned tables; write 5 analytical queries; document Lambda vs Kappa design for the same data | Hands-on project | 5 | Free |

**Total: ~23h**

---

## Enhancement B — Security & Governance Deep Dive (~8h)

> **Gap filled:** Course 7 (DBA) covers database-level security. This enhancement extends to cluster-wide governance with Apache Ranger and Apache Atlas for policy management, metadata, and data lineage.

**Topics:** Apache Ranger (policy model, plugins, Hive/HDFS integration), Apache Atlas (metadata, governance, data lineage).

**Learning objective:** Configure a Ranger policy restricting user/group access to specific Hive tables or HDFS paths; use Atlas to trace data lineage across a pipeline.

| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Apache Ranger — official documentation](https://ranger.apache.org/) — policy model, plugins, Hive/HDFS integration | Official docs | 5 | Free |
| [Apache Atlas — official documentation](https://atlas.apache.org/) — metadata/governance/data lineage | Official docs | 3 | Free |

**Total: ~8h**

---

## Enhancement C — Modern Pipeline Tooling: dbt & Data Quality (~27h)

> **Gap filled:** Course 8 covers ETL with Airflow and Kafka. This enhancement adds dbt (the industry standard for SQL-based transformation) and data quality tooling — skills required by most mid-level+ DE job postings.

**Topics:** dbt (models, tests, documentation, incremental loads), dbt advanced warehouse-specific optimizations, pipeline data quality with Great Expectations, production data observability (DataKitchen, Soda, data contracts).

**Learning objective:** Build a dbt project with models, tests, and documentation; run it against a warehouse; validate data quality with Great Expectations integrated into an Airflow DAG; apply production data observability patterns (pre-production profiling, production testing, SLA/SLO metrics, data contracts) using open-source tooling.

| Resource | Type | Hours | Cost |
|---|---|---|---|
| [dbt — official documentation](https://docs.getdbt.com/) + [dbt Learn — free "Fundamentals" course](https://courses.getdbt.com/courses/fundamentals) | Official docs + vendor course | 8 | Free |
| [DataTalks.Club — Data Engineering Zoomcamp, Module 4: Analytics Engineering with dbt](https://github.com/DataTalksClub/data-engineering-zoomcamp) | Free course module | 5 | Free |
| [Great Expectations — open-source data quality](https://docs.greatexpectations.io/docs/) — "Getting Started" guide (pipeline observability preview) | Official docs | 1 | Free |
| [dbt — "Advanced" course](https://courses.getdbt.com/courses/advanced-dbt) (warehouse-specific optimizations) | Official vendor course | 3 | Free |

**🟡 Tier 2 — Valuable but Optional**
| Resource | Type | Hours | Cost |
|---|---|---|---|
| [DataKitchen — "Data Observability and Data Quality Testing Certification"](https://info.datakitchen.io/data-observability-and-data-quality-testing-certification) — 4-part on-demand series: pre-production data profiling, production data testing (28 profiling checks, 11 custom validation patterns), regression and impact assessment, SLA/SLO metrics, Data Testing Maturity Model; hands-on labs with open-source DataOps TestGen and Observability software. Supplement with [Soda "Guide to Data Contracts"](https://soda.io/blog/guide-to-data-contracts) (~1h read) and [Data Contract Specification](https://datacontract.com) (~1h self-study) for full data contracts coverage. | Official vendor certification | 10 | Free |
| [Kestra Academy — "Kestra Fundamentals" (official free certification course)](https://academy.kestra.io/) — YAML-first declarative orchestration: flow anatomy, event-driven vs scheduled triggers, backfill patterns, KV store, GCP plugin integration (GCS + BigQuery ingestion flows), Gantt/log UI inspection | Official vendor certification | 4 | Free |

**Total: ~31h**

---

## Enhancement D — Mahmoud Mohsen Playlist Revision (~1h)

> Self-assessment checkpoint: watch after completing the IBM track.

| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Mahmoud Mohsen — #20 Revision (Midterm Solutions)](https://www.youtube.com/watch?v=6sOaYh5DhBo&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=20) (42 min) — watch without pausing and answer the questions in your head before he does. A natural self-assessment of your Big Data knowledge before moving to the Enhancement modules. | YouTube | 1 | Free |

**Total: ~1h**

---

## Enhancement E — Data Lakehouse Architecture (~10h)

> **Gap filled:** The IBM track covers data warehousing (Course 9) and Spark/Hadoop (Course 12) but has no dedicated coverage of modern lakehouse table formats (Apache Iceberg, Delta Lake, Apache Hudi) that combine data lake flexibility with warehouse-grade ACID transactions and governance.

**Topics:** Apache Iceberg catalog setup, schema evolution, hidden partitioning, compaction, snapshot management, Write-Audit-Publish pattern; lakehouse vs. data lake vs. warehouse architecture tradeoffs.

**Learning objective:** Deploy Apache Iceberg on object storage with Spark/Trino, implement schema evolution and partition management, and compare lakehouse vs. data lake vs. data warehouse architecture tradeoffs for a given use case.

| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Coursera — "Apache Iceberg: From Zero to Production Data Lakehouse"](https://www.coursera.org/learn/apache-iceberg-data-lakehouse) — full lifecycle: catalog setup, hidden partitioning, schema evolution, Write-Audit-Publish, copy-on-write vs. merge-on-read, compaction and snapshot expiration; Snowflake-authored | MOOC, audit mode | 10 | Free-audit |

**Total: ~10h**

---

## Enhancement F — Data Architecture Patterns (~10h)

> **Gap filled:** The IBM track covers data warehousing and ETL patterns at the tool level but does not teach architecture-level design frameworks — medallion architecture, data mesh, data product thinking, and federated governance — that determine how data platforms are organized at scale.

**Topics:** Data mesh (domain ownership, data-as-a-product, self-serve platform, federated governance), medallion architecture (bronze/silver/gold layers), data product design patterns, API-based data exchange.

**Learning objective:** Design a domain-oriented data mesh architecture with clear ownership boundaries and data product structures, implement federated governance policies, and map medallion layers onto a real-world use case.

| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Coursera — "Data Mesh Architectures and Implementations"](https://www.coursera.org/learn/data-mesh-architectures-implementations) — decentralized data mesh design, domain-oriented ownership, data-as-a-product, federated governance, self-serve platform capabilities, medallion architecture integration; Edureka | MOOC, audit mode | 10 | Free-audit |

**Total: ~10h**

---

## Enhancement G — Data Cataloging & Discovery (~10h)

> **Gap filled:** Enhancement B covers Apache Ranger/Atlas for security governance. This module adds modern data catalog tools (OpenMetadata, DataHub, Amundsen) for metadata management, data discovery, lineage tracking, and catalog-driven governance.

**Topics:** Metadata types and lifecycle, hands-on OpenMetadata (glossary, ownership, lineage, sensitive data classification), REST API automation for metadata workflows, catalog adoption metrics.

**Learning objective:** Deploy and operate OpenMetadata, configure glossary/ownership/lineage, automate metadata workflows via REST API, and measure catalog adoption across a simulated organization.

| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Coursera — "Metadata Management and Data Catalogs"](https://www.coursera.org/learn/metadata-management-data-catalogs) — metadata lifecycle, hands-on OpenMetadata operations, REST API automation, lineage tracking, governance workflows, adoption metrics; Edureka | MOOC, audit mode | 10 | Free-audit |

**Total: ~10h**

---

## Enhancement H — Unified Data Platform with Bruin (~5h)

> **Gap filled:** Enhancement C covers dbt (transformation), Course 8 covers Airflow (orchestration), and Great Expectations/DataKitchen cover data quality — but these are separate tools. This module adds Bruin, a unified CLI-based platform that combines ingestion, transformation, orchestration, and inline data quality checks in a single YAML-driven workflow with AI-assisted pipeline scaffolding via MCP.

**Topics:** Bruin CLI setup, pipeline YAML configuration, Python/SQL/ingestor asset types, DuckDB and BigQuery connections, three-layer architecture (ingestion → staging → reports), incremental materialization strategies (delete+insert, merge, append), inline quality check definitions in asset YAML, dependency graph visualization, AI-assisted pipeline building via Bruin MCP server in Cursor/VS Code.

**Learning objective:** Build a unified data pipeline using Bruin CLI — define assets in YAML, configure incremental materialization, add inline quality checks, visualize the dependency graph, and scaffold pipelines with AI assistance.

| Resource | Type | Hours | Cost |
|---|---|---|---|
| [Bruin Official Documentation — "Getting Started"](https://docs.getbruin.com/getting-started/introduction/) + [DE Zoomcamp Module 5: Data Platforms](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/05-data-platforms) — progressive tutorial: `bruin init`, pipeline YAML, asset types, DuckDB/BigQuery connections, three-layer architecture, incremental strategies, inline quality checks, dependency graph, MCP-assisted pipeline building | Official docs + free course module | 5 | Free (Apache 2.0) |

**Total: ~5h**

---

## Enhancement I — Capstone Pipeline Project (~25h)

> **Gap filled:** Course 14 (IBM Capstone) covers an end-to-end project using IBM stack (RDBMS, NoSQL, Hadoop, Spark, Cognos). This module provides a modern-stack capstone integrating Terraform IaC, cloud warehouse (BigQuery/Snowflake/Redshift), dbt transformations, data quality validation, BI dashboard, and GitHub delivery — the comprehensive integration exercise missing from the plan.

**Topics:** End-to-end data pipeline design and implementation: cloud infrastructure provisioning (Terraform), batch/streaming ingestion, cloud data warehouse with partitioned/clustered tables, dbt transformations and tests, data quality checks, BI dashboard, GitHub portfolio delivery.

**Learning objective:** Design, build, and document a complete end-to-end data pipeline using modern tooling — from infrastructure provisioning through ingestion, transformation, quality validation, and visualization — delivered as a public GitHub repository.

| Resource | Type | Hours | Cost |
|---|---|---|---|
| [DeepLearning.AI — "Data Modeling, Transformation, and Serving" (Course 4 of Data Engineering Professional Certificate)](https://www.coursera.org/learn/data-modeling-transformation-serving) — multi-week capstone: dbt transformations, star schema/data vault, data quality validation, stream processing integration, graded deliverable covering the full data engineering lifecycle | MOOC, audit mode | 20 | Free-audit |
| [DE Zoomcamp Final Project (self-paced, rubric-driven)](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/projects) — structured capstone: Terraform IaC → cloud warehouse → dbt transformations → BI dashboard → GitHub portfolio; peer review scoring rubric covers reproducibility, pipeline architecture, warehouse design, transformation correctness, and dashboard clarity. Use alongside the Coursera capstone if you want GCP-specific deployment practice. | Free course module | 15 | Free |

> **Note on capstone choice:** The DeepLearning.AI course provides a graded, instructor-led capstone with modern tooling (dbt, AWS, Spark) and is recommended as the primary route. The DE Zoomcamp project adds GCP/Terraform IaC deployment and a recruiter-visible GitHub deliverable with peer review — combine both if time permits, or pick the one that matches your target cloud platform.

**Total: ~25h**

---

## Suggested Week-by-Week Sequence

> Two pacing columns are shown. **IBM-Only (~10h/week)** follows just the IBM course — fastest path, ~20 weeks. **IBM + Core Supplements (~10h/week)** adds the highest-ROI supplements from each section — deeper learning, ~45 weeks. MVP learners: follow the IBM-Only column for MVP courses only (~20 weeks).

| Week (IBM-Only) | Week (IBM + Supplements) | Focus | Course / Enhancement |
|---|---|---|---|
| 1–2 | 1–3 | Data engineering landscape & lifecycle | Course 1: Introduction to Data Engineering |
| 3–5 | 4–7 | Python programming for data tasks | Course 2: Python for Data Science, AI & Development |
| 5–6 | 7–8 | Hands-on Python ETL project | Course 3: Python Project for Data Engineering |
| 6–8 | 9–11 | Relational databases: design & modeling | Course 4: Introduction to Relational Databases |
| 8–10 | 12–15 | SQL mastery with Python integration | Course 5: Databases and SQL for Data Science |
| 10–12 | 16–19 | Linux, Bash, Git, Docker basics | Course 6: Linux Commands and Shell Scripting |
| 12–14 | 20–23 | Database administration | Course 7: Relational Database Administration |
| — | — | 🎯 **Gate check: Foundations** | Can you pass the 5 foundation criteria? |
| 14–16 | 24–28 | ETL pipelines: Airflow, Kafka, Schema Registry | Course 8: ETL and Data Pipelines |
| 16–18 | 29–33 | Data warehousing: Snowflake/BigQuery, dimensional modeling | Course 9: Data Warehouse Fundamentals |
| — | — | 🎯 **Gate check: Core DE** | Can you pass the 5 core DE criteria? |
| 18–19 | 34–35 | BI dashboards: Cognos & Looker | Course 10: BI Dashboards |
| 19–21 | 35–37 | NoSQL databases: MongoDB, Cassandra | Course 11: Introduction to NoSQL |
| 21–23 | 38–41 | Big Data: Hadoop, Spark, HDFS | Course 12: Big Data with Spark and Hadoop |
| — | — | 🎯 **Gate check: Big Data** | Can you pass the 5 Big Data criteria? |
| 23–25 | 42–45 | Machine learning with Spark | Course 13: ML with Apache Spark |
| 25–27 | 46–49 | Capstone project | Course 14: Data Engineering Capstone |
| — | — | 🎯 **Gate check: Portfolio** | Does your capstone meet the 5 portfolio criteria? |
| 27–28 | 50–51 | Generative AI for data engineering | Course 15: GenAI for DE Career |
| 28–29 | 52 | Career prep & interview readiness | Course 16: Career Guide |
| 30–31 | 53–54 | Hive, Impala, Pig, Lambda/Kappa | Enhancement A: Big Data Analytics at Scale |
| 32 | 55 | Apache Ranger & Atlas (security/governance) | Enhancement B: Security & Governance |
| 33–34 | 56–58 | dbt & data quality tooling | Enhancement C: dbt & Data Quality |
| 35–36 | 59–60 | Apache Iceberg, lakehouse architecture | Enhancement E: Data Lakehouse Architecture |
| 37–38 | 61–62 | Data mesh, medallion, data product design | Enhancement F: Data Architecture Patterns |
| 39–40 | 63–64 | OpenMetadata, catalog-driven governance | Enhancement G: Data Cataloging & Discovery |

> **Pacing notes:**
> - **IBM-Only path:** ~10h/week → ~40 weeks. The fastest way to get the IBM certificate.
> - **IBM + Core Supplements path:** ~10h/week → ~64 weeks (~15 months). Includes the highest-ROI supplements only; skips the deep-dive options.
> - **Full plan (all supplements):** ~15–20h/week over 18–24 months, or ongoing alongside a job.
> - If you already have Python/SQL/Linux experience, skip Courses 1–7 supplements entirely and save 8–10 weeks.
> - The supplement resources add depth — fold them into the same weeks as their IBM course, or batch them into catch-up weeks between major sections.

---

## Gaps: Where No Adequate Free Equivalent Exists

- **Hands-on multi-node cluster administration:** free-tier cloud quotas limit true distributed ops. Use Docker Compose multi-container setups locally, or spin up and immediately tear down short-lived AWS/GCP multi-node clusters within free-tier credit windows.
- **Vendor-certified GenAI platform depth** (fine-tuning, private networking, enterprise guardrails on Bedrock/Vertex/Azure OpenAI): free tiers cover core workflows; enterprise-only features are read-only documentation study.
- **Production Feature Store at scale** (Tecton, SageMaker Feature Store): enterprise-grade managed feature stores require paid subscriptions. Feast (open-source) and Hopsworks (free tier) cover the concepts adequately for learning.
- **Official certificate of completion:** Coursera audit mode and most vendor docs don't issue free certificates. DataTalks.Club Zoomcamps (Data Engineering, LLM) offer free certificates with live cohort completion and peer review — worth timing around their cohort start dates if credentials matter.

---

## Appendix A — 2026 Data Professional Certification Roadmap

> Source: José Siles' "2026 Data Professional Certification Matrix." Only pursue certifications *after* completing the relevant IBM courses — certifications without hands-on experience rarely land jobs.

### When to certify

Complete at minimum 2 project checkpoints in the platform before attempting its certification exam. A cert without a project portfolio is weak; a project portfolio without a cert is still hirable.

### Azure Track

| Cert | Role | Prereqs in This Plan | Link |
|---|---|---|---|
| DP-900: Azure Data Fundamentals | All roles (entry) | Course 12, Course 9 | [Microsoft Learn](https://learn.microsoft.com/en-us/certifications/exams/dp-900/) |
| PL-300: Power BI Data Analyst Associate | Data Analyst | Course 10 | [Microsoft Learn](https://learn.microsoft.com/en-us/certifications/exams/pl-300/) |
| DP-700: Fabric Data Engineer Associate | Data Engineer | Course 8, Course 9 | [Microsoft Learn](https://learn.microsoft.com/en-us/certifications/exams/dp-700/) |
| DP-100: Azure Data Scientist Associate | Data Scientist | Course 13, Course 15 | [Microsoft Learn](https://learn.microsoft.com/en-us/certifications/exams/dp-100/) |
| AI-102: Azure AI Engineer Associate | AI Engineer | Course 15 | [Microsoft Learn](https://learn.microsoft.com/en-us/certifications/exams/ai-102/) |

### AWS Track

| Cert | Role | Prereqs in This Plan | Link |
|---|---|---|---|
| DEA-C01: AWS Certified Data Engineer – Associate | Data Engineer | Courses 8, 9, 11, 12 | [AWS Training](https://aws.amazon.com/certification/certified-data-engineer-associate/) |
| MLA-C01: AWS ML Engineer – Associate | ML Engineer | Course 13, Course 15 | [AWS Training](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/) |
| MLS-C01: AWS ML Specialty | Data Scientist | Course 13, Course 15 | [AWS Training](https://aws.amazon.com/certification/certified-machine-learning-specialty/) |

### Google Cloud Track

| Cert | Role | Prereqs in This Plan | Link |
|---|---|---|---|
| Google Cloud Data Analytics Professional Certificate | Data Analyst | Enhancement A, Course 10 | [Coursera](https://grow.google/certificates/data-analytics/) |
| Professional Data Engineer | Data Engineer | Courses 8, 9, 11, 12 | [Google Cloud](https://cloud.google.com/certification/data-engineer) |
| Professional Machine Learning Engineer | ML Engineer | Course 13, Course 15 | [Google Cloud](https://cloud.google.com/certification/machine-learning-engineer) |

### Snowflake Track

| Cert | Role | Prereqs in This Plan |
|---|---|---|
| SnowPro Core | All DE/DS/DA roles | Course 9 |
| SnowPro Advanced: Data Engineer | Data Engineer | Course 9 + Enhancement C |
| SnowPro Advanced: Data Analyst | Data Analyst | Course 9 + Course 10 |
| SnowPro Advanced: Data Scientist | Data Scientist | Course 13 + Course 9 |

All SnowPro prep: [Snowflake University](https://www.snowflake.com/en/data-cloud/overview/hands-on-essentials/) (free trial + free badge courses).

### Databricks Track

| Cert | Role | Prereqs in This Plan |
|---|---|---|
| Databricks Certified Data Analyst Associate | Data Analyst | Enhancement A + Courses 10, 12, 13 + Course 9 |
| Databricks Certified Data Engineer Associate | Data Engineer | Courses 8, 11, 12 + Course 9 |
| Databricks Certified Data Engineer Professional | Senior DE | All above + Course 8 |
| Databricks Certified ML Associate | ML Engineer | Course 13 + Course 15 |
| Databricks Certified ML Professional | Senior ML | Course 13 + Course 15 (deep) |

All Databricks prep: [Databricks Academy free resources](https://www.databricks.com/learn/training/home) + [Databricks Community Edition](https://community.cloud.databricks.com/).

---

## Appendix B — Mahmoud Mohsen "Big-Data Analytics" Playlist: Full Index

> [Full playlist](https://www.youtube.com/playlist?list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI) · 20 videos · by [@MahmoudMohsen0](https://www.youtube.com/@MahmoudMohsen0)  
> Arabic-language, lecture-style. Strong conceptual clarity with visual diagrams. Total runtime ~13h. Referenced individually across Courses 2, 10, 11, 12, 13 and Enhancement D. Video #20 is a midterm-style revision session (Enhancement D).

| # | Title | Duration | Where used in this plan | Link |
|---|---|---|---|---|
| 1 | Big-Data concepts (Data Model) | 31 min | Course 12 | [▶](https://www.youtube.com/watch?v=AKSYxxDczEw&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=1) |
| 2 | Big-Data concepts (Distributed File System / GFS) | 30 min | Course 12 | [▶](https://www.youtube.com/watch?v=zAkMFWYnFHA&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=2) |
| 3 | Big-Data concepts (Distributed Computing / MapReduce) | 34 min | Course 12 | [▶](https://www.youtube.com/watch?v=NpQ-zwZPXaw&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=3) |
| 4 | MongoDB (MongoDB vs RDBMS) | 17 min | Course 11 | [▶](https://www.youtube.com/watch?v=8CJbtQd8qRg&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=4) |
| 5 | MongoDB (Operations 1) | 31 min | Course 11 | [▶](https://www.youtube.com/watch?v=uk08KAZaE2k&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=5) |
| 6 | MongoDB (Operations 2) | 34 min | Course 11 | [▶](https://www.youtube.com/watch?v=2bhJkI6oW9I&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=6) |
| 7 | MongoDB (MapReduce / Relations) | 34 min | Course 11 | [▶](https://www.youtube.com/watch?v=TcjxLAXodyU&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=7) |
| 8 | Hadoop Distributed File System | 43 min | Course 12 | [▶](https://www.youtube.com/watch?v=4DuFZNVE090&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=8) |
| 9 | Python (Basics 1) | 40 min | Course 2 | [▶](https://www.youtube.com/watch?v=joztCLdwdnQ&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=9) |
| 10 | Python (Basics 2) | 48 min | Course 2 | [▶](https://www.youtube.com/watch?v=Erpsy8RJ9ms&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=10) |
| 11 | Python (NumPy) | 53 min | Course 2 | [▶](https://www.youtube.com/watch?v=gcVHEjSBB8I&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=11) |
| 12 | Python (Pandas 1) | 41 min | Course 2 | [▶](https://www.youtube.com/watch?v=TFo7ZkFIPCA&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=12) |
| 13 | Python (Pandas 2) | 38 min | Course 2 | [▶](https://www.youtube.com/watch?v=neh_0SiPuJI&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=13) |
| 14 | Data Analysis (Intro to AI / Regression Algorithms) | 47 min | Course 13 | [▶](https://www.youtube.com/watch?v=OdB_oiXMk8A&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=14) |
| 15 | Data Analysis (Classification Algorithms) | 53 min | Course 13 | [▶](https://www.youtube.com/watch?v=error0K9BSE&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=15) |
| 16 | Data Analysis (Clustering Algorithms / Deep Learning) | 39 min | Course 13 | [▶](https://www.youtube.com/watch?v=N0xFjJv5GSc&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=16) |
| 17 | Apache Spark (Introduction / RDDs) | 55 min | Course 12 | [▶](https://www.youtube.com/watch?v=tejR_7HgXcc&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=17) |
| 18 | Apache Spark (DataFrames / MLlib / Streaming) | 55 min | Course 12 | [▶](https://www.youtube.com/watch?v=mp7LFZFfDAU&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=18) |
| 19 | Data Visualization and Case Studies | ~45 min | Course 10 | [▶](https://www.youtube.com/watch?v=Lo2Byt-V_jQ&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=19) |
| 20 | Revision (Midterm Solutions) | 42 min | Enhancement D | [▶](https://www.youtube.com/watch?v=6sOaYh5DhBo&list=PLQhTr3lsMLujYMxra8scZxLTS_0J5PyQI&index=20) |

### بالعربي Big Data — Ahmed Sami ([@bigdata4756](https://www.youtube.com/@bigdata4756))

> Arabic-language Big Data & Data Engineering channel by Ahmed Sami. All content free, no copyright restrictions. Channel: [youtube.com/@bigdata4756](https://www.youtube.com/@bigdata4756). Each series mapped to the IBM course section it reinforces.
>
> **Note on URLs:** Individual video IDs for the Hadoop sub-series and the long-form series (Linux, Git, Docker, SQL) could not be independently verified via oEmbed during this session — search engines returned inconsistent or invalid IDs. All links below point to the channel page for those entries; use the title to locate the video. Entries marked **†** have oEmbed-confirmed IDs. Durations marked **\*** are sourced from consistent search results (not oEmbed-verified).

| # | Title (Arabic / English) | Duration | IBM Course Section | Link |
|---|---|---|---|---|
| 1 | Python - The Basics - Part 1 / جحر السوعبان | ~6h* | Course 2 — Python for Data Science | [▶](https://www.youtube.com/@bigdata4756) |
| 2 | Python - The Basics - Part 2 / السوعبان صديقي **†** | ~2h36min* | Course 2 — Python for Data Science | [▶](https://www.youtube.com/watch?v=mlbe7Vxr7yA) |
| 3 | SQL for Data Analysis / شاهد كيف أصبح الفيل والدرفيل أصدقاء | 10h 20min 6sec ✓ | Course 5 — Databases and SQL for Data Science | [▶](https://www.youtube.com/@bigdata4756) |
| 4 | Visual Studio Code / هنشخبط الكود على إيه؟ **†** | ~57min* | Course 6 — Linux Commands and Shell Scripting | [▶](https://www.youtube.com/watch?v=DsJOSKyxqMc) |
| 5 | Git and GitHub / شخبط وانت متطمن | ~6h* | Course 6 — Linux Commands and Shell Scripting | [▶](https://www.youtube.com/@bigdata4756) |
| 6 | Linux for Data Engineers / البطريق العضاض يعظ | 11h 24min 48sec ✓ | Course 6 — Linux Commands and Shell Scripting | [▶](https://www.youtube.com/@bigdata4756) |
| 7 | What is Big Data? / أيه هي البيج داتا؟ | ~9min* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |
| 8 | Installing Hadoop Part 1 / يلا نسطّب هادووب | ~39min* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |
| 9 | Installing Hadoop Part 2 / يلا نسطّب هادووب | ~17min* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |
| 10 | Installing Hadoop Part 3 / يلا نسطّب هادووب | ~17min* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |
| 11 | Installing Hadoop Part 4 / يلا نسطّب هادووب | ~17min* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |
| 12 | MapReduce / خطط واختصر | ~27min* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |
| 13 | The Hadoop Distributed File System / غرائب وعجائب هادووب في تخزين الملفات والحاجات | ~28min* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |
| 14 | YARN / توزيع الأرزاق | ~28min* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |
| 15 | Hadoop I/O / الملفات المفعوصة في الحفظ والصون | ~21min* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |
| 16 | Docker and Kubernetes / العلبة دي فيها سوعبان | ~10h* | Course 12 — Big Data with Spark and Hadoop | [▶](https://www.youtube.com/@bigdata4756) |

---

## Hour Summary

| Block | Content | IBM Hours | Supplement Hours | Combined |
|---|---|---|---|---|
| Courses 1–7 (Foundations) | Python, SQL, Linux, RDBMS, DBA | 120h | 96h | ~216h |
| Courses 8–11 (Core DE) | ETL, DW, BI, NoSQL | 64h | 159h | ~223h |
| Courses 12–13 (Big Data & ML) | Spark, Hadoop, MLlib | 36h | 171h | ~207h |
| Course 14 (Capstone) | End-to-end project | 18h | 25h | ~43h |
| Courses 15–16 (Career & AI) | GenAI, interview prep | 24h | 82h | ~106h |
| **IBM Track Subtotal** | | **262h** | **525h** | **~787h** |
| Post-Track Enhancements (A-D) | Hive/Impala/Pig, Ranger/Atlas, dbt/observability, revision, Kestra | — | 63h | ~63h |
| Enhancements E-G (new) | Lakehouse, Architecture Patterns, Cataloging | — | 30h | ~30h |
| Enhancements H-I (new) | Bruin Unified Platform, Capstone Pipeline Project | — | 30h | ~30h |
| **Full Plan Total** | | **262h** | **648h** | **~910h** |

> **Realistic estimate:** Following the IBM track as your primary path and adding supplements selectively based on weak areas → **~400–500h**. If you already have Python/SQL/Linux experience, skip Courses 1–7 supplements and save ~50h immediately.

**Variance note:** The biggest swing factor remains your existing SQL/Python/Linux fluency. If you're comfortable with Courses 1–7 topics already, focus only on the IBM courses for those sections and skip supplements. If new to Airflow and Kafka, add a 10h buffer to Course 8. The supplement resources are depth insurance — the IBM track alone gives you a solid foundation for entry-level DE roles.