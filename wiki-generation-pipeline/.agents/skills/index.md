# Skills Index
*Last updated: 2026-06-22*

## Purpose
Master reference for all skills under `.agents/skills/`. Read this first to identify which skill to invoke for any given task. Each entry links to the full `SKILL.md` and notes whether the skill has bundled reference files that must be fetched (per Ground-Truth Enforcement) rather than generated from memory.

---

## Quick-Reference Table

| Directory | Name | Size | Has refs/ | When to Use |
|---|---|---|---|---|
| `anthropic_product_knowledge/` | Anthropic Product Knowledge | 79 lines | Yes | User asks about Claude Code, Claude API, Claude.ai plans, pricing, or capability questions |
| `data_architecture/` | Data Architecture & Algorithms | 19 lines | No | Designing database schemas, graph vs relational decisions, dependency traversal |
| `datalab_conversion/` | Datalab Document Conversion | 46 lines | Yes | Converting PDFs/images/docs to Markdown, HTML, or JSON via Datalab |
| `datalab_core/` | Datalab Core SDK | 47 lines | Yes | Starting any Datalab workflow — install, auth, client init, error handling |
| `datalab_extraction/` | Datalab Structured Extraction | 49 lines | Yes | Extracting structured JSON from invoices, forms, or images with a schema |
| `datalab_form_filling/` | Datalab Form Filling | 27 lines | No | Filling blank PDF forms with mapped field data |
| `datalab_pipelines/` | Datalab Pipelines | 49 lines | Yes | Chaining convert + extract + segment into async pipelines |
| `docx_creation/` | docx_creation | 74 lines | No | Generating, editing, or extracting .docx files programmatically |
| `html_css_generation/` | HTML & CSS Generation Guidelines | 521 lines | Yes | Building HTML/CSS from scratch, designing frontends, creating visual reports |
| `image_processing/` | Image Processing | 31 lines | No | Handling unclear images, naming conventions, integrating into HTML |
| `modern_engineering/` | Modern Engineering (Karpathy Method) | 30 lines | No | Setting up agent workflows, defining specs, creating verification loops |
| `prompt_engineering/` | Prompt Engineering & Debugging | 39 lines | No | Crafting system prompts, resolving ambiguity, debugging failed prompts |
| `prompt_engineering_best_practices/` | Prompting Best Practices | 783 lines | No | Writing production prompts for Fable 5/Opus 4.8/Sonnet 4.6, thinking config, tool use, agentic systems, migration |
| `skill-creator/` | Skill Creator | 485 lines | Yes | Creating, testing, evaluating, and packaging new skills |
| `study_guide_generation/` | Study Guide Generation | 37 lines | No | Generating HTML study guides, exam banks, question analysis from course slides |
| `system_architecture/` | System Architecture | 30 lines | No | Orchestrating subagents, preventing compounding errors, parallelization decisions |

---

## Detailed Entries

### `anthropic_product_knowledge/`
- **Name:** Anthropic Product Knowledge
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\anthropic_product_knowledge\SKILL.md` (79 lines)
- **Has references/:** Yes — `references/self_knowledge_boundaries.md`
- **Description:** Authoritative fact-checking source for Anthropic's three product lines. Prevents hallucinations about model capabilities, pricing, and platform-specific features.
- **Sections:**
  - Question Routing — directs queries to Claude API docs, Claude Code docs, or Claude.ai support
  - Response Workflow — 5-step verification pipeline before answering product questions
  - Quick Reference — direct URLs for documentation, npm package, support center, enterprise sales
  - Advanced Capability Verification — self-knowledge boundaries protocol for tool availability checks
- **Key capabilities:**
  - Disambiguates Claude.ai (plans, features) vs Claude Code (install, MCP, config) vs Claude API (tool use, batch, SDK, rate limits, pricing)
  - Provides source-anchored answers with official doc URLs — never guesses about Anthropic product capabilities
- **Cross-references:** `prompt_engineering_best_practices` (model identity), `system_architecture` (agent identity)

### `data_architecture/`
- **Name:** Data Architecture & Algorithms
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\data_architecture\SKILL.md` (19 lines)
- **Has references/:** No
- **Description:** Dual-database strategy for separating data by geometry. Relational SQL for tabular aggregates, graph databases for interconnected entities.
- **Sections:**
  - Dual-Database Knowledge Core — when to use SQL vs graph topology
  - Set Difference Graph Traversal — computing what the user lacks vs what's required via BFS
- **Key capabilities:**
  - Compute topological deficits: `required_nodes − existing_nodes → constrained_BFS_bridge`
  - Exponentially faster relationship resolution via graph topology
- **Cross-references:** `system_architecture` (DAG execution)

### `datalab_conversion/`
- **Name:** Datalab Document Conversion
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\datalab_conversion\SKILL.md` (46 lines)
- **Has references/:** Yes — `references/document_conversion.md`
- **Description:** Converts PDFs, images, and documents to Markdown, HTML, JSON, or chunked output via the Datalab SDK. Supports multiple accuracy modes and page ranges.
- **Key capabilities:**
  - Output formats: markdown, html, json, chunks
  - Modes: fast (default), balanced, accurate; page range (0-indexed); chart understanding extra
  - Image extraction and bundled saving via `result.save_output("output/", save_images=True)`
  - Supports both local file and URL input
- **Cross-references:** `datalab_core` (required SDK init), `datalab_pipelines` (chaining), `image_processing` (downloaded images)

### `datalab_core/`
- **Name:** Datalab Core SDK
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\datalab_core\SKILL.md` (47 lines)
- **Has references/:** Yes — `references/python_sdk.md`, `references/quickstart.md`, `references/welcome.md`
- **Description:** Foundation for all Datalab workflows. Covers the critical installation trap (correct package is `datalab-python-sdk`, NOT `datalab`), authentication, and the full exception hierarchy.
- **Key capabilities:**
  - Correct pip package: `datalab-python-sdk` (hyphens) vs import module: `datalab_sdk` (underscore)
  - DatalabClient (sync) and AsyncDatalabClient (high-throughput)
  - Exception hierarchy: DatalabAPIError, DatalabTimeoutError, DatalabFileError, DatalabValidationError
  - Production tip: Always catch specific exceptions, never bare `except`
- **Cross-references:** Required by all other `datalab_*` skills

### `datalab_extraction/`
- **Name:** Datalab Structured Extraction
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\datalab_extraction\SKILL.md` (49 lines)
- **Has references/:** Yes — `references/balanced_mode.md`, `references/confidence_scoring.md`, `references/data_extraction_pipeline.md`, `references/structured_extraction.md`
- **Description:** Extracts structured JSON from PDFs or images using a predefined JSON schema. Each extracted field comes with citations and confidence metadata.
- **Key capabilities:**
  - JSON schema-driven extraction with `required` field enforcement
  - Per-field citations and extraction status metadata
  - Advanced pipeline: Extract → Validate → Reconcile → Commit (see references/)
- **Cross-references:** `datalab_core` (SDK init), `datalab_pipelines` (step sequencing), `datalab_conversion` (pre-extraction)

### `datalab_form_filling/`
- **Name:** Datalab Form Filling
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\datalab_form_filling\SKILL.md` (27 lines)
- **Has references/:** No
- **Description:** Fills blank PDF forms with structured field data. Maps field names to value + description pairs and outputs a completed PDF.
- **Key capabilities:**
  - Field mapping: `{"field_name": {"value": "...", "description": "..."}}`
  - Direct save via `result.save_output("filled_form.pdf")`
- **Cross-references:** `datalab_core` (SDK init), `datalab_extraction` (pre-fill data extraction)

### `datalab_pipelines/`
- **Name:** Datalab Pipelines
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\datalab_pipelines\SKILL.md` (49 lines)
- **Has references/:** Yes — `references/create_pipeline.md`, `references/pipeline_versioning.md`, `references/pipelines.md`, `references/run_pipeline.md`
- **Description:** Chains multiple Datalab processors (convert, extract, segment) into reusable asynchronous pipelines with polling-based execution.
- **Key capabilities:**
  - PipelineProcessor typed steps: convert, extract, segment
  - Async execution with configurable polling (max_polls=300, poll_interval=2s)
  - Step-level result retrieval by `step_index`
  - Pipeline versioning support (see references/)
- **Cross-references:** `datalab_core` (SDK init), `datalab_conversion` (convert step), `datalab_extraction` (extract step), `system_architecture` (async patterns)

### `docx_creation/`
- **Name:** docx_creation
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\docx_creation\SKILL.md` (74 lines)
- **Has references/:** No
- **Description:** Complete .docx workflow — generation, editing, extraction, and troubleshooting. Covers python-docx, docxtpl, lxml, pandoc, and raw OOXML XML manipulation.
- **Sections:**
  - Library selection guide (python-docx vs docxtpl vs Open XML SDK vs mammoth)
  - Template-based generation (docxtpl + Jinja2) vs programmatic (python-docx)
  - Reading edge cases: headers/footers, nested tables, tracked changes, split runs, embedded objects
  - Common failure points: malformed XML, broken image .rels, style ID vs name confusion
  - Image embedding with aspect ratio calculation, ZIP validation
- **Key capabilities:**
  - Diagnose "Word found unreadable content" errors by checking for unescaped `&`/`<`, mismatched tags
  - Fix broken images by repairing `.rels` relationship IDs
  - Embed images as `io.BytesIO` bytes to avoid temp file I/O failures
- **Cross-references:** `html_css_generation` (document structure), `image_processing` (image embedding)

### `html_css_generation/`
- **Name:** HTML & CSS Generation Guidelines
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\html_css_generation\SKILL.md` (521 lines)
- **Has references/:** Yes — `references/frontend_architecture.md`
- **Description:** Comprehensive frontend design system for Claude-generated HTML/CSS. Covers typography, color philosophy, layout, components, responsive design, HTML chunking, and anti-"AI slop" aesthetics.
- **Sections:**
  - Typography (Inter/Georgia system, full type scale table)
  - Color Palette Philosophy (single accent + neutrals + status colors, dark mode)
  - Layout & Spacing (max-widths, 4px base unit scale, CSS Grid/Flexbox)
  - Visual Components (cards, badges, buttons, tables, blockquotes, code blocks)
  - Information Architecture (cards vs tables vs lists vs callouts vs accordions)
  - Responsive Behavior (mandatory mobile media queries, non-negotiable)
  - Document Header & TOC (metadata badges, anchor-linked table of contents)
  - HTML Chunking Strategy (section-based chunk files for large HTML management)
  - Frontend Design Process (two-pass: token system → review → build)
  - Anti-Slop directive (avoid Inter/Arial defaults, purple-on-white gradients, predictable layouts)
  - Incremental Augmentation Protocol (never start over — inject into gaps)
  - LTHP Integration (Last-Touch Highlight for HTML edits)
- **Key capabilities:**
  - Complete CSS component library with consistent border-radius (8px/12px/999px), shadows, transitions
  - Mandatory mobile-responsive design at 768px and 480px breakpoints
  - Chunk-based HTML file management to avoid re-reading entire files on updates
  - Design token system before writing code (color, type, layout, signature element)
- **Cross-references:** `image_processing` (image inclusion), `study_guide_generation` (HTML output), `system_architecture` (subagent sync), LTHP protocol

### `image_processing/`
- **Name:** Image Processing
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\image_processing\SKILL.md` (31 lines)
- **Has references/:** No
- **Description:** Guidelines for handling unclear images, choosing extraction methods, and integrating images into HTML deliverables with descriptive naming.
- **Key capabilities:**
  - Unclear image protocol: name exactly which image is problematic, request clearer version — never fabricate content
  - Alternative extraction: high-capability vision AI (Claude) or Datalab pipeline
  - Descriptive naming convention: e.g., `alu-shift-operation-diagram.png` not `image1.png`
  - Mandatory inclusion in HTML study guides when Datalab has downloaded images
- **Cross-references:** `datalab_conversion` (image extraction), `html_css_generation` (image in HTML), `study_guide_generation` (visual priority rule)

### `modern_engineering/`
- **Name:** Modern Engineering (Karpathy Method)
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\modern_engineering\SKILL.md` (30 lines)
- **Has references/:** No
- **Description:** Three-layer architecture for 10x faster AI building. Treats AI models as statistical simulation circuits ("Ghosts") that must be managed through strict verification, not motivation.
- **Sections:**
  - Layer 1 (The Spec): Agile specking — interview before building, tight scope, precision mandates
  - Layer 2 (The Verifier): Set evaluation criteria upfront, use second AI as critic, pull external signals
  - Layer 3 (The Environment): System prompts, LLM knowledge base, custom skills, Always/Ask/Never guardrails
- **Key capabilities:**
  - Prevents "waterfall" prompting — break into small, verifiable steps
  - Ghost vs Animal metaphor: models cannot be motivated, only verified
  - Pre-tool hooks: Always Do / Ask First / Never Do triage
- **Cross-references:** `system_architecture` (compounding errors), `prompt_engineering` (system prompts), `skill-creator` (skill loop)

### `prompt_engineering/`
- **Name:** Prompt Engineering & Debugging
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\prompt_engineering\SKILL.md` (39 lines)
- **Has references/:** No
- **Description:** Core techniques for professional prompt generation, ambiguity resolution, reasoning transparency, and debugging failed prompts via self-extraction.
- **Key capabilities:**
  - Act as prompt engineering consultant — provide alternative wording and clarity improvements
  - Ambiguity protocol: stop, batch all questions, do not proceed until clear
  - Self-extraction debugging: ask the model what was ambiguous, extract lessons
  - XML Mechanical Trap: use structural system tags for mechanical adherence (conversational nudges are insufficient)
  - Bash command substitution fix: base64-encode multiline strings to prevent shell parsing errors
- **Cross-references:** `prompt_engineering_best_practices` (comprehensive techniques), `modern_engineering` (system prompts)

### `prompt_engineering_best_practices/` ⬅️ LARGEST SKILL (783 lines)
- **Name:** Prompting Best Practices
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\prompt_engineering_best_practices\SKILL.md` (783 lines)
- **Has references/:** No
- **Description:** Authoritative Anthropic reference for prompt engineering across all current Claude models. Three-part structure: model-specific guidance → techniques for all models → migration considerations.
- **Section Map:**

| Section | Line | Covers |
|---|---|---|
| **Claude Fable 5** | 22 | Dedicated prompting page; effort levels, instruction following, memory systems, `reasoning_extraction` refusals |
| **Prompting Claude Opus 4.8** | 26 | Response length, effort/thinking-depth calibration, subagent control, frontend defaults |
| **General Principles** | 30 | Clarity & directness, context/why, few-shot examples (3-5 in `<example>` tags), XML tag isolation, role setting, long-context structuring (data at top/query at bottom), model self-knowledge |
| **Output & Formatting** | 199 | Verbosity control, tell-what-to-do-not-what-not-to, LaTeX, document creation, **prefilled response migration** (replaced by structured outputs) |
| **Tool Use** | 325 | Action vs suggestion (`<default_to_action>`), parallel calling optimization, overtigger tuning for Opus 4.6+ |
| **Thinking & Reasoning** | 404 | Adaptive thinking (`thinking: {type: "adaptive"}`) vs extended thinking (`budget_tokens` — deprecated), effort parameter (low/medium/high/max), overthinking prevention, interleaved thinking, self-check prompting |
| **Agentic Systems** | 487 | Multi-context window workflows, context awareness (token budget tracking), state tracking (JSON+git), autonomy/safety balance, research & information gathering, **subagent orchestration** (Opus 4.6 overuses — dial back), prompt chaining, anti-overengineering, anti-hard-coding, hallucination minimization (`<investigate_before_answering>`) |
| **Capability-Specific** | 709 | Vision (crop tool for zoom), frontend design (anti-"AI slop" aesthetic, distinctive typography, dominant colors, motion) |
| **Migration** | 763 | Sonnet 4.5→4.6, effort default change, adaptive thinking migration path, anti-laziness dial-back |

- **Key capabilities:**
  - **Model-specific:** Each Claude generation (Fable 5, Opus 4.8, Opus 4.6/4.5, Sonnet 4.6, Haiku 4.5, older models) has different prompting requirements — adaptive vs extended thinking, prefill support, aggressiveness tuning
  - **Technique catalog:** 14 named techniques (Golden Rule, explain-the-why, few-shot, XML isolation, role setting, long-context, tell-what-to-do, action-vs-suggestion, parallel calling, thinking calibration, subagent delegation, anti-overengineering, hallucination minimization, output format control)
  - **Migration recipes:** Concrete before/after code for prefill removal, extended→adaptive thinking migration, anti-laziness dial-back
  - **Frontend anti-slop:** Full system prompt snippet for distinctive design (avoid Inter/Roboto, purple-on-white, predictable layouts)
  - **Agentic system scaffolding:** Multi-context window workflows with state files, context awareness prompts, subagent orchestration guidance
- **Cross-references:** `prompt_engineering` (core techniques), `modern_engineering` (verifier), `system_architecture` (subagents), `html_css_generation` (frontend prompting)

### `skill-creator/`
- **Name:** Skill Creator
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\skill-creator\SKILL.md` (485 lines)
- **Has references/:** Yes — `references/schemas.md`; bundled agents: `agents/analyzer.md`, `agents/comparator.md`, `agents/grader.md`; assets: `assets/eval_review.html`; eval-viewer: `eval-viewer/generate_review.py`, `eval-viewer/viewer.html`
- **Description:** Full lifecycle tool for creating, testing, evaluating, and packaging skills. Implements a rigorous draft → test → evaluate → iterate loop with quantitative benchmarking.
- **Sections:**
  - Capture Intent — interview user to extract precise behavior, trigger conditions, output format
  - Write SKILL.md — frontmatter (name + description for triggering), progressive disclosure (<500 lines), writing patterns (imperative form, examples)
  - Test Cases — 2-3 realistic prompts saved to `evals/evals.json`
  - Run & Evaluate — spawn parallel with-skill and baseline subagents, draft assertions, grade, aggregate
  - Eval Viewer — `generate_review.py` for qualitative human review + quantitative benchmark
  - Iterate — generalize from feedback, keep lean, explain the why, bundle repeated scripts
  - Description Optimization — 20 trigger eval queries, run_loop.py for automated description refinement
  - Packaging — `package_skill.py` to produce .skill file
- **Key capabilities:**
  - Complete eval framework: spawn with-skill + baseline in parallel, grade assertions, aggregate benchmark
  - Blind A/B comparison between skill versions
  - Description optimization via trigger accuracy evals (should-trigger + should-not-trigger queries)
  - Cowork/headless support via `--static` HTML output
- **Cross-references:** `prompt_engineering_best_practices` (prompt crafting in skills), `system_architecture` (parallel subagent evals), `modern_engineering` (verification loop)

### `study_guide_generation/`
- **Name:** Study Guide Generation
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\study_guide_generation\SKILL.md` (37 lines)
- **Has references/:** No
- **Description:** Rules for generating complete HTML study guides and exam banks from course slides. Mandates content completeness, visual integration, and critical question analysis.
- **Key capabilities:**
  - Content completeness: embed actual slide content, not just summaries or question banks
  - Visual priority: integrate downloaded images per image-processing protocol
  - Critical subagent prompts: require critical thinking, answer evaluation, evidence-based escalation of wrong answers
  - Format: HTML with full style guide, document header with metadata badges, TOC with anchor IDs
  - Workflow ordering: Datalab pipeline (image download) before HTML generation; subagent analysis at Message 2-3, not Message 1
- **Cross-references:** `html_css_generation` (HTML output), `image_processing` (image inclusion), `datalab_conversion` (slide extraction)

### `system_architecture/`
- **Name:** System Architecture
- **File:** `C:\Users\marwa\antigravity\subagents playing around\.agents\skills\system_architecture\SKILL.md` (30 lines)
- **Has references/:** No
- **Description:** Rules for safe subagent orchestration, error mitigation, and structural limits. Addresses compounding errors that accumulate over long AI reasoning loops.
- **Key capabilities:**
  - Continuation Prompts: drop accumulated noise, extract verified clean state, restart from anchor — preferred over looping
  - DAG execution: Step A → Step B → Step C with no looping back (alternative when continuation is impossible)
  - Prerequisites before parallelization: formulate plan first, verify parallelizability, check partial-view risk — never parallelize uncertainty
  - Fail-fast: abandon parallelization immediately if subagents produce bad work
  - Append-only delta logs for safe parallel edits (no direct parallel DOM edits)
  - Blind execution ban: read script source (`sys.argv`, `argparse`) before running
- **Cross-references:** `modern_engineering` (verifier layer), `prompt_engineering_best_practices` (subagent orchestration), `skill-creator` (parallel evals)
