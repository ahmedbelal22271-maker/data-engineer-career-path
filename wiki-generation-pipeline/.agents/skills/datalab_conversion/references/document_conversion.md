# Document Conversion

> Convert PDFs, images, and documents to Markdown, HTML, JSON, or chunks using the Datalab SDK.

## Basic Usage

```python theme={null}
from datalab_sdk import DatalabClient

client = DatalabClient()

# Convert to markdown (default)
result = client.convert("document.pdf")
print(result.markdown)

# Convert from URL
result = client.convert(file_url="https://example.com/document.pdf")
print(result.markdown)
```

## Conversion Options

Use `ConvertOptions` to control the conversion:

```python theme={null}
from datalab_sdk import DatalabClient, ConvertOptions

client = DatalabClient()

options = ConvertOptions(
    output_format="markdown",     # Output format
    mode="balanced",              # Processing mode
    paginate=True,                # Add page delimiters
    max_pages=10,                 # Limit pages processed
    page_range="0-5,10",          # Specific pages (0-indexed)
)

result = client.convert("document.pdf", options=options)
```

### All Options

| Option                        | Type | Default      | Description                                                                                                                                         |
| ----------------------------- | ---- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `output_format`               | str  | `"markdown"` | Output format: `"markdown"`, `"html"`, `"json"`, `"chunks"`                                                                                         |
| `mode`                        | str  | `"fast"`     | Processing mode: `"fast"`, `"balanced"`, `"accurate"`                                                                                               |
| `paginate`                    | bool | `False`      | Add page delimiters to output                                                                                                                       |
| `max_pages`                   | int  | None         | Maximum number of pages to process                                                                                                                  |
| `page_range`                  | str  | None         | Specific pages to process (e.g., `"0-5,10,15-20"`). For spreadsheets, filters by sheet index.                                                       |
| `skip_cache`                  | bool | `False`      | Skip cached results, force reprocessing                                                                                                             |
| `disable_image_extraction`    | bool | `False`      | Don't extract images from document                                                                                                                  |
| `disable_image_captions`      | bool | `False`      | Don't generate captions for images                                                                                                                  |
| `token_efficient_markdown`    | bool | `False`      | Optimize markdown output for LLM token usage                                                                                                        |
| `fence_synthetic_captions`    | bool | `False`      | Fence synthetic image captions                                                                                                                      |
| `include_markdown_in_chunks`  | bool | `False`      | Include markdown in chunks/JSON output                                                                                                              |
| `save_checkpoint`             | bool | `False`      | Save intermediate checkpoint for reuse                                                                                                              |
| `extras`                      | str  | None         | Comma-separated features: `"track_changes"`, `"chart_understanding"`, `"extract_links"`, `"table_row_bboxes"`, `"infographic"`, `"new_block_types"` |
| `add_block_ids`               | bool | `False`      | Add block IDs to HTML output for citations                                                                                                          |
| `keep_spreadsheet_formatting` | bool | `False`      | Preserve spreadsheet styling in HTML output                                                                                                         |
| `webhook_url`                 | str  | None         | Override account webhook URL for this request                                                                                                       |
| `additional_config`           | dict | None         | Additional configuration options                                                                                                                    |

<Tip>
  Use `save_checkpoint=True` to save the parsed document state. Then call `client.extract()` or `client.segment()` with the returned `checkpoint_id` to run extraction or segmentation without re-parsing.
</Tip>

### Processing Modes

| Mode       | Description                   | Use Case                                 |
| ---------- | ----------------------------- | ---------------------------------------- |
| `fast`     | Lowest latency (default)      | Simple documents, real-time applications |
| `balanced` | Balance of speed and accuracy | General use                              |
| `accurate` | Highest accuracy              | Complex layouts, tables, figures         |

### Output Formats

| Format     | Description                                |
| ---------- | ------------------------------------------ |
| `markdown` | Clean markdown with headers, lists, tables |
| `html`     | Structured HTML preserving layout          |
| `json`     | Block-level structure with bounding boxes  |
| `chunks`   | Pre-chunked output for RAG applications    |

## Conversion Result

The `ConversionResult` object contains the converted content and metadata:

```python theme={null}
result = client.convert("document.pdf")

# Access content based on output format
print(result.markdown)        # Markdown output
print(result.html)            # HTML output
print(result.json)            # JSON structure
print(result.chunks)          # Chunked output

# Metadata
print(result.success)         # True if conversion succeeded
print(result.page_count)      # Number of pages processed
print(result.images)          # Dict of extracted images (filename -> base64)
print(result.metadata)        # Document metadata
print(result.parse_quality_score)  # Quality score (0-5)
print(result.cost_breakdown)  # Cost in cents
```

### Result Fields

| Field                 | Type  | Description                                          |
| --------------------- | ----- | ---------------------------------------------------- |
| `success`             | bool  | Whether conversion succeeded                         |
| `markdown`            | str   | Markdown output (if format is markdown)              |
| `html`                | str   | HTML output (if format is html)                      |
| `json`                | dict  | JSON output (if format is json)                      |
| `chunks`              | dict  | Chunked output (if format is chunks)                 |
| `images`              | dict  | Extracted images as `{filename: base64_data}`        |
| `metadata`            | dict  | Document metadata                                    |
| `page_count`          | int   | Number of pages processed                            |
| `parse_quality_score` | float | Quality score from 0-5                               |
| `cost_breakdown`      | dict  | Cost details (`list_cost_cents`, `final_cost_cents`) |
| `checkpoint_id`       | str   | Checkpoint ID if `save_checkpoint` was True          |
| `error`               | str   | Error message if conversion failed                   |

## Saving Output

Save the conversion result to files:

```python theme={null}
# Save during conversion
result = client.convert("document.pdf", save_output="output/document")

# Or save afterward
result.save_output("output/document", save_images=True)
```

This creates:

* `document.md` (or `.html`, `.json` based on format)
* `document_images/` directory with extracted images (if `save_images=True`)

## Async Usage

For high-throughput applications:

```python theme={null}
import asyncio
from datalab_sdk import AsyncDatalabClient, ConvertOptions

async def convert_documents():
    async with AsyncDatalabClient() as client:
        options = ConvertOptions(mode="fast", max_pages=5)
        result = await client.convert("document.pdf", options=options)
        return result.markdown

markdown = asyncio.run(convert_documents())
```

## Polling Configuration

Control polling behavior for long-running conversions:

```python theme={null}
result = client.convert(
    "large_document.pdf",
    max_polls=600,        # Maximum polling attempts (default: 300)
    poll_interval=2,      # Seconds between polls (default: 1)
)
```

## Special Features

### Track Changes (Word Documents)

Extract tracked changes and comments from DOCX files:

```python theme={null}
options = ConvertOptions(
    output_format="html",
    extras="track_changes",
)
result = client.convert("contract.docx", options=options)
# HTML contains <ins>, <del>, and <comment> tags
```

### Chart Understanding

Extract data from charts and graphs:

```python theme={null}
options = ConvertOptions(
    extras="chart_understanding",
)
result = client.convert("report.pdf", options=options)
```

### Block IDs for Citations

Add block IDs for tracking content back to source locations:

```python theme={null}
options = ConvertOptions(
    output_format="html",
    add_block_ids=True,
)
result = client.convert("document.pdf", options=options)
# HTML elements include data-block-id attributes
```

### Structured Extraction

For structured data extraction, use the dedicated [`client.extract()`](/docs/welcome/sdk/extraction) method.

## Next Steps

<CardGroup cols={2}>
  <Card title="Structured Extraction Recipe" icon="table" href="/docs/recipes/structured-extraction/api-overview">
    Extract structured data from documents using JSON schemas.
  </Card>

  <Card title="Batch Processing" icon="layer-group" href="/docs/recipes/conversion/batch-documents">
    Process multiple documents efficiently in parallel.
  </Card>

  <Card title="Form Filling SDK" icon="pen-to-square" href="/docs/welcome/sdk/form-filling">
    Programmatically fill PDF and image forms with field data.
  </Card>

  <Card title="CLI Reference" icon="terminal" href="/docs/welcome/sdk/cli">
    Convert documents from the command line.
  </Card>
</CardGroup>