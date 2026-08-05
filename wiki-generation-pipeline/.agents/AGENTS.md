# Data Engineering Wiki Pipeline — Agent Kernel

**This pipeline's sole purpose is markdown file conversion and enrichment under `updates/`.**

---

## Root Directory Map
A `README.md` exists at `C:\Users\marwa\OneDrive\Documents\data engineering\README.md`. Read it first at session start. Update it when adding major new directories.

## Skill Load Efficiency — Pre-Check opencode.json

Before calling ANY skill via the `skill` tool, check `opencode.json` `instructions` field — files listed there are already in context. Calling `skill` for them wastes tokens.

**Currently injected via `opencode.json`:**
- `.agents/rules/websearch.md` — web search protocol
- `.agents/AGENTS.md` — this file
- `.agents/skills/index_integrity/SKILL.md` — index integrity enforcement
- `.agents/skills/md_converter/SKILL.md` — content enrichment protocol
- `.agents/skills/parallel_transcript_processor/SKILL.md` — parallel transcript orchestration
- `.agents/rules/activelearning.md` — active learning rule

**Never call `skill()` for these three** — they are already in context: `Markdown Content Converter & Enricher`, `Index Integrity Enforcer`, `Parallel Transcript Processor`.

## Web Research Policy

Before modifying ANY instruction file under `.agents/` (AGENTS.md, rules, skills, workflows), execute a web search for current best practices on the topic — required searches are documented in Pipeline Config Manager Step 2d.

## Core Processing Engine
Uses the **Large File Protocol** skill (`.agents/skills/large_file_protocol/SKILL.md`) for 5-phase extraction. Load via skill tool when processing large files. See `.agents/skills/` for available domain skills.

---

## CRITICAL MANDATE — Web Search Before Every Enrichment

**THIS IS THE MOST VIOLATED RULE. VIOLATION = BREACH.**

Every `[ENRICHED: ...]` tag MUST be verified via live web retrieval first — either an open-ended web search or, per RULE 0 in `md_converter`'s `<web_search_verification_mandate>` (injected via `opencode.json`), a targeted re-fetch (crawled this session) of an authoritative URL carried by a prior enrichment. Training data alone is NEVER sufficient. Read the mandate before any content work.

## Content Enrichment Mandate — md_converter Skill

Before ANY content enrichment under `updates/`:

1. **Use `md_converter` and `index_integrity` directly** — both are injected via `opencode.json`; do NOT call `skill` (see Skill Load Efficiency).
2. **Execute the full 9-step instruction sequence** from the md_converter skill.
3. **Run the 5-link verification chain** before presenting any output. If verdict is REVISE or REJECT, fix and re-run.

**Consequence:** Producing enriched Markdown without loading these skills first is a BREACH.

## Parallelization Mandate — DEFAULT BEHAVIOR

**Parallelization is the default operating mode.** Whenever 2+ tasks have no data dependency between them, you MUST run them in parallel using the `task` tool. Sequential processing of independent tasks is a BREACH.

**Rules:**
1. **Default to parallel.** If 2+ tasks have no data dependency between them, spawn them as concurrent subagents in a single message. Do not process them one after another.
2. **Only go sequential when there is a real dependency.** If Task B requires the output of Task A to proceed, then sequential is correct. If there is no dependency, parallel is mandatory.
3. **Batch size: up to 10 concurrent tasks per message.** If you have 15 independent files to create, spawn 10 in the first message, then 5 in the second after the first batch completes.
4. **Use the `task` tool with `subagent_type: "general"`** for content processing tasks. Each subagent gets one self-contained task with all context embedded in the prompt.
5. **Never pair or merge independent tasks into one agent** to "save on agent count" — this serializes what should be parallel and wastes time.
6. **Every task-tool subagent gets a realistic time budget at spawn time** (computed per the Time-Budget & Timeout Policy in the Parallel Transcript Processor skill). Over-budget or inactive subagents are stopped cooperatively and resumed from their on-disk state (task_id in-session, fresh spawn cross-session) — never silently re-run. Partial files are never indexed or shipped. Standalone (non-parallel) enrichment sessions are NOT budgeted.

**Triggers that MUST be parallel:**
- Multiple transcript segments to enrich
- Multiple quiz questions to convert to files
- Multiple files to create from independent source content
- Multiple skills to modify (when edits don't overlap)
- Any batch operation the user requests

**Triggers that must stay sequential:**
- File A must exist before File B can reference it
- Index must be read before writing a new entry
- Output of one analysis feeds into the next

## Transcript Content Detection Rule

When user input matches 2+ of these signals, classify it as transcript content and activate the full md_converter protocol:

- 3+ paragraphs of technical content
- Timestamps, speaker labels, or lecture-style prose
- Data engineering concepts (pipelines, databases, ETL, etc.)
- Course/module context provided
- Spoken-language patterns (filler words, sentence fragments)

**When triggered:** STOP — do not create a file yet. Execute Steps 0-9 from the md_converter skill. Do NOT paraphrase or summarize.

## Content Automation Rule

When the user asks a **clarifying question** about a concept in any file under `updates/`:

1. **Update the relevant MD file** with the explanation inline — do NOT just answer in chat.
2. **Briefly confirm in chat** what you added and where (one line).

Chat-only content explanations are a BREACH. The MD file is the permanent knowledge base.

---

## Subdirectory Organization Mandate

When placing files under `updates/providers/`:

| Content type | Location |
|-------------|----------|
| Video transcripts, readings, deep dives | `modules/module_N_name/lessons/` |
| Labs, hands-on exercises | `modules/module_N_name/labs/` |
| Practice quizzes, graded quizzes, weaknesses, exam prep | `quizzes/` at course root |
| Summaries | `summaries/` at course root |

**Thresholds:**
- General subdirectories within `lessons/` or `labs/`: require **3+ files** of that type
- Technology-specific lab subdirectories (`labs/db2/`, `labs/mysql/`): require **2+ files** of that technology
- Module root must only contain: `index.md`, `lessons/`, `labs/`, `summaries/`
- Course root must only contain: `index.md`, `modules/`, `quizzes/`, `summaries/`, `indexes/`, `assets/`

## Eliminate Redundancy (Cross-Linking Mandate)

Before creating any new file under `updates/`:

1. Check all relevant `index.md` files for existing entries covering the same topic
2. Write a descriptive Summary in the index — vague summaries are invalid
3. Cross-link related entries with `See also: [file.md]` references
4. Update indexes in the same session — deferred updates are stale

## Lab Type Categorization

Group labs by technology: `labs/db2/`, `labs/mysql/`, `labs/postgresql/`, etc. Create a technology subdirectory when **2+ lab files** of the same type exist. Maintain an `index.md` in each technology subdirectory.

## Index Integrity Mandate

Before ANY file creation, modification, movement, or deletion under `updates/` or `de_wiki/`, execute the **Index Integrity Enforcer** skill's full 6-link chain. This is the single most important operational rule — index drift is the most common and costly failure mode. The skill is injected via `opencode.json` — use it directly, do not call `skill`.

---

## PDF Input Mandate — Convert-Then-Enrich Pipeline

When a PDF is provided as input, follow this pipeline before enrichment:

1. **Detect and Classify** — identify PDF path, determine target course/module/subdirectory. Check if same-stem `.md` already exists.
2. **Convert with Datalab** — load `datalab_core` and `datalab_conversion` skills, run conversion:
   ```python
   from datalab_sdk import DatalabClient, ConvertOptions
   client = DatalabClient()
   options = ConvertOptions(output_format="markdown", mode="balanced", paginate=False)
   result = client.convert("<pdf_path>", options=options)
   result.save_output("<output_stem>", save_images=True)
   ```
3. **Organize images** — create `assets/` subdir, rename `{hash}_img.{ext}` to `c{course#}_m{module#}_{topic}_{descriptor}.{ext}`, update `![](...)` references.
4. **Feed into enrichment** — load `md_converter` skill, treat converted MD as source input, execute full 9-step sequence.
5. **Final placement** — follow Index Integrity Enforcer 6-link chain, place file in correct module directory, update indexes.

**Batch mode:** Run `python scripts/convert_pdfs.py` for bulk conversion, then process each `.md` through enrichment.

**Fallback:** If Datalab unavailable, use agent's native Read tool for text-only extraction. Note: `[ENRICHED: images — Datalab unavailable; images not extracted from PDF. Original PDF at <path>]`.

## Quiz File Formatting Mandate

When creating/updating quiz files under `updates/`, each question MUST have:

1. **Question text** — exact wording from source
2. **Options table** — every option with ✓ or ✗ marker
3. **Correct Answer** — explicit: "Answer: [correct option text]"
4. **Analysis enrichment** — why correct is correct, why others are incorrect

```markdown
## Question 1
**Which of the following is not a scenario that might require backup and restore?**
| Option | Correct? |
|--------|----------|
| **When a new user logs in** | **✓ CORRECT** |
| Transfer data from one database to another | ✗ |
**Answer:** When a new user logs in
[ENRICHED: analysis — ...]
```

**Rules:** Never omit the correct answer. Use options table format. Preserve original question wording.

## Auto-Create Quiz Files Rule

When the user provides quiz/exam content, **automatically create the enriched MD file** without being asked. Do not just answer in chat — create the file immediately.

**File naming:** `c{course#}_m{module#}_{quiz-type}_{topic-slug}.md` in `quizzes/` directory. Quiz types: `practice_quiz`, `graded_quiz`, `weakness`, `exam`.

**Required actions:** Identify quiz → read indexes → create enriched MD → place in `quizzes/` → update indexes → answer questions.

## Quiz Answering Protocol — Source-First Approach

Before answering quiz questions:

1. **Search enriched MD files** — grep key terms across the course directory for matching content
2. **Answer from evidence** — use enriched content to determine correct answers
3. **Post-answer verification** — if wrong, immediately update the relevant MD file with missing knowledge

Your enriched files are the single source of truth. If you can't answer from them, the enrichment is incomplete.

---

## Processing Flow

1. **Incoming updates file** → received into pipeline
2. **If a course index with detailed timings is detected** → execute Course Index Automation Triggers (study plan sync → Todoist update)
3. **Large File Protocol skill invoked** → phases 0–4: reconnaissance → spine → extraction → cross-reference → output mapping
4. **HTML Generation** → Phase 5 renders wiki markdown into self-contained HTML

---

# Non-Core Operations (Watered Down)

*The following sections are secondary to the wiki enrichment purpose. For full details, load the referenced skills.*

## New Course Registration — Auto-Fetch

When user says "I'm starting course X" or provides a Coursera `/learn/` URL:

1. Extract course slug from URL
2. Load `coursera_tracker` skill (`.agents/skills/coursera_tracker/SKILL.md`)
3. Fetch `https://www.coursera.org/learn/{slug}` via `webfetch`
4. Parse HTML for module structure, register course
5. Confirm captured data to user. Note: lesson-level content is behind paywall — provide manually.

## Todoist Capacity Management — 6-Week Rolling Window

Todoist project limited to 300 tasks. Only **6-8 weeks** loaded at any time. Overflow stored in `.agents/todoist_overflow_plan.json`. When current window's end is within 7 days, load next batch from overflow. Use incremental approach — never delete-and-recreate.

## Delayed Items File Mandate

Single master file at `updates/delayed_items.md` tracks ALL delayed/backlogged items. **Overwrite only, never append.** Check on session start, report unscheduled items. Update in real-time during content operations.

## Course Index Automation Triggers

When a course index with detailed timings is detected:

1. **Study Plan Sync** — load `study_plan_ai_agent_updater.md` to update hour estimates
2. **Todoist Plan Update** — load `todoist_tasks` skill to regenerate schedule

## Solving Problems — Todoist Context

When user provides a Todoist URL: fetch project → fetch sections → fetch ALL tasks (one call, limit=300) → fetch comments → fetch notes → then act. After changes, add comment describing what was done and implementation state.

## System File Modification Mandate

Before ANY modification of files under `.agents/` or `opencode.json`, load the **Pipeline Config Manager** skill via `skill(name: "Pipeline Config Manager")` and execute its workflow. This supersedes `activelearning.md`'s "edit directly" instruction for `.agents/` files.

**Scope:** AGENTS.md, rules, skills, workflows, root-level files, `opencode.json`.

**Anti-Context-Bloat Mandate:** Any system-file modification must pass the Pipeline Config Manager's Anti-Context-Bloat Audit (Step 2e): no redundant additions, prefer edit over add and on-demand over every-session placement, and clean existing bloat in the edited file. Injected instructions total ~39,500 tokens/session (measured 2026-08-05) — growth must be justified, not decorative.

**Consequence:** Modifying system files without loading Pipeline Config Manager first is a BREACH.
