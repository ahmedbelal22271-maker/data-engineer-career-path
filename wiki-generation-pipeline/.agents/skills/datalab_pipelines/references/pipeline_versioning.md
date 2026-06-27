# Pipeline Versioning

> Manage pipeline drafts, publish immutable versions, and pin production deployments.

**Before you begin**, make sure you have:

1. A [Datalab account](https://www.datalab.to/auth/sign_up) with an [API key](https://www.datalab.to/app/keys) (new accounts include \$5 in free credits)
2. Python 3.10+ installed
3. The Datalab SDK: `pip install datalab-python-sdk`
4. Your `DATALAB_API_KEY` environment variable set

## Version Lifecycle

Every pipeline goes through a predictable lifecycle:

| State     | `active_version` | Description                                 |
| --------- | ---------------- | ------------------------------------------- |
| Draft     | `0`              | Edits auto-save. No published version yet.  |
| Saved     | `0`              | Named pipeline, still no published version. |
| Published | `1`, `2`, ...    | Immutable version snapshots exist.          |

When you edit a published pipeline, your changes go into a draft. The published version is untouched until you explicitly publish again.

## Publish a Version

Create an immutable snapshot of the current pipeline steps:

<CodeGroup>
  ```python Python SDK theme={null}
  from datalab_sdk import DatalabClient

  client = DatalabClient()

  # Publish version 1
  version = client.create_pipeline_version(
      "pl_abc123",
      description="Initial production release"
  )
  print(f"Published v{version.version}")  # v1
  ```

  ```bash cURL theme={null}
  curl -X POST https://www.datalab.to/api/v1/pipelines/PIPELINE_ID/versions \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"description": "Initial production release"}'
  ```

  ```python Python (requests) theme={null}
  import os, requests

  BASE = "https://www.datalab.to/api/v1"
  headers = {"X-API-Key": os.getenv("DATALAB_API_KEY")}

  resp = requests.post(f"{BASE}/pipelines/pl_abc123/versions",
      headers={**headers, "Content-Type": "application/json"},
      json={"description": "Initial production release"})
  print(resp.json())
  ```
</CodeGroup>

Each call increments the version number. Published versions are immutable — their steps cannot be changed.

## Edit and Iterate

After publishing, any edits create a draft that is separate from the published version:

```python theme={null}
from datalab_sdk import PipelineProcessor

# Edit steps — this creates a draft
client.update_pipeline("pl_abc123", steps=[
    PipelineProcessor(type="convert", settings={"mode": "accurate"}),  # Changed
    PipelineProcessor(type="extract", settings={
        "page_schema": {"type": "object", "properties": {
            "title": {"type": "string"},
            "author": {"type": "string"}  # Added field
        }}
    })
])

# Test the draft
execution = client.run_pipeline("pl_abc123", file_path="test.pdf", version=0)

# Happy with changes? Publish a new version
version = client.create_pipeline_version("pl_abc123", description="Added author field")
print(f"Published v{version.version}")  # v2
```

<Warning>
  `version=0` explicitly runs the draft. Omitting `version` runs the active published version. See [Run a Pipeline](/docs/recipes/pipelines/run-pipeline) for version parameter details.
</Warning>

## Discard a Draft

Revert unsaved changes and restore the published version's steps:

<CodeGroup>
  ```python Python SDK theme={null}
  # Discard draft, revert to active version
  pipeline = client.discard_pipeline_draft("pl_abc123")

  # Or revert to a specific version
  pipeline = client.discard_pipeline_draft("pl_abc123", version=1)
  ```

  ```bash cURL theme={null}
  # Discard draft, revert to active version
  curl -X POST https://www.datalab.to/api/v1/pipelines/PIPELINE_ID/discard \
    -H "X-API-Key: $DATALAB_API_KEY"

  # Revert to specific version
  curl -X POST https://www.datalab.to/api/v1/pipelines/PIPELINE_ID/discard \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"version": 1}'
  ```

  ```python Python (requests) theme={null}
  import os, requests

  BASE = "https://www.datalab.to/api/v1"
  headers = {"X-API-Key": os.getenv("DATALAB_API_KEY")}

  resp = requests.post(f"{BASE}/pipelines/pl_abc123/discard", headers=headers)
  print(resp.json())
  ```
</CodeGroup>

## Browse Version History

List all published versions for a pipeline:

```python theme={null}
result = client.list_pipeline_versions("pl_abc123")

for v in result["versions"]:
    print(f"v{v.version}: {v.description} (created {v.created})")
    print(f"  Steps: {[s['type'] for s in v.steps]}")
```

Versions are returned newest-first.

## Best Practices

**Pin production integrations to a specific version.** When calling `run_pipeline()` from production code, pass an explicit `version` number. This protects you from accidental changes:

```python theme={null}
# Production code — pinned to v2
execution = client.run_pipeline(
    "pl_abc123",
    file_path="document.pdf",
    version=2  # Always runs v2, even if v3 is published later
)
```

**Test drafts before publishing.** Use `version=0` to run the draft version against test documents:

```python theme={null}
# Test draft changes
execution = client.run_pipeline(
    "pl_abc123",
    file_path="test_document.pdf",
    version=0  # Runs draft
)
```

**Use descriptions.** Include a meaningful description when publishing so your team can understand what changed:

```python theme={null}
client.create_pipeline_version(
    "pl_abc123",
    description="Switch to accurate mode, add line_items extraction"
)
```

**Archive unused pipelines.** Keep your pipeline list clean:

```python theme={null}
client.archive_pipeline("pl_old123")

# List includes archived if you need them
result = client.list_pipelines(include_archived=True)
```

## Next Steps

<CardGroup cols={2}>
  <Card title="Run a Pipeline" icon="play" href="/docs/recipes/pipelines/run-pipeline">
    Execute pipelines with version selection, overrides, and polling.
  </Card>

  <Card title="Create a Pipeline" icon="hammer" href="/docs/recipes/pipelines/create-pipeline">
    Build pipelines with Forge or the SDK.
  </Card>

  <Card title="Pipeline Overview" icon="sitemap" href="/docs/recipes/pipelines/pipeline-overview">
    Processor types, composition rules, and when to use pipelines.
  </Card>

  <Card title="SDK Reference" icon="code" href="/docs/welcome/sdk/pipelines">
    Full SDK reference for all pipeline methods.
  </Card>
</CardGroup>