---
name: Data Architecture & Algorithms
description: Dual-Database knowledge core and graph/SQL integration.
---



# Source: data-architecture-and-algorithms.md

# Data Architecture and Algorithms

## Dual-Database Knowledge Core (The Hybrid Data Strategy)
- Separate data by its fundamental geometry to maximize access speed and intelligence.
- **Relational SQL:** Use strictly for tabular aggregates (e.g., salaries, exam scores, simple flat metrics).
- **Graph Databases:** Mirror interrelated entities (e.g., skills, concept transitions, organizational nodes) into topological Graph databases for exponentially faster sequence resolution and relationship mapping.

## The Set Difference Graph Traversal Pattern
- When calculating missing dependencies or computing "topological deficits" (what the user lacks vs. what is required), use a Set Difference approach.
- Take the set of required nodes, subtract the existing user nodes, and perform constrained Breadth-First Searches (BFS) to bridge the delta via adjacent nodes.
