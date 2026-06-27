# Balanced Extraction Mode

> Extraction with per-field verification, reasoning, and citations.

Balanced mode runs an extraction pipeline with independent verification. Every extracted field includes an audit trail: where the value came from, how it was derived, and whether an independent check confirmed it.

**Before you begin**, make sure you have:

1. A [Datalab account](https://www.datalab.to/auth/sign_up) with an [API key](https://www.datalab.to/app/keys) (new accounts include \$5 in free credits)
2. Python 3.10+ installed
3. The Datalab SDK: `pip install datalab-python-sdk`
4. Your `DATALAB_API_KEY` environment variable set

## When to Use Fast vs Balanced

|                              | Fast                                                    | Balanced (default)                                                                         |
| ---------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Price**                    | \$6 / 1K pages                                          | \$25 / 1K pages                                                                            |
| **Latency**                  | Lowest                                                  | Slower — trades speed for accuracy via independent verification                            |
| **Per-field citations**      | Yes                                                     | Yes                                                                                        |
| **Extraction status**        | No                                                      | Yes (EXTRACTED / NOT\_RESOLVABLE)                                                          |
| **Per-field reasoning**      | No                                                      | Yes                                                                                        |
| **Independent verification** | No                                                      | Yes (PASS / FAIL)                                                                          |
| **Best for**                 | High-volume workflows: invoices, forms, bank statements | Compliance, financial, legal, and medical workflows where every field needs an audit trail |

Use **fast** when speed and cost matter most. Use **balanced** when you need to trust every field and want metadata to power downstream decisions.

## Schema size on short documents

For shorter documents (**under 20 pages**), balanced mode limits how large your schema can be. Documents of **20+ pages have no schema-size limit**.

If a schema is too large for a short document, the request fails with a clear error telling you your field count and your options — and **you aren't charged**.

### Count your fields

A **field** is one value you get back — a string, number, date, true/false, or one choice from a fixed list. **Objects and lists are containers, not fields** — count the fields inside them. A list of repeated items counts its fields **once**, no matter how many rows the document has.

**4 fields:**

```json theme={null}
{ "invoice_number": "string", "invoice_date": "string",
  "total_amount": "number", "currency": "string" }
```

**5 fields** — the object is a container, so count what's inside it:

```json theme={null}
{ "vendor": { "name": "string", "address": "string" },
  "total": "number", "due_date": "string", "paid": "boolean" }
```

**4 fields** — a list's columns count once, not once per row:

```json theme={null}
{ "invoice_number": "string",
  "line_items": [ { "description": "string", "quantity": "number", "unit_price": "number" } ] }
```

### How many fields can I use?

About **25 fields** is a comfortable limit for any schema on a short document. Larger schemas often work too — especially flat ones without deep nesting — but the more fields you add, and the more deeply they're nested (lists of objects several levels down), the more likely you are to reach the limit.

You don't have to guess: if a schema is too large for a short document, the request fails with a clear error (and you aren't charged), so it's safe to try a larger one.

If you need a bigger schema on a short document:

1. **Split it into multiple extractions** — for example, header fields in one request and a large list in another.
2. **Use `fast` mode** — it supports larger schemas and costs less, without the per-field verification metadata.
3. **Trim and flatten** — drop fields you don't use and reduce nesting.

<Note>This applies only to balanced mode on documents under 20 pages. Documents of 20+ pages support schemas of any size.</Note>

## Quick Start

<CodeGroup>
  ```python Python SDK theme={null}
  import json
  from datalab_sdk import DatalabClient, ExtractOptions

  client = DatalabClient()

  schema = {
      "type": "object",
      "properties": {
          "company_name": {"type": "string", "description": "Full legal name of the company"},
          "fiscal_year_end": {"type": "string", "description": "End date of the fiscal year (YYYY-MM-DD)"},
          "total_revenue": {"type": "number", "description": "Total revenue in the reporting currency"},
          "auditor_name": {"type": "string", "description": "Name of the external audit firm"}
      },
      "required": ["company_name", "fiscal_year_end"]
  }

  options = ExtractOptions(
      page_schema=json.dumps(schema),
      extraction_mode="balanced"
  )

  result = client.extract("annual_report.pdf", options=options)
  extracted = json.loads(result.extraction_schema_json)

  # Each field comes with citations and metadata
  print(f"Company: {extracted['company_name']}")
  print(f"Citations: {extracted['company_name_citations']}")
  print(f"Status: {extracted['company_name_meta']['extraction_status']}")
  print(f"Verified: {extracted['company_name_meta']['verification']['status']}")
  ```

  ```bash cURL theme={null}
  curl -X POST https://www.datalab.to/api/v1/extract \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -F "file=@annual_report.pdf" \
    -F "extraction_mode=balanced" \
    -F 'page_schema={"type":"object","properties":{"company_name":{"type":"string","description":"Full legal name"},"total_revenue":{"type":"number","description":"Total revenue"}}}'

  # Poll request_check_url from response until status is "complete"
  ```

  ```python Python (requests) theme={null}
  import requests, json, time, os

  headers = {"X-API-Key": os.getenv("DATALAB_API_KEY")}

  schema = {
      "type": "object",
      "properties": {
          "company_name": {"type": "string", "description": "Full legal name"},
          "total_revenue": {"type": "number", "description": "Total revenue"}
      }
  }

  with open("annual_report.pdf", "rb") as f:
      response = requests.post(
          "https://www.datalab.to/api/v1/extract",
          files={"file": ("annual_report.pdf", f, "application/pdf")},
          data={
              "page_schema": json.dumps(schema),
              "extraction_mode": "balanced"
          },
          headers=headers
      )

  check_url = response.json()["request_check_url"]

  while True:
      result = requests.get(check_url, headers=headers).json()
      if result["status"] == "complete":
          extracted = json.loads(result["extraction_schema_json"])
          print(json.dumps(extracted, indent=2))
          break
      elif result["status"] == "failed":
          print(f"Error: {result.get('error')}")
          break
      time.sleep(2)
  ```
</CodeGroup>

<Note>
  `extraction_mode` controls the extraction pipeline (`fast` or `balanced`). This is separate from `mode`, which controls the document parsing stage (`fast`, `balanced`, or `accurate`). You can combine them independently — for example, `mode="fast"` with `extraction_mode="balanced"`.
</Note>

## Response Format

In balanced mode, each extracted field includes three sibling keys. The `_citations` sibling is the same format as fast mode for compatibility — balanced mode adds `_meta` with richer metadata on top:

```json theme={null}
{
  "company_name": "Whitbread PLC",
  "company_name_citations": ["/page/0/Text/3", "/page/2/Table/1"],
  "company_name_meta": {
    "extraction_status": "EXTRACTED",
    "reasoning": "The company name 'Whitbread PLC' appears in the document header on the cover page (/page/0/Text/3) and is confirmed in the directors' report (/page/2/Table/1).",
    "citations": ["/page/0/Text/3", "/page/2/Table/1"],
    "verification": {
      "status": "PASS",
      "feedback": "The company name 'Whitbread PLC' is printed on the cover page (/page/0/Text/3) and confirmed in the directors' report. No conflicting name appears in the document."
    }
  }
}
```

The `_citations` key is shared with fast mode — if you switch between modes, citation-consuming code continues to work. The `_meta` key is balanced-mode-only and contains the full audit trail.

### Field Metadata

Each `_meta` object contains:

| Field               | Description                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `extraction_status` | How the value was produced: `EXTRACTED` (value found in the document) or `NOT_RESOLVABLE` (document doesn't contain this information) |
| `reasoning`         | Audit-ready prose explaining how the value was produced, with block ID citations                                                      |
| `citations`         | Block IDs from the source document that support the value                                                                             |
| `verification`      | Independent verification result with `status` and `feedback`                                                                          |

### Extraction Status

| Status           | Meaning                                             | Value               |
| ---------------- | --------------------------------------------------- | ------------------- |
| `EXTRACTED`      | The value was found in or derived from the document | The extracted value |
| `NOT_RESOLVABLE` | The document does not contain or imply this value   | `null`              |

### Verification Status

| Status              | Meaning                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------ |
| `PASS`              | The value and citations were independently confirmed against the source document                 |
| `FAIL_UNRESOLVABLE` | The document does not support a value for this field                                             |
| `FAIL_FIX`          | The value was flagged as incorrect during verification — the document supports a different value |
| `FAIL_CITATIONS`    | The value is correct but the citations are wrong or insufficient                                 |
| `ITEMS_MISSING`     | (List fields only) The document contains entries that are not present in the extraction          |

In practice, most fields will be `PASS` or `FAIL_UNRESOLVABLE` after verification. The other statuses indicate cases where the verifier flagged an issue that could not be fully resolved automatically.

## Building Workflows with Verification Metadata

The per-field metadata enables automated quality gates:

```python theme={null}
import json

extracted = json.loads(result.extraction_schema_json)

# Separate fields by verification status
auto_approved = []
needs_review = []

# Walk all fields and check their _meta
for key, value in extracted.items():
    if key.endswith("_meta"):
        field_name = key.removesuffix("_meta")
        meta = value
        verification = meta.get("verification", {})

        if verification.get("status") == "PASS":
            auto_approved.append(field_name)
        else:
            needs_review.append({
                "field": field_name,
                "extraction_status": meta.get("extraction_status"),
                "reasoning": meta.get("reasoning"),
                "verification_feedback": verification.get("feedback"),
            })

print(f"Auto-approved: {len(auto_approved)} fields")
print(f"Needs review: {len(needs_review)} fields")

# Route to human review queue
for item in needs_review:
    print(f"  {item['field']}: {item['extraction_status']}")
    print(f"    Reason: {item['reasoning'][:100]}...")
```

### Common Workflow Patterns

* **Auto-approve** when all fields have `verification.status == "PASS"` — no human review needed
* **Flag for review** when any field is `NOT_RESOLVABLE` or has a `FAIL_*` verification status — the document may be missing information or the extraction needs a human check
* **Show citations** to reviewers so they can verify in seconds — each field links back to specific blocks in the document
* **Use reasoning as an audit trail** — for compliance workflows, the per-field reasoning documents exactly how each value was produced, with block-level citations back to the source document

## Next Steps

<CardGroup cols={2}>
  <Card title="Structured Extraction Overview" icon="table" href="/docs/recipes/structured-extraction/api-overview">
    Schema format, response structure, and extraction tips
  </Card>

  <Card title="Confidence Scoring" icon="chart-bar" href="/docs/recipes/structured-extraction/confidence-scoring">
    Additional per-field confidence scores (works with both modes)
  </Card>

  <Card title="Saved Schemas" icon="bookmark" href="/docs/recipes/structured-extraction/saved-schemas">
    Save and version schemas for reuse across requests
  </Card>

  <Card title="Handling Long Documents" icon="file-lines" href="/docs/recipes/structured-extraction/handling-long-documents">
    Tips for extracting from 100+ page documents
  </Card>
</CardGroup>