# Python SDK

> The Datalab Python SDK provides a simple interface for document conversion, pipelines, structured extraction, form filling, and file management.

## Installation

```bash theme={null}
pip install datalab-python-sdk
```

Requires Python 3.10 or higher.

## Authentication

Set your API key as an environment variable (recommended):

```bash theme={null}
export DATALAB_API_KEY=your_api_key_here
```

Or pass it directly to the client:

```python theme={null}
from datalab_sdk import DatalabClient

client = DatalabClient(api_key="your_api_key_here")
```

Get your API key from the [API Keys dashboard](https://www.datalab.to/app/keys).

## Quick Example

```python theme={null}
from datalab_sdk import DatalabClient

client = DatalabClient()

# Convert a document to markdown
result = client.convert("document.pdf")
print(result.markdown)

# Save output with images
result.save_output("output/")
```

## Client Options

Both sync and async clients accept the same configuration options:

```python theme={null}
from datalab_sdk import DatalabClient, AsyncDatalabClient

# Synchronous client (blocking)
client = DatalabClient(
    api_key="your_key",           # Or use DATALAB_API_KEY env var
    base_url="https://www.datalab.to",  # API endpoint
    timeout=300,                  # Request timeout in seconds
)

# Asynchronous client (non-blocking)
async_client = AsyncDatalabClient(
    api_key="your_key",
    base_url="https://www.datalab.to",
    timeout=300,
)
```

| Parameter  | Type | Default                   | Description                |
| ---------- | ---- | ------------------------- | -------------------------- |
| `api_key`  | str  | `DATALAB_API_KEY` env var | Your Datalab API key       |
| `base_url` | str  | `https://www.datalab.to`  | API base URL               |
| `timeout`  | int  | `300`                     | Request timeout in seconds |

## Async Support

For high-throughput applications, use `AsyncDatalabClient`:

```python theme={null}
import asyncio
from datalab_sdk import AsyncDatalabClient

async def process_documents():
    async with AsyncDatalabClient() as client:
        result = await client.convert("document.pdf")
        print(result.markdown)

asyncio.run(process_documents())
```

The async client is recommended when processing multiple documents concurrently.

## Error Handling

The SDK raises specific exceptions for different error types:

```python theme={null}
from datalab_sdk import DatalabClient
from datalab_sdk.exceptions import (
    DatalabAPIError,
    DatalabTimeoutError,
    DatalabFileError,
    DatalabValidationError,
)

client = DatalabClient()

try:
    result = client.convert("document.pdf")
except DatalabAPIError as e:
    print(f"API error {e.status_code}: {e.response_data}")
except DatalabTimeoutError:
    print("Request timed out")
except DatalabFileError as e:
    print(f"File error: {e}")
except DatalabValidationError as e:
    print(f"Invalid input: {e}")
```

| Exception                | Description                                                                 |
| ------------------------ | --------------------------------------------------------------------------- |
| `DatalabAPIError`        | API returned an error response (includes `status_code` and `response_data`) |
| `DatalabTimeoutError`    | Request exceeded timeout                                                    |
| `DatalabFileError`       | File not found or cannot be read                                            |
| `DatalabValidationError` | Invalid parameters provided                                                 |

## Automatic Retries

The SDK automatically retries requests for:

* `408` Request Timeout
* `429` Rate Limit Exceeded
* `5xx` Server Errors

Retries use exponential backoff. You can control polling behavior with `max_polls` and `poll_interval` parameters on individual methods.

## SDK Features

<CardGroup cols={2}>
  <Card title="Document Conversion" icon="file-lines" href="/docs/welcome/sdk/conversion">
    Convert PDFs, images, and documents to Markdown, HTML, JSON, or chunks.
  </Card>

  <Card title="Structured Extraction" icon="table" href="/docs/welcome/sdk/extraction">
    Extract structured data from documents using JSON schemas.
  </Card>

  <Card title="Document Segmentation" icon="scissors" href="/docs/welcome/sdk/segmentation">
    Segment documents into logical sections.
  </Card>

  <Card title="Form Filling" icon="pen-to-square" href="/docs/welcome/sdk/form-filling">
    Fill PDF and image forms with structured field data.
  </Card>

  <Card title="Pipelines" icon="workflow" href="/docs/welcome/sdk/pipelines">
    Chain processors into versioned, reusable pipelines.
  </Card>

  <Card title="File Management" icon="folder-open" href="/docs/welcome/sdk/file-management">
    Upload, list, and manage files in Datalab storage.
  </Card>

  <Card title="CLI" icon="terminal" href="/docs/welcome/sdk/cli">
    Command-line interface for document conversion.
  </Card>
</CardGroup>

## Method Summary

| Method                             | Description                                                 |
| ---------------------------------- | ----------------------------------------------------------- |
| `convert()`                        | Convert documents to markdown, HTML, JSON, or chunks        |
| `extract()`                        | Extract structured data from documents using JSON schemas   |
| `segment()`                        | Segment documents into sections using a schema              |
| `track_changes()`                  | Extract tracked changes from DOCX documents                 |
| `create_document()`                | Create DOCX from markdown with track changes                |
| `run_custom_processor()`           | Execute a custom processor on a document                    |
| `fill()`                           | Fill PDF or image forms with field data                     |
| `upload_files()`                   | Upload files to Datalab storage                             |
| `list_files()`                     | List uploaded files                                         |
| `get_file_metadata()`              | Get metadata for a specific file                            |
| `get_file_download_url()`          | Generate presigned download URL                             |
| `delete_file()`                    | Delete an uploaded file                                     |
| `create_pipeline()`                | Create a new pipeline                                       |
| `list_pipelines()`                 | List pipelines for your team                                |
| `get_pipeline()`                   | Get a pipeline by ID                                        |
| `update_pipeline()`                | Update pipeline steps (creates a draft)                     |
| `save_pipeline()`                  | Promote a pipeline draft to a named, published version      |
| `archive_pipeline()`               | Archive a pipeline                                          |
| `unarchive_pipeline()`             | Restore an archived pipeline                                |
| `create_pipeline_version()`        | Snapshot the current pipeline steps as an immutable version |
| `list_pipeline_versions()`         | List all versions of a pipeline                             |
| `discard_pipeline_draft()`         | Discard draft changes and revert to a published version     |
| `get_pipeline_rate()`              | Get per-page rate for a pipeline                            |
| `run_pipeline()`                   | Execute a pipeline on a file                                |
| `get_pipeline_execution()`         | Poll pipeline execution status                              |
| `list_pipeline_executions()`       | List recent executions for a pipeline                       |
| `get_step_result()`                | Fetch the result of a specific pipeline step                |
| `list_custom_processors()`         | List custom processors for your team                        |
| `get_custom_processor_status()`    | Check custom processor generation status                    |
| `list_custom_processor_versions()` | List versions of a custom processor                         |
| `set_active_processor_version()`   | Set the active version of a custom processor                |
| `archive_custom_processor()`       | Archive a custom processor                                  |
| `create_extraction_schema()`       | Create a reusable extraction schema                         |
| `list_extraction_schemas()`        | List saved extraction schemas                               |
| `get_extraction_schema()`          | Get a schema by ID                                          |
| `update_extraction_schema()`       | Update schema fields or create a new version                |
| `delete_extraction_schema()`       | Archive (soft-delete) an extraction schema                  |
| `run_custom_pipeline()`            | *(Deprecated)* Use `run_custom_processor()` instead         |
| `ocr()`                            | *(Deprecated)* Use `convert()` instead                      |

## Next Steps

<CardGroup cols={2}>
  <Card title="Document Conversion" icon="file-lines" href="/docs/welcome/sdk/conversion">
    Convert PDFs, images, and documents to Markdown, HTML, JSON, or chunks.
  </Card>

  <Card title="Structured Extraction" icon="table" href="/docs/welcome/sdk/extraction">
    Extract structured data from documents using JSON schemas.
  </Card>

  <Card title="Document Segmentation" icon="scissors" href="/docs/welcome/sdk/segmentation">
    Segment documents into logical sections.
  </Card>

  <Card title="Form Filling" icon="pen-to-square" href="/docs/welcome/sdk/form-filling">
    Fill PDF and image forms with structured field data.
  </Card>

  <Card title="Pipelines" icon="workflow" href="/docs/welcome/sdk/pipelines">
    Chain processors into versioned, reusable pipelines.
  </Card>

  <Card title="File Management" icon="folder-open" href="/docs/welcome/sdk/file-management">
    Upload, list, and manage files in Datalab storage.
  </Card>
</CardGroup>