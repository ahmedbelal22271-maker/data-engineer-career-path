---
name: Datalab Pipelines
description: Chain processors (convert, extract, segment) into reusable asynchronous pipelines.
---

# Datalab Pipelines

## 1. The Asynchronous Execution Flow
When running pipelines, the initial execution does **not** return the result immediately. You must poll for completion, then extract the specific step's payload.
This skill requires the `datalab_core` SDK initialization.

```python
from datalab_sdk import DatalabClient, PipelineProcessor

client = DatalabClient()

# 1. Define pipeline steps
steps = [
    PipelineProcessor(type="convert", settings={"mode": "balanced"}),
    PipelineProcessor(type="extract", settings={
        "page_schema": {
            "type": "object",
            "properties": {"total_amount": {"type": "number"}}
        }
    })
]

# 2. Create and run
pipeline = client.create_pipeline(steps=steps)
execution = client.run_pipeline(
    pipeline.pipeline_id,
    file_path="invoice.pdf"
)
# exec_obj only contains metadata — most importantly: execution.execution_id

# 3. Poll Until Complete (Blocks until finished)
execution = client.get_pipeline_execution(
    execution.execution_id,
    max_polls=300,
    poll_interval=2
)

# 4. Fetch the Payload for a specific step (e.g., Step 1 = extraction step)
result = client.get_step_result(execution.execution_id, step_index=1)
print(result)
```

## 2. Full Documentation Reference
For exhaustive API parameters, creating/saving pipelines, pipeline versioning, Webhook usage, and retrieving run-level overrides, read the raw markdown files located in the `references/` subdirectory of this skill.
