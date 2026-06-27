# SESSION-START FILE REDUNDANCY PROTOCOL (SFRP)

## Role

You are the project agent. This protocol governs the **mandatory first
action** of any session in which files are uploaded — before reading,
analyzing, or processing any of them for content, building, or HPSP
purposes. It integrates with, and does not duplicate, the dash-numbered
deduplication logic already defined in `FILE_DEDUP_PROMPT.md`.

---

## Step 1 — Trigger Condition

The instant the user explicitly notifies the Agent that new content
has been introduced this session, halt all other processing. Define
"new content" strictly as a file or resource the user has explicitly
declared as newly provided in their current message. Files already
present in the workspace at session start are never treated as new
content, regardless of timestamp. Do not read new content for
substance, do not begin HPSP, do not begin any build task, until
this protocol completes.

---

## Step 2 — Inventory

List every file uploaded this session. For each, note: filename, size, and
a one-line content summary (skim only — no deep read yet).

---

## Step 3 — Classify Each Uploaded File Against Existing State

Compare each uploaded file against (a) the agent's existing directory
files and (b) every other file uploaded this session. Classify each into
exactly one category:

| Category | Definition |
|---|---|
| **A — Exact Duplicate** | Identical or functionally identical to an existing file (including dash-numbered duplicates, e.g. `AGENTS-1.md` vs `AGENTS.md`) |
| **B — Overlapping/Partial** | Shares significant content with an existing file but contains differences (additions, edits, partial overlap) — not a clean duplicate |
| **C — Unique** | No meaningful overlap with anything existing or anything else uploaded this session |

---

## Step 4 — Resolve by Category

**Category A (Exact Duplicate):**
Apply `/protocols/FILE_DEDUP_PROMPT.md` logic directly: identify the canonical keeper
(highest dash-number, or the existing directory version if the upload is a
plain re-upload), confirm the keeper is healthy, remove the duplicate,
verify.

**Category B (Overlapping/Partial):**
Do not delete either file. Integrate: merge the new content into the
canonical existing file rather than discarding the upload. If the target is
an instruction file (`AGENTS.md`, L1–L5), this merge is subject to IFMP:
read before write, sliding-window backup (`_v1`→`_v3` rotation), append
only — never replace, explicit authorization obtained before the write. If
the target is a non-instruction file, merge directly and report what was
combined.

**Category C (Unique):**
No action. Proceed to normal processing once Steps 4–5 complete for all
other files.

---

## Step 5 — Report Before Proceeding

Present a table: filename → category → action taken (removed / merged /
kept as-is). This report must be shown before any content processing,
HPSP, or build task begins for this session's files.

---

## Step 6 — Resume Normal Session Flow

Only after Step 5 is presented and any required authorization (per IFMP, if
triggered) is obtained, proceed with the session's actual task using the
now-deduplicated/integrated file set.

---

## Ambiguity Clause

If at any point you cannot determine whether an uploaded file is Category
A, B, or C, or whether a merge target is correct, stop and ask one precise
question before taking any action. Do not guess and do not delete anything
when uncertain.
