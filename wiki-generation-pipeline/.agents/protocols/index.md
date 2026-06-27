# PROTOCOL INDEX (index.md)
*Master shallow-reference index — read this first, every session.*
*Last updated: 2026-06-23 (v3) — PROTOCOL_CORE.md references removed across all prompts; Master Architect Framework defined inline in subagent prompts*

---

## Purpose

This file is a map, not a source of truth. It tells you what protocols
exist, what file each one physically lives in, and a one-paragraph summary
of what each does. For actual rule text, open the named file — never
reconstruct a protocol from memory of this index alone.

---

## Directory Structure (Canonical — DOMP enforced, relative to workspace root `./`)

| Location | Contains |
|---|---|---|
| `./` (workspace root) | Source files, `index.html`, loose scripts |
| `/instructions/` | AGENTS.md, L1–L5, GLOBAL_HUB_SYNC_LOG.md, SEIUP_STATE.md |
| `/protocols/` | All named protocol files — 20 protocols + this index |
| `/backups/original/` | Sliding-window instruction file backups (_v1→_v3) |
| `/backups/source/` | SFBP versioned source file backups (_v1, _v2, _v3) |
| `/scripts/` | Utility scripts |

**SEIUP_STATE.md location:** `/instructions/SEIUP_STATE.md` (not root)
**GLOBAL_HUB_SYNC_LOG.md location:** `/instructions/GLOBAL_HUB_SYNC_LOG.md` (not root)
---

---

## Protocol Index

### 1. SEIUP — Self-Evaluation & Instruction Update Protocol
**Lives in:** `/protocols/error_grasping_protocol.md`
**Note:** Filename does not match protocol name. Search by content, not filename.
**AGENTS.md entry:** Priority 5

Runs silently after every turn (LIVE mode default). Four phases: Detect → Root Cause → Log → Synthesize. Classifies findings as CLEAN / DRIFT / BREACH / AMBIGUOUS. Low-barrier findings go to sync log freely (Track A). High-barrier findings escalate to AGENTS.md/L1–L5 only if all 6 gates pass including mandatory user approval (Track B). Phase 4 full synthesis always runs at session end. Mode stored in `/instructions/SEIUP_STATE.md`. Switching: LIVE (default) / MILESTONE (after major tasks) / MANUAL (`!evaluate`).

---

### 2. IFMP — Instruction File Management Protocol
**Lives in:** `/protocols/IFMP_protocol_prompt.md`
**AGENTS.md entries:** Priority 4, rules 20–26

Governs every read/write touching AGENTS.md or L1–L5. Rules: manual full read before any write (never via script), sliding-window backup (`_v1`→`_v2`→`_v3`, max 3 versions, rotate on each backup) before every write, append-only (never silently replace/delete), correct-file-per-scope table, scripts allowed only for extraction/byte-counts (never content injection), explicit per-session authorization required — prior session consent does not carry over. SFBP governs `/backups/source/`. IFMP governs `/backups/original/`. Mutually exclusive.

---

### 3. HPSP — Hierarchical Progressive Summary Protocol
**Lives in:** `/protocols/large_files_protocol.md`
**Note:** File also contains agent identity and core operating principles.
**AGENTS.md entry:** Priority 2, rule 13
**Amendment (2026-06-19):** Phase 0 now script-enforced via `verify_hpsp_coverage.py` for 100% mathematical line coverage before drafting any plan.

Five phases: Phase 0 Recon → Phase 1 Spine (3–5 sentences) → Phase 2 Map (per-section) → Phase 3 Detail (fills gaps) → Phase 4 Full Synthesis (consolidated master summary, becomes active reference). Stop at earliest sufficient phase. **No-Exclusion Rule:** low-value chunks must still appear in output, tagged `[LOW-VALUE-FLAG]` with reason — never silently dropped. **PSM applies before any HPSP phase executes** — read source file raw, extract negative constraints, log to sync log before Phase 0 begins.

**HPSP Integrity Rule (learned from prior session failure):** Before Phase 0 recon, the agent must list the full working directory and flag any file whose name suggests it contains pre-built topic names, chunk labels, section headings, or an index of the source file (e.g. `headers`, `index`, `outline`, `topics`, `chunks`, or output of `extract_headings.py`). If any such file is found, stop and report to user before reading the source file. Proceeding with recon while a pre-built heading list is accessible is a session integrity failure.

---

### 4. LTHP — Last-Touch Highlight Protocol
**Lives in:** `/protocols/LTHP.md`
**Amendment (2026-06-19):** Canonical CSS source consolidated to `/protocols/LTHP.md`. Manual invocation path is now a BREACH. Two-layer enforcement: Layer 1 (CCMP template) prevents omission; Layer 2 (`lthp_audit.py`) detects omissions.

HTML-only editing protocol. Every added/modified block gets tagged `class="lthp-highlight"` (single consistent yellow defined in `/protocols/LTHP.md`). On the next edit, the previous highlight is fully removed before the new block is tagged. Exactly one generation of highlighting exists at a time. Non-HTML files are out of scope. No retroactive highlighting.

---

### 5. PDPP — Protocol Design & Propagation Protocol
**Lives in:** `/protocols/PDPP_protocol.md`
**AGENTS.md entry:** rule 27

Meta-protocol for designing new protocols proactively (SEIUP detects problems reactively; PDPP designs solutions). Five stages: 1) Agent diagnoses → 2) Agent drafts blueprint (never implements) → 3) Human reviews: approve/revise/reject → 4) Central Optimization hardens language → 5) Agent integrates via IFMP. One protocol per cycle. Blueprint ≠ implementation. Nothing written until Stage 5 with explicit authorization. PDPP Stage 5 must confirm new protocol file is physically written to `/protocols/` before any AGENTS.md or L-file entry is made.

---

### 6. SFRP — Session-Start File Redundancy Protocol
**Lives in:** `/protocols/SFRP.md`
**AGENTS.md entry:** rule 29

Mandatory first action whenever the user explicitly notifies the Agent that new content has been introduced this session — runs before any content reading, HPSP, or build task. Classifies each uploaded file as A (Exact Duplicate), B (Overlapping/Partial), or C (Unique) against existing directory state. Category A → resolve via `FILE_DEDUP_PROMPT.md` logic. Category B → merge, not discard (IFMP-governed if target is instruction file). Category C → no action. Reports classification table before any other processing begins.

---

### 7. UNIVERSAL_PROTOCOL_IMPLEMENTATION_PROMPT
**Lives in:** `/protocols/UNIVERSAL_PROTOCOL_IMPLEMENTATION_PROFESSIONAL_PROMPT_TEMPLATE.md`

Reusable 10-step template for integrating any already-approved protocol into the L1–L5/AGENTS.md architecture. Execution vehicle for PDPP Stage 5. Steps: determine target L-file → backup target → backup AGENTS.md → append protocol text verbatim → validate size increase → draft condensed AGENTS.md entry → get user confirmation → append to AGENTS.md → validate → log to sync log → final report.

---

### 8. DOMP — Directory Organization & Maintenance Protocol
**Lives in:** `/protocols/DOMP_protocol.md`
**AGENTS.md entry:** rule 30
**Amendment (2026-06-19):** `/protocols/` is now the mandatory, explicitly enforced directory for all protocol files, present and future. All future protocol files must be written here at creation.

Permanent, self-enforcing directory structure rule. Base folders: `/scripts/`, `/instructions/` (AGENTS.md, L1–L5, GLOBAL_HUB_SYNC_LOG.md, SEIUP_STATE.md), `/protocols/`, `/backups/original/`. Source files and `index.html` stay in root. New subfolders only when 5+ files of a distinct sub-type exist AND sub-type is growing. Applies retroactively once, then permanently to every new file at creation. DOMP L1 Exemption (2026-06-19): unauthorized writes allowed solely for bounded, verified file relocation (copy → verify → delete source, size must match, logged before move executes).

---

### 9. PSM — Protocol Sourcing Mandate
**Lives in:** `/protocols/PSM_protocol.md`
**AGENTS.md entry:** rule 34
**Status:** L1 violation if breached

Trigger: any named protocol execution. Rules: (1) Before executing a named protocol for the first time in a session, read its source file raw — no summaries, no memory. (2) If more than one major build step has passed since last read, re-read before executing again. (3) Immediately after reading, extract every negative constraint ("must never," "must not," "is prohibited," "is a breach") and append to sync log: `[PSM] [PROTOCOL] negative constraints loaded: - [constraint] [PSM] Proceeding to execute [PROTOCOL].` (4) If sync log does not contain the extraction entry, protocol is not properly sourced — output is invalid, redo after proper sourcing. PSM wraps every other protocol.

---

### 10. SFBP — Source File Backup Protocol
**Lives in:** `/protocols/SFBP_protocol.md`
**AGENTS.md entry:** rule 21
**Last Modified:** 2026-06-19 (Rules 5 and 6 added)

Scope: all project deliverables (`index.html`, `.py`, `.ts`, `.css`, `.js`). Instruction files excluded — governed by IFMP. Trigger: before any write, replace, or terminal command modifying an existing source file. Backup to `/backups/source/` as `[basename]_v[N].[ext]`. Max 3 versions — delete oldest before writing new if at 3. Verification gate: confirm backup written before executing modification — backup write failure → halt. Rule 5: if new file is >15% smaller than backup and no deletion was instructed → hard revert immediately, halt, report original size / new size / percentage drop / revert executed, wait for user acknowledgment. Rule 6: after every write append `[SFBP] [filename] | Before: [X bytes] | After: [Y bytes] | Delta: [Z%] | Revert triggered: [Yes/No]` to sync log regardless of revert. Rule 3 (Deadlock-Free Approval Gates), present in the standalone file but not in L1_core_directives.md, defines the approval sequencing logic that prevents circular halt conditions during backup verification.

---

### 11. ISIP — Isolated Script Injection Protocol
**Lives in:** `/protocols/ISIP_protocol.md`
**AGENTS.md entry:** rule 32
**Status:** L1 violation if breached

Trigger: any new JavaScript added to a file with existing populated `<script>` blocks. Rules: (1) Never append into an existing script block. (2) Wrap new logic in IIFE or place in new `<script>` block after all existing blocks. (3) Before injecting, scan all existing blocks for variable/function name collisions — rename new variables if collision found, log rename to sync log. (4) After injection, verify no duplicate top-level variable declarations across all `<script>` blocks.

---

### 12. CCMP — Component Co-Migration Protocol
**Lives in:** `/protocols/CCMP_protocol.md`
**AGENTS.md entry:** rule 31, rule 38
**Amendment (2026-06-19):** Standard injection template added — enforces `lthp-highlight` use on all text/data elements at write time.

Trigger: any HTML block cut, copied, pasted, or restored from backup. Ensures associated CSS, JS dependencies, and structural context migrate with the block. Layer 1 of LTHP enforcement.

---

### 13. PCOM — Protocol Conflict Override Matrix
**Lives in:** `/protocols/PCOM_protocol.md`
**AGENTS.md entry:** rule 33

Trigger: any user prompt that conflicts with a codified protocol rule. Governs resolution order when user instructions and protocol rules collide.

---

### 14. AST — AST-Driven Refactoring: Safe Mass Code Modification
**Lives in:** `/protocols/AST_refactoring_protocol.md`
**AGENTS.md entry:** Not referenced

Governs safe mass code modifications by parsing source code into an Abstract Syntax Tree (AST) or concrete syntax tree (CST) rather than using regex/string replacement, ensuring syntactic and semantic correctness before re-emitting. Recommends language-specific tools like LibCST, ts-morph, and rope, and outlines an 8-step execution path for signature changes requiring call-site identification, mutation API usage, error checks, and regression suite execution.

---

### 15. FILE_DEDUP — File Deduplication Prompt (Category A Resolution)
**Lives in:** `/protocols/FILE_DEDUP_PROMPT.md`
**AGENTS.md entry:** Not referenced

Defines the exact detection and resolution logic for Category A (Exact Duplicate) files identified during the Session-Start File Redundancy Protocol (SFRP) or the Directory Organization & Maintenance Protocol (DOMP). Detection relies on matching two of three conditions: same filename/variant, same byte size, or same hash. Non-authoritative duplicates are automatically archived to the appropriate backups folder and deleted from the live workspace.

---

### 16. TAP — TURBO_AUTONOMY_PROTOCOL
**Lives in:** `/protocols/TURBO_AUTONOMY_PROTOCOL.md`
**AGENTS.md entry:** Not referenced

Governs agent behavior across three autonomy modes: Approval Mode (default, human permission required for writes and shell commands), Turbo Mode (full autonomous execution with strict internal adherence to core safety protocols), and Hybrid Turbo Mode (autonomous execution within a single task container, halting for approval only before starting a new top-level action).

---

### 17. API_REVERSING — Hypothesis-Driven API Reversing: Safe Probing of Undocumented Interfaces
**Lives in:** `/protocols/api_reversing_protocol.md`
**AGENTS.md entry:** Not referenced

Governs the safe probing of undocumented functions, classes, or APIs using isolated, disposable test harnesses and falsifiable hypotheses before production integration. Prohibits guessing method contracts and mandates sentinel probes to serve as regression guards under system upgrades.

---

### 18. MEMORY_GC — Agentic Memory Eviction: Garbage Collection for Long-Running Agents
**Lives in:** `/protocols/memory_GC_protocol.md`
**AGENTS.md entry:** Not referenced

Defines proactive garbage collection of context window bloat (tool outputs, dead-end explorations, stale files) by classifying context into transient, load-bearing, or stale. Enforces a promote-then-evict compression format where takeaways are saved in a structured summary and raw files are cleared.

---

### 19. SUBAGENT_HANDOFF — Subagent Handoff Protocol (Context Compression)
**Lives in:** `/protocols/subagent_handoff_protocol.md`
**AGENTS.md entry:** Not referenced

Mandates the creation of a structured `handoff.md` file whenever the `invoke_subagent` tool is called. Directs the parent agent to write a high-density, non-narrative snapshot of the current state, constraints, next steps, key files, and ruled-out approaches to minimize subagent context consumption.

---

### 20. SYSTEMATIC_DEBUGGING — Systematic Root-Cause Debugging Protocol
**Lives in:** `/protocols/systematic_debugging_protocol.md`
**AGENTS.md entry:** Not referenced

Enforces a 7-step debugging framework (Freeze/Read, Reproduce Minimally, Single Hypothesis, Probe, Trace Backward, Smallest Correct Fix, Regression Check) to isolate error root causes and prevent "Guess and Check" loops. Triggered when a test or compile fails 2+ times consecutively.

---

---

## Skills Directory (Full Paths for Agent Search)

Each skill is available at `.agents/skills/<name>/SKILL.md`. All 16 skills with their paths:

| # | Skill Name | Full Path |
|---|---|---|
| 1 | `anthropic_product_knowledge` | `.agents/skills/anthropic_product_knowledge/SKILL.md` |
| 2 | `data_architecture` | `.agents/skills/data_architecture/SKILL.md` |
| 3 | `datalab_conversion` | `.agents/skills/datalab_conversion/SKILL.md` |
| 4 | `datalab_core` | `.agents/skills/datalab_core/SKILL.md` |
| 5 | `datalab_extraction` | `.agents/skills/datalab_extraction/SKILL.md` |
| 6 | `datalab_form_filling` | `.agents/skills/datalab_form_filling/SKILL.md` |
| 7 | `datalab_pipelines` | `.agents/skills/datalab_pipelines/SKILL.md` |
| 8 | `docx_creation` | `.agents/skills/docx_creation/SKILL.md` |
| 9 | `html_css_generation` | `.agents/skills/html_css_generation/SKILL.md` |
| 10 | `image_processing` | `.agents/skills/image_processing/SKILL.md` |
| 11 | `modern_engineering` | `.agents/skills/modern_engineering/SKILL.md` |
| 12 | `prompt_engineering` | `.agents/skills/prompt_engineering/SKILL.md` |
| 13 | `prompt_engineering_best_practices` | `.agents/skills/prompt_engineering_best_practices/SKILL.md` |
| 14 | `skill-creator` | `.agents/skills/skill-creator/SKILL.md` |
| 15 | `study_guide_generation` | `.agents/skills/study_guide_generation/SKILL.md` |
| 16 | `system_architecture` | `.agents/skills/system_architecture/SKILL.md` |

Also available (detailed, unsummarized): `.agents/fully detailed skills without summarization/claude skills/improve_frontend_skills.md`

---

## Active Session Constraints (Learned — Not in Protocol Files)

| Constraint | Detail |
|---|---|
| `extract_headings.py` execution | Prohibited during all HPSP phases without explicit per-turn written authorization. File targets old `test/` directory but must not be run without authorization. |
| `SEIUP_STATE.md` | Lives in `/instructions/SEIUP_STATE.md`. Default content: `SEIUP_MODE: LIVE`. |
| `GLOBAL_HUB_SYNC_LOG.md` | Lives in `/instructions/GLOBAL_HUB_SYNC_LOG.md`. Not root. |
| Prior session termination reason | `headers` file (pre-built heading index of source file) was present during HPSP Phase 0, contaminating recon. Session voided. File has been deleted. |

---

## Cross-Protocol Relationships

| Relationship | Detail |
|---|---|
| SEIUP → IFMP | SEIUP decides what to change; IFMP governs how it is physically written. Sequence: SEIUP Gate 6 approval → IFMP backup → IFMP read → IFMP append. |
| PSM → All protocols | PSM wraps every named protocol. Read source file raw, extract negative constraints, log to sync log before any protocol executes. |
| PDPP → IFMP | PDPP Stage 5 executes entirely through IFMP — no bypass. |
| PDPP → UNIVERSAL_PROMPT | Template is the concrete execution vehicle for PDPP Stage 5. |
| PDPP → HPSP | If problem under diagnosis involves a large file, HPSP applies within PDPP Stage 1. |
| SFBP → IFMP | SFBP governs `/backups/source/`. IFMP governs `/backups/original/`. Mutually exclusive. |
| SFRP → FILE_DEDUP_PROMPT.md | SFRP Category A resolution defers to dedup logic. |
| DOMP → IFMP | Any instruction-file move during reorg is IFMP-governed. |
| DOMP → PDPP | PDPP Stage 5 must confirm new protocol file is in `/protocols/` before any AGENTS.md or L-file entry. |
| CCMP → LTHP | CCMP is Layer 1 of LTHP enforcement. `lthp_audit.py` is Layer 2. |
| PSM → All (includes write-safety items formerly in PROTOCOL_CORE.md) | PSM wraps every named protocol; write-safety constraints are now bundled into SFBP and PSM. |

---

## Known Open Items

- DOMP/IFMP path mismatch, SEIUP silent-mode tool-call conflict, IFMP shrink-on-deletion conflict, PDPP's nonexistent "Central Chat" instance — remediation directed but not confirmed applied to live files. Check actual protocol files before assuming summaries reflect corrected wording.
- Write enforcement scripts (approval gate, version selection, log append) — no scripts exist yet for these operations.
- CCMP has no rule requiring injected content to use surrounding template CSS classes — pending PDPP amendment, not yet implemented.

---

## Usage Rule

Read this index first every session. If a task only requires knowing which protocol governs a situation, this index may be sufficient. If a task requires executing a protocol's rules, open the actual named file — this index is never a substitute for full text. If this index conflicts with a protocol's actual file content, the file always wins. Flag the discrepancy and ask the user before proceeding.
