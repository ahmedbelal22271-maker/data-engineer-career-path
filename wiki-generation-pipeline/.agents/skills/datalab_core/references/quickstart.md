# Quickstart

> Get started with Datalab to convert PDFs, images, and documents into Markdown, HTML, or JSON in minutes.

## Get Your API Key

Sign up at [datalab.to/auth/sign\_up](https://www.datalab.to/auth/sign_up) — new accounts include **\$5 in free credits**, enough to process hundreds of pages.

Then grab your API key from the [API Keys dashboard](https://www.datalab.to/app/keys).

<Tip>
  **Want to try before writing code?** Upload a document to the [Forge Playground](https://www.datalab.to/app/playground) to see results instantly — no API key required.
</Tip>

## Installation

Install the Datalab SDK:

```bash theme={null}
pip install datalab-python-sdk
```

Set your API key as an environment variable:

```bash theme={null}
export DATALAB_API_KEY=your_api_key_here
```

## Convert a Document

The SDK provides a simple interface to convert documents to Markdown, HTML, JSON, or chunks.

<CodeGroup>
  ```python SDK theme={null}
  from datalab_sdk import DatalabClient

  client = DatalabClient()  # Uses DATALAB_API_KEY env var

  # Convert PDF to markdown
  result = client.convert("document.pdf")
  print(result.markdown)

  # Save output and images
  result.save_output("output/")
  ```

  ```python Python (requests) theme={null}
  import requests
  import time

  url = "https://www.datalab.to/api/v1/convert"
  headers = {"X-API-Key": "YOUR_API_KEY"}

  with open("document.pdf", "rb") as f:
      response = requests.post(
          url,
          files={"file": ("document.pdf", f, "application/pdf")},
          data={"output_format": "markdown"},
          headers=headers
      )

  data = response.json()
  check_url = data["request_check_url"]

  # Poll for completion
  while True:
      response = requests.get(check_url, headers=headers)
      result = response.json()
      if result["status"] == "complete":
          print(result["markdown"])
          break
      time.sleep(2)
  ```

  ```bash cURL theme={null}
  # Submit document
  curl -X POST https://www.datalab.to/api/v1/convert \
    -H "X-API-Key: YOUR_API_KEY" \
    -F "file=@document.pdf" \
    -F "output_format=markdown"

  # Poll for results (use request_check_url from response)
  curl -X GET "https://www.datalab.to/api/v1/convert/{request_id}" \
    -H "X-API-Key: YOUR_API_KEY"
  ```
</CodeGroup>

<Warning>
  **Common mistakes:**

  * Forgetting to set the `DATALAB_API_KEY` environment variable
  * Using `file_url` with a private/authenticated URL (must be publicly accessible)
  * Not polling for results — the initial response only contains a `request_id`, not the actual output
</Warning>

## Conversion Options

Control the conversion with options:

```python theme={null}
from datalab_sdk import DatalabClient, ConvertOptions

client = DatalabClient()

options = ConvertOptions(
    output_format="markdown",  # "markdown", "html", "json", "chunks"
    mode="balanced",           # "fast", "balanced", "accurate"
    paginate=True,             # Add page delimiters
    page_range="0-10",         # Process specific pages (0-indexed)
)

result = client.convert("document.pdf", options=options)
```

### Processing Modes

| Mode       | Description                                             |
| ---------- | ------------------------------------------------------- |
| `fast`     | Lowest latency, good for simple documents (SDK default) |
| `balanced` | Balance of speed and accuracy                           |
| `accurate` | Highest accuracy, best for complex layouts              |

## Fill PDF Forms

Fill forms in PDFs or images with structured data:

<CodeGroup>
  ```python SDK theme={null}
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

  ```python Python (requests) theme={null}
  import requests
  import json

  url = "https://www.datalab.to/api/v1/fill"
  headers = {"X-API-Key": "YOUR_API_KEY"}

  field_data = {
      "full_name": {"value": "John Doe", "description": "Full legal name"},
      "date": {"value": "2024-01-15", "description": "Today's date"},
  }

  with open("form.pdf", "rb") as f:
      response = requests.post(
          url,
          files={"file": ("form.pdf", f, "application/pdf")},
          data={"field_data": json.dumps(field_data)},
          headers=headers
      )
  # Poll for completion using request_check_url
  ```
</CodeGroup>

## Upload and Manage Files

Upload files to Datalab for use in pipelines:

```python theme={null}
from datalab_sdk import DatalabClient

client = DatalabClient()

# Upload files
uploaded = client.upload_files(["doc1.pdf", "doc2.pdf"])
for file in uploaded:
    print(f"{file.original_filename}: {file.reference}")
    # Output: doc1.pdf: datalab://file-abc123

# List your files
files = client.list_files(limit=50)
print(f"Total files: {files['total']}")
```

## CLI

The SDK includes a command-line interface:

```bash theme={null}
# Convert a single document
datalab convert document.pdf --format markdown

# Convert with options
datalab convert document.pdf --mode accurate --paginate

# Convert a directory
datalab convert ./documents/ --output_dir ./output/
```

## Run a Pipeline

Pipelines chain processors (convert, extract, segment) into a single reusable call. Create them in [Forge](https://www.datalab.to/app/playground) or via the SDK:

```python theme={null}
from datalab_sdk import DatalabClient

client = DatalabClient()

# Run an existing pipeline
execution = client.run_pipeline(
    "pl_abc123",              # Your pipeline ID
    file_path="document.pdf"
)

# Poll until complete
execution = client.get_pipeline_execution(
    execution.execution_id,
    max_polls=300
)

# Get extraction results (step index 1 = extract step)
result = client.get_step_result(execution.execution_id, step_index=1)
print(result)
```

See [Pipelines](/docs/recipes/pipelines/pipeline-overview) for creating, versioning, and running pipelines.

## Async Support

For high-throughput applications, use the async client:

```python theme={null}
import asyncio
from datalab_sdk import AsyncDatalabClient

async def convert_documents():
    async with AsyncDatalabClient() as client:
        result = await client.convert("document.pdf")
        print(result.markdown)

asyncio.run(convert_documents())
```

## Next Steps

<CardGroup cols={2}>
  <Card title="SDK Reference" icon="code" href="/docs/welcome/sdk">
    Full Python SDK documentation with typed clients and async support.
  </Card>

  <Card title="API Reference" icon="book" href="/docs/welcome/api">
    REST API reference for document conversion, form filling, and file management.
  </Card>

  <Card title="Pipelines" icon="workflow" href="/docs/recipes/pipelines/pipeline-overview">
    Chain processors into versioned, reusable pipelines.
  </Card>

  <Card title="Document Conversion" icon="file-lines" href="/docs/recipes/conversion/conversion-api-overview">
    Detailed guide to converting PDFs and documents to Markdown, HTML, or JSON.
  </Card>
</CardGroup>