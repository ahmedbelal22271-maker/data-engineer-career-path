# Run a Pipeline

> Execute pipelines with version selection, overrides, polling, and per-processor result retrieval.

**Before you begin**, make sure you have:

1. A [Datalab account](https://www.datalab.to/auth/sign_up) with an [API key](https://www.datalab.to/app/keys) (new accounts include \$5 in free credits)
2. Python 3.10+ installed
3. The Datalab SDK: `pip install datalab-python-sdk`
4. Your `DATALAB_API_KEY` environment variable set

## Basic Execution

Run a pipeline on a document:

<CodeGroup>
  ```python Python SDK theme={null}
  from datalab_sdk import DatalabClient

  client = DatalabClient()

  execution = client.run_pipeline(
      "pl_abc123",
      file_path="document.pdf"
  )

  # Poll until complete
  execution = client.get_pipeline_execution(
      execution.execution_id,
      max_polls=300,
      poll_interval=2
  )

  print(f"Status: {execution.status}")
  ```

  ```bash cURL theme={null}
  # Start execution
  curl -X POST https://www.datalab.to/api/v1/pipelines/PIPELINE_ID/run \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -F "file=@document.pdf"

  # Poll for completion (use execution_id from response)
  curl https://www.datalab.to/api/v1/pipelines/executions/EXECUTION_ID \
    -H "X-API-Key: $DATALAB_API_KEY"
  ```

  ```python Python (requests) theme={null}
  import os, time, requests

  BASE = "https://www.datalab.to/api/v1"
  headers = {"X-API-Key": os.getenv("DATALAB_API_KEY")}

  # Start execution
  with open("document.pdf", "rb") as f:
      resp = requests.post(f"{BASE}/pipelines/pl_abc123/run",
          headers=headers,
          files={"file": ("document.pdf", f, "application/pdf")})

  execution_id = resp.json()["execution_id"]

  # Poll
  for _ in range(300):
      resp = requests.get(f"{BASE}/pipelines/executions/{execution_id}",
          headers=headers)
      data = resp.json()
      if data["status"] in ("completed", "completed_with_errors", "failed"):
          break
      time.sleep(2)

  print(f"Status: {data['status']}")
  ```
</CodeGroup>

You can also pass a URL instead of a file:

```python theme={null}
execution = client.run_pipeline(
    "pl_abc123",
    file_url="https://example.com/document.pdf"
)
```

## Version Selection

The `version` parameter controls which pipeline configuration runs:

| Value            | Behavior                                                                           |
| ---------------- | ---------------------------------------------------------------------------------- |
| Omitted / `None` | Runs the **active published version**. If no version is published, runs the draft. |
| `0`              | Explicitly runs the **draft** (current unpublished edits).                         |
| `1`, `2`, ...    | Runs a **specific published version**.                                             |

```python theme={null}
# Run active published version (recommended for production)
execution = client.run_pipeline("pl_abc123", file_path="doc.pdf")

# Run draft for testing
execution = client.run_pipeline("pl_abc123", file_path="doc.pdf", version=0)

# Pin to specific version
execution = client.run_pipeline("pl_abc123", file_path="doc.pdf", version=2)
```

<Warning>
  If you omit `version` and no version has been published, the draft runs. Publish a version before using a pipeline in production to avoid running unfinished drafts.
</Warning>

## Run-Level Overrides

Override pipeline behavior per execution without changing the pipeline configuration:

```python theme={null}
execution = client.run_pipeline(
    "pl_abc123",
    file_path="document.pdf",
    page_range="0-5",          # Process specific pages
    output_format="json",      # Override output format
    skip_cache=True,           # Force reprocessing (skip cached results)
    run_evals=True,            # Run evaluation rubrics defined on steps
    webhook_url="https://example.com/webhook",  # Notify on completion
    version=2,                 # Pin to version 2
)
```

### Override Reference

| Parameter       | Type | Default | Description                                                  |
| --------------- | ---- | ------- | ------------------------------------------------------------ |
| `file_path`     | str  | -       | Local file to process (mutually exclusive with `file_url`)   |
| `file_url`      | str  | -       | URL to document                                              |
| `page_range`    | str  | -       | Pages to process (e.g., `"0-5,10"`, 0-indexed)               |
| `output_format` | str  | -       | Override output format: `markdown`, `html`, `json`, `chunks` |
| `skip_cache`    | bool | `False` | Skip cached results, reprocess from scratch                  |
| `run_evals`     | bool | `False` | Run evaluation rubrics configured on steps                   |
| `webhook_url`   | str  | -       | URL to POST when execution completes                         |
| `version`       | int  | -       | Pipeline version to run (see above)                          |
| `max_polls`     | int  | `1`     | Polling attempts after submission                            |
| `poll_interval` | int  | `1`     | Seconds between polls                                        |

## Execution Status

Poll for status using `get_pipeline_execution()`:

```python theme={null}
execution = client.get_pipeline_execution(
    execution.execution_id,
    max_polls=300,      # Keep polling until complete
    poll_interval=2     # Check every 2 seconds
)

print(f"Status: {execution.status}")
print(f"Version: {execution.pipeline_version}")
print(f"Started: {execution.started_at}")
print(f"Completed: {execution.completed_at}")
```

### Status Values

| Status                  | Description                       |
| ----------------------- | --------------------------------- |
| `pending`               | Queued, not started               |
| `running`               | Processors are executing          |
| `completed`             | All steps finished successfully   |
| `completed_with_errors` | Some steps completed, some failed |
| `failed`                | Execution failed                  |

### Per-Processor Tracking

Each processor in the execution reports its own status:

```python theme={null}
for step in execution.steps:
    print(f"Step {step.step_index} ({step.step_type}): {step.status}")
    if step.error_message:
        print(f"  Error: {step.error_message}")
    if step.result_url:
        print(f"  Result available")
```

Step status values: `pending`, `dispatched`, `running`, `completed`, `failed`, `skipped`.

## Retrieve Processor Results

Fetch the output of a specific processor:

```python theme={null}
# Get result for step at index 1 (e.g., extract step)
result = client.get_step_result(execution.execution_id, step_index=1)
print(result)
```

<CodeGroup>
  ```bash cURL theme={null}
  curl https://www.datalab.to/api/v1/pipelines/executions/EXECUTION_ID/steps/1/result \
    -H "X-API-Key: $DATALAB_API_KEY"
  ```

  ```python Python (requests) theme={null}
  resp = requests.get(
      f"{BASE}/pipelines/executions/{execution_id}/steps/1/result",
      headers=headers)
  print(resp.json())
  ```
</CodeGroup>

<Warning>
  Results are deleted from Datalab servers one hour after processing completes. Retrieve your results promptly.
</Warning>

## Webhooks

Get notified when a pipeline execution completes instead of polling:

```python theme={null}
execution = client.run_pipeline(
    "pl_abc123",
    file_path="document.pdf",
    webhook_url="https://your-server.com/pipeline-webhook"
)
```

Datalab sends a POST request to your webhook URL when the execution reaches a terminal status. See [Webhooks](/platform/webhooks) for payload details.

## List Executions

View recent executions for a pipeline:

```python theme={null}
result = client.list_pipeline_executions("pl_abc123", limit=20)

for ex in result["executions"]:
    print(f"{ex.execution_id}: {ex.status} (v{ex.pipeline_version})")
```

## Billing

Pipeline execution is billed per page, with rates additive across processors. Each processor type has its own per-page rate. Check a pipeline's rate before running:

```python theme={null}
rate = client.get_pipeline_rate("pl_abc123")
print(f"Rate per 1000 pages: {rate['rate_per_1000_pages_cents']} cents")
print(f"Breakdown: {rate['rate_breakdown']}")
```

## End-to-End Example

Create a pipeline, publish it, and run it in production:

```python theme={null}
from datalab_sdk import DatalabClient, PipelineProcessor

client = DatalabClient()

# 1. Create and save
pipeline = client.create_pipeline(steps=[
    PipelineProcessor(type="convert", settings={"mode": "balanced"}),
    PipelineProcessor(type="extract", settings={
        "page_schema": {
            "type": "object",
            "properties": {
                "vendor": {"type": "string", "description": "Vendor name"},
                "amount": {"type": "number", "description": "Total amount"},
                "date": {"type": "string", "description": "Invoice date"}
            }
        }
    })
])
pipeline = client.save_pipeline(pipeline.pipeline_id, name="Invoice Parser")

# 2. Test the draft
test_exec = client.run_pipeline(
    pipeline.pipeline_id,
    file_path="test_invoice.pdf",
    version=0
)
test_exec = client.get_pipeline_execution(test_exec.execution_id, max_polls=300)
test_result = client.get_step_result(test_exec.execution_id, step_index=1)
print(f"Test result: {test_result}")

# 3. Publish
version = client.create_pipeline_version(
    pipeline.pipeline_id,
    description="Initial release — balanced mode, basic fields"
)

# 4. Run in production (pinned to version)
execution = client.run_pipeline(
    pipeline.pipeline_id,
    file_path="real_invoice.pdf",
    version=version.version
)
execution = client.get_pipeline_execution(execution.execution_id, max_polls=300)

if execution.status == "completed":
    result = client.get_step_result(execution.execution_id, step_index=1)
    print(f"Extracted: {result}")
else:
    for step in execution.steps:
        if step.error_message:
            print(f"Step {step.step_index} failed: {step.error_message}")
```

## Next Steps

<CardGroup cols={2}>
  <Card title="Pipeline Overview" icon="sitemap" href="/docs/recipes/pipelines/pipeline-overview">
    Processor types, composition rules, and when to use pipelines.
  </Card>

  <Card title="Pipeline Versioning" icon="code-branch" href="/docs/recipes/pipelines/pipeline-versioning">
    Manage drafts, versions, and production pinning.
  </Card>

  <Card title="Webhooks" icon="bell" href="/platform/webhooks">
    Configure webhook notifications for pipeline executions.
  </Card>

  <Card title="SDK Reference" icon="code" href="/docs/welcome/sdk/pipelines">
    Full SDK reference for all pipeline methods.
  </Card>
</CardGroup>