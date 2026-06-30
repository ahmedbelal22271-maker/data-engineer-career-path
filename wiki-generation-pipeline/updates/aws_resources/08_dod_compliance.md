# Department of Defense Cloud Service Provider Security Requirements Guide

Source: https://aws.amazon.com/compliance/dod/

(DoD CSP SRG)

## Overview

A growing number of military customers are adopting AWS services to process, store, and transmit US Department of Defense (DoD) data. AWS enables defense organizations and their business associates to create secure environments to process, maintain, and store DoD data.

The Department of Defense (DoD) [Cloud Computing Security Requirements Guide](<https://public.cyber.mil/dccs/>) provides a standardized assessment and authorization process for cloud service providers (CSPs) to gain a DoD provisional authorization, so that they can serve DoD customers. The AWS provisional authorization from the Defense Information Systems Agency (DISA) provides a reusable certification that attests to AWS compliance with DoD standards, reducing the time necessary for a DoD mission owner to assess and authorize one of their systems for operation in AWS. For more information about the SRG, including the full definition of the security control baselines defined for Levels 2, 4, 5 and 6, visit the [Document Library](<https://public.cyber.mil/dccs/dccs-documents/>) on the [DoD Cloud Computing Security](<https://public.cyber.mil/dccs/>) webpage.

As a DoD customer, you are responsible for complying with DoD security guidance within your AWS application environment, which includes:

* Mission owner responsibilities described in the [DoD-Compliant Implementations in the AWS Cloud whitepaper](<https://d1.awsstatic.com/whitepapers/compliance/AWS_DOD_CSM_Reference_Architecture.pdf>)
* All relevant operating system Security Technical Implementation Guides (STIGs)
* All relevant application STIGs
* DoD ports and protocols guidance (DoD Instruction 8551.01)

The infrastructure, governance, and operating environment of AWS have been assessed and authorized through the FedRAMP and DoD authorization processes. As a customer deploying an application on AWS infrastructure, you inherit security controls pertaining to our physical, environmental and media protection, and no longer need to provide a detailed description of how you comply with these control families. The remaining DoD Risk Management Framework (RMF) controls are shared between AWS and customers, with each organization retaining responsibility for control implementation within their portion of the shared IT security model.

* FAQs 14

## FAQs

Open all

###  How do I review AWS security documentation and guidance?

Our DoD customers and vendors can use our FedRAMP and DoD authorizations to accelerate their certification and accreditation efforts. To support the authorization of military systems hosted on AWS, we provide DoD security personnel with documentation so you can verify AWS compliance with applicable NIST 800-53 (Revision 5) controls and the DoD Cloud Computing SRG (Version 1, Release 3).

We provide our DoD customers with a package of security guidance and documentation about security and compliance for using AWS as a DoD hosting solution. In particular, we provide an AWS FedRAMP SSP template based upon NIST 800-53 (Rev 5), which is prepopulated with the applicable FedRAMP and DoD control baseline. The inherited controls within the template are prepopulated by AWS; shared controls are the responsibility of both AWS and the customer; and some controls are fully the responsibility of the customer.

Military organizations or contractors conducting business with the DoD can request access to AWS security documentation by contacting your AWS Account Manager or submitting the [AWS Compliance Contact Us Form](<https://pages.awscloud.com/compliance-contact-us.html>). Non-government customers, such as AWS partners, can download the AWS Partner FedRAMP Security Package using [AWS Artifact](<https://console.aws.amazon.com/artifact>).

###  What value do I get from moving to AWS?

We believe that for government customers, migration to the cloud is an opportunity to improve your level of security assurance and reduce your operational risk. The AWS operating environment allows you to have a level of security and compliance only possible in an environment supported by high levels of automation. Rather than the traditional data center conducting periodic inventories and "point-in-time" audits, AWS customers have the ability to conduct audits on a continual basis. Having this level of visibility into your environment enhances data control and increases your ability to maintain assurance that only authorized users have access.

For example, DoD mission owners can realize higher levels of control over applications through programmatic enforcement of DoD security and compliance guidelines. AWS allows you to create pre-approved templates for common application use cases, reducing the time to authorize new applications. The templates can help ensure that application owners do not change vital security settings such as security groups and network ACLs, and can enforce the use of STIG-hardened machine images. This programmatic enforcement of DoD security guidelines reduces manual configuration efforts, which can decrease improper configuration and reduce overall risk to the DoD.

###  Will DoD compliance increase AWS service prices?

No, there is no increase in service costs for any service as a result of AWS’ compliance programs.

###  How does a mission owner achieve an Authorization to Operate (ATO)?

As a DoD mission owner, you are responsible for building an authorization package that fully defines your implementation of the security controls applicable to your application. As with any traditional authorization package, you need to document your security control baseline with a system security plan, and have this plan and its implementation reviewed by the relevant certification personnel from your DoD organization. As part of this review, your certification personnel or your authorizing official may review the AWS authorization package to gain a holistic view of the security control implementation from top to bottom. After reviewing your security authorization package, and the AWS security authorization packages, your authorizing official will have the information necessary to make an accreditation decision for your application and grant an ATO.

For more information about the responsibility of DoD application owners operating in AWS, see the [DoD-Compliant Implementations in the AWS Cloud whitepaper](<https://d1.awsstatic.com/whitepapers/compliance/AWS_DOD_CSM_Reference_Architecture.pdf>).

###  Do AWS Cloud services meet DoD requirements?

Yes, AWS has been assessed and approved as a cloud service provider for the US East and US West Regions at Impact Level 2, AWS GovCloud (US) at Impact Levels 4 and 5, and the AWS Secret Region at Impact Level 6.

* At Impact Level 2, the US-based AWS Regions US East/West, AWS GovCloud (US) has been assessed by DISA and issued two provisional authorizations after demonstrating compliance with DoD requirements. AWS’ compliance with DoD requirements was achieved by leveraging our existing FedRAMP Joint Authorization Board (JAB) Provisional Authorization to Operate (P-ATO). The provisional authorizations allow DoD entities to evaluate AWS' security and the opportunity to store, process, and maintain a diverse array of DoD data in the AWS Cloud.
* At Impact Levels 4 and 5, AWS GovCloud (US) has been issued a provisional authorization from DISA to allow DoD customers to deploy production applications with the enhanced control baselines corresponding to those levels of the SRG. DoD customers with prospective Impact Level 4 or Impact Level 5 applications should contact DISA to begin the approval process.
* At Impact Level 6, The AWS Secret Region holds a DoD provisional authorization for workloads up to and including Secret level. A service catalog for the AWS Secret Region is available from your AWS Account Executive.

###  How does the AWS provisional authorization affect the mission owner's ATO?

When operating an application in AWS, in the spirit of [shared security responsibility](</compliance/shared-responsibility-model/>), the DoD mission owner is responsible for a reduced baseline of security controls. AWS provides a secure hosting environment with applicable security controls for mission owners to field their applications, but this does not relieve the mission owner of their responsibility to securely deploy, manage, and monitor their application in accordance with DoD security controls and compliance policy.

For more information about the responsibility of DoD application owners operating in AWS, see the [DoD-Compliant Implementations in the AWS Cloud whitepaper](<https://d1.awsstatic.com/whitepapers/compliance/AWS_DOD_CSM_Reference_Architecture.pdf>).

###  Can other AWS services be used?

Yes, customers can evaluate their workloads for suitability with other AWS services. Each mission owner is empowered to evaluate and accept the risk of any of our services that they choose to employ. For more information about security controls and risk acceptance considerations, please contact [AWS Compliance](<https://pages.awscloud.com/compliance-contact-us.html>).

###  What AWS Regions are covered?

Our provisional authorizations cover multiple regions within the continental United States, including AWS GovCloud (US) (Impact Levels 2, 4, and 5), AWS US East/West regions (Impact Level 2), and the AWS Secret Region (Impact Level 6).

###  What classifications of DoD systems can be placed on AWS?

The AWS Regions US East and US West hold a provisional authorization for Impact Level 2, which permits mission owners to deploy public, unclassified information in these AWS Regions with both the AWS authorization and the mission application’s ATO. AWS GovCloud holds a provisional authorization for Impact Levels 2, 4, and 5, and permits mission owners to deploy the full range of controlled, unclassified information categories covered by these levels. The AWS Secret Region holds a provisional authorization for Impact Level 6 and permits workloads up to and including Secret classification.

###  Are other DoD entities using AWS now?

Yes, many DoD entities and other organizations that provide systems integration and other products and services to DoD are using the wide range of AWS services today. AWS cannot disclose many of the customers who have achieved DoD Authorizations to Operate (ATOs) for systems on AWS, but we regularly work with customers and their assessors in planning for, deploying, certifying, and accrediting their DoD workloads on AWS.

###  Which AWS services are covered?

For a complete list of covered services, visit the [AWS Services in Scope by Compliance Program](</compliance/services-in-scope/>) webpage.

###  What does this mean to me as a DoD mission owner?

Our Impact Level 2 provisional authorizations enable DoD customers to use our compliant AWS infrastructure and services to deploy workloads including data cleared for public release, as well as some DoD private unclassified information. Moving your DoD IT environment to AWS can help improve your own compliance oversight with the services and features made available by AWS.

Our Impact Level 4 and 5 provisional authorizations for AWS GovCloud (US) mean that our DoD customers can deploy their production applications to AWS GovCloud (US). This authorization allows customers to engage in design, development, and integration activities for workloads that are required to comply with Impact Levels 4 and 5 of the DoD Cloud Service Provider SRG.

Our Impact Level 6 provisional authorization for AWS Secret Region means that DoD customers can use our services to store, process, or transmit data up to and including Secret level. Customers can rely on our authorization to cover all infrastructure requirements defined by Impact Level 6, which helps them manage their own compliance and certification, including audits and security management.

###  Does an ATO require a physical walkthrough of a service provider's data center?

No. DoD customers can rely on the work performed by our FedRAMP third-party assessment organizations (3PAO), which includes an extensive on-site review of the physical security of our data centers. In accordance with the DoD Cloud Service Provider SRG, a DoD customer can achieve an Authorization to Operate(ATO) without a physical walkthrough of a service provider's data center that already has authorizations.

###  Why is the DoD Cloud Service Provider SRG important?

The DoD Cloud Service Provider SRG supports the overall US Federal Government’s goal to increase their use of cloud computing and provides a means for the DoD to support this goal. On February 8, 2011, the Office of Management and Budget (OMB) established The Federal Cloud Computing Strategy which established guidance for all federal agencies to adopt cloud technologies across the federal government. This strategy was followed by a federal requirement released in December 2011 establishing the Federal Risk and Authorization Management Program (FedRAMP). FedRAMP is mandatory for federal agency cloud deployments and service models at the low, moderate, and high-risk impact levels.

In July 2012, the DoD issued its Cloud Computing Strategy from the DoD Chief Information Officer CIO). This established the Joint Information Environment (JIE) and the DoD Enterprise Cloud Environment: "The DoD Cloud Computing Strategy introduces an approach to move the Department from the current state of a duplicative, cumbersome, and costly set of application silos to an end state which is an agile, secure, and cost-effective service environment that can rapidly respond to changing mission needs. The DoD Chief Information Officer (CIO) is committed to accelerating the adoption of cloud computing within the Department..."

The DoD Cloud Service Provider SRG leverages the FedRAMP program as a means to establish a standardized approach for the DoD to assess cloud service providers (CSPs).

## DoD SRG Resources

### [Landing Zone Accelerator on AWS Landing Zone Accelerator on AWS ](<https://docs.aws.amazon.com/solutions/landing-zone-accelerator-on-aws/>)

### [DoD-Compliant Implementations in the AWS Cloud – Reference Architectures DoD-Compliant Implementations in the AWS Cloud – Reference Architectures ](<https://d1.awsstatic.com/whitepapers/compliance/AWS_DOD_CSM_Reference_Architecture.pdf>)

### [AWS Well-Architected Framework AWS Well-Architected Framework ](<https://d1.awsstatic.com/whitepapers/architecture/AWS_Well-Architected_Framework.pdf>)

### [AWS Security Documentation AWS Security Documentation ](<https://docs.aws.amazon.com/security/>)

### [Introduction to AWS Security Introduction to AWS Security ](<https://d1.awsstatic.com/whitepapers/Security/Intro_to_AWS_Security.pdf>)

## Next steps

### [Have Questions? Connect with an AWS Business Representative Contact Us ](</compliance/contact/>)

### [Exploring compliance roles? Apply today » ](</careers/security/>)

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
