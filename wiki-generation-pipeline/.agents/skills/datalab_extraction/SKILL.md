---
name: Datalab Structured Extraction
description: Extract highly structured JSON data from PDFs or images using predefined JSON schemas in Datalab.
---

# Datalab Structured Extraction

## 1. Schema Definition & Extraction
Use `ExtractOptions` to define a strict JSON schema for the data you want to extract.
This skill requires the `datalab_core` SDK initialization.

```python
import json
from datalab_sdk import DatalabClient, ExtractOptions

client = DatalabClient()

# Define strict JSON schema
schema = {
    "type": "object",
    "properties": {
        "invoice_number": {"type": "string", "description": "Invoice ID or number"},
        "total_amount": {"type": "number", "description": "Total amount due"},
        "vendor_name": {"type": "string", "description": "Company or vendor name"}
    },
    "required": ["invoice_number", "total_amount"]
}

options = ExtractOptions(
    page_schema=json.dumps(schema),
    mode="balanced"
)

result = client.extract("invoice.pdf", options=options)
extracted = json.loads(result.extraction_schema_json)

# Each field comes with citations and metadata!
print(f"Invoice: {extracted['invoice_number']}")
print(f"Citations: {extracted['invoice_number_citations']}")
print(f"Status: {extracted['invoice_number_meta']['extraction_status']}")
```

## 2. Full Documentation Reference
For exhaustive API parameters, confidence scoring logic, balanced extraction modes, and edge cases, read the raw markdown files located in the `references/` subdirectory of this skill.

---

## 3. Advanced Extraction Pipeline Protocol
For strict architectural rules on structured data mapping (Extract → Validate → Reconcile → Commit) and handling missing fields without hallucinating defaults, refer to the [Data Extraction Pipeline Protocol](file:///C:/Users/marwa/OneDrive/Documents/College%20Courses/agentic%20workflow/general%20tips/.agents/skills/datalab_extraction/references/data_extraction_pipeline.md).
