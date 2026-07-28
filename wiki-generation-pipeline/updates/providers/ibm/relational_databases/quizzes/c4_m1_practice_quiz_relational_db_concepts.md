> **Course 4:** Introduction to Relational Databases (RDBMS)
> **Module 1:** Fundamental Relational Database Concepts
> **Quiz:** Practice Quiz — Fundamental Relational Database Concepts

# Practice Quiz: Fundamental Relational Database Concepts

**Due:** Jul 8, 11:59 PM EEST  
**Attempts:** Unlimited (not scored)

---

## Question 1

**Which widely-used data model for databases allows for data independence?**

- Hierarchical Model
- Relational Model
- Information Model
- Entity-Relationship Data Model

**Correct answer: Relational Model**

[ENRICHED: explanation — The **Relational Model**, introduced by E.F. Codd in 1970, provides **data independence** — the ability to change the physical storage or logical schema without affecting applications that use the data. This is achieved through:
- **Physical data independence:** Changes to storage structures (indexes, file organization) do not require changes to queries or applications.
- **Logical data independence:** Changes to the schema (adding columns, splitting tables) can be absorbed by views without breaking existing queries.
The Hierarchical Model (pre-relational) tightly coupled the physical and logical layers, requiring application changes when storage changed. See `lessons/c4_m1_relational_model_concepts.md` for the full relational model overview.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Hierarchical Model** (incorrect) | The hierarchical model (e.g., IMS) uses parent-child tree structures and does not provide data independence — application code depends on the physical path structure. |
| **Relational Model** (correct) | The relational model's set-based algebra and declarative SQL provide logical and physical data independence. |
| **Information Model** (incorrect) | The Information Model is a conceptual framework (part of the Zachman Framework / ISO 10012), not a database implementation model. |
| **Entity-Relationship Data Model** (incorrect) | The ER model is a **design** tool for modeling data requirements at the conceptual level. It is not a database implementation model. Tables derived from an ERD are implemented within a relational (or other) DBMS. |

---

## Question 2

**Which two cardinalities are most commonly emphasized by crow's foot notation (using the crow's foot symbol)? [Select two]**

- Multiple primary
- One-to-many
- One-to-one
- Many-to-many

**Correct answers: One-to-many, Many-to-many**

[ENRICHED: explanation — Crow's foot notation is a visual method for representing cardinality in ERDs. The **crow's foot symbol** (three-pronged fork at the end of a relationship line) specifically represents the "many" side of a relationship:
- **One-to-many (1:N):** One line has a single vertical bar (the "one" side), the other has a crow's foot (the "many" side). The crow's foot is used on the "many" end.
- **Many-to-many (M:N):** Both sides have a crow's foot.
- **One-to-one (1:1):** Both sides have a single vertical bar — no crow's foot symbol is used.
See `lessons/c4_m1_erds_and_types_of_relationships.md` for ERD notation details and relationship types.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Multiple primary** (incorrect) | "Multiple primary" is not a cardinality type in ERD notation. Primary keys are constraints, not relationship cardinalities. |
| **One-to-many** (correct) | Uses a crow's foot on the "many" side. |
| **One-to-one** (incorrect) | One-to-one uses single vertical bars on both sides — no crow's foot symbol. |
| **Many-to-many** (correct) | Uses crow's feet on both sides of the relationship. |

---

## Question 3

**Entity Relationship Diagrams (ERDs) serve as the cornerstone for designing databases. After creating an ERD, what is the first step to convert it into a table?**

- Arranging the attributes by importance
- Listing the attributes alphabetically
- Separating the entity from the attributes
- Adding data values to the table's column

**Correct answer: Separating the entity from the attributes**

[ENRICHED: explanation — The process of mapping an ERD to a relational schema follows these steps:
1. **Separate the entity from its attributes** — each entity becomes a table, and each attribute becomes a column in that table.
2. Identify the primary key (the attribute that uniquely identifies each instance).
3. Map relationships as foreign keys.
The ERD shows entities (rectangles) and their attributes (ovals in Chen notation, listed inside the rectangle in crow's foot). The first step in converting to a table is recognizing that the entity rectangle maps to a table and its attribute list maps to columns. See `lessons/c4_m1_mapping_entities_to_tables.md` for the complete mapping process.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Arranging attributes by importance** (incorrect) | Column order in a table is a presentation choice, not a design step. The mapping from ERD to table is concerned with which columns exist, not their order. |
| **Listing attributes alphabetically** (incorrect) | Alphabetical ordering is not part of the ERD-to-table mapping process. |
| **Separating entity from attributes** (correct) | Each entity becomes a table; its attributes become columns. This is the fundamental mapping step. |
| **Adding data values** (incorrect) | Data values are populated after the table structure is created, not during the design-to-implementation mapping. |

---

## Question 4

**Which of the following represents floating-point number with approximate precision?**

- CHAR
- DECIMAL
- INTEGER
- FLOAT

**Correct answer: FLOAT**

[ENRICHED: explanation — `FLOAT` is a floating-point data type that stores numbers with **approximate precision** using scientific notation (mantissa × 2^exponent). This means:
- Very large and very small numbers can be represented (e.g., 1.23 × 10^38)
- But some values cannot be represented exactly (e.g., 0.1 in binary floating-point is an infinite repeating fraction)
- Comparison with equality (`=`) on FLOAT columns can produce unexpected results due to rounding

Other types in the question:
- `CHAR(n)`: Fixed-length character string — not numeric at all.
- `DECIMAL(p,s)`: Exact numeric type — stores the value exactly as specified (e.g., `DECIMAL(10,2)` represents 99,999,999.99 exactly). Used for financial/monetary values where precision is critical.
- `INTEGER`: Exact whole numbers — no fractional part.

See `lessons/c4_m1_data_types.md` for the full data type comparison including FLOAT vs. DECIMAL precision behavior.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **CHAR** (incorrect) | Character type — not numeric. |
| **DECIMAL** (incorrect) | Exact numeric type — does not use approximate precision. Preferred for currency and accounting. |
| **INTEGER** (incorrect) | Exact integer type — no fractional component. |
| **FLOAT** (correct) | Approximate numeric type — uses floating-point representation. |

---

## Question 5

**What constitute the building blocks of the Relational Model?**

- Collections and Items
- Relations and sets
- Mathematical model and terms
- Index and Elements

**Correct answer: Relations and sets**

[ENRICHED: explanation — The Relational Model is built on **relations** (tables) and **sets** (of tuples/rows). The key building blocks are:
- **Relation:** A table with rows and columns, where each row represents an entity instance and each column represents an attribute.
- **Tuple:** A row in a relation (ordered set of attribute values).
- **Attribute:** A named column of a relation.
- **Domain:** The set of permissible values for an attribute.
- **Set:** The collection of tuples in a relation is a set — no duplicate tuples are allowed (though in practice most RDBMSs permit duplicate rows unless a PRIMARY KEY or UNIQUE constraint is enforced).

The term "relational" comes from the mathematical concept of a **relation** (a subset of the Cartesian product of domains). Codd's 1970 paper defined the relational model using set theory and first-order predicate logic. See `lessons/c4_m1_relational_model_concepts.md` for the formal definitions.]

### Distractor Analysis

| Option | Analysis |
|---|---|
| **Collections and Items** (incorrect) | These are generic programming terms, not specific to the relational model. |
| **Relations and sets** (correct) | The relational model is fundamentally based on relations (tables) and set theory. |
| **Mathematical model and terms** (incorrect) | While the relational model is grounded in mathematics, "mathematical model" is a description of the approach, not the building blocks themselves. |
| **Index and Elements** (incorrect) | Indexes are performance optimization structures, not foundational building blocks of the relational model. |

---

## Enrichment Log

| # | Location | Type | Summary | Confidence |
|---|---|---|---|---|
| 1 | Q1 | Explanation | Connected data independence to Relational Model with physical/logical independence definitions and cross-reference to Relational Model Concepts lesson | HIGH |
| 2 | Q2 | Explanation | Connected crow's foot cardinalities to ERDs and Relationships lesson with notation details | HIGH |
| 3 | Q3 | Explanation | Connected ERD-to-table mapping process with cross-reference to Mapping Entities to Tables lesson | HIGH |
| 4 | Q4 | Explanation | Connected FLOAT approximate precision to exact vs. approximate numeric type comparison with cross-reference to Data Types lesson | HIGH |
| 5 | Q5 | Explanation | Connected relational model building blocks to Relational Model Concepts lesson with formal definitions (relation, tuple, attribute, domain, set) | HIGH |
