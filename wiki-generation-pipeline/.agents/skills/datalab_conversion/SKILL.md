---
name: Datalab Document Conversion
description: Convert PDFs, images, and documents to Markdown, HTML, JSON, or chunks using Datalab.
---

# Datalab Document Conversion

## 1. Core Conversion Logic
This skill requires the `datalab_core` SDK initialization.

```python
from datalab_sdk import DatalabClient, ConvertOptions

client = DatalabClient()

options = ConvertOptions(
    output_format="markdown",     # "markdown", "html", "json", "chunks"
    mode="balanced",              # "fast" (default), "balanced", "accurate"
    paginate=True,                # Add page delimiters
    page_range="0-10",            # Specific pages (0-indexed)
    extras="chart_understanding", # Optional: extract data from charts
)

# Convert from local file
result = client.convert("document.pdf", options=options)
# Convert from URL
# result = client.convert(file_url="https://example.com/doc.pdf", options=options)

print(result.markdown)        # Markdown output (if output_format="markdown")
print(result.html)            # HTML output
print(result.json)            # JSON structure
print(result.chunks)          # Chunked output

print(result.metadata)        # Document metadata
```

## 2. Image Extraction
If the pipeline outputs markdown with image tags, the images are bundled inside the result. You must save them.

```python
# Save output markdown and automatically save images to an `output_images/` dir
result.save_output("output/", save_images=True)
```

## 3. Full Documentation Reference
For exhaustive API parameters, pricing breakdown, and edge cases regarding Document Conversion, read the raw markdown files located in the `references/` subdirectory of this skill.
