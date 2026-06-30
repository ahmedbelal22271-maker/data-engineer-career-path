# What is Edge Computing?

Source: https://aws.amazon.com/what-is/edge-computing/

[Create an AWS Account](<https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?pg=what_is_header>)

## Page topics

* What is Edge Computing?
* Why is edge computing important?
* Which industries use edge computing?
* How does edge computing work?
* What is the difference between edge computing and cloud computing?
* What are some AWS edge computing use cases?
* How can AWS help you with your edge computing requirements?

## What is Edge Computing?

Edge computing is the process of bringing information storage and computing abilities closer to the devices that produce that information and the users who consume it. Traditionally, applications have transmitted data from smart devices like sensors and smartphones to a central data center for processing. However, the unprecedented complexity and scale of data have outpaced network capabilities. By shifting processing capabilities closer to users and devices, edge computing systems significantly improve application performance, reduce bandwidth requirements, and give faster real-time insights.

## Why is edge computing important?

Edge computing is becoming more popular because it allows enterprises to collect and analyze their raw data more efficiently. More than ever, organizations need instant access to their data to make informed decisions about their operational efficiency and business functions. When appropriately used, edge computing has the potential to help organizations improve safety and performance, automate processes, and improve user experience.

Here are some benefits of edge computing.

### **Reduced latency/increased speed**

In many industries, technology demands almost instant transfer of data. Take the example of a piece of robotic machinery on a factory floor. If a production incident makes it unsafe for that robot to keep operating, it needs to receive that information as fast as possible so it can shut down.

### **Improved data security**

With edge computing, the majority of data is processed and stored locally. Any information that needs to be sent back to the data center can be encrypted before transmission. Enterprises also use edge computing to comply with data sovereignty laws, such as the General Data Protection Regulation (GDPR), by keeping any sensitive data close to the source.

### **Increased productivity**

Enterprises improve operational and employee productivity by responding more quickly to information. By analyzing data collected at the source, organizations can improve areas of their facilities, infrastructure, or equipment that are underperforming. Edge computing can be teamed with [artificial intelligence](</what-is/artificial-intelligence/>) and [machine learning](</what-is/machine-learning/>) tools to derive business intelligence and insights that helps employees and enterprises perform more productively.

### **Remote data collection**

It is challenging to collect data from places with unreliable connectivity and bandwidth. Establishing compute and data storage capabilities at the network edge helps enterprises collect and transmit data from distant oil fields, industrial zones, and offshore vessels.

### **Reduced costs**

Sending large quantities of data from its origin to centralized data centers is expensive because it requires more bandwidth. The edge computing model allows you to decrease the amount of data being sent from sites to data centers because end users only send critical data. Depending on how much data your business sends and processes, this could significantly save operating costs.

### **Reliable performance**

Edge computing often takes place in remote areas where internet connectivity is scarce. By setting up an edge computing environment, enterprises ensure that their operations reliably process, analyze, and store data. This significantly reduces the chances of suffering from operational downtime caused by network or connectivity disruption.

## Which industries use edge computing?

The high speeds and low latency of data transfer, combined with the relative ease of installing edge devices, have seen edge computing widely used across industries. Here are some examples.

### **Manufacturing**

The proliferation of Internet of Things (IoT) devices such as sensors and gateways has made edge computing systems prevalent in the manufacturing industry. Manufacturers utilize edge computing solutions to enable automation, collect data on-site, improve production efficiency, and allow rapid machine-to-machine communication. [Learn more about edge computing in manufacturing >>](</manufacturing/>)

### **Autonomous vehicles**

Autonomous vehicles like self-driving cars are fitted with several IoT sensors that collect large amounts of data every second. They require real-time data processing for instant response and cannot rely on a remote server for split-second decision-making.

Additionally, autonomous vehicles interact more efficiently if they communicate with each other first, as opposed to sending data on weather conditions, traffic, accidents, or detours to a remote server. Edge computing is critical technology for ensuring their safety and ability to accurately judge road conditions.

### **Energy**

Energy companies use edge computing to collect and store data on oil rigs, gas fields, wind turbines, and solar farms. Rig operators commonly deploy edge artificial intelligence to detect hazards and optimize and inspect their pipelines. Edge computing helps the industry improve operational efficiency, keep its workers safe, and forecast when maintenance work needs to be undertaken. [Learn more about edge computing in energy >>](</energy-utilities/solutions/>)

### **Healthcare**

Edge devices monitor critical patient functions such as temperature and blood sugar levels. Edge computing allows the healthcare sector to store this patient data locally and improve privacy protection. Medical facilities also reduce the data volume they send to central locations and cut the risk of data loss.

## How does edge computing work?

Edge computing works by bringing computation and storage closer to the producers and consumers of data. Edge deployments vary for different use cases, but can be grouped into two broad categories.

### **Upstream applications**

Upstream applications prioritize collecting data from smart sensors and other devices, then transmitting it to data centers for further processing. Data collected falls into three main categories:

- Redundant or irrelevant data, like room temperature data that a sensor measures every 5 minutes
- Useful data with long-term storage requirements, like average temperature over a few hours
- Useful data with short-term implications, like room temperature values below which the heater must turn on

Edge computing in upstream use cases focuses on distinguishing between these three types of data sources, then only transmitting critical information to the data center. Edge strategies could include the following examples.

#### ***Local on-premises data center***

Companies put storage, servers, and other edge devices next to the data source. For example, an energy company might install some server racks and a remote LAN within a wind turbine to collect and process the data it generates.

#### ***Compute capacity in Internet of Things (IoT) devices***

The company uses sensors with enough compute capacity to process data using predetermined filtering rules before transmission.

#### ***Regional edge servers***

A company uses cloud services to process data from several different sensors within a single region. Cloud providers can localize the cloud services so that computing takes place on edge servers local to the company's required region.

### **Downstream applications**

Downstream applications prioritize data delivery to end users. Examples include live video streaming in media and entertainment, online gaming, or virtual reality video feeds. Edge computing for downstream use cases focus on reducing network latency so users experience events as they take place. Here are some examples of downstream edge computing.

#### ***Caching***

A company sets up a content delivery network (CDN) that caches content on edge servers geographically closer to the users, thus reaching their computers much faster. [Learn more about CDNs >>](</what-is/cdn/?trk=faq_card>)

#### ***Cloud edge services***

You can use a cloud computing service to run latency-sensitive portions of your application local to endpoints and resources in a specific geography.

#### ***Mobile edge computing***

A company uses mobile edge computing infrastructure such as 5G networks and 5G-based mobile cloud computing services to develop, deploy, and scale ultra-low-latency applications.

## What is the difference between edge computing and cloud computing?

Edge computing is running workloads at the edge—that is, closer to devices and end users. On the other hand, cloud computing is a broad term that includes running all types of workloads in a cloud service provider's data center.

However, it is important to note that cloud service providers also provide edge computing services. For example, [AWS edge services](</edge/>) deliver data processing, analysis, and storage close to your endpoints, allowing you to deploy APIs and tools to locations outside AWS data centers.

## What are some AWS edge computing use cases?

A large number of leading enterprises utilize AWS edge computing tools. We give three prominent examples below.

### **Volkswagen Group**

Volkswagen, one of the world's leading automobile groups, uses AWS IoT, machine learning, and edge services to power its Industrial Cloud. It can connect data from more than 120 manufacturing plants to improve efficiency and uptime at its plant facilities, improve production flexibility, and drive vehicle quality standards. [Read how Volkswagen uses AWS >>](</solutions/case-studies/innovators/volkswagen-group/>)

### **Hulu**

The streaming platform Hulu utilizes AWS edge networking services to ensure customers enjoy stellar content and user experiences, even when user traffic is high. Hulu uses AWS services to provide scalable, agile, and cost-effective infrastructure. [Read how Hulu uses AWS >>](</solutions/case-studies/hulu/>)

### **Riot Games**

Riot Games develops, publishes, and supports the most player-focused games in the world, including *League of Legends*, one of the world's most popular PC games. With the 2020 global launch of *VALORANT*, a team-based tactical shooter game, Riot wanted to reduce "peeker's advantage" caused by latency and ensure competitive integrity. Riot uses [AWS Outposts](</outposts/>) to rapidly deploy game servers and reduce latency by 10 to 20 milliseconds, minimizing peeker's advantage and creating a level playing field for all players. [Watch how Riot Games uses AWS >>](<https://www.youtube.com/watch?v=g9nQXafMo4A>)

## How can AWS help you with your edge computing requirements?

[AWS for the Edge](</edge/>) brings the world's most capable and secure cloud closer to your endpoints and users. AWS is the only provider that extends infrastructure, services, APIs, and tools offered in the cloud as a fully managed service to virtually any on-premises data center, co-location space, or edge facility.

Take advantage of managed hardware deployed in locations outside AWS data centers— extending secure edge computing capabilities to metro areas, 5G networks, on-premises locations, and disconnected or remote locations. You can employ capabilities purpose-built for specific edge use cases, and choose from more than 200 integrated device services to deploy edge applications to billions of devices quickly and easily.

Here are ways AWS can help with edge computing:

- [AWS Outposts](</outposts/>) extends your AWS infrastructure and services to virtually anywhere and enjoys a consistent hybrid experience
- [AWS Storage Gateway](</storagegateway/>) provides on-premises access to virtually unlimited cloud storage
- [AWS Snow Family](</snow/>) devices run operations in austere, non-data-center environments, and in locations where there is a lack of consistent network connectivity
- [Amazon SageMaker Edge Manager](</sagemaker/neo/>) optimizes, secures, monitors, and maintains machine learning models on fleets of edge devices

Get started with edge computing on AWS by [creating a free AWS account](</?nc2=h_lg>) today!

## AWS Edge Computing Next Steps

### [Check out additional product-related resources Learn more about Compute Services ](</products/compute/>)

### [Sign up for a free account Instantly get access to the AWS free tier. Sign up ](<https://portal.aws.amazon.com/gp/aws/developer/registration/index.html>)

### [Start building in the console Get started building with AWS in the AWS Management Console. Sign in ](<https://console.aws.amazon.com>)

## Browse all cloud computing concepts

Browse all cloud computing concepts content here:

Loading

Loading

Loading

Loading

Loading

## Did you find what you were looking for today?

Let us know so we can improve the quality of the content on our pages

Yes No

[Create an AWS account](<https://signin.aws.amazon.com/signup?request_type=register>)

## Learn

* [What Is AWS?](</what-is-aws/?nc1=f_cc>)
* [What Is Cloud Computing?](</what-is-cloud-computing/?nc1=f_cc>)
* [What Is Agentic AI?](</what-is/agentic-ai/?nc1=f_cc>)
* [Cloud Computing Concepts Hub](</what-is/?nc1=f_cc>)
* [AWS Cloud Security](</security/?nc1=f_cc>)
* [What's New](</new/?nc1=f_cc>)
* [Blogs](</blogs/?nc1=f_cc>)
* [Press Releases](<https://press.aboutamazon.com/press-releases/aws>)

## Resources

* [Getting Started](</getting-started/?nc1=f_cc>)
* [Training](</training/?nc1=f_cc>)
* [AWS Trust Center](</trust-center/?nc1=f_cc>)
* [AWS Solutions Library](</solutions/?nc1=f_cc>)
* [Architecture Center](</architecture/?nc1=f_cc>)
* [Product and Technical FAQs](</faqs/?nc1=f_dr>)
* [Analyst Reports](</resources/analyst-reports/?nc1=f_cc>)
* [AWS Partners](</partners/work-with-partners/?nc1=f_dr>)

## Developers

* [Builder Center](<https://builder.aws.com/?nc1=f_dr>)
* [SDKs & Tools](<https://builder.aws.com/build/tools?nc1=f_dr>)
* [.NET on AWS](<https://builder.aws.com/build/tools?nc1=f_dr>)
* [Python on AWS](</developer/language/python/?nc1=f_dr>)
* [Java on AWS](</developer/language/java/?nc1=f_dr>)
* [PHP on AWS](</developer/language/php/?nc1=f_cc>)
* [JavaScript on AWS](</developer/language/javascript/?nc1=f_dr>)

## Help

* [Contact Us](</contact-us/?nc1=f_m>)
* [File a Support Ticket](<https://console.aws.amazon.com/support/home/?nc1=f_dr>)
* [AWS re:Post](<https://repost.aws/?nc1=f_dr>)
* [Knowledge Center](<https://repost.aws/knowledge-center/?nc1=f_dr>)
* [AWS Support Overview](</premiumsupport/?nc1=f_dr>)
* [AWS Accessibility](</accessibility/?nc1=f_cc>)
* [Legal](</legal/?nc1=f_cc>)
* [Event Code of Conduct](</codeofconduct/?nc1=f_cc>)
* [Event Terms & Conditions](</events/terms/?nc1=f_cc>)

English

Back to top

Amazon is an equal opportunity employer and does not discriminate on the basis of protected veteran status, disability or other legally protected status.

* [Privacy](</privacy/?nc1=f_pr>)
* [Site terms](</terms/?nc1=f_pr>)
* Your Privacy Choices  California Consumer Privacy Act (CCPA) Opt-Out Icon
* Cookie Preferences

© 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.
