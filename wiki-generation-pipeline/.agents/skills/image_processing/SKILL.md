---
name: Image Processing
description: Guidelines for handling, formatting, and processing images.
---

# Image Processing Protocol

## External URL Image Acquisition

When the user provides any website, LinkedIn post, blog, or article URL containing images:

### Step 1 — Scrape images from URLs

Use `scripts/scrape_images.py` to extract images:

```
python scripts/scrape_images.py --urls "URL1" "URL2" ... --output-dir scraped_images/
```

The script:
- Uses `requests` + `BeautifulSoup` for static content
- Optionally falls back to Playwright for JS-rendered pages (LinkedIn, dynamic blogs)
- Downloads images to `scraped_images/{domain}/{filename}`
- Filters images by min dimensions (100x100), file size (10MB), and discards base64/svg icons
- Generates `scraped_images/manifest.json` with source URL, alt text, page context, local path

Always verify: `manifest.json` exists, has entries, and files exist at listed paths.

### Step 2 — AI Agent Handoff for Image Analysis

Prepare `scraped_images/image_analysis_handoff.md` as a structured prompt for the smarter AI agent (Antigravity/Codex). Include:

- Project context (what the wiki/study guide covers)
- Every image with its path, source URL, alt text, page context, dimensions
- Exact JSON output schema per image: `{path, description, relevance_score, suggested_placement, suggested_filename}`
- Instruction to write results to `scraped_images/analysis_report.json`

### Step 3 — Process the Agent Report

Read `scraped_images/analysis_report.json`:
- relevance >= 3: integrate into wiki pipeline
- relevance == 2: keep file, skip pipeline, log reason
- relevance <= 1: reject, log reason
- score == 0 with ERROR: investigate file

Apply suggested filename renames using `os.rename(old, new)`.
Update `manifest.json` with descriptions and relevance scores.

### Step 4 — Integrate Images into Wiki / HTML

During Phase 2 (Deep Extraction):
- Insert `![description](repo-root-relative-path)` into relevant topic files
- Images should accompany the section they illustrate

During Phase 5 (HTML Rendering):
- Resolve paths relative to `index.html` location
- Paths starting with `scraped_images/` are repo-root-relative
- Add `loading="lazy"` attribute
- Apply CSS max-width constraints

### Step 5 — Ongoing Agent Dialogue (Optional)

If placement is uncertain:
- Write `scraped_images/placement_query.md` with images + section structure + specific placement questions
- The external agent responds with `scraped_images/placement_response.json`
- Apply placement decisions from the response

## Unclear Images
- If an image provided is **not clear**, immediately notify the user.
- **Specify exactly which image** is problematic (by name, number, or description).
- **Request a clearer version directly** from the user — do not attempt to guess or fabricate content from an unclear image.

## Alternative Extraction Methods
If a clear version cannot be obtained directly, suggest one of the following alternatives:

1. **High-Capability Vision AI:** Use a high-capability vision model (e.g., Claude) to extract information from the unclear image, then feed that extracted text to Gemini Pro or the working agent.
2. **Datalab Integration:** Explore the Datalab option if images reside in the same directory as the Markdown file generated from slides — this pipeline may already have the images accessible.

## Using Downloaded Images in HTML Guides
- If images have been downloaded to the working directory via the Datalab pipeline API or external URL scraping, **you have no excuse to omit them** from generated HTML study guides or reference documents.
- You are required to include them and make the guide **as visual as possible** — using images and diagrams wherever the source material supports it.
- Give every image a **clear, distinctive filename** in the directory so images are not lost among content and are easy to locate and reference.

## Image Naming Convention
- Names must be descriptive and unique: e.g., `alu-shift-operation-diagram.png`, `state-machine-fall2020-q3.jpg`.
- Avoid generic names like `image1.png` or `img_001.jpg`.
- The name should immediately communicate what the image depicts without needing to open it.

## Per-Source Image Organization (Datalab Output)

When reorganizing Datalab-extracted images from flat `images/` into per-source subdirectories:

### COPY — Never MOVE
- Images may be **shared** across multiple markdown files (same hash image referenced by multiple PDFs)
- **Always COPY** images to each source subdirectory, never MOVE
- Only DELETE the original after ALL copies are made
- MOVE causes broken refs in all but the first source

### Sequential Renaming
```
images/{source_stem}/
  {source_stem}_img_001.jpg
  {source_stem}_img_002.jpg
  ...
```
- Each source gets its own numbered sequence
- Images must be named after the source stem, not the hash

### Ref Update Strategy
1. Count unique image refs per markdown file (deduplicate by hash)
2. Assign each unique hash a sequential number
3. Copy (not move) to per-source subdir with `{source_stem}_img_{seq:03d}.ext`
4. Update ALL markdown refs to point to the new path

### Python Path Traversal Pitfalls (Windows)
- `Path.glob('*_img.*')` returns **0 results** on Windows for paths with underscores → use `sd.iterdir()` and filter by `.is_file()` instead
- `re.findall(r'\]\(images/([^)]+)\)', content)` with `[^)]+` **breaks on parenthesized paths** like `stem (1) (1)/file.jpg` → use `r'\]\(images/(.+?_img\.\w+)\)'` instead (non-greedy match to `_img.ext)`)
- Always verify file existence with `(img_dir / ref).exists()` after updating refs

### Content Dedup Note
When the same hash image is referenced by multiple markdown files (shared lecture diagrams), only ONE copy will exist on disk (in the first source's subdir). The other sources lose that image unless you COPY. Acceptable loss only by explicit decision.
