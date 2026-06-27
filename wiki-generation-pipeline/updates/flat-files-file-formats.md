> **Course 1:** Introduction to Data Engineering
> **Module 2:** The Data Engineering Ecosystem

# Flat Files and File Formats in Data Engineering

---

## Overview

When working with data, one of the first decisions a data engineer must make is understanding **how data is stored and structured in files**. Different file formats carry different implications for performance, portability, readability, and tooling compatibility. This document explains what flat files are, then compares them against the most common file formats encountered in data engineering: CSV, TSV, spreadsheet files (XLSX/ODS), and XML documents.

---

## What is a Flat File?

A **flat file** is a plain-text or binary file that stores data in a **two-dimensional, tabular structure** — rows and columns — with **no hierarchical relationships, no embedded logic, and no internal references** between records.

### Core Characteristics

- **Self-contained:** Each row (record) is independent; there are no joins, foreign keys, or relational links inside the file.
- **Plain text (usually):** Most flat files are human-readable and can be opened in any text editor.
- **Single table:** A flat file holds one dataset — there is no concept of multiple related tables in a single file.
- **Delimiter or fixed-width:** Fields within a row are separated either by a special character (delimiter) or by a fixed number of characters (fixed-width format).
- **No schema enforcement:** The file format itself does not enforce data types, nullability, or constraints. Any validation must happen at the application or pipeline level.

### Two Subtypes of Flat Files

| Subtype | Description | Example |
|---|---|---|
| **Delimited** | Fields are separated by a special character | CSV, TSV, pipe-delimited (`\|`) |
| **Fixed-Width** | Each field occupies a predefined number of characters | Legacy mainframe exports, COBOL outputs |

### Example: Delimited Flat File (pipe-separated)

```
employee_id|first_name|last_name|department|salary
1001|Alice|Johnson|Engineering|95000
1002|Bob|Smith|Marketing|72000
1003|Carol|Lee|Engineering|88000
```

### Example: Fixed-Width Flat File

```
1001Alice     Johnson    Engineering95000
1002Bob       Smith      Marketing  72000
1003Carol     Lee        Engineering88000
```

> In fixed-width files, each column starts at a predefined character position. Parsing requires a schema spec (e.g., "columns 1–4 = employee_id, columns 5–14 = first_name...").

### Why Flat Files Matter in Data Engineering

Flat files are the **lingua franca of data exchange**. Despite their simplicity, they are ubiquitous because:

- Every database, spreadsheet tool, and programming language can read and write them.
- They require no special software to inspect.
- They are lightweight, compressible, and fast to transfer.
- They are the default export/import format for most SaaS platforms, ERPs, and legacy systems.

---

## CSV (Comma-Separated Values)

CSV is the **most widely used subtype of flat file**. It is a delimited flat file where fields are separated by commas.

### Structure

```csv
employee_id,first_name,last_name,department,salary
1001,Alice,Johnson,Engineering,95000
1002,Bob,Smith,Marketing,72000
1003,Carol,Lee,Engineering,88000
```

### Key Rules (RFC 4180 Standard)

- The first row is typically (but not always) a header row containing column names.
- Fields containing commas, newlines, or double quotes must be enclosed in double quotes.
- A literal double quote inside a quoted field is escaped by doubling it (`""`).

```csv
name,bio
"Alice, PhD","She said ""Hello World"" to start her career."
```

### Strengths

- Near-universal compatibility across tools, languages, and databases.
- Human-readable and editable in any text editor.
- Extremely compact — no markup overhead.
- Natively supported by Python (`csv`, `pandas`), SQL `COPY` commands, Excel, and virtually every ETL tool.

### Weaknesses

- **No data types:** All values are strings by default; a downstream system must cast `95000` to integer.
- **No schema:** There is no embedded definition of what columns mean or their types.
- **Delimiter conflicts:** If data contains commas, quoting rules must be applied consistently — inconsistency causes parse errors.
- **No support for nested or hierarchical data.**
- **Encoding ambiguity:** Files may be UTF-8, UTF-16, or Latin-1; the format does not declare its encoding.

### Common Use Cases in Data Engineering

- Bulk data loads into databases (`COPY`, `LOAD DATA INFILE`).
- Intermediate files between pipeline stages.
- Data exports from SaaS platforms (Salesforce, HubSpot, Stripe).
- Machine learning dataset distribution.

---

## TSV (Tab-Separated Values)

TSV is functionally identical to CSV, with one difference: **the delimiter is a tab character (`\t`) instead of a comma**.

### Structure

```
employee_id	first_name	last_name	department	salary
1001	Alice	Johnson	Engineering	95000
1002	Bob	Smith	Marketing	72000
```

### How TSV Differs from CSV

| Property | CSV | TSV |
|---|---|---|
| Delimiter | Comma (`,`) | Tab (`\t`) |
| Quoting requirement | Needed when data contains commas | Rarely needed (tabs in text are uncommon) |
| Human readability | Moderate (commas blend into content) | Higher (tab visually spaces columns) |
| Tool compatibility | Near-universal | Very high, slightly less than CSV |
| Common sources | SaaS exports, spreadsheets | Bioinformatics, NLP datasets, gene databases |

### When to Choose TSV Over CSV

- When the data contains many commas (e.g., natural language text, addresses, descriptions).
- When working with bioinformatics or genomics pipelines, where TSV is the community standard (e.g., VCF, GFF, BED file variants).
- When loading data into tools like PostgreSQL's `\copy` with tab as the default delimiter.

### Shared Limitations with CSV

TSV shares all the weaknesses of CSV: no data types, no schema enforcement, no support for nested structures, and encoding ambiguity.

---

## Spreadsheet Files (XLSX, ODS, Google Sheets)

Spreadsheet files represent a **significant step beyond plain flat files**. While they store tabular data, they are **not plain text** — they are binary or XML-compressed archive formats with rich metadata.

### Common Formats

| Format | Full Name | Creator | Notes |
|---|---|---|---|
| `.xlsx` | Office Open XML Spreadsheet | Microsoft | ZIP archive containing XML files; current Excel format |
| `.xls` | Binary Interchange File Format | Microsoft | Legacy binary format; largely obsolete |
| `.ods` | OpenDocument Spreadsheet | ISO/OASIS Standard | Used by LibreOffice, Google Sheets export |
| Google Sheets | Cloud-native | Google | Stored in Google Drive; exported as XLSX/CSV |

### What Spreadsheet Files Add Over Flat Files

```
Flat file (CSV)          Spreadsheet (XLSX)
─────────────────        ──────────────────────────────────────
Plain text               Binary (ZIP of XML)
No formatting            Cell colors, fonts, borders
No formulas              Formulas (=SUM(A1:A10))
Single table             Multiple sheets (tabs)
No charts                Embedded charts and pivot tables
No data validation       Dropdown lists, input constraints
No named ranges          Named ranges and structured tables
```

### Internal Structure of XLSX

An `.xlsx` file is a **ZIP archive**. Unzipping it reveals:

```
[Content_Types].xml
xl/
  workbook.xml            ← sheet names, references
  worksheets/
    sheet1.xml            ← actual cell data
  sharedStrings.xml       ← string values (deduplicated)
  styles.xml              ← formatting definitions
  charts/                 ← chart definitions (if any)
```

### Challenges for Data Engineering Pipelines

- **Not streamable:** The entire file must be loaded into memory to parse (unlike CSV, which can be read line by line).
- **Formulas, not values:** A cell containing `=A1+B1` stores the formula, not the result, until the file is opened and calculated by Excel.
- **Multiple sheets create ambiguity:** A pipeline must explicitly specify which sheet to read.
- **Merged cells:** Cells merged across rows/columns break naive row-by-row parsing.
- **Formatting masquerading as data:** A cell may appear to show `2024-01-15` but actually store a serial number (`45306`) formatted as a date.

### When Spreadsheet Files Appear in Data Pipelines

Spreadsheet files frequently appear as **source data** provided by business users (finance teams, ops teams, analysts). A data engineer's role is typically to **ingest and normalize** them into a structured format, not to produce them. Python libraries like `openpyxl` and `pandas` with `xlrd` are standard tools for this.

```python
import pandas as pd

# Reading a specific sheet from an Excel file
df = pd.read_excel("sales_report.xlsx", sheet_name="Q4_2024", header=0)
print(df.dtypes)
```

---

## XML (eXtensible Markup Language)

XML is **fundamentally different** from flat files. It is a **hierarchical, self-describing markup language** designed to represent structured and nested data — not just flat rows and columns.

### Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<employees>
  <employee>
    <employee_id>1001</employee_id>
    <first_name>Alice</first_name>
    <last_name>Johnson</last_name>
    <department>Engineering</department>
    <salary currency="USD">95000</salary>
    <projects>
      <project>Data Lake Migration</project>
      <project>ETL Modernization</project>
    </projects>
  </employee>
  <employee>
    <employee_id>1002</employee_id>
    <first_name>Bob</first_name>
    <last_name>Smith</last_name>
    <department>Marketing</department>
    <salary currency="USD">72000</salary>
    <projects/>
  </employee>
</employees>
```

### XML Key Concepts

| Concept | Description |
|---|---|
| **Element** | A tag pair: `<salary>95000</salary>` |
| **Attribute** | Metadata on a tag: `currency="USD"` inside `<salary>` |
| **Nesting** | Elements can contain other elements (tree structure) |
| **Schema (XSD)** | An XML Schema Definition can enforce structure and types |
| **Namespace** | Prevents naming conflicts when combining XML from different sources |
| **DTD** | Document Type Definition — an older mechanism to define valid structure |

### How XML Differs from Flat Files

| Property | Flat File (CSV/TSV) | XML |
|---|---|---|
| Structure | Two-dimensional (rows × columns) | Hierarchical (tree) |
| Nesting | Not supported | Natively supported |
| Self-describing | No (column names in header only) | Yes (element names carry meaning) |
| Schema support | None in format | XSD, DTD |
| Human readability | High (minimal syntax) | Moderate (verbose tags) |
| File size | Compact | Verbose (tags repeat for every record) |
| Parsing complexity | Simple (split by delimiter) | Complex (DOM or SAX parser required) |
| Common domains | General data exchange | Web services (SOAP), config files, publishing |

### Parsing Strategies for XML

Two primary approaches exist for parsing XML in data engineering:

**DOM (Document Object Model) Parsing** — loads the entire document into memory as a tree:

```python
import xml.etree.ElementTree as ET

tree = ET.parse("employees.xml")
root = tree.getroot()

for employee in root.findall("employee"):
    emp_id = employee.find("employee_id").text
    name = employee.find("first_name").text
    print(emp_id, name)
```

**SAX (Simple API for XML) Parsing** — event-driven, streams through the document without loading it all at once. Suitable for very large XML files.

### When XML Appears in Data Engineering

- **SOAP web services:** Legacy enterprise APIs (banking, insurance, government) often return XML payloads.
- **Configuration files:** Many systems (Hadoop, Maven, Spring) use XML for configuration.
- **Data exchange standards:** HL7 (healthcare), FpML (finance), XBRL (financial reporting) are XML-based standards.
- **RSS/Atom feeds:** News and content syndication formats.
- **Office file formats:** Internally, `.docx` and `.xlsx` files are XML documents inside a ZIP archive.

---

## Comprehensive Comparison

| Property | Flat File | CSV | TSV | Spreadsheet (XLSX) | XML |
|---|---|---|---|---|---|
| **Structure** | Tabular | Tabular | Tabular | Tabular (multi-sheet) | Hierarchical |
| **Text format** | Usually yes | Yes | Yes | No (binary/ZIP) | Yes |
| **Nesting** | No | No | No | No | Yes |
| **Data types** | No | No | No | Yes (cell types) | Optional (via XSD) |
| **Schema** | No | No | No | Partial | Yes (XSD/DTD) |
| **Multi-table** | No | No | No | Yes (sheets) | Yes (nesting) |
| **Formulas/logic** | No | No | No | Yes | No |
| **Streamable** | Yes | Yes | Yes | No | Yes (SAX) |
| **Human readable** | Yes | Yes | Yes | No | Yes (verbose) |
| **File size** | Compact | Compact | Compact | Medium | Large |
| **Parse complexity** | Low | Low | Low | Medium | High |
| **Best for** | Bulk transfer | General exchange | Text-heavy data | Business reports | Nested/structured data |

---

## Key Takeaways

- **Flat files** are the broadest category: any file storing data as plain rows and columns with no hierarchy. CSV and TSV are the most common flat file subtypes.
- **CSV** is the industry default for data exchange — compact, universal, but type-less and schema-less.
- **TSV** solves the comma-conflict problem in CSV, and is particularly common in scientific and NLP workloads.
- **Spreadsheet files (XLSX)** extend flat files with formatting, formulas, and multiple sheets. They are rich user-facing artifacts, but present significant parsing challenges for automated pipelines.
- **XML** is not a flat file at all — it is a hierarchical markup format capable of representing nested, self-describing data structures. It is verbose, schema-capable, and dominant in legacy enterprise integrations and web services.

> **Best Practice:** In production data pipelines, flat files (especially CSV/TSV) should be treated as an **ingestion source**, not a storage layer. Once data enters a pipeline, move it to a typed, schema-enforced format (Parquet, Avro, a relational table) as early as possible to eliminate ambiguity and improve downstream performance.
