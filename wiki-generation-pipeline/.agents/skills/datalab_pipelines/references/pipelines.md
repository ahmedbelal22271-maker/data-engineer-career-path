# Pipelines

> Build versioned document processing pipelines by chaining processors together.

Pipelines chain processors — convert, extract, segment, and custom — into a single reusable unit. Define a pipeline once, version it, and run it against any document with one API call.

**Before you begin**, make sure you have:

1. A [Datalab account](https://www.datalab.to/auth/sign_up) with an [API key](https://www.datalab.to/app/keys) (new accounts include \$5 in free credits)
2. Python 3.10+ installed
3. The Datalab SDK: `pip install datalab-python-sdk`
4. Your `DATALAB_API_KEY` environment variable set

## Why Pipelines

Individual endpoints like `/convert` and `/extract` work well for one-off tasks. Pipelines are better when you need to:

* **Chain processors** — Convert a document, then extract structured data, in one call
* **Version your configuration** — Pin production integrations to a specific version while iterating on drafts
* **Standardize processing** — Share pipeline configurations across your team
* **Track execution** — Monitor each processor's status as a pipeline runs

<Info>
  You can build pipelines visually in [Forge](https://www.datalab.to/app/playground) or programmatically via the SDK and API.
</Info>

## How Pipelines Work

A pipeline is an ordered chain of processors. Each processor processes the document and passes its output to the next via checkpoints.

```
convert → segment → extract
```

Most pipelines start with `convert`. The `fill` processor is the exception — it runs as a standalone step and cannot be chained.

### Processor Types

| Processor | Description                                                         | Can Follow                     |
| --------- | ------------------------------------------------------------------- | ------------------------------ |
| `convert` | Parse document to markdown/HTML/JSON                                | Must be first                  |
| `segment` | Split document into logical sections                                | `convert`                      |
| `extract` | Extract structured data using a JSON schema                         | `convert`, `segment`, `custom` |
| `custom`  | Run a [custom processor](/docs/recipes/pipelines/custom-processors) | `convert`                      |
| `fill`    | Fill form fields in a PDF or image                                  | Standalone only                |

### Composition Rules

* Every pipeline starts with a `convert` or `fill` processor
* `extract` is always terminal (nothing can follow it)
* `segment` can feed into `extract`
* `custom` can feed into `extract`
* `fill` is always standalone — it cannot follow or precede other processors

Common patterns:

| Pattern                       | Use Case                                 |
| ----------------------------- | ---------------------------------------- |
| `convert`                     | Simple document parsing                  |
| `convert → extract`           | Parse and extract structured fields      |
| `convert → segment`           | Parse and split into sections            |
| `convert → segment → extract` | Split, then extract from each section    |
| `convert → custom → extract`  | Apply custom processing, then extract    |
| `fill`                        | Version and track form-filling workflows |

## Pipeline Lifecycle

Pipelines have three states:

1. **Draft** — Edits auto-save. Not versioned yet.
2. **Saved** — Named and visible in your pipeline list.
3. **Published** — An immutable version snapshot. Safe to use in production.

```
Create (draft) → Save (named) → Publish version (immutable)
         ↑                              |
         └──── Edit (new draft) ←───────┘
```

When you edit a published pipeline, your changes go into a draft. The published version remains unchanged until you publish a new version. You can discard the draft at any time to revert.

See [Pipeline Versioning](/docs/recipes/pipelines/pipeline-versioning) for the full lifecycle.

## Quick Example

Create a pipeline that converts a document and extracts invoice data:

<CodeGroup>
  ```python Python SDK theme={null}
  from datalab_sdk import DatalabClient, PipelineProcessor

  client = DatalabClient()

  # Define steps
  steps = [
      PipelineProcessor(type="convert", settings={"mode": "balanced"}),
      PipelineProcessor(type="extract", settings={
          "page_schema": {
              "type": "object",
              "properties": {
                  "invoice_number": {"type": "string"},
                  "total_amount": {"type": "number"},
                  "vendor_name": {"type": "string"}
              }
          }
      })
  ]

  # Create and save
  pipeline = client.create_pipeline(steps=steps)
  pipeline = client.save_pipeline(pipeline.pipeline_id, name="Invoice Extractor")

  # Run on a document
  execution = client.run_pipeline(
      pipeline.pipeline_id,
      file_path="invoice.pdf"
  )

  # Poll until complete
  execution = client.get_pipeline_execution(
      execution.execution_id,
      max_polls=300
  )

  # Get extraction result
  result = client.get_step_result(execution.execution_id, step_index=1)
  print(result)
  ```

  ```bash cURL theme={null}
  # Create pipeline
  curl -X POST https://www.datalab.to/api/v1/pipelines \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "steps": [
        {"type": "convert", "settings": {"mode": "balanced"}},
        {"type": "extract", "settings": {
          "page_schema": {
            "type": "object",
            "properties": {
              "invoice_number": {"type": "string"},
              "total_amount": {"type": "number"}
            }
          }
        }}
      ]
    }'

  # Save pipeline (use pipeline_id from response)
  curl -X PUT https://www.datalab.to/api/v1/pipelines/PIPELINE_ID/save \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"name": "Invoice Extractor"}'

  # Run pipeline
  curl -X POST https://www.datalab.to/api/v1/pipelines/PIPELINE_ID/run \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -F "file=@invoice.pdf"

  # Poll execution (use execution_id from response)
  curl https://www.datalab.to/api/v1/pipelines/executions/EXECUTION_ID \
    -H "X-API-Key: $DATALAB_API_KEY"
  ```

  ```python Python (requests) theme={null}
  import os, time, requests, json

  BASE = "https://www.datalab.to/api/v1"
  headers = {"X-API-Key": os.getenv("DATALAB_API_KEY")}

  # Create pipeline
  resp = requests.post(f"{BASE}/pipelines", headers={
      **headers, "Content-Type": "application/json"
  }, json={
      "steps": [
          {"type": "convert", "settings": {"mode": "balanced"}},
          {"type": "extract", "settings": {
              "page_schema": json.dumps({
                  "type": "object",
                  "properties": {
                      "invoice_number": {"type": "string"},
                      "total_amount": {"type": "number"}
                  }
              })
          }}
      ]
  })
  pipeline_id = resp.json()["pipeline_id"]

  # Save
  requests.put(f"{BASE}/pipelines/{pipeline_id}/save",
      headers={**headers, "Content-Type": "application/json"},
      json={"name": "Invoice Extractor"})

  # Run
  with open("invoice.pdf", "rb") as f:
      resp = requests.post(f"{BASE}/pipelines/{pipeline_id}/run",
          headers=headers,
          files={"file": ("invoice.pdf", f, "application/pdf")})
  execution_id = resp.json()["execution_id"]

  # Poll
  for _ in range(300):
      resp = requests.get(f"{BASE}/pipelines/executions/{execution_id}",
          headers=headers)
      data = resp.json()
      if data["status"] in ("completed", "failed"):
          break
      time.sleep(2)

  # Get step result
  resp = requests.get(
      f"{BASE}/pipelines/executions/{execution_id}/steps/1/result",
      headers=headers)
  print(resp.json())
  ```
</CodeGroup>

## Pipelines vs Individual Endpoints

|                   | Individual Endpoints      | Pipelines                        |
| ----------------- | ------------------------- | -------------------------------- |
| **Processors**    | One at a time             | Chain multiple processors        |
| **Versioning**    | None                      | Draft, saved, published versions |
| **Configuration** | Pass options per request  | Configure once, reuse            |
| **Forge UI**      | Playground                | Full pipeline builder            |
| **Best for**      | Quick tests, simple tasks | Production integrations          |

Individual endpoints (`/convert`, `/extract`, `/segment`) are not going away. Use them for simple, one-off processing. Use Pipelines when you need repeatability, versioning, or multi-processor chains.

## Next Steps

<CardGroup cols={2}>
  <Card title="Create a Pipeline" icon="hammer" href="/docs/recipes/pipelines/create-pipeline">
    Build your first pipeline with Forge or the SDK.
  </Card>

  <Card title="Pipeline Versioning" icon="code-branch" href="/docs/recipes/pipelines/pipeline-versioning">
    Manage drafts, versions, and production deployments.
  </Card>

  <Card title="Run a Pipeline" icon="play" href="/docs/recipes/pipelines/run-pipeline">
    Execute pipelines with overrides, polling, and webhooks.
  </Card>

  <Card title="SDK Reference" icon="code" href="/docs/welcome/sdk/pipelines">
    Full SDK reference for all pipeline methods.
  </Card>
</CardGroup>