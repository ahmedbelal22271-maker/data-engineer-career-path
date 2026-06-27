---
name: HTML & CSS Generation Guidelines
description: Rules for generating responsive, visually stunning HTML components using vanilla CSS, including chunking strategies.
---



# Source: html-css-generation-style-guide.md

# HTML/CSS Generation Style Guide (Claude Role Model)

> **Directive:** When generating HTML and CSS, adopt the creativity, visual hierarchy, and organizational excellence of Claude's output style. Capture *all* source information without summarizing, organizing it into clear sections with visual structure. HTML files must include **mobile media queries** — this is non-negotiable.

---

## 1. Typography

**Headers:** `'Inter', -apple-system, 'Segoe UI', sans-serif` — clean, geometric sans-serif. For an editorial/report feel, optionally use `'Georgia', serif` for H1 only with sans-serif body.

**Body:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

| Role | Size | Weight | Line-height | Letter-spacing |
|---|---|---|---|---|
| H1 | 2.25rem (36px) | 700 | 1.2 | -0.02em |
| H2 | 1.75rem (28px) | 700 | 1.3 | default |
| H3 | 1.25rem (20px) | 600 | 1.4 | default |
| Body | 1rem (16px) | 400 | 1.6 | default |
| Small/meta | 0.875rem (14px) | 400 | — | default |
| Labels | 0.75rem | 600 | — | 0.08em (uppercase) |

```css
h1 { font-size: 2.25rem; font-weight: 700; line-height: 1.2; letter-spacing: -0.02em; }
body { font-size: 1rem; line-height: 1.6; }
.label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
```

---

## 2. Color Palette Philosophy

One dominant accent color (Blue `#2563eb`, Indigo `#4f46e5`, or Teal `#0d9488`), used **sparingly** for links, key highlights, and active states — not everywhere.

Neutrals do the heavy lifting:

```css
:root {
  --accent: #2563eb;
  --text-primary: #0f172a;   /* near-black */
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --border: #e2e8f0;
  --bg-subtle: #f8fafc;
  --bg-card: #ffffff;
}
```

**Status colors** (use as subtle 10% opacity background tints with full-strength text/border):
- Success: `#16a34a`
- Warning: `#d97706`
- Danger: `#dc2626`

**Dark mode:** Invert neutrals (`#0f172a` background, `#f1f5f9` text); keep accent hue but slightly lighter/brighter for contrast.
- In the dark mode template, the header itself requires a slider.

---

## 3. Layout & Spacing

- **Max content width:** `840px–960px` for text-heavy reports; `1200px` for dashboard-style layouts. Centered with horizontal padding.
- **Spacing scale (4px base unit):** 4, 8, 12, 16, 24, 32, 48, 64px
  - Sections separated by 48–64px
  - Elements within a section by 16–24px

```css
.container { max-width: 880px; margin: 0 auto; padding: 0 24px; }
.section { margin-bottom: 48px; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
```

---

## 4. Information Architecture

> **Golden Rule: Never drop facts — restructure them.** Long prose gets broken into tables/cards. Repeated patterns in the source become repeated card/row templates. Default toward full inclusion over summarization.

| Component | Use When |
|---|---|
| **Cards** | Discrete, comparable items (features, team members, metrics) |
| **Tables** | Structured multi-attribute data, comparisons across rows/columns |
| **Lists** | Sequential steps, simple enumerations |
| **Callout boxes** | Warnings, tips, key takeaways — anything that must interrupt normal flow |
| **Accordions** | Optional/secondary detail that would otherwise bloat the page (FAQs, appendices) |

---

## 5. Visual Components (CSS)

```css
/* Card */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}

/* Badge / Pill */
.badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(37,99,235,0.1);
  color: var(--accent);
}

/* Button */
.btn {
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease;
}
.btn:hover { background: #1d4ed8; }

/* Table */
table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
th, td { padding: 10px 14px; border-bottom: 1px solid var(--border); text-align: left; }
th { font-weight: 600; color: var(--text-secondary); background: var(--bg-subtle); }

/* Blockquote */
blockquote {
  border-left: 3px solid var(--accent);
  padding-left: 16px;
  color: var(--text-secondary);
  font-style: italic;
}

/* Code */
code, pre {
  font-family: 'SF Mono', 'Fira Code', monospace;
  background: var(--bg-subtle);
  border-radius: 6px;
}
pre { padding: 16px; overflow-x: auto; }

hr { border: none; border-top: 1px solid var(--border); margin: 32px 0; }
```

---

## 6. Hierarchy & Emphasis

- Signal importance primarily through **size and weight** first, then **color** second.
- Background fill is a **last resort** — used sparingly for callouts only.
- Avoid heavy borders everywhere — one accent border (left-border on callouts) is enough.
- Never use more than **one accent color** plus neutrals plus 1–2 status colors.
- **Bold is reserved for genuinely key terms**, not decoration.

---

## 7. Responsive Behavior (Mobile Media Queries — MANDATORY)

All generated HTML files must implement responsive media queries. This is non-negotiable.

```css
@media (max-width: 768px) {
  .card-grid { grid-template-columns: 1fr; }
  h1 { font-size: 1.75rem; }
  .container { padding: 0 16px; }
  .toc-grid { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
  table { font-size: 0.8rem; }
  .btn { width: 100%; }
}
```

---

## 8. Micro-Details

- **Border-radius:** 8px (buttons/inputs), 12px (cards), 999px (badges/pills)
- **Shadows:** Very subtle — `0 1px 2px rgba(0,0,0,0.04)` default, up to `0 4px 12px rgba(0,0,0,0.08)` on hover
- **Transitions:** `0.15s–0.2s ease` on color/background/transform only
- **Icons:** Inline SVG (lucide-style, stroke-based, 16–20px) — never emoji in formal reports unless explicitly playful
- **Hover effects:** Slight `translateY(-2px)` on cards; color darken on buttons/links

---

## 9. Document Header and Topic Navigation

Every long HTML document must begin with a proper header and navigation system. This is what separates a "compiled markdown" feel from a polished reference document.

### 9a. Header Block

```html
<header class="doc-header">
  <h1>Document Title Here</h1>
  <p class="doc-subtitle">A description of what this document covers.</p>
  <div class="doc-meta">
    <span class="meta-badge">42 Questions</span>
    <span class="meta-badge">Fall 2020 – Spring 2023</span>
    <span class="meta-badge">Topic Tag</span>
  </div>
</header>
```

```css
.doc-header { padding: 40px 0 32px; border-bottom: 1px solid var(--border); margin-bottom: 32px; }
.doc-header h1 { margin-bottom: 8px; }
.doc-subtitle { color: var(--text-secondary); font-size: 1.05rem; margin-bottom: 16px; }
.doc-meta { display: flex; gap: 8px; flex-wrap: wrap; }
.meta-badge { font-size: 0.8rem; font-weight: 600; padding: 4px 12px; border-radius: 999px; background: var(--bg-subtle); border: 1px solid var(--border); color: var(--text-secondary); }
```

### 9b. Table of Contents / Topic Navigation

- Immediately after the header, include a TOC listing every section as a **clickable jump link** (`href="#anchor-id"`).
- Group by category (e.g., by exam term or topic cluster).
- Each TOC entry should have a **short descriptive phrase** summarizing what the section covers — not just a number.
- If the document has more than ~15 items, make the TOC collapsible using `<details>`/`<summary>` (no JS required).

```html
<nav class="toc">
  <h2 class="toc-title">Contents</h2>
  <div class="toc-grid">
    <div class="toc-group">
      <h3 class="toc-group-title">Fall 2020</h3>
      <a href="#q25" class="toc-link">Q25 — ALU Shift Operation Identification</a>
      <a href="#q26" class="toc-link">Q26 — Synthesizability Check</a>
    </div>
  </div>
</nav>
```

```css
.toc { background: var(--bg-subtle); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 48px; }
.toc-title { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 16px; }
.toc-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 24px; }
.toc-group-title { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); margin-bottom: 8px; }
.toc-link { display: block; font-size: 0.9rem; color: var(--text-secondary); text-decoration: none; padding: 4px 0; transition: color 0.15s ease; }
.toc-link:hover { color: var(--accent); }
```

### 9c. Anchor IDs
- Every section card must have a matching `id` attribute (e.g., `id="q25"`) for TOC links to work.
- This is **required**, not optional, even for short documents.

---

## 10. Creativity and Variation Directives

The design patterns above are a **baseline, not a ceiling**.

- Adapt structure to content needs. Build custom visuals (SVG diagrams, styled tables for signal transitions) where appropriate — don't force everything into a generic code block.
- Include an option for mermaid smart diagrams where suitable.
- **Introduce additional visual patterns** where they help: comparison tables, side-by-side panels, progress indicators for multi-part questions, visual groupings that cluster related content.
- **Vary presentation to prevent monotony.** 40 identical card layouts in a row becomes hard to scan. Introduce subtle variation: different accent colors per topic category, different icons per question type (code/diagram/conceptual), alternating layouts for visual rhythm — while keeping the overall design language consistent.
- **Add value beyond formatting** where the source material supports it: a "concept summary" callout box at the start of a topic cluster, a legend/key if you introduce icons or color-coding.
- **Vary information density** intelligently. Some content warrants a fuller layout; simple items can be compact cards. Do not force uniform card heights if it hurts readability.
- **Goal:** The document should feel like it was thoughtfully designed by someone who understands the subject — not like a template was mechanically applied. Prioritize clarity and genuine usefulness over consistency for its own sake, but never sacrifice the core design system (colors, typography, spacing).

---

## 11. Why Claude over Gemini for HTML
- Gemini's HTML generation is less polished and less organized than Claude's.
- When using Gemini Pro for HTML generation, provide Claude's style guide as a role model.
- Instruct Gemini Pro explicitly: adhere to information comprehensively, go all out on token usage, and use Claude's visual hierarchy and design system as the standard to match or exceed.

---

## 12. HTML Project Standards & Agent Identity
When acting as an HTML Project Agent, you must adopt the following core principles:
1. **Understand before touching:** Plan before you write. Ask precise questions if ambiguous.
2. **Self-contained output:** HTML files must run correctly with no missing dependencies or placeholders.
3. **Single source of truth:** Store scripts/assets in a logical directory structure (`/assets/`, `/scripts/`).
5. **Visual Quality & Responsiveness:** All output must be visually polished, using consistent typography/color, and MUST implement mobile media queries (non-negotiable). Use CSS Grid/Flexbox over fixed pixel widths.
6. **Framework Assumptions:** Never default to React/Vite/Tailwind for documents unless explicitly instructed. Use vanilla HTML/CSS as the absolute baseline.
7. **Strict Negative Constraints:** Listen precisely to user dislikes (e.g. "no sliding boxes"). Substitute immediately with clean standard alternatives.

---

## 13. Strict Anti-Dump UI Protocol
- **Raw logs and unformatted chunks must never be injected directly into production HTML.**
- Data parsing and raw extraction must occur in the filesystem (e.g. within `_extraction_scratchpad/`).
- Presentation must occur in the UI via properly styled, meaningful semantic components (cards, tables, lists).
- **Literal Dialogue Transcription Ban:** Raw dialogue transcription is prohibited in HTML deliverables. This includes any literal use of `User:`, `AI:`, or equivalent turn-marker labels. Source dialogue must be synthesized into native UI components (insight boxes, tables).

## 14. Incremental Augmentation Protocol (Anti-Destruction)
- When told your output lacks detail, **you must not "start over" and destroy the existing UI framework.**
- Instead, you must inject newly extracted hierarchical chunk data directly into the gaps of the existing HTML framework.
- Preserve what works; increment what is missing.

## 15. Targeted Elaborative Modes & Subagent Synchronization
- **Zero-Summary Policy:** When elaboration is requested on a specific section, that chunk must be translated *un-summarized* into the premium UI.
- Break massive elaborations into macro/micro chunks if necessary to preserve detail.
- **Subagent Synchronization:** Subagents must follow sequential synchronization when editing the HTML to prevent data overwrite and structural mess. Parallel edits on the same DOM structure are prohibited.

## 16. LTHP (Last-Touch Highlight Protocol)
- Use visual identification to track recently modified blocks in the HTML.
- When you execute a targeted edit, apply a temporary CSS highlight class (e.g., `class="lthp-edited"`) or amber borders to the exact section you modified.
- This allows the user to instantly verify the delta without hunting through the entire document.

---

## 17. Advanced Frontend Architecture Protocol
For rigorous operational rules regarding Layout Strategy (Flexbox vs Grid decisions), Z-Index Stacking Contexts, Box-Sizing Baselines, and computed-style programmatic validation, refer to the [Frontend Architecture Protocol](file:///C:/Users/marwa/OneDrive/Documents/College%20Courses/agentic%20workflow/general%20tips/.agents/skills/html_css_generation/references/frontend_architecture.md).


# Source: html-chunking-strategy.md

# HTML Chunking Strategy for Large Files

> ⚠️ **Before reading this file, visit and read the L1 master file in its entirety if you have not done so in this session.**

> **Terminology Disambiguation:** This file governs **Output HTML Chunk Mapping** (maintaining an index of the UI structure). Do not confuse this with **Input Extraction Chunking** (using an `_extraction_scratchpad/` to parse massive log files), which is governed by `file-management-and-context-optimization.md`.

## Purpose
When generating or updating large HTML files, re-reading the entire file from scratch on every update is wasteful and risks context overflow. The chunking strategy solves this by maintaining a set of small reference files — one per logical section of the HTML — so updates can be targeted and verified without full re-reads.

---

## Directory Structure

For every major HTML file you generate or manage, create a dedicated **chunk directory** alongside it:

- The directory name must be **unique** and **directly related** to the HTML filename.
- Example: for `digital-logic-exam-bank.html` → create directory `digital-logic-exam-bank_html-chunks/`

```
project/
├── digital-logic-exam-bank.html
└── digital-logic-exam-bank_html-chunks/
    ├── chunk-01-header-and-toc.md
    ├── chunk-02-alu-operations.md
    ├── chunk-03-synthesizability.md
    └── chunk-04-timing-and-waveforms.md
```

---

## Chunking Rules

### Chunk by Logical Section, NOT by Line Count
- The "500 lines" example is a guideline for sizing — the actual boundary of each chunk must be a **logical section boundary** (e.g., a complete `<section>`, a full topic group, a complete `<nav>` block).
- Never cut off a chunk in the middle of a component or semantic unit — always end at a clean close tag.

### What Goes in Each Chunk File
Each chunk `.md` file must contain:
1. **The chunk name and its position** (e.g., `Chunk 02 — ALU Operations Section`).
2. **The corresponding HTML lines or section range** (approximate, for reference).
3. **A summary of what HTML content this chunk covers.**
4. **Status flag:** `[ ] Not yet populated` / `[x] Content written` / `[x] Last updated: YYYY-MM-DD`
5. Optionally: a short excerpt of the key HTML structure (landmark tags, IDs, section headings) for quick orientation.

### Example Chunk File

```markdown
# Chunk 02 — ALU Operations Section

**HTML Section:** `<section id="alu-operations">` ... `</section>`  
**Approximate position:** Lines 180–420 of the HTML file  
**Status:** [x] Content written — Last updated: 2026-06-15

## Contents
- 8 question cards (Q10–Q17)
- Each card has: question text, code block, multiple choice options, answer callout
- TOC anchor IDs: #q10 through #q17

## Key IDs in this chunk
- `#alu-operations` (section anchor)
- `#q10` through `#q17` (question card anchors)
```

---

## Update Workflow

When you make changes to the HTML file:

1. **Identify which chunk(s) are affected** by the change — do not re-read the whole file.
2. **Make the update** in the HTML file targeted to that section.
3. **Immediately update the corresponding chunk file** to reflect the change (status flag, summary, key IDs if added/removed).
4. Use your detection mechanisms to **confirm the target section has been updated** before moving on.

> These chunk files are not made in vain. You are **required** to use them as your navigational index for any future update to the HTML file. Ignoring them and re-reading the full HTML file each time is a violation of this protocol.

---

## Consistency and Performance Guarantee

- Chunk files serve as a **compact map** of the HTML file's structure.
- Before making any update, consult the chunk index to locate the relevant section quickly.
- After any update, the chunk file for that section must be kept in sync — treat out-of-sync chunk files as a bug to fix immediately.
- This approach ensures you never need to load the full HTML into context just to make a targeted change.


# Source: frontend-design-principles-and-process.md

# Frontend Design Principles and Process

> **Role:** Approach every design task as the design lead at a small studio known for giving every client a visual identity that could not be mistaken for anyone else's. This client has already rejected proposals that felt templated, and is paying for a distinctive point of view. Make deliberate, opinionated choices about palette, typography, and layout that are specific to the brief — and take one real aesthetic risk you can justify.

---

## Ground It in the Subject

- If the brief does not pin down what the product or subject is, **pin it yourself before designing**: name one concrete subject, its audience, and the page's single job — and state your choice explicitly.
- If there is any information available about the user's preferences, context about what they're building, or designs made before — use that as a hint.
- The subject's own world — its materials, instruments, artifacts, and vernacular — is where **distinctive choices come from**. Build with the brief's real content and subject matter throughout.

---

## Core Design Principles

### The Hero is a Thesis
- Open with the most **characteristic thing** in the subject's world, in whatever form makes sense: a headline, an image, an animation, a live demo, an interactive moment.
- Be deliberate with your choice. A big number with a small label, supporting stats, and a gradient accent is the **template answer** — only use it if it's truly the best option for this brief.

### Typography Carries Personality
- Pair display and body faces **deliberately**, not the same families you would reach for on any other project.
- Set a clear type scale with intentional weights, widths, and spacing.
- Make the type treatment itself a **memorable part of the design** — not a neutral delivery vehicle for content.

### Structure is Information
- Structural devices — numbering, eyebrows, dividers, labels — should **encode something true** about the content, not just decorate it.
- Many generic designs use numbered markers (01 / 02 / 03) — this is only appropriate if the content actually is a sequence (a real process, a typed timeline where order matters). **Question whether numbered markers actually make sense** before using them.

### Motion Must Serve the Subject
- Think carefully about where and if animation serves the brief: page-load sequences, scroll-triggered reveals, hover micro-interactions, ambient atmosphere.
- An orchestrated moment usually lands harder than scattered effects — choose what the direction calls for.
- **Sometimes less is more.** Extra animation can make a design feel AI-generated. Use restraint.

### Match Complexity to the Vision
- Maximalist directions need elaborate execution.
- Minimal directions need precision in spacing, type, and detail.
- Elegance is executing the chosen vision well — not adding more.

---

## The Two-Pass Design Process

Work in two passes. Do most of the planning in your thinking — only show ideas to the user when you have high confidence they will delight them.

### Pass 1: Brainstorm the Design Plan
Create a compact token system with these four components:

1. **Color** — describe the palette as 4–6 named hex values.
2. **Type** — the typefaces for 2+ roles:
   - A characterful display face used with restraint.
   - A complementary body face.
   - A utility face for captions or data if needed.
3. **Layout** — a layout concept described with one-sentence prose and ASCII wireframes to ideate and compare.
4. **Signature** — the **single unique element** this page will be remembered by, that embodies the brief in an appropriate way.

### Pass 2: Review Before Building
Before writing any code, review the plan against the brief:
- Does any part of it read like the generic default you would produce for *any similar page*?
- If yes — **revise that part**, state what you changed and why.
- Only after confirming the relative uniqueness of your design plan should you start writing code.
- Follow the revised plan exactly, deriving every color and type decision from it.

> **Watch for CSS selector conflicts.** It's easy to generate CSS classes that cancel each other out (especially `.section` vs `.cta`, or element-level selectors vs class selectors). Pay attention to padding/margin conflicts between sections in particular.

---

## Avoiding Generic Defaults

AI-generated design currently clusters around three looks — all are legitimate for *some* briefs, but they appear regardless of subject. Be aware of them:

1. **Warm cream background** (~`#F4F1EA`) with high-contrast serif display and terracotta accent.
2. **Near-black background** with a single bright acid-green or vermilion accent.
3. **Broadsheet/newspaper layout** with hairline rules, zero border-radius, and dense columns.

- Where the brief **explicitly** asks for one of these looks, follow it — the brief's words always win.
- Where it leaves the aesthetic axis **free**, don't spend that freedom on one of these defaults.

---

## Restraint and Self-Critique

- **Spend your boldness in one place.** Let the signature element be the one memorable thing — keep everything around it quiet and disciplined.
- Cut any decoration that does not serve the brief.
- Not taking a risk can itself be a risk.
- Build to a quality floor without announcing it: **responsive down to mobile**, visible keyboard focus, reduced motion respected.
- Critique your own work as you build. Take screenshots if your environment supports it — a picture is worth 1000 tokens.
- Consider Chanel's rule: before leaving the house, look in the mirror and remove one accessory.
- If you have space to jot notes about what you've tried, do it — it helps in future passes.

---

## Writing in Design (Copy Guidelines)

Words appear in a design for one reason: **to make it easier to understand, and therefore easier to use.** They are design material, not decoration. Bring the same intentionality to copy as to spacing and color.

### Core Principles
- Before writing anything, ask: *what does the design need to say, and how can it best be said to help the person navigate the experience?*
- Write from the **end user's side of the screen**. Name things by what people control and recognize — never by how the system is built.
  - ✅ "manage notifications" — ❌ "configure webhook settings"
- Describe what something **does** in plain terms, rather than selling it.
- Being **specific is always better than being clever**.

### Voice and Grammar
- Use **active voice** as the default.
- A control should say exactly what happens when it's used: "Save changes," not "Submit."
- An action keeps the **same name through the whole flow**: the button that says "Publish" produces a toast that says "Published." Vocabulary is signposting.
- Keep the register **conversational and tuned**: plain verbs, sentence case, no filler, tone matched to the brand and audience.
- Let each element do **exactly one job**: a label labels, an example demonstrates — nothing quietly does double duty.

### Errors and Empty States
- Treat failure and emptiness as **moments for direction**, not mood.
- Explain what went wrong and how to fix it, in the interface's voice — not a person's voice.
- Errors don't apologize and are **never vague** about what happened.
- An empty screen is **an invitation to act**.
