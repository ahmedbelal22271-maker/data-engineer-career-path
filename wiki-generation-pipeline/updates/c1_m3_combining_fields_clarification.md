> **Course 1:** Introduction to Data Engineering
> **Module 3:** Data Engineering Lifecycle

# Clarification: What "Combining Fields" Means in Data Wrangling

## Overview

The Data Wrangling lesson refers to "combining fields" as part of structural transformations. This document provides a detailed clarification of what that term means in practice.

---

## Question

When the lesson on structural transformations mentions **combining fields** as part of structuring data — what does that actually mean? How does it relate to joins, concatenation, and resolving schema differences?

---

## Answer

**Combining fields** means taking data that lives in separate columns and merging them together into one — either by concatenating values or by pulling related fields from different tables into the same record.

### Simple Combination — Concatenation

You have a `first_name` column and a `last_name` column. Combining them creates a single `full_name` field:

| first_name | last_name | → | full_name |
|---|---|---|---|
| John | Doe | → | John Doe |
| Jane | Smith | → | Jane Smith |

### Cross-Source Combination — Joins

You have a customer table from your CRM and an orders table from your e-commerce system:

| customer_id | name | email |
|---|---|---|
| 1 | Alice | alice@example.com |

| customer_id | product | amount |
|---|---|---|
| 1 | Widget | 49.99 |

A join combines the columns from both tables into one row using `customer_id` as the link:

| customer_id | name | email | product | amount |
|---|---|---|---|---|
| 1 | Alice | alice@example.com | Widget | 49.99 |

### The Schema Difference Problem

This is why the lesson mentions combining fields in the context of structuring. Before you can combine fields across sources, you must resolve schema differences:

| Issue | Source A | Source B |
|---|---|---|
| Field name | `postal_code` | `zip` |
| Data type | String | Integer |

Before combining, these differences must be reconciled — renaming, retyping, and standardizing so the combined field is consistent. That resolution *is* the structuring transformation.

---

## Summary

In short, **combining fields** = merging data that was previously separate, whether at the value level (concatenation) or the record level (joins). The "complex structures" the lesson references are just cases where that merging involves more steps than a simple rename.
