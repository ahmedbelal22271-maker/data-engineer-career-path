# PROTOCOL_INDEX.md
*Master shallow-reference index — read this first, every session.*
*Last updated: 2026-06-22 — synced against actual directory contents, 7 entries added, 3 paths corrected, 1 entry content gap resolved (SFBP Rule 3)*

---

## Purpose

This file is a map, not a source of truth. It tells you what protocols
exist, what file each one physically lives in, and a one-paragraph summary
of what each does. For actual rule text, open the named file — never
reconstruct a protocol from memory of this index alone.

---

## Directory Structure (Canonical — DOMP enforced)

| Location | Contains |
|---|---|
| `c:/Users/marwa/antigravity/test2/` | Root — source files, `index.html`, loose scripts |
| `/instructions/` | AGENTS.md, L1–L5, GLOBAL_HUB_SYNC_LOG.md, SEIUP_STATE.md |
| `/protocols/` | All named protocol files (PSM, CCMP, DOMP, IFMP, ISIP, LTHP, PCOM, PDPP, SFRP, large_files_protocol.md, error_grasping_protocol.md) |
| `/backups/original/` | Sliding-window instruction file backups (_v1→_v3) |
| `/backups/source/` | SFBP versioned source file backups (_v1, _v2, _v3) |
| `/scripts/` | Utility scripts |

**SEIUP_STATE.md location:** `/instructions/SEIUP_STATE.md` (not root)
**GLOBAL_HUB_SYNC_LOG.md location:** `/instructions/GLOBAL_HUB_SYNC_LOG.md` (not root)

---

## PROTOCOL_CORE.md — Seven Operations

See /protocols/PROTOCOL_CORE.md — seven operations, read before every file write.

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
**AGENTS.md entry:** rule 28

Governs permanent directory structure and file naming conventions. Files must be located at correct logical directory. All protocol files must live in `/protocols/`. Prohibits creating files in directory structures not explicitly defined in map. All new file creations must be validated against DOMP structure.

---

### 9. PSM — Protocol Sourcing Mandate
**Lives in:** `/instructions/L1_core_directives.md` (Directive 1)
**AGENTS.md entry:** Priority 1, rules 1–4

PSM wraps every other protocol in this index. Before executing any protocol, its source file must be read raw, and all negative constraints logged. Prohibits executing protocols based on memory or summarization.

---

### 10. SFBP — Source File Backup Protocol
**Lives in:** `/instructions/L1_core_directives.md` (Directive 8)
**AGENTS.md entry:** Priority 3, rules 5–12

Requires backing up any source file or deliverable in the workspace to `/backups/source/` before performing any edit. Mandates reverting and investigating if file size drops by >15%. Appends synchronization log entries to `GLOBAL_HUB_SYNC_LOG.md` after every file write.

---

### 11. ISIP — Isolated Script Injection Protocol
**Lives in:** `/instructions/L1_core_directives.md` (Directive 9)
**AGENTS.md entry:** Priority 6, rules 14–19

Governs JS code injection into HTML documents. Requires wrapping code in IIFE or fresh script block to isolate scope. Mandates performing variable and function collision scan prior to injection. Prohibits appending code directly to existing, populated script blocks.

---

### 12. CCMP — Component Co-Migration Protocol
**Lives in:** `/protocols/CCMP_protocol.md`
**AGENTS.md entry:** rule 30

Ensures all dependencies (CSS custom properties, typography rules, layout dimensions, external assets, scripts) migrate cleanly along with any HTML snippet that is cut, copied, pasted, or restored. Mandates using standard CCMP HTML comment boundaries.

---

### 13. PCOM — Protocol Conflict Override Matrix
**Lives in:** `/protocols/PCOM_protocol.md`
**AGENTS.md entry:** rule 31

Defines the resolution order when user requests conflict with core protocols. Core OS security constraints and negative constraints occupy level 1; user explicit requests occupy level 2. Never bypass a protocol constraint unless PCOM explicitly authorizes it.

---

### 14. AST — AST-Driven Refactoring
**Lives in:** `/protocols/AST_refactoring_protocol.md`
**AGENTS.md entry:** Not referenced

Requires structural code modifications to be driven by AST parsing (Abstract Syntax Tree) to ensure structural safety. Prohibits raw regex/string replacement for mass structural code refactorings.

---

### 15. FILE_DEDUP — File Deduplication Protocol
**Lives in:** `/protocols/FILE_DEDUP_PROMPT.md`
**AGENTS.md entry:** Not referenced

Deduplication protocol for Category A exact duplicates. Compares files by cryptographic hash, size, and metadata, archives duplicates, and redirects imports.

---

### 16. TAP — Turbo Autonomy Protocol
**Lives in:** `/protocols/TURBO_AUTONOMY_PROTOCOL.md`
**AGENTS.md entry:** Not referenced

Governs internal execution rules, checkpoint gates, and safety overrides when operating in Turbo Autonomy mode.

---

### 17. API_REVERSING — Hypothesis-Driven API Reversing
**Lives in:** `/protocols/api_reversing_protocol.md`
**AGENTS.md entry:** Not referenced

Hypothesis-driven API reversing and probing protocol. Prohibits raw contract guessing. Requires isolatedDisposable test harnesses.

---

### 18. MEMORY_GC — Agentic Memory Eviction
**Lives in:** `/protocols/memory_GC_protocol.md`
**AGENTS.md entry:** Not referenced

Memory Garbage Collection protocol to compress and evict stale context window state.

---

### 19. SUBAGENT_HANDOFF — Subagent Handoff Protocol
**Lives in:** `/protocols/subagent_handoff_protocol.md`
**AGENTS.md entry:** Not referenced

Structured context compression and serialization for agent handoffs and subagent delegation.

---

### 20. SYSTEMATIC_DEBUGGING — Systematic Root-Cause Debugging Protocol
**Lives in:** `/protocols/systematic_debugging_protocol.md`
**AGENTS.md entry:** Not referenced

Enforces a 7-step debugging framework (Freeze/Read, Reproduce Minimally, Single Hypothesis, Probe, Trace Backward, Smallest Correct Fix, Regression Check) to isolate error root causes and prevent "Guess and Check" loops. Triggered when a test or compile fails 2+ times consecutively.

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
| PROTOCOL_CORE.md → All | Read before every file write. Six operations govern all write actions. |

---

## Known Open Items

- DOMP/IFMP path mismatch, SEIUP silent-mode tool-call conflict, IFMP shrink-on-deletion conflict, PDPP's nonexistent "Central Chat" instance — remediation directed but not confirmed applied to live files. Check actual protocol files before assuming summaries reflect corrected wording.
- Four enforcement script gaps: SFBP, approval gate, version selection, log append — no scripts exist for any of the six PROTOCOL_CORE.md operations.
- CCMP has no rule requiring injected content to use surrounding template CSS classes — pending PDPP amendment, not yet implemented.

---

## Usage Rule

Read this index first every session. If a task only requires knowing which protocol governs a situation, this index may be sufficient. If a task requires executing a protocol's rules, open the actual named file — this index is never a substitute for full text. If this index conflicts with a protocol's actual file content, the file always wins. Flag the discrepancy and ask the user before proceeding.
