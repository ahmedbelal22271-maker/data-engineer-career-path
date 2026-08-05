# Data Engineering — Workspace Root

Root index for the entire data engineering learning workspace. Use this to orient yourself at the start of every session.

---

## Top-Level Directories

### `big data and data engineering plan/`
Master learning plan and updater tools.
- **`data-engineer-career-path/big_data_de_learning_plan.md`** — Full IBM DE + supplements plan (v11.3+, ~950h). Changelog tracks every revision. Companion files: `.wiki_coverage_log.md`, `.wiki_freshness_check.md`.
- **`study plan updater/`** — Tooling: `study_plan_v3.md` (plan document), `scrape_resources.py` (Playwright-based URL scraper), `study_plan_ai_agent_updater.md` (agent prompt for automated plan sync), `wiki_to_plan_sync_agent.md` (sync agent).
- **`updates/scraped_resources/`** — Raw scraped output from URL verification.

### `certificates/`
Completed certificates organized by provider.
- **`IBM Data Engineering Professional Certificate/`** — PDFs for completed IBM courses.
- **`UCSD Big Data Specialization/`** — UCSD Big Data Specialization certificates.
- **`Datacamp/`** — DataCamp track certificates (Data Engineer in Python, SQL Associate Data Engineer).
- **`NTI-ITIDA/`** — NTI Big Data Analysis certificate.

### `claude skills/`
Standalone skill files (not part of the wiki pipeline agent skill set).
- `prompt_engineering/SKILL.md`, `modern_engineering/SKILL.md`, `prompting_best_practice.md`.

### `Data enginner in python/`
DataCamp Python courses (typo preserved from original name).
- `Cleaning Data in Python/`, `Intermediate importing data in python/`, `Introduction to APIs in Python/`, `Writing efficient python code/`.

### `fabric-data-engineering/`
- `fabric-data-engineering.pdf` — Microsoft Fabric DE resource.

### `IBM Certificate content/`
Empty — placeholder for future extracted IBM content.

### `SQL associate data engineer career path/`
SQL-focused learning path.
- `SQL Fundamentals Skill Path/`, `Introduction to Snowflake SQL/`, `Data Warehousing concepts/`, `Associate Data Engineer in SQL.pdf`.

### `projects/`
Completed course projects — one neat subdirectory per project.
- **`course2-data-aggregator/`** — Course 2 project: World Bank GDP data aggregator (CSV + API, melt/merge, analysis notebook).
- **`course3-banks-project/`** — Course 3 Python project: banks ETL pipeline (web scraping, BeautifulSoup, pandas, SQLite). Script, outputs, docs, and screenshots.
- **`c4_coffee_shop_database_final_project/`** — Course 4 final project: Coffee Shop Database (SQL dumps, generated ERD, task screenshots, views, test script).
- **`c5_databases_and_sql_for_data_science_final_project/`** — Course 5 final project: Module 5 final project notebook.
- **`c6_linux_shell_scripting_final_project/`** — Course 6 final project: Linux shell scripting backup automation (backup.sh, crontab schedule, task screenshots).
- **`c9_data_warehouse_fundamentals_practice_project/`** — Course 9 practice project: consumer electronics retail data warehouse (star schema design, PostgreSQL, docker-compose, CSV data, task screenshots).
- **`c9_data_warehouse_fundamentals_final_project/`** — Course 9 final project: solid waste management company data warehouse (star schema, GROUPING SETS/ROLLUP/CUBE queries, materialized view, PostgreSQL + pgAdmin).
- *(prepared, not yet committed)* **`c8_etl_data_pipelines_with_shell_airflow_and_kafka_final_project/`** — Course 8 final project: Build ETL Data Pipelines with BashOperator using Apache Airflow (assignment PDF + enriched handouts).

### `updates/`
Transient raw course update files too large or unstructured for the wiki pipeline.
- `c1_m1_modern_data_ecosystem.md` through `c1_m4_final_project_guidelines.md`, `c2_full_course_index.md`, `c2_m1_*` files, `linkedin_posts/`.

### `wiki-generation-pipeline/`
The main wiki generation pipeline — processes course updates into `de_wiki/` and renders HTML. This is the primary workspace.

#### Core Files
| File | Purpose |
|---|---|
| `wiki.html` | Built single-file HTML wiki (GitHub Pages deployable) |
| `wiki_template.html` | HTML generation template |
| `build_html.py` | Markdown-to-HTML builder |
| `continuation_prompt.md` / `initialization_prompt.md` | Agent session prompts |
| `brain.md` / `aim.md` | Agent memory and goals |

#### `.agents/` — Agent Kernel
- **`AGENTS.md`** — THIS FILE. Agent configuration, protocols list, skills list, processing flow.
- **`protocols/`** — 27 protocols (directory organization, dedup, commits, debugging, error tracking, large files, etc.)
- **`skills/`** — 17 domain skills (data architecture, datalab, HTML/CSS, prompt engineering, study guides, etc.)
- `general_purpose_chat_init.md` — Multi-domain init prompt.

#### `de_wiki/` — Generated Wiki
Markdown topic files (~40+) covering:
- **Course 1:** Data ecosystem, data repositories, ETL/ELT, NoSQL, big data foundations
- **Course 2:** Python basics, data structures, NumPy, pandas, file I/O, APIs, web scraping
- **Course 3:** ETL pipelines, IDE development
- **AWS resources:** Big data, Spark, Kafka, Kinesis, streaming, security, RabbitMQ
- **UCSD:** Big Data Specialization topics
- **Governance/compliance, data roles, quiz study references**
- State tracking: `.lthp_state.json`, `log.md`, `index.md`

#### `scripts/`
- `build_wiki.py` — Wiki assembler
- `scrape_images.py` — Image extraction utility

#### `output/option_a/`
- `index.html` — Rendered HTML wiki (deployed to GitHub Pages)

#### `updates/` — Course Content Being Processed
| Subdirectory | Content |
|---|---|
| `course_1_intro_data_engineering/` | 23 files — C1 M1–M4 deep-dives, quizzes, summaries, viewpoints, weakness notes, final project guide (merged from former `ibm_data_engineering_foundations/`) |
| `course_2_python_data_science/` | 76+ files across 5 modules (Python basics, data structures, programming, NumPy/pandas, APIs/web scraping) + 32 Jupyter notebooks + course index |
| `course_3_python_project/` | 18 files — Course index, M1 ETL, IDE setup, labs, deep-dives + `code/` (project scripts, data, logs) + `screenshots/` (task screenshots) |
| `course_4_relational_databases/` | 5 files + `assets/` — course index, M1 course intro, information & data models (enriched with ERD types, data independence), ERDs & relationship types |
| `aws_resources/` | 20 files — AWS explainer pages (01–19 + ecosystem map) covering Spark, Kafka, Kinesis, streaming, security, RabbitMQ |
| `big_data_specialization_ucsd/` | UCSD Big Data Specialization index + Course 1 intro (6 modules, 150+ files) |
| `general/` | 10 files — data roles, file formats, data types, SQL dialects |
| `linkedin_posts/` | LinkedIn post drafts with images |
| `scraped_resources/` | Raw scraped Coursera course content (courses 11–23, 83 resources indexed) |
| `assets/` | `data_platform_architecture.png` |

### `index.html`
Built HTML wiki deployed to GitHub Pages.

### `*.txt` files (root)
`wiki_card_check.txt`, `wiki_end_check.txt`, `wiki_missing_check.txt`, `wiki_sidebar_check.txt` — Post-build validation outputs.

---

## Quick Reference

**Build the wiki:** `python scripts/build_wiki.py` (inside `wiki-generation-pipeline/`)
**Rebuild HTML:** `python build_html.py` (inside `wiki-generation-pipeline/`)
**Scrape URLs:** `python scrape_resources.py` (inside `study plan updater/`)
**Learning plan:** `big data and data engineering plan/data-engineer-career-path/big_data_de_learning_plan.md`

---

*Generated 2026-07-05. Update this file when adding major new directories.*
