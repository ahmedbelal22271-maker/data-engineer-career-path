# Output Mapping

Maps all 34 wiki topic pages to the downstream HTML wiki output at `output/option_a/index.html`. Cards are organized into 7 sections plus a glossary.

---

## Section 1: Landing / Overview

| Card Title | Primary Source Page | Description |
|------------|--------------------|-------------|
| Data Engineering Scope | data_engineering_scope.md | Core definition, four pillars, lifecycle stages |
| Modern Data Ecosystem | modern_data_ecosystem.md | Ecosystem entities, stages, emerging tech, build vs buy |

**Key content:** Core DE definition, collect/process/store/consume pillars, ecosystem overview, team sport framing.

**Contradictions/caveats:** None. **Coverage confidence:** HIGH.

---

## Section 2: Foundations — Defining Data Engineering

| Card Title | Primary Source Page | Description |
|------------|--------------------|-------------|
| Practitioner Definitions | defining_data_engineering.md | "Plumbers of data," three-role comparison, four guarantees |
| Evolution of Data Engineering | evolution_of_data_engineering.md | Five major shifts, then vs now, what hasn't changed |

**Key content:** Practitioner perspectives, historical context, role differentiation.

**Contradictions/caveats:** None. **Coverage confidence:** HIGH.

---

## Section 3: Data Roles and Responsibilities

| Card Title | Primary Source Page | Description |
|------------|--------------------|-------------|
| Role Landscape | data_roles_overview.md | DE, DA, DS, BA/BIA role definitions |
| DE Specializations | data_engineering_specializations.md | DWE, Data Architect, Data Manager, DBA |
| Role Deep Dive & Comparisons | role_comparisons_deep_dive.md | Cross-role tables, interaction map, tools, best practices, common pitfalls |
| Day in the Life | day_in_the_life.md | Practitioner narrative with concrete task examples |

**Key content:** Comprehensive role taxonomy, comparison framework, specialization paths, practical narrative.

**Contradictions/caveats:** None. **Coverage confidence:** HIGH.

---

## Section 4: Skills and Qualities

| Card Title | Primary Source Page | Description |
|------------|--------------------|-------------|
| Skill Taxonomy | skills_and_responsibilities.md | Technical/functional/soft skills with tools and examples |
| Practitioner Viewpoints | practitioner_skills_viewpoints.md | Four essential skills, real-world tool stacks, industry variability |

**Key content:** Analytics-ready data goal, three skill categories, essential skills, specialization vs breadth.

**Contradictions/caveats:** None (formal taxonomy and practitioner views complement each other). **Coverage confidence:** HIGH.

---

## Section 5: Data Ecosystem — Types, Sources, and Languages

| Card Title | Primary Source Page | Description |
|------------|--------------------|-------------|
| Types of Data | data_types.md | Structured, semi-structured, unstructured classification |
| File Formats | file_formats.md | CSV, JSON, XML, Parquet, Avro, ORC trade-offs |
| Data Sources | data_sources.md | Source categories, integration overview, data ecosystem landscape |
| Languages for Data Professionals | languages_for_data_pros.md | Query, programming, shell/scripting, markup languages |
| Metadata Management | metadata_management.md | Technical/business/operational metadata, data catalog, lineage |

**Key content:** Complete taxonomy of data types, formats, sources, and languages with metadata governance.

**Contradictions/caveats:** C-4 resolved (structured/semi-structured boundary clarified). **Coverage confidence:** HIGH.

---

## Section 6: Data Storage and Repositories

| Card Title | Primary Source Page | Description |
|------------|--------------------|-------------|
| Data Repositories | data_repositories.md | Transactional vs analytical, selection criteria, viewpoints |
| Relational Databases | relational_databases.md | RDBMS principles, ACID, normalization, SQL, indexes, transactions |
| NoSQL Databases | nosql_databases.md | Four categories, CAP theorem, BASE, use case guidance |
| Data Warehouses, Lakes, Lakehouses | data_warehouses_lakes.md | DW vs DM vs DL vs lakehouse comparison |
| Unstructured Data Storage | unstructured_data_storage.md | Object storage, blob, HDFS, NAS/SAN, selection criteria |

**Key content:** Full storage spectrum — from relational to NoSQL to warehouse/lake to unstructured.

**Contradictions/caveats:** C-5 resolved (ELT dominance for lakes). **Coverage confidence:** HIGH.

---

## Section 7: Data Processing and Big Data Platforms

| Card Title | Primary Source Page | Description |
|------------|--------------------|-------------|
| ETL, ELT, and Data Pipelines | etl_elt_pipelines.md | ETL vs ELT, batch vs streaming, orchestration |
| Data Integration Platforms | data_integration_platforms.md | Platform categories, features, selection |
| Big Data Foundations | big_data_foundations.md | 5 Vs, Lambda vs Kappa, distributed principles |
| Hadoop Ecosystem | hadoop_ecosystem.md | HDFS, MapReduce, YARN, Hive, HBase, Spark |
| Data Platform Architecture | data_platform_architecture.md | Platform layers, design, security, viewpoints |
| SQL Vendors and Dialects | sql_vendors_dialects.md | MySQL, PostgreSQL, SQL Server, Oracle, Db2, SQLite comparisons |

**Key content:** Processing patterns, big data tools, platform design, SQL implementation diversity.

**Contradictions/caveats:** C-6 resolved (5 Vs with footnote about 3/7 Vs variants). **Coverage confidence:** HIGH.

---

## Section 8: Quiz and Exam Reference

| Card Title | Primary Source Page | Description |
|------------|--------------------|-------------|
| Quiz Study Reference | quiz_study_reference.md | Module 1 + Module 2 quiz concepts with explanations + Big Data quiz review |
| Weakness Review | checkpoint_weakness_review.md | Module 1 gap analysis with scenario-based exam logic |

**Key content:** All quiz content from both modules, scenario exam framework.

**Contradictions/caveats:** None. **Coverage confidence:** HIGH.

---

## Section 9: Course and Career

| Card Title | Primary Source Page | Description |
|------------|--------------------|-------------|
| Course Syllabus & Index | course_syllabus_and_index.md | 4-module syllabus with detailed content maps |
| 16-Course Sequence | course_sequence_16.md | Full IBM certificate course descriptions |
| Career Ladder | career_ladder.md | 5-level ladder + MVP fast-track (~192h) |
| Certification Roadmap | certification_roadmap.md | Azure, AWS, GCP, Snowflake, Databricks cert matrix |
| Enhancement Modules | enhancement_modules.md | Post-track modules A–D |

**Key content:** Complete course blueprint, career progression, certification planning.

**Contradictions/caveats:** None. **Coverage confidence:** HIGH.

---

## Glossary (Embedded)

| Source Page | Terms |
|-------------|-------|
| glossary.md | 81 terms covering all 34 pages (embedded directly into HTML, no separate card) |

---

## Coverage Summary

| Section | Cards | Confidence |
|---------|-------|------------|
| 1. Landing / Overview | 2 | HIGH |
| 2. Foundations | 2 | HIGH |
| 3. Data Roles | 4 | HIGH |
| 4. Skills & Qualities | 2 | HIGH |
| 5. Data Ecosystem | 5 | HIGH |
| 6. Data Storage | 5 | HIGH |
| 7. Data Processing & Big Data | 6 | HIGH |
| 8. Quiz Reference | 2 | HIGH |
| 9. Course & Career | 5 | HIGH |
| Glossary | 1 (embedded) | HIGH |
| **Total** | **34** | **100% coverage** |

**Pages not mapped:** 0
**Unresolved issues:** 0
