## PIPELINE EXECUTOR — v1.0

You are a pipeline executor. Read this entire message, then execute the steps below in order. Do not ask for confirmation. Do not propose alternatives. Do not pause to reflect. If you hit an ambiguity, pick the most common interpretation and proceed.

**Rules:**
- Always read the current file on disk before writing to it
- Log every phase completion to `de_wiki/log.md` immediately
- File paths are valid — use them directly
- Return a structured summary of what you did

---

### Lock File

At start: If `.quiz_pipeline_running` does not exist, create it (empty file).
At end: Run `Remove-Item -LiteralPath "wiki-generation-pipeline/.quiz_pipeline_running"` even if a phase fails.

---

## STEP 1: READ ALL INDEX FILES

Goal: Read every index file across the entire project to understand (a) what content structure exists, (b) what's already been processed, (c) what protocols/skills will be needed.

### 1.1 — Discover all index files

Search the entire project tree for files matching `*index*`. Read each one.

Expected index files (verify existence on disk — do not assume):

**Pipeline structure indexes:**
- `pipeline/stage_prompts/stage_index.md`
- `output/option_a/stage_prompts/stage_index.md`

**Course content indexes:**
- `updates/full-course-index.md`
- `updates/*module*-index.md` (any dated module index files)

**Wiki state indexes:**
- `de_wiki/index.md`
- `de_wiki/topics/course_syllabus_and_index.md`
- `useful side prompts/course1-index.txt`

**Protocol/skill catalog:**
- `.agents/AGENTS.md`
- `.agents/protocols/index.md` (if it exists)

**Any other file matching `*index*`** — read it too.

### 1.2 — Extract structural information from each index

For each index file found, record:

**What does it map?**
- Course modules → lessons → items
- Pipeline stages → protocol phases
- Wiki pages → content domains
- Updates files → module assignments

**What does it reveal about existing state?**
- Which `de_wiki/topics/*.md` files already exist
- Which updates files have already been processed (from log.md last entries)
- What's still pending (referenced in indexes but no topic file exists yet)

**What does it reveal about dependencies?**
- Which modules depend on which
- Which pipeline stages must run in sequence
- What content overlaps exist between updates files

### 1.3 — Determine the processing delta

Compare every item referenced in the course content indexes against:
- Existing files in `de_wiki/topics/`
- Last entries in `de_wiki/log.md`

The difference = what must be processed this session.

Also identify:
- Updates files that exist on disk but are NOT referenced in any index → UNCATEGORIZED
- Updates files referenced in indexes but NOT found on disk → MISSING (log and skip)
- Existing topic files that reference outdated or superseded content → mark for Phase 3 contradiction resolution

### 1.4 — Write the discovery summary

Write to `de_wiki/log.md`:
```
## [STEP 1] Index Discovery — COMPLETE
Index files read: [list each with its type: pipeline/course-content/wiki-state]
Processing delta: [N] new items to process across [M] updates files
Uncategorized files: [list]
Existing topic pages: [list]
Missing referenced files: [list, if any]
Content dependencies identified: [e.g., Module 2 sequential after Module 1]
Status: INDEXES READ — PROCEEDING TO CONTEXT LOADING
```

---

## STEP 2: CONTEXT LOADING

Load only what the indexes tell you is needed.

### 2.1 — Determine required protocols

Read `.agents/AGENTS.md` and/or `.agents/protocols/index.md` to see the full catalog. Select:

**Always-mandatory:**
- `.agents/protocols/large_files_protocol.md` — Core processing engine

**Session-relevant (evaluate based on what the course indexes revealed):**
- `PCOM_protocol.md` — Needed if the session ends with a git commit
- `IFMP_protocol_prompt.md` — Needed if writing/updating instruction files
- `PSM_protocol.md` — Needed if modifying stage prompts
- `SFBP_protocol.md` — Needed if modifying existing files
- `DOMP_protocol.md` — Needed if creating new directories
- Any others whose description matches this session's tasks

### 2.2 — Determine required skills

Read the skills catalog in AGENTS.md. Select based on what the course content indexes revealed:

**Always-mandatory:**
- `.agents/skills/html_css_generation/SKILL.md` — Required for Phase 5 HTML rendering

**Content-driven (select based on what the updates content covers):**
- `.agents/skills/study_guide_generation/SKILL.md` — Load if the course indexes reveal quiz/assessment content
- `.agents/skills/data_architecture/SKILL.md` — Load if content involves data architecture, data stores, big data
- `.agents/skills/docx_creation/SKILL.md` — Load if output format requires .docx
- Any other skill whose description matches the domains visible in the course indexes

### 2.3 — Load each file with existence verification

For every file identified above:
1. `(Get-Item <full_path>).Length` — verify file exists and is non-empty
2. Copy the COMPLETE verbatim content into this session
3. If file is missing or empty: log as MISSING and skip

### 2.4 — Log the session context inventory

```
## [STEP 2] Context Load — COMPLETE
Protocols loaded:
  - large_files_protocol.md [VERIFIED]
  - [others] [VERIFIED]
Skills loaded:
  - html_css_generation/SKILL.md [VERIFIED]
  - [others] [VERIFIED]
Reference files loaded:
  - aim.md (project scope)
  - AGENTS.md (protocol/skill catalog)
  - [index files] (read inline during Step 1)
Status: ALL LOADED, ALL VERIFIED
```

---

## STEP 3: PIPELINE EXECUTION

Execute the phases below sequentially. Each phase must pass its gate before the next begins.

### Phase 1 — Spine Pass

Read NEW content files sequentially, tracking coverage precisely, producing `de_wiki/spine.md`.

Reading mechanics:
- Read in chunk sizes appropriate to file density
- Process order: index-mapped content first, uncategorized second
- Log every completed chunk to `de_wiki/log.md` IMMEDIATELY
- If a tool call returns fewer lines than requested: stop, record shortfall, re-read, then log complete
- NEVER skip a chunk based on judgment

Per-chunk output in spine.md:
```
### Chunk [N] — File: [filename], Lines [X]–[Y]
Content type(s): [from Section 3 classification]
Primary themes: [2–4 bullets]
Flags: [OFF-TOPIC] / [CONTRADICTION] / [SUPERSEDED] / [DEPRECATED] / [DENSE]
Independence: [INDEPENDENT / DEPENDS ON / SEQUENTIAL-ONLY]
```

Phase 1 Gate:
- [ ] Every chunk has spine entry
- [ ] Every chunk logged as COMPLETE
- [ ] Line ranges arithmetically reconciled per file
- [ ] spine.md exists
- [ ] Oracle-DAG decision recorded in log.md

### Oracle-DAG Decision

Based on independence assessments in the spine: record in log.md whether Oracle-DAG parallelism is feasible.
- Course content is typically sequential (later modules depend on earlier)
- Quiz data may be independent and parallelizable
- Decision recorded in log.md with reasoning

### Phase 2 — Deep Extraction

Extract content from new chunks into `de_wiki/topics/`. Merge with existing topic files — do NOT overwrite.

Mandatory 4-Layer Analysis before extracting:
1. What is this chunk saying? (One sentence)
2. Which topic file? (Match existing or create new)
3. Specificity level? (High-level / specific detail / opinion / deprecated / exploratory / off-topic)
4. Cross-references? (Existing wiki pages this connects to)

Extraction rules from Section 7 of the Large File Protocol — apply in order.

Update `de_wiki/index.md` after each topic file write/update.

Phase 2 Gate:
- [ ] Every new chunk processed
- [ ] Every chunk accounted for per Section 3 disposition table
- [ ] All flagged items in contradictions.md as PENDING
- [ ] index.md current
- [ ] No `[REQUIRES VERIFICATION]` without contradictions.md entry

### Phase 3 — Cross-Reference Synthesis

Build connections between ALL wiki pages (old + new). Resolve contradictions.
Steps: directory audit → cross-ref audit → contradiction resolution → distribution check → gap audit → lint check

Phase 3 Gate:
- [ ] All cross-references in place; no orphan pages
- [ ] No PENDING contradictions (all RESOLVED or UNRESOLVED)
- [ ] Distribution check passed
- [ ] Gap audit complete
- [ ] Lint check passed
- [ ] log.md Phase 3 entry written

### Phase 4 — Output Mapping & Master Synthesis

Define output structure in `output_map.md`. Write `master_summary.md`.

Phase 4 Gate:
- [ ] output_map.md exists and covers all output sections
- [ ] master_summary.md complete
- [ ] All wiki pages mapped or logged as not relevant
- [ ] log.md Phase 4 entry written
- [ ] Source files unmodified
- [ ] No open `[REQUIRES VERIFICATION]` or `[PENDING]`

### Phase 5 — HTML Rendering

Render `de_wiki/` to `output/option_a/index.html`:
- Self-contained, inline CSS, no external dependencies
- Use the HTML/CSS generation skill loaded in Step 2

---

## PRE-HANDOFF CHECKLIST

- [ ] index.md on disk and current
- [ ] log.md has entries for all phases and chunk completions
- [ ] spine.md has entry for every chunk
- [ ] contradictions.md exists; no PENDING entries
- [ ] All topics/ files on disk and populated
- [ ] output_map.md covers all output sections
- [ ] master_summary.md complete
- [ ] No open `[REQUIRES VERIFICATION]` or `[STATUS: PENDING]`
- [ ] Unresolved contradictions listed in master_summary.md
- [ ] Source files unmodified
- [ ] No fabricated content
- [ ] HTML rendered and verified
- [ ] All VERIFIED tags passed

---

## POST-PIPELINE: DEPLOYMENT & COMMIT

### Output file
- `wiki.html` — self-contained single-file SPA (~4 MB, mermaid inlined)
- Written to **two locations** by `build_wiki.py`:
  1. `wiki-generation-pipeline/wiki.html` (project source)
  2. `index.html` at the **git repository root** (GitHub Pages entry)

Only the repo-root `index.html` needs committing. The stale `wiki.html` at repo root (if present) must be `git rm`'d — the build no longer writes it there.

### Commit scope
- Commit the entire `wiki-generation-pipeline/` directory
- No need to detail individual `.md` files in the `updates/` folder
- The commit message should include a **brief abstract** of what new content was added (2–4 short lines)

### Suggested commit message format
```
wiki: rebuild + [very short abstract of new content]

- e.g., "C1M3 summary: data collection, wrangling, wrangling tools"
- e.g., "C2M1 intro: data platforms, security, big data lifecycle"
```

### Abstract line conventions
One line per distinct content domain added, max 80 chars each:
```
New content — C1M3 Data Collection & Wrangling summary (gathering methods, transformation/cleansing, tool overview)
```

Keep it high-level. Never enumerate individual update filenames.

---

## GIT WORKFLOW

### Author identity
Maintain `git config user.name` and `user.email` matching the GitHub account
(`ahmedbelal22271-maker` / `ahmedbelal22271@gmail.com`) so commits are attributed
correctly. Check with `git config user.name && git config user.email`.

### What to stage (and what never to stage)

**Always stage:**
- `index.html` at repo root (GitHub Pages entry)
- `wiki-generation-pipeline/wiki.html`
- `wiki-generation-pipeline/wiki_template.html`
- `wiki-generation-pipeline/scripts/build_wiki.py`
- `wiki-generation-pipeline/useful side prompts/plan-mode.md`
- `wiki-generation-pipeline/useful side prompts/plan-mode-subagent.md`
- `wiki-generation-pipeline/de_wiki/.lthp_state.json`
- Any modified `de_wiki/topics/*.md`
- Any new `updates/*.md` files added this session
- `wiki-generation-pipeline/package.json` and `package-lock.json` (if deps changed)

**Never stage:**
- `node_modules/` — not tracked; do not `git add` it
- `wiki.html` at repo root — stale file; `git rm` to delete from tracking
- Random PDFs, unrelated directories, stray `.md` files at repo root

### Commit message format

First line: `wiki: rebuild + <abstract>`

Body (2-4 short lines, no file enumeration):
```
New content — <domain summary, e.g., C1M3 Data Collection & Wrangling>
<other structural changes, e.g., Sidebar hierarchy fix>
<other changes, e.g., Mermaid inlined for single-file offline use>
```

### After commit
Always push: `git push origin main`

---

## LOCK CLEANUP

After commit and push: `Remove-Item -LiteralPath "wiki-generation-pipeline/.quiz_pipeline_running" -ErrorAction SilentlyContinue`

Do this even if a phase failed — the lock must always be released.
