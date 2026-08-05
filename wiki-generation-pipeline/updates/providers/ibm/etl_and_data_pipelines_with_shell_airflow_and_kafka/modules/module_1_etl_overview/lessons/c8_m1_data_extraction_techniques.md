**Course 8:** ETL and Data Pipelines with Shell, Airflow and Kafka
**Module 1:** Extract, Transform, Load (ETL) Overview

# Data Extraction Techniques

## Learning Objectives

After watching this video, you will be able to list examples of raw data sources, describe data extraction techniques, and relate use cases with data sources and extraction techniques.

## Raw Data Sources

Here are some examples of raw data sources:

- **Archived text and images** from paper documents and PDFs.
- **Web pages**, including text, tables, images, and links.
- **Analog audio and video**, which can be recorded on media such as magnetic tapes, or streaming in real time.
- **Survey data, statistical, and economic data**, and transactional data from business, financial, real estate, and point of sale or POS transactions.

Here are more examples of raw data sources:

- **Event-based data** such as social media streams, weather data from weather station networks, internet of things, or IoT sensor streams.
- **Medical records**, such as prescription history, medical treatments, and medical images, and also personal genetic data encoded in DNA and RNA samples.

Evidently, data is everywhere, and much of it is highly sensitive and personal and needs to be very carefully guarded for privacy and other concerns.

[ENRICHED: defined "POS (Point of Sale) transactions" — records generated at the moment a customer makes a purchase, capturing item details, quantity, price, payment method, timestamp, and store/location. POS data is a primary source for retail analytics: inventory management, sales forecasting, and customer behavior analysis.] [ENRICHED: ecosystem — data privacy regulations like GDPR (EU), CCPA (California), HIPAA (US healthcare), and LGPD (Brazil) impose strict requirements on how personal and sensitive data is collected, stored, and processed. Extraction pipelines must implement data masking, encryption, and access controls at the extraction stage to avoid regulatory violations. This is why "carefully guarded" is not optional — it is a legal requirement.]

## Data Extraction Techniques

There are many techniques for extracting data, depending on the kind of data source and the intended use of the data. Examples include:

### Optical Character Recognition (OCR)

**Optical character recognition or OCR**, which is used to interpret and digitize text scanned from paper documents so it can be stored as a computer readable file.

[ENRICHED: concrete example — a bank processes 10,000 paper loan applications per day. Each application is scanned into a TIFF image. An OCR pipeline (using tools like Tesseract, AWS Textract, or Azure Form Recognizer) extracts the applicant's name, income, loan amount, and signature from the image into structured JSON fields, which are then loaded into the loan processing database. Without OCR, each application would require manual data entry.]

### Analog-to-Digital Converters (ADCs)

**Analog to digital converters or ADCs**, which can digitize analog audio recordings and signals.

[ENRICHED: defined "ADC (Analog-to-Digital Converter)" — a hardware device or circuit that converts continuous analog signals (sound waves, voltage levels, temperature readings) into discrete digital values (binary numbers) that computers can process. ADCs sample the analog signal at regular intervals (the sampling rate, measured in Hz) and quantize each sample to a digital value. A CD-quality audio ADC samples at 44,100 Hz with 16-bit resolution, producing 44,100 discrete amplitude measurements per second.]

### Charge-Coupled Devices (CCDs)

**Charge couple devices or CCDs** that capture and digitize images.

[ENRICHED: defined "CCD (Charge-Coupled Device)" — a semiconductor image sensor that converts light into electrical charge. Each pixel on the CCD accumulates charge proportional to the light intensity it receives. The charges are then read out sequentially and converted to digital values, producing a digital image. CCDs were the dominant sensor in digital cameras and scientific imaging until CMOS sensors largely replaced them in consumer devices due to lower power consumption and cost. CCDs remain preferred in astronomy and microscopy for their superior noise characteristics.]

### Polling and Census Methods

**Opinions, questionnaires, and vital statistical data** obtained through polling and Census methods.

[ENRICHED: concrete example — the US Census Bureau conducts a decennial census (every 10 years) and the American Community Survey (ACS, ongoing). The census collects data on population count, age, race, housing status, and income from every household. The ACS samples 3.5 million addresses annually and produces estimates of demographic and economic characteristics used for federal fund allocation, congressional apportionment, and business planning. Extraction from census data typically uses the Census Bureau's API or pre-packaged CSV downloads.]

### Behavioral Tracking

**Cookies, user logs, and other methods** used for tracking human or system behavior.

[ENRICHED: defined "cookies" — small text files stored in a user's web browser by a website. Session cookies track a user's activity within a single visit; persistent cookies remember preferences across visits. Third-party cookies, set by domains other than the one being visited, enable cross-site tracking for advertising analytics. Note: third-party cookies are being phased out by major browsers (Chrome, Safari, Firefox) due to privacy concerns, driving the shift toward first-party data collection strategies.] [ENRICHED: defined "user logs" — automatically generated records of user interactions with a system. Web server logs record every HTTP request (IP address, timestamp, URL, user agent, response code). Application logs record business events (login, purchase, search query). System logs record infrastructure events (CPU usage, disk I/O, error messages). These logs are a primary data source for user behavior analytics, debugging, and security auditing.]

### Web Scraping

**Web scraping** used to crawl web pages and search of text images, tables, and hyperlinks.

[ENRICHED: concrete example — a competitive intelligence team scrapes a competitor's e-commerce website daily: product names, prices, descriptions, and availability status are extracted using Python's `requests` library to fetch HTML and `BeautifulSoup` to parse the DOM. The extracted data feeds a price monitoring dashboard that alerts the team when the competitor changes pricing on overlapping products.]

### APIs

**APIs**, which are readily available for extracting data from all online data repositories and feeds, such as government bureaus of statistics, libraries, weather networks, online shopping, and social networks.

[ENRICHED: defined "API (Application Programming Interface)" — a set of protocols and endpoints that allow one software application to request data or services from another. In data extraction, REST APIs are most common: the extractor sends an HTTP request (GET, POST) to a defined endpoint URL with authentication credentials, and receives a structured response (usually JSON or XML). APIs provide programmatic, reliable, and often rate-limited access to data, making them preferable to web scraping for data sources that offer them.] [ENRICHED: concrete example — extracting weather data from the OpenWeatherMap API: send a GET request to `api.openweathermap.org/data/2.5/weather?lat=40.71&lon=-74.01&appid=API_KEY`, receive a JSON response containing temperature, humidity, wind speed, and conditions for New York City. Rate limits: 60 calls/minute on the free tier.]

### SQL and NoSQL Query Languages

**SQL languages** for querying relational databases, and **NoSQL** for querying, document, key value, graph, or other non-structured data repositories.

[ENRICHED: defined "NoSQL" — a category of database systems that do not use the traditional relational (table-based) model. Four main types: document stores (MongoDB, Couchbase — store JSON-like documents), key-value stores (Redis, DynamoDB — simple key→value pairs), graph databases (Neo4j, Amazon Neptune — nodes and edges), and wide-column stores (Cassandra, HBase — rows with flexible columns). NoSQL databases are chosen for horizontal scalability, flexible schemas, and high throughput on non-relational data patterns.] [ENRICHED: concrete example — extracting from a document store: using MongoDB's aggregation pipeline to query a `user_events` collection, filtering by event type and date range, grouping by user_id, and computing session duration totals. Extracting from a graph database: using Cypher query language in Neo4j to traverse a social network graph, finding all friends-of-friends of a given user within 2 hops.]

### Edge Computing Devices

**Edge computing devices**, such as video cameras that have built-in processing that can extract features from raw data.

[ENRICHED: defined "edge computing" — a distributed computing paradigm where data processing occurs near the data source (the "edge" of the network) rather than in a centralized cloud data center. This reduces latency (no round-trip to the cloud), reduces bandwidth costs (only processed features are transmitted, not raw data), and enables real-time decision-making. Examples: a security camera running on-device object detection and only transmitting bounding box coordinates (not the full video feed), or a factory sensor computing vibration frequency locally and sending only the anomaly flag.] [ENRICHED: ecosystem — edge computing is a critical enabler for IoT data extraction at scale. The alternative — transmitting all raw sensor data to the cloud — is often impractical due to bandwidth limits (a single 4K camera produces ~15 Mbps of raw video) and latency requirements (autonomous vehicles need sub-10ms response times, not achievable with cloud round-trips). Frameworks like TensorFlow Lite and ONNX Runtime enable running trained ML models directly on edge devices.]

### Biomedical Devices

Finally, **biomedical devices**, such as microfluidic arrays, that can extract DNA sequences.

[ENRICHED: defined "microfluidic array" — a device that manipulates tiny volumes of fluid (nanoliters to picoliters) through microscopic channels on a chip. In genomics, microfluidic arrays are used in next-generation sequencing (NGS) platforms (e.g., Illumina) to prepare and sequence DNA fragments in parallel, producing millions of short DNA reads simultaneously. The extraction technique here is converting biological DNA samples into digital sequence data that bioinformatics pipelines can analyze.]

## Use Cases

Here are a few high-level examples of use cases along with their raw data sources and extraction techniques:

- You can use **APIs** to extract data from **multiple structured data sources** for integration into a central repository.
- You can also use **APIs** to capture **periodic or asynchronous events** to store them in a history archive.
- Rather than transmitting potentially very large volumes of redundant data from **IoT devices**, you can use **edge computing** to reduce that data volume by extracting features of interest from the raw data. Often this kind of extraction at the source is impractical, so the data is migrated to storage as is for further processing, analysis, or modeling.
- Also, you can use **medical imaging devices** and **biometric sensors** to acquire data for diagnostic purposes.

## Summary

In this video, you learned that some examples of raw data sources are archive, text, and images from paper documents and PDFs and pages, including text, tables, images, and links. Many extraction techniques rely on sophisticated technology to capture information from raw data. SQL, NoSQL, web scraping, and APIs are important techniques for extracting data, and you can use medical imaging devices and biometric sensors to acquire data for diagnostic purposes.

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | POS transactions | Definition | Defined POS transactions with retail analytics use case | HIGH |
| 2 | Data privacy paragraph | Ecosystem | Connected "carefully guarded" to GDPR, CCPA, HIPAA, LGPD regulations | HIGH |
| 3 | OCR section | Concrete example | Bank loan application OCR pipeline: scan→Tesseract/Textract→JSON→database | HIGH |
| 4 | ADC section | Definition | Defined ADC as analog→digital converter with sampling rate and quantization explanation | HIGH |
| 5 | CCD section | Defined CCD as semiconductor image sensor, noted CMOS replacement in consumer devices | HIGH |
| 6 | Polling section | Concrete example | US Census Bureau decennial census + ACS: 3.5M addresses, API/CSV extraction | HIGH |
| 7 | Cookies section | Definition | Defined session vs persistent vs third-party cookies, noted third-party phase-out | HIGH |
| 8 | User logs section | Defined web server logs, application logs, system logs with use cases | HIGH |
| 9 | Web scraping section | Concrete example | Competitive intelligence: daily competitor price scraping with BeautifulSoup | HIGH |
| 10 | APIs section | Definition | Defined API as protocol+endpoint for inter-application data requests | HIGH |
| 11 | APIs section | Concrete example | OpenWeatherMap REST API: GET request → JSON response with rate limits | HIGH |
| 12 | NoSQL section | Defined NoSQL 4 types: document, key-value, graph, wide-column with examples | HIGH |
| 13 | NoSQL section | Concrete example | MongoDB aggregation pipeline + Neo4j Cypher traversal examples | HIGH |
| 14 | Edge computing section | Defined edge computing: processing near source, reduced latency/bandwidth | HIGH |
| 15 | Edge computing section | Ecosystem | Connected edge to IoT scale, TF Lite/ONNX Runtime, 4K camera 15 Mbps example | HIGH |
| 16 | Biomedical section | Defined microfluidic array and NGS (Illumina) DNA sequencing | HIGH |

<!-- EXTRACTION_CHECKLIST: 36 sentences extracted, 36 sentences in output -->
