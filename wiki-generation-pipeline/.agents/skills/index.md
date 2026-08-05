# Skills Index
*Last updated: 2026-08-05*

## Purpose
Master reference for all skills under `.agents/skills/`. Read this first to identify which skill to invoke for any given task. Each entry links to the full `SKILL.md` and notes whether the skill has bundled reference files that must be fetched (per Ground-Truth Enforcement) rather than generated from memory.

---

## Quick-Reference Table

| Directory | Name | Size | Has refs/ | When to Use |
|---|---|---|---|---|
| `anthropic_product_knowledge/` | Anthropic Product Knowledge | 79 lines | Yes | User asks about Claude Code, Claude API, Claude.ai plans, pricing, or capability questions |
| `data_architecture/` | Data Architecture & Algorithms | 19 lines | No | Designing database schemas, graph vs relational decisions, dependency traversal |
| `datalab_conversion/` | Datalab Document Conversion | 157 lines | Yes | Converting PDFs/images/docs to Markdown with image extraction and embedding |
| `datalab_core/` | Datalab Core SDK | 47 lines | Yes | Starting any Datalab workflow — install, auth, client init, error handling |
| `datalab_extraction/` | Datalab Structured Extraction | 49 lines | Yes | Extracting structured JSON from invoices, forms, or images with a schema |
| `datalab_form_filling/` | Datalab Form Filling | 27 lines | No | Filling blank PDF forms with mapped field data |
| `datalab_pipelines/` | Datalab Pipelines | 49 lines | Yes | Chaining convert + extract + segment into async pipelines |
| `coursera_tracker/` | Coursera Course Tracker | 199 lines | Yes (scripts/) | Tracking Coursera course progress, modules, scores; robots.txt-compliant safety layer; adaptive learning pathways |
| `docx_creation/` | docx_creation | 74 lines | No | Generating, editing, or extracting .docx files programmatically |
| `html_css_generation/` | HTML & CSS Generation Guidelines | 521 lines | Yes | Building HTML/CSS from scratch, designing frontends, creating visual reports |
| `image_processing/` | Image Processing | 31 lines | No | Handling unclear images, naming conventions, integrating into HTML |
| `modern_engineering/` | Modern Engineering (Karpathy Method) | 30 lines | No | Setting up agent workflows, defining specs, creating verification loops |
| `prompt_engineering/` | Prompt Engineering & Debugging | 39 lines | No | Crafting system prompts, resolving ambiguity, debugging failed prompts |
| `prompt_engineering_best_practices/` | Prompting Best Practices | 783 lines | No | Writing production prompts for Fable 5/Opus 4.8/Sonnet 4.6, thinking config, tool use, agentic systems, migration |
| `opencode_skill_authoring/` | opencode Skill Authoring Guide | 197 lines | No | opencode-exclusive: writing, creating, improving, restructuring, or renaming opencode skills — description crafting, trigger optimization, progressive disclosure, creation workflow, quality checklist |
| `skill-creator/` | Skill Creator | 485 lines | Yes | Creating, testing, evaluating, and packaging new skills (Anthropic eval harness — tooling-dependent, use opencode_skill_authoring for opencode-native guidance) |
| `study_guide_generation/` | Study Guide Generation | 37 lines | No | Generating HTML study guides, exam banks, question analysis from course slides |
| `system_architecture/` | System Architecture | 38 lines | No | Orchestrating subagents, preventing compounding errors, parallelization decisions; subagent time-budget pointer (enforcement lives in parallel_transcript_processor) |
| `todoist_api/` | Todoist REST API v1 | 328 lines | No | Integrating with Todoist, automating task management, building Todoist-powered tools, querying/manipulating Todoist data via REST or Sync API |
| `todoist_tasks/` | Todoist Task Architect | 748 lines | No | Todoist Task Architect brain.md-style prompt for managing the Data Engineer Study Plan Todoist project. Load via `skill` tool when creating/closing/updating Todoist study plan tasks. |
| `opencode_core_concepts/` | opencode Core Concepts | 50 lines | No | "what is opencode", "how does opencode work", architecture, Plan vs Auto, conceptual overview |
| `opencode_cli_commands/` | opencode CLI Commands & Flags | 664 lines | No | "how to run opencode", specific command usage, CLI flags, piped input, CI/CD integration |
| `opencode_configuration/` | opencode Configuration Reference | 458 lines | No | "opencode.json", "configure opencode", config field reference, setup questions |
| `opencode_tools_catalog/` | opencode Tools Catalog | 246 lines | No | "which tool", tool parameters/behavior, custom tools, tool selection |
| `opencode_rules_permissions/` | opencode Rules & Permissions | 103 lines | No | "permissions", "rules", "block a tool", security, Always/Ask/Never, policies |
| `opencode_agents_subagents/` | opencode Agents & Subagents | 107 lines | No | "subagent", "which agent type", delegation, task tool, agent configuration |
| `opencode_models_providers/` | opencode Models & Providers | 160 lines | No | "model", "provider", "API key", "which model", pricing/provider-specific setup |
| `opencode_tui_customization/` | opencode TUI & Customization | 183 lines | No | "TUI", "keyboard shortcut", "theme", "keybinding", "/command", "@mention", file viewer |
| `opencode_integrations/` | opencode Integrations | 116 lines | No | "MCP", "ACP", "LSP", "GitHub", "IDE", "VS Code", "JetBrains", "SSH", "Share", "Server" |
| `opencode_skills_framework/` | opencode Skills Framework | 66 lines | No | "how skills work", "create a skill", "SKILL.md format", "trigger matching", "customize-opencode" |
| `opencode_troubleshooting_advanced/` | opencode Troubleshooting & Advanced | 200 lines | No | "error", "troubleshoot", "debug mode", "Windows/WSL", "enterprise", "plugin", "SDK", "verifier" |
| `opencode_decision_trees/` | opencode Decision Trees | 291 lines | No | "best way to", "which approach", "what's the optimal", strategic decisions, scenarios |
| `opencode_agent_instructions_guide/` | opencode Agent Instructions Guide (AGENTS.md) | 220 lines | No | "adjust your AGENTS.md", "update your instructions", "change how you behave", "modify AGENTS.md", "edit your agent file", or any AGENTS.md/CLAUDE.md writing questions |
| `pipeline_config_manager/` | Pipeline Config Manager | 370 lines | No | ANY intent to change, add, remove, or reconfigure ANY system file under .agents/ — including AGENTS.md, rules, skills, workflows, root-level files, opencode.json, registers, or injection templates. Also triggers for config audits, token budget analysis, or "what's currently loaded?" |
| `diagnosis/` | Diagnosis | 67 lines | No | "diagnosis", "diagnose", "what went wrong", "why did you fail", "troubleshoot", any indication that a diagnosis is needed, or agent-detected rule violations |
| `parallel_transcript_processor/` | Parallel Transcript Processor | ~976 lines | No | Orchestrating parallel processing of multi-transcript files — splits transcripts via AI-assisted boundary detection, spawns 5-10 concurrent subagents each following md_converter enrichment protocol, orchestrator owns all index coordination via append-only delta pattern. Enforces permanent Time-Budget & Timeout Policy (budget + caps + cooperative stop + resume)
| `context_bloat_audit/` | Context Bloat Auditor | 93 lines | Yes | Auditing/measuring/reducing always-injected instruction load; "is the context too big"; justifying any growth to opencode.json `instructions` or injected files. Runs measurement script + 5-check audit + evidence lookup before any `.agents/` enlargement |

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
- **File:** `C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\.agents\skills\datalab_conversion\SKILL.md` (157 lines)
- **Has references/:** Yes — `references/document_conversion.md`
- **Description:** Converts PDFs, images, and documents to Markdown via the Datalab SDK. Extracts images from PDFs, saves them to an `assets/` subdirectory, and rewrites markdown `![]()` paths so images are embedded at correct positions with proper relative paths. Handles image-heavy PDFs with accurate mode and chart understanding extras.
- **Key capabilities:**
  - Output formats: markdown, html, json, chunks
  - Modes: fast (default), balanced, accurate; page range (0-indexed); chart understanding extra
  - **Image extraction and embedding** — extracts base64 images from `result.images`, saves to `assets/` subdirectory, rewrites `![]()` markdown references to correct relative paths
  - `process_conversion_images()` helper function for complete image processing pipeline
  - Conversion options table for image-heavy PDFs (mode, paginate, extras recommendations)
  - Fallback path when Datalab is unavailable (text-only extraction with enrichment log note)
  - Supports both local file and URL input
- **Cross-references:** `datalab_core` (required SDK init), `datalab_pipelines` (chaining), `image_processing` (downloaded images), `md_converter` (downstream enrichment handles pipeline naming convention)

### `datalab_core/`
- **Name:** Datalab Core SDK
- **File:** `C:\Users\marwa\OneDrive\Documents\data engineering\wiki-generation-pipeline\.agents\skills\datalab_core\SKILL.md` (47 lines)
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

### `coursera_tracker/`
- **Name:** Coursera Course Tracker
- **File:** `wiki-generation-pipeline\.agents\skills\coursera_tracker\SKILL.md` (199 lines)
- **Has references/:** Yes — `scripts/` directory with `safety.py` (robots.txt enforcement), `schema.py` (data models), `tracker.py` (core class), `robots.txt` (cached Coursera rules), `test_tracker.py` (20-test suite)
- **Description:** Local-first Coursera course progress tracker with robots.txt enforcement. Tracks completed modules, pending tasks, scores, and adaptive learning pathways. Respects Coursera's robots.txt — only accesses publicly allowed `/learn/`, `/specializations/`, and `/professional-certificates/` paths. No API access, no authentication, no restricted endpoints.
- **Sections:**
  - Safety Layer — `RobotsTxtGuard.validate(url)` checks every URL against cached robots.txt before any fetch; blocks `/api/`, `/lecture/`, `/account/`, `/search`; logs all attempts to `data/access_log.json`
  - Schema — `CourseMetadata`, `CourseRecord`, `ModuleRecord`, `ModuleStatus` (pending/in_progress/completed/skipped), `ProgressReport`; all JSON-serializable with round-trip `to_dict()`/`from_dict()`
  - Core Class — `CourseraTracker` with `fetch_progress()`, `update_status()`, `validate_access()`, `register_course()`, `suggest_next()`, `export_report()`, `export_json()`
  - Persistence — Auto-save on every change to `data/progress.json`; cross-instance state recovery
- **Key capabilities:**
  - Enforces Coursera robots.txt for ClaudeBot — merged `*` baseline with agent-specific rules; Allow overrides Disallow for specific paths (e.g., `/api/utilities/v1/imageproxy`)
  - Self-reported progress tracking with timestamps, scores, and notes per module
  - Smart next-module suggestions: in-progress first, then pending in registration order
  - Markdown and JSON export for chat, files, or Todoist sync integration
  - 20-test validation suite covering guard, schema, tracker, persistence, and error handling
- **Cross-references:** `todoist_tasks` (sync progress to Todoist), `todoist_api` (API integration patterns), `system_architecture` (local state management)

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
- **Cross-references:** `system_architecture` (compounding errors), `prompt_engineering` (system prompts), `opencode_skill_authoring` (skill creation loop)

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

### `opencode_skill_authoring/`
- **Name:** opencode Skill Authoring Guide
- **File:** `.agents/skills/opencode_skill_authoring/SKILL.md` (197 lines)
- **Has references/:** No
- **Description:** opencode-exclusive, practical, opinionated guide for writing SKILL.md files that trigger reliably, load efficiently, and produce better outputs. Built specifically for opencode's skill system — NOT for Claude Code, Codex, Antigravity Gemini, or other agents.
- **Sections:**
  - Skill Anatomy — directory structure, frontmatter (name + description), body (<500 lines), bundled resources (scripts/, references/, assets/), three-level progressive disclosure
  - Writing the Description — how opencode trigger matching works, the "pushy" description philosophy, description formula and template, good vs bad description examples
  - Writing the Body — six writing principles (explain-the-why, keep lean, imperative form, generalize from feedback, bundle repeated work, principle of lack of surprise), content patterns (output format templates, examples, domain organization, cross-references)
  - Creation Workflow — five-step process: capture intent → draft → test (2-3 prompts) → iterate → finalize
  - Quality Checklist — ten-point pre-ship verification
  - Improving Existing Skills — read first, preserve name/directory, identify the problem, apply checklist, update index
  - Updating the Skills Index — mandatory post-creation step for `.agents/skills/index.md`
- **Key capabilities:**
  - "Pushy" description formula that prevents the #1 failure mode (under-triggering)
  - Progressive disclosure architecture: metadata (always) → body (on trigger) → resources (on demand)
  - Six skill writing principles distilled from production skill-creation workflows
  - Concrete description template with good vs bad examples
  - Ten-point quality checklist for pre-ship verification
  - Explicitly opencode-scoped — NOT for Claude Code, Codex, Antigravity, or Gemini
- **Cross-references:** `opencode_skills_framework` (system reference), `prompt_engineering_best_practices` (prompt crafting), `modern_engineering` (verification loops), `opencode_agent_instructions_guide` (AGENTS.md interaction)

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
- **Cross-references:** `opencode_skill_authoring` (opencode-native creation guide), `prompt_engineering_best_practices` (prompt crafting in skills), `system_architecture` (parallel subagent evals), `modern_engineering` (verification loop)

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
- **File:** `wiki-generation-pipeline\.agents\skills\system_architecture\SKILL.md` (38 lines)
- **Has references/:** No
- **Description:** Rules for safe subagent orchestration, error mitigation, and structural limits. Addresses compounding errors that accumulate over long AI reasoning loops.
- **Sections:**
  - Continuation Prompts: drop accumulated noise, extract verified clean state, restart from anchor — preferred over looping
  - DAG execution: Step A → Step B → Step C with no looping back (alternative when continuation is impossible)
  - Prerequisites before parallelization: formulate plan first, verify parallelizability, check partial-view risk — never parallelize uncertainty
  - Fail-fast: abandon parallelization immediately if subagents produce bad work
  - Subagent Time-Budget & Timeout Policy (reference-only pointer): budgets/caps/cooperative-stop/resume doctrine; enforcement lives in `parallel_transcript_processor`
  - Append-only delta logs for safe parallel edits (no direct parallel DOM edits)
  - Blind execution ban: read script source (`sys.argv`, `argparse`) before running
- **Cross-references:** `modern_engineering` (verifier layer), `prompt_engineering_best_practices` (subagent orchestration), `opencode_skill_authoring` (parallel evals), `parallel_transcript_processor` (time-budget enforcement owner), `context_bloat_audit` (compounding-errors/bloat doctrine)

### `todoist_api/`
- **Name:** Todoist REST API v1
- **File:** `wiki-generation-pipeline\.agents\skills\todoist_api\SKILL.md` (328 lines)
- **Has references/:** No
- **Description:** Complete reference for the Todoist REST API v1 and Sync API. Covers authentication (personal tokens, OAuth, DCR, refresh tokens), all REST endpoints (Tasks, Projects, Sections, Comments, Labels, Reminders, Workspaces, etc.), Sync API for batch read/write, pagination, webhooks, request limits, error handling, the Todoist CLI, and MCP server setup.
- **Sections:**
  - Authentication — personal tokens, OAuth code flow, refresh tokens (rotation, 60s grace window, replay detection), DCR (RFC 7591), OAuth Client ID Metadata Documents, token revocation
  - REST Endpoints — 90+ endpoints across 14 resource groups with methods, paths, and parameters
  - Sync API — batch read/write, resource types, commands, temp_id/uuid, incremental sync, response/error format
  - Pagination — cursor-based pagination with `limit` and `cursor` parameters
  - Due Dates & Deadlines — full-day, floating, timezoned formats; deadline objects
  - Error Handling — REST error format (`error_tag`, `error_code`, `error_extra`) and Sync API command errors
  - Todoist CLI — install, auth, quick add, task/project list, shell completions, agent skill installation
  - Todoist MCP — setup for Claude, Cursor, VS Code; response format with `structuredContent`
- **Key capabilities:**
  - Complete REST endpoint inventory with correct HTTP methods and paths
  - Sync API command types and resource field schemas for all major objects
  - OAuth refresh token lifecycle including rotation, grace window, and replay detection
  - CLI agent skill installation (`td skill install <agent>`) for coding agents
  - MCP server URL (`https://ai.todoist.net/mcp`) with client setup for 4 platforms
- **Cross-references:** `prompt_engineering` (API integration patterns), `system_architecture` (subagent task management)

### `todoist_tasks/`
- **Name:** Todoist Task Architect
- **File:** `wiki-generation-pipeline\.agents\skills\todoist_tasks\SKILL.md` (748 lines)
- **Has references/:** No
- **Description:** Todoist Task Architect brain.md-style prompt for managing the Data Engineer Study Plan Todoist project. Includes dynamic study plan loading, progress log cross-reference, full course resource index (IBM URLs + supplement links for all 16 courses + enhancements A–I), task creation templates, 4-block daily structure, brain directives (Name the Loss, Minute-Rule, Monthly Review, Weekly Schedule Update), and practitioner tips embedded across courses 1–16. Load this via the `skill` tool when the user wants to create/close/update study plan tasks on Todoist.
- **Sections:**
  - Role Definition — Todoist Task Architect with brain module mandate
  - Auto Feedback Loop — automatic prompt evolution on user corrections
  - User Preferences — 20+ codified rules covering structure, pacing, capacity, content, cleanup, process
  - Context — fixed credentials, 15 section IDs, absolute file paths
  - Phase 0a–0c — Load study plan, progress log, and Todoist state
  - Phase 1–5 — Cross-reference, Plan, Execute, Log, Deliver
  - Course Resource Index — all 16 IBM course URLs + supplement URLs
  - Task Structure Template — parent-subtask hierarchy with hour derivation rules
  - Constraints — 22 brain-enforced rules (incremental-only, time derivation, redundancy elimination)
  - Brain Directives — Eternal Vigilance, Hostile-Reader, Name the Loss, Momentum Check, Breach Invalidation
  - Practitioner Tips — embedded across courses 1–16
  - Known Failure Modes — 12+ cataloged bugs (PID variable, pagination, date formatting, rate limiting, etc.)
- **Key capabilities:**
  - Complete Todoist task lifecycle: create/close/update/move with parent-subtask hierarchy
  - 3-source cross-reference (study plan → progress log → Todoist state) before any mutation
  - Incremental diff-based cleanup — never delete-and-recreate
  - Rule 22 pre-creation check: 5-step validation before every task creation
  - Time derivation from actual course content — never guessed hours
  - Auto-feedback loop that codifies user corrections as permanent rules
- **Cross-references:** `todoist_api` (REST API implementation), `system_architecture` (subagent task management), AGENTS.md (Todoist Capacity Management section)

### `opencode_core_concepts/`
- **Name:** opencode Core Concepts
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_core_concepts\SKILL.md` (50 lines)
- **Has references/:** No
- **Description:** Foundational understanding of opencode — architecture, Plan vs Auto modes, session lifecycle, project structure, and how skills/rules/instructions/agents/tools relate.
- **Sections:** What is opencode, Architecture, Two Operational Modes, Project Structure, Skills vs Rules vs Instructions vs Agents comparison table, How Skills Work overview, Tips
- **Key capabilities:** Explains opencode's stateless architecture, mode switching, and the role of each mechanism (instructions/rules/skills/agents/MCP). Entry point for learning opencode.
- **Cross-references:** All other `opencode_*` skills

### `opencode_cli_commands/`
- **Name:** opencode CLI Commands & Flags
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_cli_commands\SKILL.md` (664 lines)
- **Has references/:** No
- **Description:** Complete reference for every opencode CLI command and flag. Covers main entry point, global flags, all 12 commands (init, config, run, plan, execute, install, publish, check, completion, mcp, ssh, update), piped input, formatters, and CI/CD integration.
- **Key capabilities:** Every command with signature, all flags, usage examples. Shell completion setup. CI/CD exit codes and JSON output for pipeline integration. Largest single command reference.
- **Cross-references:** `opencode_configuration` (config command), `opencode_tui_customization` (TUI launch), `opencode_decision_trees` (output format selection)

### `opencode_configuration/`
- **Name:** opencode Configuration Reference
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_configuration\SKILL.md` (458 lines)
- **Has references/:** No
- **Description:** Complete reference for opencode.json/opencode.jsonc — every configuration field with type, description, behavioral implications, and examples. Covers $schema, instructions, system_prompt, tools allow/deny, models, agents, hooks, notifications, custom_keys, theme, keybindings, rules, skills, permissions, network, mcp_servers, output_formats, and more.
- **Key capabilities:** Full annotated config example. Detailed field reference for 20+ fields with behavioral notes. ENV_VAR interpolation for secrets. Thinking/effort configuration.
- **Cross-references:** `opencode_cli_commands` (config command), `opencode_rules_permissions`, `opencode_models_providers`, `opencode_agents_subagents`, `opencode_integrations` (MCP), `opencode_tui_customization`

### `opencode_tools_catalog/`
- **Name:** opencode Tools Catalog
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_tools_catalog\SKILL.md` (246 lines)
- **Has references/:** No
- **Description:** Complete reference for all 12 built-in opencode tools — bash, read, edit, write, glob, grep, web_search, web_fetch, task, question, todowrite, skill. Every parameter with schema, when-to-use guidance, behavioral rules, multi-tool workflow patterns, and custom tools via MCP.
- **Key capabilities:** Exact parameter schemas for all tools. Single-tool selection matrix. Multi-tool workflow sequences (e.g., "fix a bug" = grep→read→edit→bash). Custom tool definition format.
- **Cross-references:** `opencode_configuration` (tool config), `opencode_rules_permissions` (tool permissions), `opencode_agents_subagents` (task tool), `opencode_decision_trees` (selection guidance)

### `opencode_rules_permissions/`
- **Name:** opencode Rules & Permissions
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_rules_permissions\SKILL.md` (103 lines)
- **Has references/:** No
- **Description:** Complete reference for opencode's security model — Always/Ask/Never rule types, .opencode/rules/ directory structure and file format, rule inheritance and matching algorithm, permission modes (bypass/non-bypass/default/rules-based), fine-grained permission flags, policy files, and permission groups.
- **Sections:** Purpose, Rule Types (table), Rule File Format (annotated YAML), Rule Directory Structure, Rule Inheritance & Matching, Permission Modes, Fine-Grained Flags, Policy Files, Permission Groups, Evaluation Order
- **Key capabilities:** Rule matching algorithm (most specific wins, most restrictive wins). Policy file format with conditions. Permission groups for bulk tool management. Evaluation order chain.
- **Cross-references:** `opencode_configuration` (permissions config), `opencode_tools_catalog` (tool perms), `opencode_troubleshooting_advanced` (permission errors)

### `opencode_agents_subagents/`
- **Name:** opencode Agents & Subagents
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_agents_subagents\SKILL.md` (107 lines)
- **Has references/:** No
- **Description:** Complete reference for opencode's subagent architecture — all 7 built-in agent types (general, code, architect, explore, debug, frontend, ask), their code names, default tool access, configuration in opencode.json, the task tool handoff protocol, --subagent CLI flag usage, agent-specific instructions, and concurrency.
- **Sections:** Overview, Built-in Agent Types (detailed table), Agent Configuration (annotated JSON), Subagent Handoff Protocol, --subagent CLI Flag, Agent Concurrency, Agent-Specific Instructions, Tool Restrictions per Agent
- **Key capabilities:** Default tool access per agent type. Task tool handoff protocol (step-by-step). Agent configuration with model refs and skills. Per-agent tool overrides.
- **Cross-references:** `opencode_configuration` (model refs), `opencode_tools_catalog` (task tool), `opencode_models_providers` (per-agent model selection), `opencode_skills_framework`, `opencode_decision_trees`

### `opencode_models_providers/`
- **Name:** opencode Models & Providers
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_models_providers\SKILL.md` (160 lines)
- **Has references/:** No
- **Description:** Complete reference for all supported AI providers — Anthropic, OpenAI, Google/Gemini, AWS Bedrock, Azure OpenAI, GCP Vertex AI, Ollama (local), OpenRouter, and custom OpenAI-compatible endpoints. Covers model config fields, thinking/effort parameters, provider-specific authentication, model selection strategy, and fallback configuration.
- **Sections:** Model Configuration, Model Config Fields, Provider Reference (9 providers with config snippets), Model Selection Strategy (table), Fallback Models, Model Picker in TUI
- **Key capabilities:** All 9 provider config templates. Thinking (adaptive/enabled/disabled) and effort (low/medium/high/max) explained. Selection strategy table by criterion (reasoning/speed/cost/context/offline). Fallback model chain.
- **Cross-references:** `opencode_configuration` (models config), `opencode_agents_subagents` (per-agent model), `opencode_decision_trees` (model decisions)

### `opencode_tui_customization/`
- **Name:** opencode TUI & Customization
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_tui_customization\SKILL.md` (183 lines)
- **Has references/:** No
- **Description:** Complete reference for opencode's terminal UI — screen layout, all / commands (help, plan, task, clear, model, setting, theme, export, save, undo, redo, diff, file, search, copy, quit), @ mentions (file, web, url, issue, pr, diff, selection, clipboard), keyboard navigation (30+ keybindings including vim mode), model picker, file viewer, diff view, settings panel, scrollback, multi-block editing, theme format (20+ tokens), and keybinding configuration.
- **Sections:** Screen Layout, / Commands table, @ Mentions table, Keyboard Navigation table (30+ bindings), Vim Keybindings, Model Picker, File Viewer, Diff View, Settings Panel, Themes (built-in + custom JSON format with all tokens), Keybinding Configuration JSON
- **Key capabilities:** Complete theme token reference (background, foreground, status_bar, file_viewer with syntax tokens, diff colors, chat colors). Full keybinding JSON format with custom_keys. Vim mode toggle.
- **Cross-references:** `opencode_configuration` (theme/keybinding config), `opencode_cli_commands` (startup), `opencode_models_providers` (model picker)

### `opencode_integrations/`
- **Name:** opencode Integrations
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_integrations\SKILL.md` (116 lines)
- **Has references/:** No
- **Description:** Complete reference for connecting opencode to external systems — MCP server configuration (SSE and stdio transports), ACP agent-to-agent communication, LSP language intelligence, GitHub integration (PR review, issues, Actions workflow YAML), IDE plugins (VS Code, JetBrains), opencode Share, opencode Server, SSH remote sessions, and Zen mode.
- **Sections:** MCP (config + CLI + tool interface), ACP (discovery, message passing, delegation), LSP, GitHub, IDE (VS Code + JetBrains), Share, Server, SSH, Zen Mode
- **Key capabilities:** Full MCP server config with both transport types. Sample GitHub Actions workflow. VS Code extension usage. Server startup with TLS. SSH remote session flags.
- **Cross-references:** `opencode_cli_commands` (mcp, ssh commands), `opencode_configuration` (mcp_servers), `opencode_agents_subagents` (ACP), `opencode_tools_catalog` (MCP tools)

### `opencode_skills_framework/`
- **Name:** opencode Skills Framework
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_skills_framework\SKILL.md` (66 lines)
- **Has references/:** No
- **Description:** Complete reference for opencode's skills system — what skills are, YAML frontmatter anatomy, trigger matching mechanism, skill location convention, loading via config, built-in customize-opencode skill, and comparison with protocols.
- **Sections:** What is a Skill?, Skill Anatomy, Trigger Matching, Skill Location Convention, Built-in customize-opencode Skill, Creating a Skill, Skill Testing, Skills vs Protocols
- **Key capabilities:** Trigger matching explanation (semantic matching against description field). customize-opencode built-in skill behavior. Skill testing via `opencode check --skills`. Differentiation between skills and protocols.
- **Cross-references:** `opencode_core_concepts` (ecosystem overview), `opencode_configuration` (skills array), `opencode_cli_commands` (check command), `opencode_skill_authoring` (creating, writing, and improving skills)

### `opencode_troubleshooting_advanced/`
- **Name:** opencode Troubleshooting & Advanced Features
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_troubleshooting_advanced\SKILL.md` (200 lines)
- **Has references/:** No
- **Description:** Complete reference for diagnosing opencode issues — API errors (401/429/500), token limits, tool failures (edit oldString not found, write not read first, bash permission denied), config validation, network/proxy, Windows/WSL specifics, debug mode, recovery. Also covers Verifier (test runner), Network config, Enterprise (audit log, SSO, RBAC, usage reporting), plugins, and SDK.
- **Sections:** API Errors table, Token Limits solutions, Tool Failures table, Config Validation Errors, Network Issues, Windows/WSL Specific Issues, Session Hangs/Slow Performance, Debug Mode, Recovery Procedures, Verifier (test runner config), Network Configuration, Enterprise Features (Audit Log, SSO, RBAC, Usage Reporting), Plugins, SDK, Ecosystem
- **Key capabilities:** Complete error→cause→solution tables. Windows/WSL path/line-ending/PowerShell specifics. Verifier test runner with auto_fix and on_failure policy. Enterprise RBAC roles config. SDK programmatic usage example.
- **Cross-references:** `opencode_configuration` (network, verifier config), `opencode_rules_permissions` (enterprise RBAC), `opencode_integrations` (ecosystem), `opencode_cli_commands` (verbose, config validate), `opencode_tools_catalog` (tool errors)

### `opencode_decision_trees/`
- **Name:** opencode Decision Trees — Best Approach Selector
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_decision_trees\SKILL.md` (291 lines)
- **Has references/:** No
- **Description:** Structured decision logic for choosing the optimal opencode approach for any task. 9 decision trees: Mode Selection (Plan vs Auto vs opencode run), Agent Selection (which of 7 agent types), Tool Selection (which tool + workflow sequences), Instructions Strategy (AGENTS.md vs rules vs skills vs inline vs scripts vs agent instructions), Integration Decision (MCP vs ACP vs GitHub vs IDE vs SDK vs SSH vs LSP), Model Selection (Opus vs Sonnet vs Haiku vs GPT vs Gemini vs Ollama), Permission Strategy (bypass vs non-bypass vs rules vs flags), Output Format Selection (terminal vs json vs markdown vs html vs edit), Error Recovery Tree. Plus a Common Scenarios Quick-Reference table mapping 15+ user requests to recommended approaches.
- **Sections:** All 9 decision trees with scenario tables + Common Scenarios Quick-Reference
- **Key capabilities:** Scenario→approach mapping for every major decision. Workflow patterns for common tasks (e.g., "automate weekly report" → create opencode run script + cron). Permission strategy by risk level. Error recovery diagnostic tree. 15+ common scenarios answered instantly.
- **Cross-references:** All other `opencode_*` skills (consumes their content in decision form)

### `opencode_agent_instructions_guide/`
- **Name:** opencode Agent Instructions Guide (AGENTS.md)
- **File:** `wiki-generation-pipeline\.agents\skills\opencode_agent_instructions_guide\SKILL.md` (220 lines)
- **Has references/:** No
- **Description:** Guide for opencode itself on how to customize and update its own AGENTS.md file. Primary trigger is when the user tells opencode to "adjust your AGENTS.md", "update your instructions", "change how you behave", "modify AGENTS.md", or "edit your agent file". Covers project conventions, build/test/lint commands, architecture overview, behavioral rules, writing effective instructions, file locations and precedence, opencode.json configuration for glob-pattern instruction files, behavioral patterns (session-start mandates, verification steps, escalation rules, naming conventions), maintenance tips, minimal starter example, and pipeline-specific instructions.
- **Sections:** What Goes in AGENTS.md, Writing Effective Instructions (specific/actionable table, hierarchical structure, external file references), File Locations & Precedence, Using opencode.json to Include More Files (glob patterns, remote URLs), Behavioral Patterns (session-start mandates, verification steps, escalation rules, naming convention enforcement), Maintenance Tips, Minimal Starter Example, Pipeline-Specific Example, Key Takeaway
- **Key capabilities:** Complete AGENTS.md authoring guide. File precedence chain (project → Claude fallback → global → global fallback). Glob pattern support in opencode.json instructions field. Session-start mandate pattern for hard behavioral rules. Verification/escalation pattern templates.
- **Cross-references:** `opencode_core_concepts` (instructions vs skills vs rules), `opencode_configuration` (opencode.json instructions field), `opencode_skills_framework` (skills vs instructions), `AGENTS.md` (this project's own agent file)

### `pipeline_config_manager/`
- **Name:** Pipeline Config Manager
- **File:** `wiki-generation-pipeline\.agents\skills\pipeline_config_manager\SKILL.md` (370 lines)
- **Has references/:** No
- **Description:** Meta-skill for modifying ANY system file under .agents/. Loads on ANY natural-language intent to change behavioral instructions, rules, mandates, skills, workflows, root-level files, opencode.json, registers, or injection templates. Enforces a rigid 5-step workflow with deep opencode.json integration: plan mode entry → config state analysis (reads opencode.json, catalogs instructions, estimates tokens) + web research → structured plan-agent prompt (three mandatory fields: operation+target, context+config state, demand) → **orchestrator-subagent adversarial debate** (orchestrator self-critique → independent position generation → bidirectional cross-critique → structured rebuttal with concede/rebut → convergence verification with deadlock escalation) → clarifying questions + final implementation plan with both-analyses presentation and resolution trail.
- **Sections:** System File Taxonomy (9 file types with load mechanisms, indexes, blast radius), Trigger Conditions (9 intent categories), Mandatory 5-Step Workflow (Step 1: Enter Plan Mode, Step 2: Analyze opencode.json Config State + Step 2d: Web Research, Step 3: Write Structured Prompt, Step 4: Orchestrator-Subagent Adversarial Debate with self-critique/independent positions/cross-critique/rebuttal/convergence verification, Step 5: Clarifying Questions + Return Final Plan with both-analyses presentation), Decision Tree (compressed to indented lists), Blast Radius Framework
- **Key capabilities:**
  - Handles ALL system file types: AGENTS.md, rules, skills, workflows, root-level files, injection templates, registers, opencode.json
  - Mandatory opencode.json config state analysis before every modification (token budget, instruction ordering, config impact)
  - Three-field structured prompt format with config state included in Context
  - **Orchestrator self-critique** — orchestrator must critically analyze its own demand before engaging the sub-agent, producing position + known weaknesses + pre-emptive responses
  - **Independent position generation** — both parties reason independently before seeing each other's output, preventing anchoring bias (uncorrelated context windows)
  - **Bidirectional cross-critique** — both orchestrator and sub-agent challenge each other's positions with specificity, not just sub-agent critiques orchestrator
  - **Structured rebuttal protocol** — every challenge must be addressed with CONCEDE (and revise) or REBUT (with specific evidence from rules/skills/config)
  - **Convergence verification** — requires all challenges resolved, both parties agree on exact change, no open questions; deadlock after 2 rounds escalated to user
  - Final deliverable includes both analyses with resolution trail (where they agreed, where they disagreed, what each conceded)
  - Blast radius framework for assessing session-wide impact of config changes
  - Expanded decision tree routing to 9+ file type destinations
- **Cross-references:** `opencode_skill_authoring` (skill body creation), `opencode_agent_instructions_guide` (AGENTS.md editing), `opencode_configuration` (config field reference), `opencode_skills_framework` (skill system mechanics), `index_integrity` (if changes affect content under updates/)

### `diagnosis/`
- **Name:** Diagnosis
- **File:** `wiki-generation-pipeline\.agents\skills\diagnosis\SKILL.md` (67 lines)
- **Has references/:** No
- **Description:** Diagnostic analyst skill for identifying WHY instructions were not followed. Triggers on any user indication that something went wrong, any request for diagnosis/troubleshooting, or agent-detected rule violations. Produces structured diagnosis entries written to `dumps/diagnosis_dump.md` for the pipeline-fixing AI to consume. Focuses on systemic root causes and permanent fixes, not instance-specific patches. No file names in diagnoses — general and structural only.
- **Sections:** Activation triggers, Diagnosis Protocol (6 steps: Identify Failure, Name Rule, Root Cause Analysis, Systemic Diagnosis, Write to Dump, Confirm to User), Constraints (no file names, no blame, permanent fixes only, write the dump)
- **Key capabilities:**
  - Triggers on any form of "diagnosis", "what went wrong", "why did you fail", or agent self-detected violations
  - 6-step structured diagnosis protocol with root cause analysis table
  - Outputs to `dumps/diagnosis_dump.md` in append-only mode
  - General, file-agnostic diagnoses designed for consumption by pipeline-fixing AI
  - Common root cause pattern library (classification failure, priority inversion, default behavior override, rule overload, missing trigger, ambiguous rule, no enforcement checkpoint)
- **Cross-references:** `pipeline_config_manager` (for implementing proposed fixes), `activelearning` (for rule modifications based on diagnosis findings)

### `parallel_transcript_processor/`
- **Name:** Parallel Transcript Processor
- **File:** `wiki-generation-pipeline\.agents\skills\parallel_transcript_processor\SKILL.md` (~976 lines)
- **Has references/:** No
- **Description:** Orchestration skill for parallel processing of multi-transcript files. Splits a single file containing multiple video transcripts, readings, articles, and labs into individual segments using AI-assisted boundary detection. Spawns 5-10 subagents concurrently via the `task` tool, each processing one segment through the md_converter enrichment protocol. Orchestrator owns ALL index coordination via append-only delta pattern — subagents are pure content producers that never touch index files. Handles batch processing with fail-fast rules, error recovery, rollback protocol, and post-completion verification. Enforces a permanent Time-Budget & Timeout Policy: every subagent gets a realistic budget, enrichment cap, and live-search cap at spawn; over-budget/inactive subagents are stopped cooperatively and resumed from their on-disk state, never silently re-run.
- **Sections:**
  - Activation Self-Check — standard transcript detection triggers
  - Role — Parallel Transcript Processor Orchestrator (coordinator, not content producer)
  - Task — 6-phase workflow: parse → index pre-allocate → spawn → batch execute → verify
  - Parsing Protocol — AI-assisted segment splitting with boundary detection signals, metadata extraction, validation rules
  - Index Coordination Protocol — append-only delta pattern (Link 1-4 pre-allocation, atomic batch apply, Link 6 verification)
  - Time-Budget & Timeout Policy (Phase 1.7) — budget formula, caps, stop conditions, stop & resume mechanics, fail-fast on timeouts
  - Subagent Task Template — exact prompt template with budget fields, index integrity override, md_converter protocol reference, directory setup, expected output format, cooperative self-stop (Step 9)
  - Batch Processing — 5-10 concurrent subagents, batch lifecycle, result categorization, inter-batch index application, continuation decision
  - Error Handling — 8 failure modes (empty result, partial write, wrong path, timeout, index modified, context compaction, index update fail, parsing error), rollback protocol
  - Verification — file existence + completion-marker check, sentence count verification, index integrity final check, final report
  - Index Integrity Override — explicit instruction to subagents to skip all index operations
  - Directory Organization — pre-spawn directory verification, subagent directory instructions
  - Orchestrator Quick Reference — phase sequence, key numbers, decision table, subagent prompt checklist
- **Key capabilities:**
  - Deterministic segment parsing via AI boundary detection with confidence scoring
  - Zero index race conditions via orchestrator-owned append-only delta coordination
  - Batch concurrency (5-10) with fail-fast (2+ failures = halt) and sequential fallback
  - Permanent Time-Budget & Timeout Policy: 15-min base + write + search terms; enrichment cap max(25, ceil(words/150)) ≤ 60; 25-search sub-cap; inactivity gate; task_id resume in-session / fresh-spawn cross-session
  - Complete error handling with rollback protocol for catastrophic failures
  - Post-completion verification: file existence + extraction-checklist marker, sentence coverage, index integrity
  - Subagent task prompt template with budget fields and index integrity override (subagents skip all index ops)
- **Cross-references:** `md_converter` (enrichment protocol for subagents), `index_integrity` (orchestrator follows full 6-link chain), `system_architecture` (append-only delta execution pattern, fail-fast rule, time-budget pointer), `context_bloat_audit` (growth of this injected skill is audited before enlargement), `opencode_agents_subagents` (task tool handoff protocol, agent type selection)

### `context_bloat_audit/`
- **Name:** Context Bloat Auditor
- **File:** `wiki-generation-pipeline\.agents\skills\context_bloat_audit\SKILL.md` (93 lines)
- **Has references/:** Yes — `references/context_bloat_evidence.md` (36 live-verified sources, 6 evidence groups), `scripts/measure_context_load.ps1`
- **Description:** Evidence-backed audit of the pipeline's always-injected instruction load (opencode.json `instructions` + injected skill files). Triggers on any request to audit, measure, or reduce context bloat, or to justify adding/enlarging an instruction file. Runs the measurement script (per-file bytes/lines/words/tokens, delta vs baseline), the 5-check audit (redundancy, token-delta, instruction-density, cleanup obligation, placement preference — aligned with Pipeline Config Manager Step 2e), evidence lookup, and produces an Anti-Bloat Verdict. Pairs with Pipeline Config Manager for any `.agents/` or opencode.json modification.
- **Sections:**
  - Activation Self-Check — audit triggers vs content-work exclusion
  - Role — Context Bloat Auditor (injected load ≈ 39,500 tokens/session, taxed on every session and subagent)
  - Audit Workflow — 5 steps: MEASURE (script), 5-CHECK AUDIT, CONSULT EVIDENCE, VERDICT, ENFORCE & PERSIST
  - Lean Doctrine — operational thresholds table (load cap, effective context, density, prefix stability, position, compaction survival)
  - Self-Mandate — stay lean; expand evidence file, not this skill
- **Key capabilities:**
  - One-command load measurement with per-file token estimate and delta vs baseline
  - 5-check audit producing a required Anti-Bloat Verdict before any `.agents/` growth
  - Evidence base of 36 live-verified sources across 6 groups (degradation, instruction-following, economics, compaction, real-world failures, design doctrine)
  - Prompt-cache-safe guidance (stable prefix, no date banners in injected files)
- **Cross-references:** `pipeline_config_manager` (mandatory companion for system-file changes), `md_converter` + `index_integrity` + `parallel_transcript_processor` + AGENTS.md + websearch.md + activelearning.md (the injected set it audits), `system_architecture` (compounding errors)


