> **Course 9:** Data Warehouse Fundamentals
> **Module 1:** An Introduction to Data Warehouses, Data Marts, and Data Lakes

# Selecting a Data Warehouse System

Welcome to "Selecting a Data Warehouse System." After watching this video, you will be able to: Identify criteria organizations can use to evaluate data warehouse systems; Describe key considerations for each data warehouse selection criteria; Summarize how organizations decide between an on-premises or a public cloud data warehouse system; List the various types of warehouse costs.

## Evaluation Criteria Overview

Let's look at the criteria businesses use to evaluate data warehouse systems, including features and capabilities, compatibility and implementation considerations, ease of use and skills, support considerations, and various costs. [ENRICHED: definition — Data warehouse evaluation is a structured process of assessing vendor solutions against organizational requirements across technical, operational, and financial dimensions. The five core criteria categories — features/capabilities, compatibility/implementation, ease of use/skills, support, and cost — form a weighted decision framework used by enterprise procurement teams. Source: GigaOm Key Criteria for Evaluating Data Warehouse Solutions] [Source: https://d.gigaom.com/report/key-criteria-for-evaluating-data-warehouse-solutions/]

## Location

One of the primary data warehouse features, or consideration, for an organization is location. Data warehouses can exist on-premises, on appliances, and on one or more cloud locations. To select a location, organizations must balance multiple demands related to data ingestion, storage, and access.

For some organizations, securing their data is their highest priority, requiring a mandatory on-premises solution. Multi-location businesses that grapple with data privacy requirements such as CCPA or GDPR need on-premises or geo-specific data warehouse locations. [ENRICHED: definition — CCPA (California Consumer Privacy Act) is a California state law that grants consumers rights over their personal data, including the right to know, delete, and opt-out of data sales. GDPR (General Data Protection Regulation) is the European Union's comprehensive data protection law that requires explicit opt-in consent for processing personal data of EU residents, with penalties up to €20 million or 4% of global revenue. Both regulations mandate strict data residency and handling requirements that directly influence where an organization can legally store and process data. Source: Usercentrics] [Source: https://usercentrics.com/knowledge-hub/gdpr-vs-ccpa-compliance/] [ENRICHED: performance context — The global data warehouse market is projected to reach $85.7 billion by 2032, with cloud data warehousing growing at approximately 27% annually. On-premises deployments remain prevalent in regulated industries (finance, healthcare, defense) where data sovereignty mandates require physical control over data location, while cloud deployments offer economies of scale with 99.9% uptime guarantees from major providers. Source: MetaOption LLC] [Source: https://erpsoftwareblog.com/2026/03/on-premise-vs-cloud-data-warehouse/]

Every organization balances security and data privacy requirements with the need for speed that delivers critical, profit-producing business insights.

## Features and Capabilities

Organizations will also want to consider features and capabilities related to architecture and structure.

Is the organization ready to commit to a vendor-specific architecture? Does the organization need multi-cloud installation such as multiple data warehouses in multiple locations? Does the solution scale to meet anticipated future needs? What data types are supported and what types of data does the organization ingest?

If your organization currently analyzes dark data or is planning for the implementation of using semi-structured and unstructured data, you'll want a data warehouse system that supports these data types. [ENRICHED: definition — Dark data is data that organizations collect but never analyze or use for any purpose — it sits idle in storage systems, consuming resources without generating value. Common examples include raw sensor data, old email archives, log files, and previous campaign data. According to industry estimates, organizations analyze only about 1-5% of their total data, leaving the vast majority as dark data. Source: IBM] [Source: https://www.ibm.com/think/topics/data-warehouse] And an organization that processes big data needs a system that supports both batch and streaming data. [ENRICHED: ecosystem — Batch processing handles large volumes of data at scheduled intervals (e.g., nightly ETL jobs), while streaming processing handles continuous data flows in real-time (e.g., IoT sensor data, clickstreams). Modern data warehouses increasingly support both paradigms through architectures like the lakehouse, which unifies batch and streaming on a single storage layer. Source: Databricks] [Source: https://www.databricks.com/blog/data-warehouse-tools]

Capabilities that affect the ease of implementation include data governance, data migration, and data transformation capabilities. [ENRICHED: definition — Data governance refers to the collection of processes, roles, policies, standards, and metrics that ensure the effective and efficient use of information in enabling an organization to achieve its goals. It encompasses data quality management, metadata management, data lineage, access control, and regulatory compliance. Source: Vertica] [Source: https://www.vertica.com/wp-content/uploads/2020/04/key-criteria-for-evaluating-data-warehouses-2-2.pdf] With the data warehouse system in place, how easily can the organization optimize and reoptimize system performance as needs change?

Another consideration is user management. With more organizations implementing a zero-trust security policy because of expensive data breaches, implementing programs that manage and validate system users is mandatory. [ENRICHED: definition — Zero-trust security is a cybersecurity model that requires strict identity verification for every person and device accessing resources on a private network, regardless of location. It operates on the principle of "never trust, always verify," assuming that threats can come from both inside and outside the network perimeter. This approach has become increasingly important as data breaches cost organizations an average of $4.45 million per incident. Source: IBM] [Source: https://www.ibm.com/think/topics/data-warehouse] And notifications and reports are essential for organizations to correct errors and mitigate risks before minor issues become larger problems.

## Ease of Use and Skills

Let's explore ease of use and skills.

Does your organization's staff have the skills needed to implement a specific data warehousing vendor's technology, and if not, how quickly and easily can they gain those skills? Complex, large data warehouse deployments can require additional work from your implementation partner, so their expertise also greatly matters. Finally, do the technology and engineering staff who architect, deploy, and administer front-end querying, reporting, and visualization tools have the skills needed to configure your new system quickly? [ENRICHED: ecosystem — Implementation partner expertise is critical because modern data warehouses involve complex integration across ETL/ELT pipelines, BI tools, data governance frameworks, and cloud infrastructure. Vendor selection often depends on the availability of certified implementation partners and the maturity of the partner ecosystem. Organizations should evaluate partner certifications, case studies, and domain expertise before committing to a platform. Source: GigaOm] [Source: https://d.gigaom.com/report/key-criteria-for-evaluating-data-warehouse-solutions/]

## Support Considerations

Next, let's review some support considerations.

Support is essential and can become frustrating and expensive if not well planned for. You might find that by using a single vendor, you can leverage one highly accountable, responsible source, potentially saving you time, money, and frustration. You'll also want to verify the availability of service level agreements for uptime, security, scalability, and other data warehouse system issues. [ENRICHED: definition — A Service Level Agreement (SLA) is a contractual commitment between a vendor and customer that defines the expected level of service, including uptime guarantees, performance metrics, response times for support tickets, and remedies for service failures. Enterprise data warehouse SLAs typically guarantee 99.9% to 99.99% uptime, which translates to approximately 8.7 hours to 52 minutes of allowed downtime per year. Source: AWS] [Source: https://aws.amazon.com/redshift/features/] Validate the vendor's support hours and channels, such as by phone, email, chat, or text. Finally, does the vendor offer self-service solutions and an active rich user community?

## Cost Evaluation

After all this analysis, it's time to evaluate and compare costs.

When calculating costs for a data warehouse system, consider more than the initial costs. Consider the total cost of ownership, or TCO, for running systems for several years. [ENRICHED: definition — Total Cost of Ownership (TCO) is a financial estimate that includes not just the initial purchase price but all direct and indirect costs associated with acquiring, deploying, operating, maintaining, and eventually retiring a technology system over its entire lifecycle. For data warehouses, TCO typically spans 5-7 years and can reveal that cloud solutions with lower upfront costs may ultimately exceed on-premises costs for stable, high-volume workloads. Source: TCOIQ] [Source: https://tcoiq.com/blog/tco-on-premises-vs-cloud.html] TCO includes:

- **Infrastructure** such as compute and storage costs – whether on-premises or on cloud; [ENRICHED: performance context — On-premises infrastructure costs include servers ($12,000-$25,000 per unit), SAN/NAS storage ($80,000-$200,000 for 100TB), networking equipment ($8,000-$30,000), and facility costs ($1,500-$4,000 per rack per year). Cloud infrastructure operates on pay-as-you-go models but can accumulate significantly over time — a mid-market company spending $800K on hardware refresh could see positive cloud ROI within 18-24 months depending on usage patterns. Source: TCOIQ] [Source: https://tcoiq.com/blog/tco-on-premises-vs-cloud.html]

- **Software licensing**, or in case of cloud offerings, their subscription or usage costs; [ENRICHED: ecosystem — On-premises software licensing typically involves perpetual licenses with annual maintenance fees (15-20% of license cost), while cloud offerings use subscription models (monthly/annual) or consumption-based pricing (per query, per compute-hour). Cloud pricing can be unpredictable for variable workloads, with costs escalating 40% or more during peak seasons without proper governance. Source: Data Consulting Firms] [Source: https://dataconsultingfirms.com/insights/data-platform-tco-analysis]

- **Data migration and integration costs** for moving data into the warehouse and pruning and purging as required; [ENRICHED: performance context — Data migration costs vary widely based on volume, complexity, and source systems. Enterprise migrations typically involve 3-6 months of planning and execution, with costs including data assessment, pipeline development, testing, validation, and cutover. Organizations should budget for parallel running periods during transition to ensure data integrity. Source: MetaOption LLC] [Source: https://erpsoftwareblog.com/2026/03/on-premise-vs-cloud-data-warehouse/]

- **Administration costs** for personnel to manage the systems and to train them; and [ENRICHED: ecosystem — On-premises data warehouses require dedicated teams including database administrators, systems engineers, network specialists, and security professionals. Organizations that transition to cloud platforms see approximately 25% reduction in administrative labor costs but must reinvest approximately 15% of those savings into FinOps governance to manage cloud consumption effectively. Source: Data Consulting Firms] [Source: https://dataconsultingfirms.com/insights/data-platform-tco-analysis]

- **Recurring support and maintenance costs** paid to the warehousing vendor or implementation partner.

## Key Takeaways

In this video you learned that:

Businesses evaluate data warehouse systems based on features and capabilities, compatibility and implementation, ease of use and required skills, support quality and availability, and multiple cost considerations.

An organization might need a traditional on-premises installation to adhere to data security and privacy requirements.

Public cloud sites offer organizations the benefits of economies of scale including powerful compute power and scalable storage resulting in flexible price-for-performance options. [ENRICHED: performance context — Cloud data warehouses offer elastic scaling where compute and storage can be independently adjusted based on workload demands. This separation of compute and storage is a key architectural advantage that allows organizations to scale one without paying for the other. For seasonal workloads, pay-per-use models can deliver 40% higher cost-efficiency compared to always-on on-premises appliances. Source: Data Consulting Firms] [Source: https://dataconsultingfirms.com/insights/data-platform-tco-analysis]

And, when selecting a data warehouse system consider the total cost of ownership including infrastructure, compute and storage, data migration, administration, and data maintenance costs in your calculations.

## Enrichment Log

| # | Location | Type | Summary | Confidence | Source |
|---|---|---|---|---|---|
| 1 | Evaluation Criteria Overview | Definition | Defined structured evaluation framework with five core criteria categories | HIGH | https://d.gigaom.com/report/key-criteria-for-evaluating-data-warehouse-solutions/ |
| 2 | Location section | Definition | Defined CCPA and GDPR with specific compliance requirements and penalties | HIGH | https://usercentrics.com/knowledge-hub/gdpr-vs-ccpa-compliance/ |
| 3 | Location section | Performance context | Added market size projections and deployment model distribution | HIGH | https://erpsoftwareblog.com/2026/03/on-premise-vs-cloud-data-warehouse/ |
| 4 | Features and Capabilities | Definition | Defined dark data with industry analysis statistics | HIGH | https://www.ibm.com/think/topics/data-warehouse |
| 5 | Features and Capabilities | Ecosystem connection | Connected batch vs streaming processing to lakehouse architecture | HIGH | https://www.databricks.com/blog/data-warehouse-tools |
| 6 | Features and Capabilities | Definition | Defined data governance with core components | HIGH | https://www.vertica.com/wp-content/uploads/2020/04/key-criteria-for-evaluating-data-warehouses-2-2.pdf |
| 7 | User Management | Definition | Defined zero-trust security model with breach cost context | HIGH | https://www.ibm.com/think/topics/data-warehouse |
| 8 | Ease of Use and Skills | Ecosystem connection | Added implementation partner evaluation criteria | HIGH | https://d.gigaom.com/report/key-criteria-for-evaluating-data-warehouse-solutions/ |
| 9 | Support Considerations | Definition | Defined SLA with specific uptime guarantees and calculations | HIGH | https://aws.amazon.com/redshift/features/ |
| 10 | Cost Evaluation | Definition | Defined TCO with typical timeframe and cost comparison framework | HIGH | https://tcoiq.com/blog/tco-on-premises-vs-cloud.html |
| 11 | Infrastructure costs | Performance context | Added specific hardware cost ranges and ROI timeframe | HIGH | https://tcoiq.com/blog/tco-on-premises-vs-cloud.html |
| 12 | Software licensing | Ecosystem connection | Compared perpetual vs subscription licensing models with cost governance | HIGH | https://dataconsultingfirms.com/insights/data-platform-tco-analysis |
| 13 | Data migration | Performance context | Added migration timeline and cost components | HIGH | https://erpsoftwareblog.com/2026/03/on-premise-vs-cloud-data-warehouse/ |
| 14 | Administration costs | Ecosystem connection | Added staffing requirements and FinOps governance needs | HIGH | https://dataconsultingfirms.com/insights/data-platform-tco-analysis |
| 15 | Key Takeaways | Performance context | Added compute-storage separation advantage and seasonal efficiency | HIGH | https://dataconsultingfirms.com/insights/data-platform-tco-analysis |

<!-- EXTRACTION_CHECKLIST: 49 sentences extracted, 49 sentences in output -->
