---
name: Datalab Form Filling
description: Fill forms in PDFs or images with structured data using Datalab.
---

# Datalab Form Filling

## 1. Form Filling Logic
Fill blank PDFs or forms with strictly mapped field data.
This skill requires the `datalab_core` SDK initialization.

```python
from datalab_sdk import DatalabClient, FormFillingOptions

client = DatalabClient()

options = FormFillingOptions(
    field_data={
        "full_name": {"value": "John Doe", "description": "Full legal name"},
        "date": {"value": "2024-01-15", "description": "Today's date"},
        "signature": {"value": "John Doe", "description": "Signature field"},
    }
)

result = client.fill("form.pdf", options=options)
result.save_output("filled_form.pdf")
```
