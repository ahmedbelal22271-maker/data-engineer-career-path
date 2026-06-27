# Extraction Confidence Scoring

> Score extraction results with per-field confidence ratings and reasoning.

Score your structured extraction results to get per-field confidence ratings (1–5) with reasoning that explains what evidence was found or missing.

<Note>
  **Extraction scoring is in beta.**

  We'd love your feedback — reach out at [support@datalab.to](mailto:support@datalab.to).

  Scoring is free.
</Note>

**Before you begin**, make sure you have:

1. A [Datalab account](https://www.datalab.to/auth/sign_up) with an [API key](https://www.datalab.to/app/keys) (new accounts include \$5 in free credits)
2. Python 3.10+ installed
3. The Datalab SDK: `pip install datalab-python-sdk`
4. Your `DATALAB_API_KEY` environment variable set

## How It Works

Scoring runs automatically after every extraction. When you poll `request_check_url`, the extraction result initially contains just the extracted fields and citations. If you continue polling the same URL, the response will eventually include `_score` fields and an `extraction_score_average` once scoring completes.

Each scored field receives:

* A **score** from 1 (very low confidence) to 5 (high confidence)
* A **reasoning** string explaining what evidence supports or undermines the extracted value

No extra parameters or endpoints are needed — just keep polling until scores appear.

<Info>
  **Using balanced extraction mode?** Balanced mode includes its own per-field verification (`_meta.verification`) that runs as part of the extraction pipeline. Confidence scoring is designed for fast mode — if you're using balanced mode, the built-in verification metadata provides richer per-field quality signals. See [Balanced Mode](/docs/recipes/structured-extraction/balanced-mode).
</Info>

## Example

<CodeGroup>
  ```python Python (requests) theme={null}
  import requests, json, time, os

  headers = {"X-API-Key": os.getenv("DATALAB_API_KEY")}

  schema = {
      "type": "object",
      "properties": {
          "invoice_number": {"type": "string", "description": "Invoice ID or number"},
          "total_amount": {"type": "number", "description": "Total amount due"},
          "vendor_name": {"type": "string", "description": "Vendor or company name"}
      },
      "required": ["invoice_number", "total_amount"]
  }

  with open("invoice.pdf", "rb") as f:
      resp = requests.post(
          "https://www.datalab.to/api/v1/extract",
          files={"file": ("invoice.pdf", f, "application/pdf")},
          data={
              "page_schema": json.dumps(schema),
              "mode": "balanced"
          },
          headers=headers
      )
  check_url = resp.json()["request_check_url"]

  # Poll until extraction is complete
  while True:
      result = requests.get(check_url, headers=headers).json()
      if result["status"] == "complete":
          extracted = json.loads(result["extraction_schema_json"])
          print("Extraction:", extracted)
          break
      time.sleep(2)

  # Continue polling — scores are enriched asynchronously
  while "extraction_score_average" not in result:
      time.sleep(2)
      result = requests.get(check_url, headers=headers).json()

  scored = json.loads(result["extraction_schema_json"])
  for key, value in scored.items():
      if key.endswith("_score"):
          field = key.replace("_score", "")
          print(f"{field}: score={value['score']}, reasoning={value['reasoning']}")
  ```

  ```bash cURL theme={null}
  curl -X POST https://www.datalab.to/api/v1/extract \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -F "file=@invoice.pdf" \
    -F 'page_schema={"type":"object","properties":{"invoice_number":{"type":"string","description":"Invoice ID"},"total_amount":{"type":"number","description":"Total due"},"vendor_name":{"type":"string","description":"Vendor or company name"}}}' \
    -F "mode=balanced"

  # Poll request_check_url until status is "complete" for extraction results.
  # Continue polling — scores will appear in the response once scoring finishes.
  ```
</CodeGroup>

## Response Format

Without scoring, `extraction_schema_json` contains fields and citations:

```json theme={null}
{
  "invoice_number": "INV-2024-001",
  "invoice_number_citations": ["block_123"],
  "total_amount": 1500.00,
  "total_amount_citations": ["block_456"]
}
```

With scoring, each field also gets a `_score` object, and the top-level response includes an `extraction_score_average`:

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

### Score Rubric

| Score | Meaning                                                    |
| ----- | ---------------------------------------------------------- |
| 5     | High confidence — clear match with strong citation support |
| 4     | Good confidence — match found with minor ambiguity         |
| 3     | Moderate confidence — partial match or uncertain citation  |
| 2     | Low confidence — match is inferred or weakly supported     |
| 1     | Very low confidence — no clear evidence found              |

## Using Scores in Practice

Use `extraction_score_average` for a quick quality check, then inspect individual `_score` fields to flag low-confidence results:

```python theme={null}
import json

# After getting scored result (from either approach)
avg = result["extraction_score_average"]
print(f"Average score: {avg}")

scored = json.loads(result["extraction_schema_json"])
for key, value in scored.items():
    if not key.endswith("_score"):
        continue

    field = key.replace("_score", "")
    if value["score"] <= 2:
        print(f"Low confidence for '{field}': {value['reasoning']}")
    elif value["score"] >= 4:
        print(f"'{field}' = {scored[field]}")
```

This is useful for building review workflows — auto-accept high-confidence fields and route low-confidence ones to a human reviewer.

## Next Steps

<CardGroup cols={2}>
  <Card title="Structured Extraction" icon="table" href="/docs/recipes/structured-extraction/api-overview">
    Full extraction API reference and schema examples
  </Card>

  <Card title="Handling Long Documents" icon="file-lines" href="/docs/recipes/structured-extraction/handling-long-documents">
    Strategies for extracting from 100+ page documents
  </Card>

  <Card title="Pipelines" icon="workflow" href="/docs/recipes/pipelines/pipeline-overview">
    Chain processors into versioned, reusable pipelines.
  </Card>

  <Card title="Document Conversion" icon="file-text" href="/docs/recipes/conversion/conversion-api-overview">
    Convert documents to various formats
  </Card>
</CardGroup>