> **Course 1:** IBM Data Engineering
> **Module 3:** Data Engineering Lifecycle — Performance Tuning & Troubleshooting

# Q&A: Data Volume Monitoring in Pipelines

## Question

Which type of monitoring determines whether the **size of a workload** is slowing the system down?

## Answer

**Monitoring the amount of data being processed through a data pipeline** (data volume monitoring).

The key phrase is **"size of a workload"** — a data volume concern, not a query, job, or database concern.

---

## Monitoring Type Comparison

| Monitoring Type | What It Targets |
|---|---|
| **Database monitoring** | Database health snapshots — when and how a problem started |
| **Query performance monitoring** | Query throughput, execution speed, resource utilization patterns |
| **Job-level runtime monitoring** | Individual steps within a job — completion and time-to-completion |
| **Data volume monitoring** | Whether the size of the workload is slowing the system down |

---

## Signal Words Reference

The following signal words help distinguish monitoring types in exam questions:

| Monitoring Type | Signal Words / Phrases |
|---|---|
| **Data volume monitoring** | "size of workload", "amount of data", "data flowing through pipeline" |
| **Job-level runtime monitoring** | "steps within a job", "logical steps", "long-running processes" |
| **Query performance monitoring** | "query throughput", "execution performance", "resource utilization patterns" |
| **Database monitoring** | "snapshots", "when a problem started", "database health indicators" |

---

## Source

Derived from **Module 3 — Performance Tuning & Troubleshooting**, Part 4: Monitoring and Alerting Systems. See the data volume monitoring row in the Types of Monitoring Tools table:

> **Data volume monitoring** — Monitors the amount of data flowing through a pipeline. Assesses whether workload size is causing system slowdowns.
