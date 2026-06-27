# Structured Extraction

> Extract structured data from documents using JSON schemas.

Extract specific fields from documents by providing a JSON schema. Marker parses the document and fills in your schema with extracted values.

**Before you begin**, make sure you have:

1. A [Datalab account](https://www.datalab.to/auth/sign_up) with an [API key](https://www.datalab.to/app/keys) (new accounts include \$5 in free credits)
2. Python 3.10+ installed
3. The Datalab SDK: `pip install datalab-python-sdk`
4. Your `DATALAB_API_KEY` environment variable set

<Info>
  **Building for production?** Use [Pipelines](/docs/recipes/pipelines/pipeline-overview) to chain processors, version your configuration, and deploy with a single API call.
</Info>

## Quick Start

<CodeGroup>
  ```python Python SDK theme={null}
  import json
  from datalab_sdk import DatalabClient, ExtractOptions

  client = DatalabClient()

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
  print(f"Invoice: {extracted['invoice_number']}")
  print(f"Total: ${extracted['total_amount']}")
  ```

  ```bash cURL theme={null}
  curl -X POST https://www.datalab.to/api/v1/extract \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -F "file=@invoice.pdf" \
    -F "mode=balanced" \
    -F 'page_schema={"type":"object","properties":{"invoice_number":{"type":"string","description":"Invoice ID"},"total_amount":{"type":"number","description":"Total due"}}}'

  # Poll request_check_url from response until status is "complete"
  ```

  ```python Python (requests) theme={null}
  import requests, json, time, os

  headers = {"X-API-Key": os.getenv("DATALAB_API_KEY")}

  schema = {
      "type": "object",
      "properties": {
          "invoice_number": {"type": "string", "description": "Invoice ID"},
          "total_amount": {"type": "number", "description": "Total due"}
      }
  }

  with open("invoice.pdf", "rb") as f:
      response = requests.post(
          "https://www.datalab.to/api/v1/extract",
          files={"file": ("invoice.pdf", f, "application/pdf")},
          data={"page_schema": json.dumps(schema), "mode": "balanced"},
          headers=headers
      )

  check_url = response.json()["request_check_url"]

  while True:
      result = requests.get(check_url, headers=headers).json()
      if result["status"] == "complete":
          extracted = json.loads(result["extraction_schema_json"])
          print(extracted)
          break
      elif result["status"] == "failed":
          print(f"Error: {result.get('error')}")
          break
      time.sleep(2)
  ```
</CodeGroup>

## Extraction Modes

The `extraction_mode` parameter controls how extraction runs. This is separate from `mode`, which controls document parsing.

| Mode                   | Description                                                                          | Price           | Latency                                   |
| ---------------------- | ------------------------------------------------------------------------------------ | --------------- | ----------------------------------------- |
| **fast**               | Extraction with per-field citations                                                  | \$6 / 1K pages  | Lowest                                    |
| **balanced** (default) | Extraction with independent verification, per-field reasoning, and extraction status | \$25 / 1K pages | Slower — trades speed for higher accuracy |

Both modes return citations for every extracted field. Balanced mode additionally returns `_meta` per field with `extraction_status`, `reasoning`, and `verification` results.

<Note>
  `balanced` is the default. Teams that made an extraction request in the 30 days before June 4, 2026 default to `fast` instead. Pass `extraction_mode` explicitly to override the default in either case.
</Note>

```python theme={null}
# Fast
options = ExtractOptions(page_schema=json.dumps(schema), extraction_mode="fast")

# Balanced (default)
options = ExtractOptions(page_schema=json.dumps(schema))
```

See [Balanced Extraction Mode](/docs/recipes/structured-extraction/balanced-mode) for a full guide on the balanced mode response format and building workflows with verification metadata.

## Schema Format

Use JSON Schema format to define what you want to extract:

```json theme={null}
{
  "type": "object",
  "properties": {
    "field_name": {
      "type": "string",
      "description": "Describe what this field contains"
    },
    "numeric_field": {
      "type": "number",
      "description": "A numeric value"
    },
    "list_field": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "nested_field": {"type": "string"}
        }
      }
    }
  },
  "required": ["field_name"]
}
```

### Tips for Better Extraction

1. **Use descriptive field names** - `invoice_number` is clearer than `id`
2. **Add descriptions** - The `description` field helps the model understand context
3. **Specify types correctly** - Use `number` for numeric values, `string` for text
4. **Use arrays for repeating data** - Line items, table rows, etc.

<Warning>
  **Common schema pitfalls:**

  * Using vague field names like `data` or `info` — be specific (e.g., `invoice_number`, `total_amount`)
  * Forgetting `description` fields — these help the model understand what to extract
  * Setting `type: "string"` for numeric values — use `type: "number"` for amounts, quantities, etc.
  * Deeply nested schemas — keep schemas as flat as possible for better extraction accuracy
</Warning>

## Response

The extracted data is returned in `extraction_schema_json`:

```json theme={null}
{
  "status": "complete",
  "success": true,
  "json": {...},
  "extraction_schema_json": "{\"invoice_number\": \"INV-2024-001\", \"total_amount\": 1500.00, ...}",
  "page_count": 2
}
```

### Citation Tracking

Each extracted field includes citations to the source blocks:

```json theme={null}
{
  "invoice_number": "INV-2024-001",
  "invoice_number_citations": ["block_123", "block_124"],
  "total_amount": 1500.00,
  "total_amount_citations": ["block_456"]
}
```

Use these block IDs with the `json` output to trace extracted values back to the source document.

## Schema Examples

### Financial Document

```python theme={null}
schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string", "description": "Company name"},
        "fiscal_year": {"type": "string", "description": "Fiscal year"},
        "total_revenue": {"type": "number", "description": "Total revenue in dollars"},
        "net_income": {"type": "number", "description": "Net income in dollars"},
        "eps": {"type": "number", "description": "Earnings per share"}
    }
}
```

### Scientific Paper

```python theme={null}
schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Paper title"},
        "authors": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of author names"
        },
        "abstract": {"type": "string", "description": "Paper abstract"},
        "keywords": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Keywords or tags"
        }
    }
}
```

### Contract

```python theme={null}
schema = {
    "type": "object",
    "properties": {
        "parties": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "role": {"type": "string"}
                }
            }
        },
        "effective_date": {"type": "string", "description": "Contract start date"},
        "termination_date": {"type": "string", "description": "Contract end date"},
        "total_value": {"type": "number", "description": "Total contract value"}
    }
}
```

## Using Checkpoints

If you already converted a document with `save_checkpoint=True` using the [Convert API](/docs/recipes/conversion/conversion-api-overview), pass the `checkpoint_id` to `ExtractOptions` to skip re-parsing. This saves time and cost when running extraction on a previously converted document.

```python theme={null}
from datalab_sdk import DatalabClient, ConvertOptions, ExtractOptions
import json

client = DatalabClient()

# Step 1: Convert and save checkpoint
convert_result = client.convert("invoice.pdf", options=ConvertOptions(save_checkpoint=True))
checkpoint_id = convert_result.checkpoint_id

# Step 2: Extract using checkpoint (no re-parsing needed)
schema = {
    "type": "object",
    "properties": {
        "invoice_number": {"type": "string", "description": "Invoice ID"},
        "total_amount": {"type": "number", "description": "Total due"}
    }
}

options = ExtractOptions(
    page_schema=json.dumps(schema),
    checkpoint_id=checkpoint_id
)
result = client.extract("invoice.pdf", options=options)
extracted = json.loads(result.extraction_schema_json)
```

The extract endpoint accepts the following parameters: `file`, `page_schema` or `schema_id` (one is required), `schema_version`, `mode`, `max_pages`, `page_range`, `save_checkpoint`, `checkpoint_id`, `webhook_url`, and `processing_location` (e.g. `"eu"` — routes processing and storage to EU infrastructure; requires `file_url` or a pre-uploaded `datalab://` reference instead of a multipart upload).

### Using Saved Schemas

Instead of passing `page_schema` inline, you can save schemas to Datalab and reference them by ID. This avoids repeating the schema in every request and enables versioning.

```bash theme={null}
curl -X POST https://www.datalab.to/api/v1/extract \
  -H "X-API-Key: $DATALAB_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "schema_id=sch_k8Hx9mP2nQ4v"
```

Pass `schema_version` to pin to a specific schema version; omit it to always use the latest. See [Saved Schemas](/docs/recipes/structured-extraction/saved-schemas) for full CRUD API reference.

## Confidence Scoring

<Note>
  **Extraction scoring is in beta.**

  We'd love your feedback — reach out at [support@datalab.to](mailto:support@datalab.to).

  Scoring is free.
</Note>

Scoring runs automatically after every extraction. When you poll `request_check_url`, the response initially contains just the extracted fields and citations. If you continue polling the same URL, the response will eventually include `_score` fields and an `extraction_score_average` once scoring completes. No extra parameters or endpoints are needed.

Each `_score` field is a `{"score": int, "reasoning": str}` object explaining what evidence was found or missing.

### Score response format

Without scoring complete, `extraction_schema_json` contains fields and citations:

```json theme={null}
{
  "invoice_number": "INV-2024-001",
  "invoice_number_citations": ["block_123"],
  "total_amount": 1500.00,
  "total_amount_citations": ["block_456"]
}
```

Once scoring finishes, each field also gets a `_score` object, and the top-level response includes an `extraction_score_average`:

```json theme={null}
{
  "invoice_number": "INV-2024-001",
  "invoice_number_citations": ["block_123"],
  "invoice_number_score": {
    "score": 5,
    "reasoning": "Value found verbatim in the document header with a matching citation."
  },
  "total_amount": 1500.00,
  "total_amount_citations": ["block_456"],
  "total_amount_score": {
    "score": 4,
    "reasoning": "Amount found in the totals row; minor ambiguity due to a subtotal nearby."
  }
}
```

The top-level response also includes `extraction_score_average` (4.5 in this case), averaging all field scores.

**Score rubric:**

| Score | Meaning                                                    |
| ----- | ---------------------------------------------------------- |
| 5     | High confidence — clear match with strong citation support |
| 4     | Good confidence — match found with minor ambiguity         |
| 3     | Moderate confidence — partial match or uncertain citation  |
| 2     | Low confidence — match is inferred or weakly supported     |
| 1     | Very low confidence — no clear evidence found              |

See [Confidence Scoring](/docs/recipes/structured-extraction/confidence-scoring) for a full walkthrough with code examples.

## Auto-Generate Schemas

Don't want to write schemas by hand? Use the schema generation endpoint to automatically suggest schemas for your document. This requires a checkpoint from a previous conversion:

```python theme={null}
import os, requests, json, time

headers = {"X-API-Key": os.getenv("DATALAB_API_KEY")}

# Step 1: Convert with checkpoint
with open("invoice.pdf", "rb") as f:
    resp = requests.post(
        "https://www.datalab.to/api/v1/convert",
        files={"file": ("invoice.pdf", f, "application/pdf")},
        data={"save_checkpoint": "true", "output_format": "markdown"},
        headers=headers
    )
check_url = resp.json()["request_check_url"]

# Poll until complete
while True:
    result = requests.get(check_url, headers=headers).json()
    if result["status"] == "complete":
        checkpoint_id = result["checkpoint_id"]
        break
    time.sleep(2)

# Step 2: Generate schemas
resp = requests.post(
    "https://www.datalab.to/api/v1/marker/extraction/gen_schemas",
    json={"checkpoint_id": checkpoint_id},
    headers=headers
)
gen_check_url = resp.json()["request_check_url"]

while True:
    result = requests.get(gen_check_url, headers=headers).json()
    if result["status"] == "complete":
        suggestions = result["suggestions"]
        print("Simple schema:", suggestions["simple_schema"])
        print("Moderate schema:", suggestions["moderate_schema"])
        print("Complex schema:", suggestions["complex_schema"])
        break
    time.sleep(2)
```

The endpoint returns three schema options at different complexity levels — use the one that best matches your needs, then customize it.

## Using Forge Playground

Create and test schemas visually in [Forge Playground](https://www.datalab.to/app/playground):

1. Upload a sample document
2. Define fields in the visual editor
3. Switch to JSON Editor to copy the schema
4. Test extraction before deploying

## Next Steps

<CardGroup cols={2}>
  <Card title="Balanced Extraction Mode" icon="shield-check" href="/docs/recipes/structured-extraction/balanced-mode">
    Per-field verification, reasoning, and extraction status for compliance workflows
  </Card>

  <Card title="Saved Schemas" icon="bookmark" href="/docs/recipes/structured-extraction/saved-schemas">
    Create reusable schemas and reference them by ID — no need to repeat the schema in each request
  </Card>

  <Card title="Confidence Scoring" icon="chart-bar" href="/docs/recipes/structured-extraction/confidence-scoring">
    Score extraction results with per-field confidence ratings
  </Card>

  <Card title="Handling Long Documents" icon="file-lines" href="/docs/recipes/structured-extraction/handling-long-documents">
    Strategies for extracting from 100+ page documents
  </Card>
</CardGroup>