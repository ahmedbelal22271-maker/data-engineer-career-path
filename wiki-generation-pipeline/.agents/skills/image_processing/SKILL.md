---
name: Image Processing
description: Guidelines for handling, formatting, and processing images.
---



# Source: image-processing-protocol.md

# Image Processing Protocol

## Unclear Images
- If an image provided is **not clear**, immediately notify the user.
- **Specify exactly which image** is problematic (by name, number, or description).
- **Request a clearer version directly** from the user — do not attempt to guess or fabricate content from an unclear image.

## Alternative Extraction Methods
If a clear version cannot be obtained directly, suggest one of the following alternatives:

1. **High-Capability Vision AI:** Use a high-capability vision model (e.g., Claude) to extract information from the unclear image, then feed that extracted text to Gemini Pro or the working agent.
2. **Datalab Integration:** Explore the Datalab option if images reside in the same directory as the Markdown file generated from slides — this pipeline may already have the images accessible.

## Using Downloaded Images in HTML Guides
- If images have been downloaded to the working directory via the Datalab pipeline API, **you have no excuse to omit them** from generated HTML study guides or reference documents.
- You are required to include them and make the guide **as visual as possible** — using images and diagrams wherever the source material supports it.
- Give every image a **clear, distinctive filename** in the directory so images are not lost among content and are easy to locate and reference.

## Image Naming Convention
- Names must be descriptive and unique: e.g., `alu-shift-operation-diagram.png`, `state-machine-fall2020-q3.jpg`.
- Avoid generic names like `image1.png` or `img_001.jpg`.
- The name should immediately communicate what the image depicts without needing to open it.
