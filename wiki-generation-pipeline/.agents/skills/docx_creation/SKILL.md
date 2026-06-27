---
name: docx_creation
description: "Instructions for programmatic .docx handling, generation, and extraction. Best practices for python-docx, docxtpl, raw XML manipulation, and edge cases."
---

# DOCX Creation, Editing, and Analysis

## 1. Understanding the Format
A `.docx` file is a ZIP archive containing XML files following the Office Open XML (OOXML) standard (ECMA-376). Key internal structure:
- `word/document.xml`       <- main body content
- `word/styles.xml`         <- style definitions
- `word/numbering.xml`      <- list/numbering definitions
- `word/media/`             <- embedded images
- `word/_rels/`              <- relationship files (linking images, hyperlinks, etc.)
- `[Content_Types].xml`     <- declares MIME types of parts

Understanding this matters because many "weird" bugs (broken images, missing styles) come from relationship (`.rels`) mismatches, not logic.

## 2. Choosing a Library

| Task | Best Tool | Notes |
|---|---|---|
| Generate new docs (Python) | `python-docx` | Great for paragraphs, tables, styles. No native chart/SmartArt support. |
| Edit existing docs preserving formatting | `python-docx` + `lxml` | python-docx alone can't touch some elements; drop to raw XML when needed. |
| Convert to/from other formats | `pandoc` | Excellent for docx ↔ markdown/html/odt. Less reliable for pixel-perfect Word styling. |
| Reading/extracting text only | `docx2txt`, `mammoth` | `mammoth` converts docx to clean semantic HTML. |
| Track changes / comments | Open XML SDK | python-docx has very limited support for revisions; expect to hand-write XML. |

**Rule of thumb:** For simple generation, use a high-level library. For templates, tracked changes, or precise style fidelity, manipulate the underlying XML directly.

## 3. Common Generation Patterns

### Template-based generation (Recommended)
Create a Word template with placeholder text, then use a templating library:
- **Python**: `docxtpl` (built on python-docx + Jinja2) — supports loops, conditionals, image insertion via `{{ }}` syntax inside the Word doc itself.
- **Node.js**: `docxtemplater` — mature, good image/table-loop support.

### Programmatic generation from scratch
- Default styles in python-docx come from a minimal built-in template. Set styles explicitly or base off a template file (`Document('template.docx')`).

## 4. Reading and Extraction Edge Cases
- **Headers/footers and text boxes** live in separate XML parts (`header1.xml`) and need explicit handling.
- **Tables nested in tables** trip up naive extraction — handle `<w:tbl>` elements recursively.
- **Tracked changes**: Naive text extraction includes deleted text unless you filter `<w:del>` elements.
- **Text split across multiple `<w:r>` runs**: A single visible word can be split across runs. Search across concatenated text, then walk the runs to apply replacements.
- **Embedded objects** show up as binary blobs in `word/embeddings/`.

## 5. Common Failure Points

| Symptom | Likely Cause |
|---|---|
| "Word found unreadable content" on open | Malformed XML (unescaped `&`, `<`, mismatched tags) |
| Images appear as red X / broken icon | Missing or mismatched relationship ID in `.rels` file | 
| Styles don't apply / fall back to Normal | Style ID vs. style *name* confusion in `styles.xml` |
| Mail-merge templates silently fail | Placeholder text got split across multiple runs by autocorrect |

## 6. Working with Images
- Calculate aspect ratios in code to avoid stretching/squashing.
- Embed images as bytes directly (`add_picture(io.BytesIO(...))`) rather than writing temp files to avoid I/O failure points.

## 7. Performance & Validation
- For massive documents, `lxml` XML manipulation significantly outperforms building in-memory object graphs.
- Always run `python -m zipfile -t file.docx` to confirm the ZIP container isn't corrupted before debugging XML issues.

---
## Legacy NodeJS Fallback & Scripts
If node.js generation is strictly required:
```javascript
const { Document, Packer } = require('docx');
const doc = new Document({ sections: [{ children: [] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```
Always set page size explicitly for consistent results:
`margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch margins`
