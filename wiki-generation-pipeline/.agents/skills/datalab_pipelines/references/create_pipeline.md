# Create a Pipeline

> Build pipelines using Forge or the SDK to chain document processors.

**Before you begin**, make sure you have:

1. A [Datalab account](https://www.datalab.to/auth/sign_up) with an [API key](https://www.datalab.to/app/keys) (new accounts include \$5 in free credits)
2. Python 3.10+ installed
3. The Datalab SDK: `pip install datalab-python-sdk`
4. Your `DATALAB_API_KEY` environment variable set

## Using Forge

[Forge](https://www.datalab.to/app/playground) provides a visual pipeline builder where you can:

1. **Start from a template** or create a blank pipeline
2. **Add processors** — click to add convert, extract, segment, custom, or fill processors
3. **Configure each processor** — set processing mode, schemas, field data, and options in the configuration panel
4. **Test with a document** — run the pipeline and watch each processor complete in real-time
5. **Save and version** — name your pipeline and publish versions for production use

Edits in Forge auto-save as a draft. Your published versions remain unchanged until you explicitly publish a new version.

## Using the SDK

### Create a Pipeline

Define processors using `PipelineProcessor` and create the pipeline:

```python theme={null}
from datalab_sdk import DatalabClient, PipelineProcessor

client = DatalabClient()

steps = [
    PipelineProcessor(type="convert", settings={
        "mode": "balanced",
        "output_format": "markdown"
    }),
    PipelineProcessor(type="extract", settings={
        "page_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Document title"},
                "date": {"type": "string", "description": "Document date"},
                "summary": {"type": "string", "description": "Brief summary"}
            }
        }
    })
]

pipeline = client.create_pipeline(steps=steps)
print(f"Created: {pipeline.pipeline_id}")  # pl_XXXXX
```

The pipeline starts as an unsaved draft.

### Save the Pipeline

Name and save the pipeline so it appears in your pipeline list:

```python theme={null}
pipeline = client.save_pipeline(
    pipeline.pipeline_id,
    name="Document Summarizer"
)
print(f"Saved: {pipeline.name}")
```

### Update Steps

Update a pipeline's steps. This creates a draft if the pipeline has a published version:

```python theme={null}
updated_steps = [
    PipelineProcessor(type="convert", settings={
        "mode": "accurate",  # Changed from balanced
        "output_format": "markdown"
    }),
    PipelineProcessor(type="extract", settings={
        "page_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "date": {"type": "string"},
                "summary": {"type": "string"},
                "author": {"type": "string"}  # Added field
            }
        }
    })
]

pipeline = client.update_pipeline(pipeline.pipeline_id, steps=updated_steps)
```

## Using the REST API

<CodeGroup>
  ```bash Create theme={null}
  curl -X POST https://www.datalab.to/api/v1/pipelines \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "steps": [
        {"type": "convert", "settings": {"mode": "balanced"}},
        {"type": "extract", "settings": {
          "page_schema": "{\"type\":\"object\",\"properties\":{\"title\":{\"type\":\"string\"}}}"
        }}
      ]
    }'
  ```

  ```bash Save theme={null}
  curl -X PUT https://www.datalab.to/api/v1/pipelines/PIPELINE_ID/save \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"name": "Document Summarizer"}'
  ```

  ```bash Update steps theme={null}
  curl -X PUT https://www.datalab.to/api/v1/pipelines/PIPELINE_ID \
    -H "X-API-Key: $DATALAB_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "steps": [
        {"type": "convert", "settings": {"mode": "accurate"}},
        {"type": "extract", "settings": {
          "page_schema": "{\"type\":\"object\",\"properties\":{\"title\":{\"type\":\"string\"}}}"
        }}
      ]
    }'
  ```
</CodeGroup>

## Processor Configuration Reference

### Convert Processor

Controls how the document is parsed.

```python theme={null}
PipelineProcessor(type="convert", settings={
    "mode": "balanced",           # fast, balanced, accurate
    "output_format": "markdown",  # markdown, html, json, chunks
    "paginate": True,             # Add page delimiters
    "include_images": True,       # Extract images
    "include_image_captions": True,
    "add_block_ids": False,       # Block IDs for citations
})
```

| Setting                    | Type | Default      | Description                         |
| -------------------------- | ---- | ------------ | ----------------------------------- |
| `mode`                     | str  | `"fast"`     | Processing mode                     |
| `output_format`            | str  | `"markdown"` | Output format                       |
| `paginate`                 | bool | `false`      | Add page delimiters                 |
| `include_images`           | bool | `true`       | Extract images from document        |
| `include_image_captions`   | bool | `true`       | Generate image captions             |
| `include_headers_footers`  | bool | `false`      | Include page headers/footers        |
| `add_block_ids`            | bool | `false`      | Add block IDs for citation tracking |
| `fence_synthetic_captions` | bool | `false`      | Fence synthetic image captions      |

### Extract Processor

Extracts structured data using a JSON schema. Requires a preceding `convert` processor (or `segment` / `custom`).

```python theme={null}
PipelineProcessor(type="extract", settings={
    "page_schema": {
        "type": "object",
        "properties": {
            "invoice_number": {"type": "string", "description": "Invoice ID"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "number"}
                    }
                }
            }
        }
    }
})
```

| Setting       | Type | Description                            |
| ------------- | ---- | -------------------------------------- |
| `page_schema` | dict | JSON schema defining fields to extract |

<Tip>
  Use detailed `description` fields in your schema to improve extraction accuracy. Tell the model what to look for.
</Tip>

### Segment Processor

Splits a document into logical sections. Requires a preceding `convert` processor.

```python theme={null}
PipelineProcessor(type="segment", settings={
    "segmentation_schema": {
        "Cover Letter": "The cover letter or introductory section",
        "Resume": "The applicant's resume or CV",
        "References": "Reference letters or contact information"
    }
})
```

| Setting               | Type | Description                          |
| --------------------- | ---- | ------------------------------------ |
| `segmentation_schema` | dict | Map of section names to descriptions |

### Custom Processor

Applies use-case-specific customizations to convert output. Requires a preceding `convert` processor. See [Custom Processors](/docs/recipes/pipelines/custom-processors) for details.

```python theme={null}
PipelineProcessor(
    type="custom",
    settings={},
    custom_processor_id="cp_abc123"  # Your custom processor ID
)
```

| Field                 | Type | Description                             |
| --------------------- | ---- | --------------------------------------- |
| `custom_processor_id` | str  | ID of the custom processor (`cp_XXXXX`) |
| `eval_rubric_id`      | int  | Optional evaluation rubric to apply     |

### Fill Processor

Fills form fields in a PDF or image. `fill` is always the only step in a pipeline — it cannot be chained with `convert`, `extract`, or `segment`. Use it to apply versioning and execution tracking to your form-filling workflows.

```python theme={null}
PipelineProcessor(type="fill", settings={
    "field_data": {
        "full_name": {"value": "John Doe", "description": "Full legal name"},
        "date": {"value": "2024-01-15", "description": "Today's date"},
    },
    "context": "Employee onboarding form",  # Optional
    "confidence_threshold": 0.5,             # Optional, default 0.5
})
```

| Setting                | Type  | Required | Description                                                    |
| ---------------------- | ----- | -------- | -------------------------------------------------------------- |
| `field_data`           | dict  | Yes      | Map of field keys to `{value, description}` objects            |
| `context`              | str   | No       | Additional context to improve field matching                   |
| `confidence_threshold` | float | No       | Minimum confidence for field matching (0.0–1.0, default `0.5`) |

## List and Manage Pipelines

```python theme={null}
# List saved pipelines
result = client.list_pipelines(saved_only=True, limit=50)
for p in result["pipelines"]:
    print(f"{p.pipeline_id}: {p.name} (v{p.active_version})")

# Get a specific pipeline
pipeline = client.get_pipeline("pl_abc123")

# Archive (soft-delete)
client.archive_pipeline("pl_abc123")

# Restore
client.unarchive_pipeline("pl_abc123")
```

## Next Steps

<CardGroup cols={2}>
  <Card title="Pipeline Versioning" icon="code-branch" href="/docs/recipes/pipelines/pipeline-versioning">
    Manage drafts, publish versions, and pin production deployments.
  </Card>

  <Card title="Run a Pipeline" icon="play" href="/docs/recipes/pipelines/run-pipeline">
    Execute pipelines with overrides and track results.
  </Card>

  <Card title="Structured Extraction" icon="table" href="/docs/recipes/structured-extraction/api-overview">
    Deep dive on extraction schemas and confidence scoring.
  </Card>

  <Card title="SDK Reference" icon="code" href="/docs/welcome/sdk/pipelines">
    Full SDK reference for all pipeline methods.
  </Card>
</CardGroup>