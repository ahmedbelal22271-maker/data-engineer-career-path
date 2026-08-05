---
name: Datalab Document Conversion
description: "Convert PDFs, images, and documents to Markdown, HTML, JSON, or chunks using Datalab. TRIGGER: When the user provides a PDF file (upload, path, or reference) and expects it to be converted to markdown and placed in the wiki structure. This skill handles the conversion step of the PDF Input Mandate pipeline. Extracts images from PDFs, embeds them in the converted markdown at correct positions with proper relative paths, and saves them to the assets/ subdirectory. Always follow with index integrity checks and placement in the correct module directory."
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
    paginate=False,               # False for wiki pipeline (no page delimiters in final output)
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

## 2. Image Extraction & Embedding

When a PDF contains images, Datalab extracts them and includes `![](...)` image tags in the markdown output referencing flat filenames (e.g., `hash_img.png`). The images are available in `result.images` as `{filename: base64_data}`.

**The problem:** `result.save_output("output/", save_images=True)` dumps images to a separate `output_images/` directory with generic hash filenames. The markdown references point to files that are not co-located with the markdown.

**The solution:** Extract images from the result, save them to an `assets/` subdirectory alongside the markdown file, and rewrite the markdown `![]()` paths to point to the correct relative location.

### Complete Image Processing Script

Run this after `client.convert()` to produce a self-contained markdown file with embedded images:

```python
import os
import re
import base64

def process_conversion_images(result, output_dir):
    """
    Extract images from Datalab conversion result, save to assets/
    subdirectory, and rewrite markdown image references.

    Args:
        result: Datalab ConversionResult object
        output_dir: Directory where the markdown file will be saved
                    (e.g., "updates/providers/ibm/course/modules/module_1/lessons/")

    Returns:
        str: Updated markdown with corrected image paths
    """
    md_content = result.markdown
    images = result.images  # dict: {filename: base64_data}

    if not images:
        return md_content

    # Create assets/ subdirectory alongside the markdown
    assets_dir = os.path.join(output_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Save each image from base64 to disk
    saved_files = {}
    for filename, b64_data in images.items():
        image_path = os.path.join(assets_dir, filename)
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(b64_data))
        saved_files[filename] = True

    # Rewrite markdown image references to point to assets/
    # Matches: ![any alt text](original_filename)
    # Replaces with: ![any alt text](assets/original_filename)
    def rewrite_path(match):
        alt_text = match.group(1)
        original_ref = match.group(2)
        # Only rewrite if this references an extracted image
        basename = os.path.basename(original_ref)
        if basename in saved_files:
            return f"![{alt_text}](assets/{basename})"
        return match.group(0)  # Leave non-extracted images unchanged

    updated_md = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)',
        rewrite_path,
        md_content
    )

    return updated_md


# --- Usage after conversion ---
result = client.convert("document.pdf", options=options)

# Define where the markdown file will live
output_dir = "updates/providers/ibm/course/modules/module_1/lessons/"

# Process images and get updated markdown
updated_markdown = process_conversion_images(result, output_dir)

# Write the updated markdown
os.makedirs(output_dir, exist_ok=True)
md_path = os.path.join(output_dir, "c4_m1_my_topic.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write(updated_markdown)
```

### What This Does

1. **Saves images to `assets/`** — co-located with the markdown file, not in a separate `output_images/` directory
2. **Rewrites `![]()` paths** — changes `![alt](hash_img.png)` to `![alt](assets/hash_img.png)` so the markdown is self-contained
3. **Handles no-image PDFs** — if `result.images` is empty, returns markdown unchanged
4. **Preserves non-extracted images** — if the markdown references images that aren't in `result.images` (e.g., from URLs), those references are left untouched

### Image Naming Convention

By default, images keep their Datalab-assigned filenames (e.g., `hash_img.png`). For pipeline naming convention (`c{course#}_m{module#}_{topic}_{descriptor}.{ext}`), see **AGENTS.md Step 3** or the **md_converter** skill — renaming happens during the enrichment phase when course/module metadata is available.

## 3. Conversion Options for Image-Heavy PDFs

When converting PDFs with significant visual content (diagrams, charts, screenshots, figures), use these options:

| Option | Recommended Value | Why |
|--------|------------------|-----|
| `mode` | `"accurate"` | Highest accuracy for complex layouts, tables, and figures |
| `paginate` | `False` | No page delimiters in wiki output — content flows naturally |
| `disable_image_extraction` | `False` (default) | Images are always extracted — do not override |
| `disable_image_captions` | `False` (default) | Captions help identify image context in markdown |
| `extras` | `"chart_understanding"` | Extracts data from charts and graphs when present |

**Note:** `mode="fast"` does NOT skip image extraction — images are extracted regardless of mode. `mode="accurate"` is recommended for image-heavy PDFs because it better preserves layout and figure boundaries, but `mode="balanced"` is acceptable for general use.

## 4. Fallback — No Images Extracted

If Datalab is unavailable or image extraction fails, use the agent's native Read tool for text-only extraction. Note the gap in the enrichment log:

```
[ENRICHED: images — Datalab unavailable; images not extracted from PDF. Original PDF at <path>]
```

## 5. Full Documentation Reference

For exhaustive API parameters, pricing breakdown, and edge cases regarding Document Conversion, read the raw markdown files located in the `references/` subdirectory of this skill.
