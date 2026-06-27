# A Day in the Life of a Data Engineer

*Told through the story of Sarah Flinch, a Data Engineer at a multinational hair care company.*

## Business Context

The company is launching a new shampoo in a market where social media sentiment can make or break a product launch. The business team needs to monitor customer sentiment across social media and online platforms in real time — broken down by demographic, across multiple channels — from day one of the launch.

**Platforms to monitor:** Social media (Twitter, Facebook, Instagram), eCommerce platforms (product reviews), bloggers and media (review blogs, articles).

**What to track:** Positive feedback, negative comments, suggestions/feature requests, competitor comparisons.

## From Prototype to Production

The **Data Science team** had already built a prototype dashboard using a sentiment analysis algorithm with dummy data — showing graphs of sentiment scores plotted across time, broken down by source and demographic. The prototype was well-received by the business team. **This is where the Data Engineering team stepped in** — to turn the prototype into a production-ready, real-data system.

## The Engineering Workflow

### Step 1 — Data Collection via APIs
Sarah pulled data from social media APIs (Twitter, Facebook) — tweets and posts containing the product hashtag — in structured JSON format. APIs are the standard method for programmatically retrieving data, allowing engineers to request specific data and receive it in a structured format for further processing. All collected data was moved into temporary storage.

### Step 2 — Data Collection via Web Scraping
For sources without APIs (eCommerce portals, review blogs), Sarah used web scraping to extract review text, star ratings, and reviewer demographics from HTML. Web scraping navigates to a URL, reads the HTML content, and extracts specific data elements. This data was also moved into temporary storage.

### Step 3 — Temporary Staging
All raw data was moved into temporary storage — a staging area where raw data sits before transformation. This is a standard pattern in data engineering: raw data is held in an intermediate location before being processed, allowing engineers to inspect, validate, and plan transformations without affecting source systems.

### Step 4 — Data Inspection
With all raw data collected and staged, Sarah examined the data to understand what transformations would be needed. She assessed format diversity across sources:

| Content Type | Format Characteristics |
|-------------|----------------------|
| Tweets | Short text, hashtags, emojis, @mentions, URLs, timestamps |
| Facebook Posts | Longer text, reactions, comment threads, media attachments |
| eCommerce Reviews | Star ratings, structured review text, verified purchase flags |
| Blog Articles | Long-form text, HTML markup, embedded images, author metadata |
| Memes | Image-based, often with embedded text — unstructured |

This diversity is a hallmark of real-world data engineering: sources rarely conform to a single format, and the engineer must assess and plan for every variation before writing transformation code.

### Step 5 — Data Processing with Python
After inspection, Sarah and her team designed and built a Python program to handle all processing tasks. Python is the dominant language in data engineering for pipeline logic, data manipulation, and integration with external services and algorithms. The program handled:

| Processing Task | Description |
|----------------|-------------|
| Cleaning | Removing duplicates, nulls, irrelevant HTML tags |
| Normalization | Standardizing formats — date formats, text encoding, casing |
| Transformation | Reshaping raw data into the schema required by the database |
| Sentiment Preparation | Formatting text fields for the sentiment analysis algorithm |

### Step 6 — Loading to Database
Clean, transformed data was loaded into the production database that the dashboard queries. This follows the classic ETL pattern: Extract (APIs + web scraping) → Transform (Python processing) → Load (production database) → Dashboard (data scientists view).

### Step 7 — Validation with Data Scientists
Output matched the prototype — sentiment scores, demographic breakdowns, and source-level graphs rendered correctly.

### Step 8 — Building the Automated Pipeline

After the initial load, a critical limitation emerged: every time business users wanted updated sentiment data, they would have to submit a new request to the data engineering team to re-run the collection and processing. This manual workflow creates a bottleneck, introduces latency, and removes the self-service capability that business teams need. The final and most impactful step was operationalizing the one-time ETL into an ongoing automated pipeline running without manual intervention.

| Before Pipeline | After Pipeline |
|----------------|----------------|
| Manual request for each update | Automatic updates on schedule/trigger |
| Data engineers are bottleneck | Business users are fully self-service |
| Hours/days between data and dashboard | Real-time or near-real-time visibility |
| Error-prone manual re-runs | Monitored, automated, reliable process |

## APIs vs. Web Scraping

| Dimension | APIs | Web Scraping |
|-----------|------|-------------|
| How it works | Structured endpoint call | Parse HTML to extract data |
| Data format | Typically JSON/XML | Raw HTML — requires parsing |
| Reliability | High — designed for programmatic access | Lower — breaks if site HTML changes |
| Rate limits | Usually enforced by platform | Depends on site; may need throttling |
| Legal/ToS | Generally permitted within terms | Must check site's terms of service |

## Key Concepts Illustrated

| Concept | How It Appeared in Sarah's Project |
|---------|-----------------------------------|
| Data Collection | APIs for social media, web scraping for eCommerce and blogs |
| Temporary / Staging Storage | Raw data held before transformation |
| Data Inspection | Assessing format diversity before writing transformation logic |
| ETL Pipeline | Extract (API/scrape) → Transform (Python) → Load (database) |
| Data Cleaning | Removing duplicates, nulls, irrelevant markup |
| Data Transformation | Reshaping raw heterogeneous data into a consistent database schema |
| Pipeline Automation | Moving from one-time load to ongoing, self-service data flow |
| Collaboration | Working with Data Scientists (prototype) and Business Users (requirements) |
| Analytics-Ready Data | The final database output — accurate, accessible, formatted for the dashboard |

## Key Takeaways

- Data engineering projects begin with a business need — the technical work always serves a specific organizational goal
- Real-world data comes in diverse formats — tweets, reviews, articles, memes — requiring planned transformations for each
- APIs and web scraping are complementary collection techniques chosen based on what the source platform provides
- A one-time ETL run is not a solution — it must be automated into a pipeline for genuine business value
- The end goal is real-time, self-service access for business users, with engineering disappearing into the background

## Glossary

| Term | Definition |
|------|------------|
| Sentiment Analysis | An NLP technique that scores text as positive, negative, or neutral |
| API | Application Programming Interface — structured data exchange between programs |
| Web Scraping | Automated extraction of data from web pages by parsing HTML |
| Temporary Storage | A staging area where raw data is held before transformation and loading |
| Data Pipeline | An automated, ongoing ETL process without manual intervention |
| Dashboard | A visual interface displaying data metrics and reports for business users |
| Schema | The defined structure of a database — tables, columns, types, relationships |
| Real-Time Data | Data processed and made available immediately as it is generated |

[Cross-ref: topics/data_engineering_scope.md — the four pillars illustrated in practice (collect → process → store → make available)]
[Cross-ref: topics/data_roles_overview.md — how the Data Engineer role manifests in real project work]
