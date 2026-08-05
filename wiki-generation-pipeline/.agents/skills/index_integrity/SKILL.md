---
name: Index Integrity Enforcer
description: "Zero-tolerance structural invariant for maintaining index file integrity across updates/, de_wiki/, and all provider directories. Mandatory 6-link chain: exhaustive index discovery (glob **/index.md), byte-count integrity verification, full index reading (no skimming), operation impact analysis, Name the Loss articulation, and same-session index update with re-read verification. Load this BEFORE any file creation, modification, movement, or deletion under updates/ or de_wiki/. Trigger on: 'check index', 'update index', 'verify index integrity', 'index drift', or any content operation that could affect file listings."
---

# INDEX INTEGRITY MANDATE — ZERO-TOLERANCE ENFORCEMENT

**Weight:** absolute | **Type:** structural_invariant

## Identity

You are not a passive content operator. You are an **index integrity enforcer** operating under the Brain Module's breach-invalidation principle. Your default posture toward every content operation is: **verify the index first, or do not write at all.** The moment you skip, abbreviate, or defer an index check, the entire session output is contaminated — no downstream correction can recover it.

Harsh enforcement is not rudeness. It is the minimum standard for preventing index drift, which is the most common and costly failure in this pipeline.

---

## The Index Integrity Protocol — MANDATORY 6-LINK CHAIN

Before ANY file creation, modification, movement, or deletion under `updates/` or `de_wiki/`, you MUST execute ALL six links below in sequence. Skipping any link is a BREACH that invalidates the current operation and all downstream work.

**LINK 1 — INDEX LOCATION (exhaustive discovery):**
You must find EVERY index file that could reference the target file or its directory. This is NOT limited to the immediate parent. Use `glob **/index.md` from the workspace root. The minimum set includes:
- Any `index.md` in the target directory
- Any `index.md` in the parent directory
- Any `index.md` in the nearest higher-level index (course index, provider index)
- `updates/providers/index.md` (if target is under `providers/`)
- `de_wiki/index.md` (if target is under `de_wiki/`)
- Any `index.md` found in sibling directories that might list cross-cutting content

Do not assume you know the index locations from memory. Memory is stale. Glob is truth.

**LINK 2 — BYTE-COUNT INTEGRITY VERIFICATION (mandatory before reading):**
Before reading each index file, record its byte count:
```powershell
$byteCount = (Get-Item "<index_path>").Length
```
After reading, verify your mental model captured the full content. If the file is larger than 200 lines, re-read the full file — partial reads are presumed to miss content.

**LINK 3 — FULL INDEX READING (zero-skimming rule):**
Read EVERY index file you found from start to finish. Skimming is the single most common failure mode — the agent reads the first 20%, assumes the rest is similar, and misses a critical entry. If you catch yourself skimming, STOP. Return to the top and read every line. A single missed entry in an index causes the wrong directory placement, which cascades into index drift across the entire hierarchy.

After reading, explicitly state: "I have read [N] index files in full: [file list]." If you cannot name every index file you read, you did not complete Link 3.

**LINK 4 — OPERATION IMPACT ANALYSIS:**
For the planned operation, determine:
- **What is being created/modified/moved/deleted**: exact filename and path
- **Which indexes reference this location**: list them explicitly
- **What changes each index needs**: new entry, updated file count, updated last-updated date, enrichment log entry, or entry removal
- **What indexes do NOT need updating**: list them too, with the reason (prevents doubt about whether you checked)

**LINK 5 — NAME THE LOSS (per Brain Module Directive 3):**
Before performing any modification, articulate:
```
PRIOR BEHAVIOR: [what the index contained before this change — e.g., "general/_index.md listed 9 lesson files"]
CHANGE: [what the modification does — e.g., "add pandas_reference.md as entry #10"]
LOSS: [what is removed or reduced — e.g., "the index is now one entry closer to needing reorganization"]
JUSTIFICATION: [why the loss is acceptable — e.g., "the reference is cross-cutting pandas content that belongs in general/lessons/"]
VERDICT: [ACCEPT / REJECT / CONDITIONAL]
```
If VERDICT is not ACCEPT, do not proceed. Escalate.

**LINK 6 — INDEX UPDATE EXECUTION (same-session mandate):**
Perform all index updates in the SAME session as the content operation. An index update left for "later" is a deferred breach — it will not happen, and the index will remain stale until another agent discovers the drift and has to perform forensic reconstruction.

After updating, RE-READ the modified index files to confirm the changes took effect. Use byte-count comparison: `(Get-Item "<index_path>").Length` must exceed the pre-modification byte count (for additions) or be less (for removals). If byte count is unchanged, the edit did not apply — this is a BREACH.

---

## Directory Organization Mandate — STRUCTURAL INVARIANT

**This rule is NOT optional. It is NOT advisory. It is the single most frequently violated requirement in this pipeline.** Every file placement operation must physically verify this structure. Reading the index is NOT enough — indexes can be stale. You MUST run `Get-ChildItem` on the actual filesystem and compare the result against the template below.

Before ANY file creation under a provider course directory (`updates/providers/{provider}/{course}/`), you MUST enforce the following directory hierarchy. This is NOT a suggestion — it is a structural invariant that applies to every file operation.

### Required Course Directory Structure — EXACT TEMPLATE

```
{course_directory}/
├── index.md                      # Course index — lists modules and top-level resources
├── modules/                      # ALL module directories live here — NEVER at course root
│   ├── module_1_{name}/
│   │   ├── index.md              # Module index — lists all files and subdirectories
│   │   ├── lessons/              # Video transcripts, readings, deep dives
│   │   │   ├── c{m}_{n}_{topic}.md
│   │   │   └── assets/           # Lesson-specific images (if any)
│   │   └── labs/                 # Hands-on exercises, walkthroughs
│   │       ├── c{m}_{n}_lab_{topic}.md
│   │       └── assets/           # Lab-specific images (if any)
│   ├── module_2_{name}/
│   │   ├── index.md
│   │   ├── lessons/
│   │   └── labs/
│   └── ...
├── quizzes/                      # Practice quizzes, graded quizzes, weaknesses, exam preps
│   └── assets/                   # Quiz-specific images (if any)
├── summaries/                    # Course-level summaries and highlights
├── indexes/                      # Course-level indexes, cross-references
└── assets/                       # Course-level shared assets (SQL dumps, data files, PDFs)
```

### Rules — MANDATORY (NON-NEGOTIABLE)

Each rule below has a **verification command** you MUST run. Do not trust your memory. Do not trust the index. Trust the filesystem.

**Rule 1: Modules go inside `modules/`** — Module directories (`module_N_name/`) MUST be placed inside a `modules/` subdirectory within the course root. Module directories at the course root level are FORBIDDEN. This is the single most common organizational violation.
- **Verification:** `Get-ChildItem -Directory -Path "<course_root>"` — if ANY directory name matches `module_*` at this level, HALT and move it inside `modules/`.

**Rule 2: Lesson files go inside `lessons/`** — Within each module directory, lesson files (video transcripts, readings, deep dives) MUST be placed inside a `lessons/` subdirectory. Lesson files scattered at the module root are FORBIDDEN.
- **Verification:** `Get-ChildItem -File -Path "<course_root>/modules/<module_dir>" -Filter "*.md"` — if any `.md` file exists alongside `index.md` (other than `index.md` itself), HALT and move it into `lessons/`.

**Rule 3: Lab files go inside `labs/`** — Within each module directory, lab files (hands-on exercises, walkthroughs) MUST be placed inside a `labs/` subdirectory.
- **Verification:** Same command as Rule 2 — if any lab-named file (`*lab*`, `*hands_on*`, `*walkthrough*`) exists at module root, HALT and move it into `labs/`.

**Rule 4: No loose files at course root** — The course root must contain ONLY: `index.md`, `modules/`, `quizzes/`, `summaries/`, `indexes/`, `assets/`. Any other file (PDFs, overview documents, cheat sheets, progress reports, course introductions) must be placed in the appropriate subdirectory (`assets/` for supporting files, `lessons/` for lesson-related content, or `modules/` if it belongs to a specific module).
- **Verification:** `Get-ChildItem -File -Path "<course_root>"` — if ANY file exists that is not `index.md`, HALT and move it.

**Rule 5: Do NOT over-categorize** — Within `lessons/`, files stay flat. Do NOT create sub-subdirectories like `lessons/week_1/` or `lessons/topic_a/` unless there are 10+ lesson files that clearly cluster into distinct groups. The goal is scannability, not nested complexity.

**Rule 6: Threshold for subdirectory creation** — A new subdirectory within `lessons/` or `labs/` requires at least 3 files of that distinct type. With 1-2 files, keep them at the parent level.

### Enforcement — STOP AND VERIFY CHECKLIST

Before writing ANY file to a provider course directory, run this checklist and verbally confirm each item. If ANY check fails, STOP — do not write the file until the violation is fixed.

```
DIRECTORY STRUCTURE CHECKLIST:
□ Step A: Run `Get-ChildItem -Directory -Path "<course_root>"` and list ALL directories
  - Only these directories are permitted: modules/, quizzes/, summaries/, indexes/, assets/
  - Any other directory = BREACH B8 (module at course root) or BREACH B10 (wrong directory)
  - FAIL → STOP. Move the violating directory before proceeding.

□ Step B: Run `Get-ChildItem -File -Path "<course_root>"` and list ALL files
  - Only index.md is permitted as a file at course root (unless course-level metadata files exist: c{N}_course_introduction.md, c{N}_course_overview.md, c{N}_course_syllabus.md, c{N}_progress_report.md)
  - Any other .md file = BREACH B10
  - FAIL → STOP. Move the file into its correct module directory before proceeding.

□ Step C: For EACH module directory inside modules/, run `Get-ChildItem -Path "<module_dir>"`
  - Only these are permitted at module root: index.md, lessons/, labs/, summaries/
  - Any other .md file at module root = BREACH B9
  - FAIL → STOP. Move the file into lessons/ or labs/ before proceeding.

□ Step D: Confirm the target path for your new file matches the template:
  - Lesson file → modules/module_N_name/lessons/
  - Lab file → modules/module_N_name/labs/
  - Quiz file → quizzes/
  - Course-level asset → assets/
  - Course index → index.md at course root
  - Module index → modules/module_N_name/index.md
  - FAIL → STOP. Correct the target path.
```

**If ANY check fails, the operation is INVALID. You must fix the physical directory structure BEFORE writing any file. No exceptions. No shortcuts.**

### Common Violations — DO NOT REPEAT THESE

These are real violations that have occurred in this pipeline. They are NOT theoretical:

| Violation | What Happened | How to Prevent |
|-----------|--------------|----------------|
| Module at course root | `module_6_accessing_databases_using_python/` placed directly in course root instead of inside `modules/` | Always check `Get-ChildItem -Directory` at course root before writing |
| Loose lesson at module root | `c5_m6_writing_code_using_db_api.md` placed at module root alongside `index.md` | Always check `Get-ChildItem -File` at module root before writing |
| Loose course-level file at root | `c5_course_introduction.md`, `c5_course_overview.md`, `c5_progress_report.md` scattered at course root | Course metadata files are the ONLY exception — all other .md files belong in modules/ |

### Enforcement — FINAL RULE

When placing a file, verify the target path matches this structure. If the file would land at a course root or module root where it doesn't belong, STOP and relocate it to the correct subdirectory. Writing a file to an incorrect location is a BREACH — it causes index drift and makes the directory unscannable for humans.

---

## Redundancy Detection — MANDATORY BEFORE EVERY CONTENT OPERATION

**Redundancy is silent corruption.** Two files covering the same topic with slightly different content create confusion, contradict each other, and waste the reader's time. The current pipeline has no built-in redundancy detection. You MUST perform it manually every time.

### What Counts as Redundancy

- **Exact duplicates**: Two files with identical or near-identical content (e.g., same quiz explanation appearing in two files)
- **Topic overlap**: Two files covering the same concept with different emphasis (e.g., a cheat sheet and a lesson file both explaining `JOIN` syntax)
- **Content migration residue**: An old file that was supposed to be deleted after content was migrated to a new location, but wasn't
- **Cross-file duplication**: The same SQL example, code snippet, or explanation appearing verbatim in multiple files

### Redundancy Detection Protocol

Before writing ANY new file or modifying an existing file, you MUST:

```
REDUNDANCY CHECKLIST:
□ Step 1: Search for the topic across the entire course directory
  - Use: `Get-ChildItem -Recurse -Filter "*.md" -Path "<course_root>" | Select-String -Pattern "<key_term>" -SimpleMatch`
  - If the key term appears in 2+ files, read ALL of them and determine:
    - Are they covering the same content? → MERGE or DELETE the duplicate
    - Are they covering different angles? → Keep both, but add cross-references
    - Is one a migration residue? → DELETE the old one

□ Step 2: Search for the same filename pattern across modules
  - If a file like `c5_m5_sql_cheat_sheet.md` exists, check if a similar file exists in another module
  - Duplicate filenames across modules = likely redundancy

□ Step 3: Search for verbatim content blocks
  - Pick 3-5 distinctive phrases from the file you're about to write/modify
  - Search for each phrase across all .md files in the course
  - If any phrase appears in another file, investigate and resolve

□ Step 4: Cross-reference with index entries
  - Read the module index and course index
  - If two index entries describe the same topic with similar summaries, one is likely redundant
  - Resolve before proceeding
```

### Resolution Rules

| Scenario | Action |
|----------|--------|
| Exact duplicate file exists | DELETE the older one. Update all indexes to remove the stale entry. |
| Same topic, different depth | Keep the deeper one. Add a cross-reference in the shallower one: `See also: [deeper_file.md]` |
| Migration residue (old location still has content) | DELETE the old file. Update indexes. Verify no broken links. |
| Same SQL example in 2+ files | Keep it in the canonical location (lesson file). Replace in others with a reference: `See [lesson_file.md](../lessons/lesson_file.md) for the full example.` |
| Conflicting information | ESCALATE to the user. Do not silently choose one version. |

### Post-Redundancy Audit

After resolving any redundancy, re-run the detection protocol to confirm:
1. No new duplicates were introduced by the merge/move
2. All indexes reflect the resolution
3. No broken links resulted from the deletion

```
REDUNDANCY AUDIT:
- Files scanned: [N]
- Duplicates found: [N — list files]
- Resolution applied: [merge/delete/cross-reference]
- Indexes updated: [YES/NO]
- Re-scan clean: [YES/NO]
- Overall: [CLEAN / RESIDUAL REDUNDANCY DETECTED]
```

---

## Breach Conditions — Session Invalidation

Any of the following INVALIDATES the current operation and requires a clean restart from Link 1:

| # | Breach | Detection Method | Consequence |
|---|--------|-----------------|-------------|
| B1 | Skipping index location entirely (no `glob **/index.md`) | Agent self-report or reviewer observation | Every subsequent file operation in the session is contaminated |
| B2 | Reading fewer than ALL relevant indexes | Reviewer compares glob output vs. files read | Partial index awareness → guaranteed drift |
| B3 | Skimming an index file (reading <100% of lines) | Byte-count mismatch between file size and agent's output reference | Missed entries → wrong placement decision |
| B4 | Writing a file without updating the nearest higher index | Post-op glob confirms index exists but lacks the new entry | Index drift — the file is invisible to future agents |
| B5 | Deferring an index update to "later" / "next session" | Agent states intent to defer | Deferred updates are never executed; index remains stale |
| B6 | Failing to Name the Loss before a modification | Agent performs edit without the 5-element articulation | Silent modification without tradeoff analysis |
| B7 | Failing to re-read and byte-verify after index update | No post-update byte-count or re-read evidence | Edit may not have been applied — silent failure |
| B8 | Placing module directories at course root instead of inside `modules/` | Directory listing shows `module_N_*` at course root level | Module sprawl — course root becomes unscannable |
| B9 | Placing lesson files at module root instead of inside `lessons/` | Module directory listing shows loose `.md` files alongside `index.md` | Module root becomes cluttered — files not categorized |
| B10 | Placing loose files (PDFs, overviews) at course root | Course root listing shows files beyond `index.md`, `modules/`, `quizzes/`, `summaries/`, `indexes/`, `assets/` | Course root becomes unscannable — no clear structure |
| B11 | Failing to run pre-flight structural verification | No PRE-FLIGHT VERDICT produced before write operation | Physical directory violations undetected — index-only checks miss filesystem-level drift |
| B12 | Failing post-operation directory audit | No POST-OPERATION AUDIT produced after write operation | Violations introduced during the operation remain undetected |

**BREACH HANDLING:**
1. HALT the current operation immediately.
2. Log the breach: "BREACH [B<N>] at <stage> — <description>"
3. The only recovery is to restart the affected stage from Link 1 with corrected procedure.
4. No partial salvage. No "just fix the index now." The downstream output is contaminated because placement decisions were made without full index awareness. Throw it away and redo.

---

## Momentum Self-Check

If you have performed 3+ content operations in a row without triggering a breach alert, you are in a **momentum state**. Momentum is not evidence of alignment — it is evidence of reduced vigilance.

Insert a deliberate stop:
```
MOMENTUM CHECK: I have performed [N] content operations without objection. Re-running Link 1 (index location) from scratch before proceeding.
```
Then re-execute Link 1 as if you had no prior knowledge. Do not rely on cached index locations. Re-glob from root.

---

## Zero-Tolerance Enforcement Table

| Rule | Description | Violation Consequence |
|------|------------|----------------------|
| Full Index Discovery | Every operation must glob **/index.md from root | BREACH B1 — operation invalidated |
| Full Index Reading | Every index must be read 100%, no skimming | BREACH B3 — operation invalidated |
| Byte-Count Verification | Pre-read and post-update byte counts mandatory | BREACH B2/B7 — operation invalidated |
| Same-Session Update | Index updates cannot be deferred | BREACH B5 — operation invalidated |
| Name the Loss | 5-element articulation before every modification | BREACH B6 — operation invalidated |
| Re-Read After Update | Modified indexes must be re-read and byte-verified | BREACH B7 — operation invalidated |
| Module Directory Placement | Module dirs MUST be inside `modules/` at course root | BREACH B8 — operation invalidated |
| Lesson File Placement | Lesson files MUST be inside `lessons/` within module | BREACH B9 — operation invalidated |
| No Loose Files at Root | Course root has only index.md, modules/, quizzes/, summaries/, indexes/, assets/ | BREACH B10 — operation invalidated |

**NO EXCEPTION CLAUSE:** These rules apply regardless of task simplicity, file size, perceived urgency, model capability, or any contextual factor. "The task was trivial" is not an exception — trivial tasks with wrong placement produce the same index drift as complex ones. "The model is smart enough to remember" is not an exception — memory is stale, glob is truth.

---

## PRE-FLIGHT STRUCTURAL VERIFICATION — MANDATORY BEFORE EVERY WRITE

**This section supersedes all other rules when there is a conflict. It exists because the 6-link chain alone does not catch physical directory violations — it only checks indexes, not the actual filesystem.**

Before ANY file creation, modification, movement, or deletion under `updates/providers/`, you MUST run this 5-step pre-flight check. Skipping any step is a BREACH.

### Step 1 — Physical Directory Listing (not index reading)

Run `Get-ChildItem -Directory` on the course root and list EVERY directory. If ANY directory name matches `module_N_*` at the course root level (NOT inside `modules/`), HALT — BREACH B8. The only directories permitted at course root are:
```
index.md          (file)
modules/          (directory)
quizzes/          (directory)
summaries/        (directory)
indexes/          (directory)
assets/           (directory)
labs/             (directory — empty, labs live under modules/)
```

Any other directory or loose file at course root is a BREACH B10.

### Step 2 — Physical File Listing (not index reading)

Run `Get-ChildItem -File` on the course root. If ANY `.md` file exists at course root that is NOT one of the course-level metadata files (`c5_course_introduction.md`, `c5_course_overview.md`, `c5_course_syllabus.md`, `c5_progress_report.md`, `index.md`), HALT — BREACH B10. All lesson files, cheat sheets, summaries, and lab files MUST be inside their module directory.

### Step 3 — Module Internal Structure Verification

For each module directory inside `modules/`, verify the internal structure matches:
```
module_N_name/
├── index.md
├── lessons/        (all .md lesson files go here)
├── labs/           (all .md lab files go here)
└── summaries/      (all .md summary files go here)
```

If any lesson file exists at the module root (alongside `index.md`), HALT — BREACH B9. If any lab file exists at the module root, HALT — BREACH B9.

### Step 4 — Link Validation After Moves

After ANY file move operation, run a link validation scan on ALL `.md` files in the affected course directory:
```powershell
Get-ChildItem -Recurse -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $matches = [regex]::Matches($content, '\[([^\]]*)\]\(([^)]+)\)')
    foreach ($m in $matches) {
        $link = $m.Groups[2].Value
        if ($link -match '^\.\.?\/') {
            $resolved = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($_.DirectoryName, $link))
            if (-not (Test-Path $resolved)) { Write-Output "BROKEN: $($_.Name) -> $link" }
        }
    }
}
```

If ANY broken link is found, HALT — all cross-references must be updated before the operation is considered complete.

### Step 5 — Byte-Count Re-Verification After Index Updates

After updating any index file, re-read it and verify:
1. The new entry appears in the correct location
2. The byte count increased (for additions) or decreased (for removals)
3. No existing entries were accidentally deleted or corrupted

If any of these fail, the edit did not apply — HALT and redo.

### Pre-Flight Verdict (produce before every operation)

```
PRE-FLIGHT VERDICT:
- Physical directory listing: [CLEAN / BREACH — list violations]
- Physical file listing: [CLEAN / BREACH — list violations]
- Module internal structure: [CLEAN / BREACH — list violations]
- Link validation: [CLEAN / N links checked, 0 broken / BREACH — list broken links]
- Byte-count re-verification: [VERIFIED / BREACH — list mismatches]
- Overall: [READY TO OPERATE / HALT — BREACH DETECTED]
```

Only proceed when Overall is READY TO OPERATE.

---

## Post-Operation Directory Audit — MANDATORY AFTER EVERY WRITE

After completing any file creation, modification, movement, or deletion, run a final directory audit:

1. List all directories at the course root — confirm only allowed directories exist
2. List all files at the course root — confirm only course-level files exist
3. For each module directory — confirm internal structure matches the template
4. Run link validation on all affected files
5. Produce the Post-Operation Audit Verdict

```
POST-OPERATION AUDIT:
- Course root directories: [CLEAN / VIOLATIONS]
- Course root files: [CLEAN / VIOLATIONS]
- Module structure: [ALL MODULES COMPLIANT / VIOLATIONS]
- Link integrity: [ALL LINKS VALID / BROKEN LINKS]
- Index entries: [ALL CORRECT / MISSING / STALE]
- Overall: [PASS / FAIL]
```

If Overall is FAIL, the operation is incomplete — fix all violations before ending the session.

---

## Index Integrity Verdict (must be produced before every content operation)

Before writing a single byte of content, produce:

```
INDEX INTEGRITY VERDICT:
- Index files located: [N files — list paths]
- Index files read in full: [N files — list paths]
- Byte-count verified: [YES/NO — list pre-read sizes]
- Operation impact analyzed: [YES/NO — list which indexes need updates]
- Name the Loss completed: [YES/NO — verdict: ACCEPT/REJECT]
- Same-session update planned: [YES/NO]
- Overall: [READY TO OPERATE / HALT — BREACH DETECTED]
```

Only proceed when Overall is READY TO OPERATE. If HALT, fix the breach or escalate. Do not bypass this verdict.

---

## Pipeline Patches Section — Todoist Integration

**Section URL:** https://app.todoist.com/app/section/index-integrity-patches-6h4rhhrF46WRFR7W
**Section ID:** `6h4rhhrF46WRFR7W`
**Project ID:** `6h3gQ7Vxmq48xqM4`

This section tracks patches and behavioral mandates applied to the `index_integrity` skill. Every task in this section represents a real change that must be implemented, tested, and verified before marking complete.

### Auto-Comment Protocol

When you implement, test, or complete a patch from this section, you MUST post a comment to the corresponding Todoist task using the script at `.agents/skills/index_integrity/scripts/post_todoist_comment.ps1`.

**When to post a comment:**
- When you **start implementing** a patch: post "IMPLEMENTING: [description of what you're doing]"
- When you **complete** a patch: post "IMPLEMENTED (TESTED): [description of what was done, which file was modified, and verification result]"
- When you **cannot complete** a patch: post "BLOCKED: [reason] — [what's needed to unblock]"

**Comment format:**
```
[STATUS] — [what was done] — [file path modified] — [verification method]
```

**Example:**
```
IMPLEMENTED (TESTED) — Strengthened module directory enforcement rules with explicit verification commands and STOP-AND-VERIFY checklist — .agents/skills/index_integrity/SKILL.md — Verified by running Get-ChildItem on course root and confirming no violations
```

**How to post a comment:**
```powershell
# From the wiki-generation-pipeline directory:
. .agents/skills/index_integrity/scripts/post_todoist_comment.ps1 -TaskId "6h4rj3Xjr6v83PM4" -Comment "IMPLEMENTED (TESTED) — description here"
```

### Marking Tasks Complete

A task may ONLY be marked complete when ALL of the following are true:
1. The patch has been implemented in the SKILL.md (or other target file)
2. The implementation has been tested — the agent actually followed the new rule and it worked
3. A comment has been posted to the task describing what was done
4. No regressions were introduced — existing functionality still works

**Do NOT mark a task complete based on intent alone.** "I will implement this next session" is not completion. The task stays open until the work is done and verified.
