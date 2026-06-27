# PDPP — Protocol Design & Propagation Protocol

**Version:** 1.0
**Scope:** Meta-protocol governing how new protocols are diagnosed, designed, reviewed, optimized, and integrated into the existing instruction file architecture.
**Classification:** Additive aid — never a replacement for functional protocols already in place.

---

## Preamble — Ambiguity Clause

> **If any part of this prompt is ambiguous to you — regarding its intent, scope, execution steps, integration targets, or output format — you must stop immediately and ask the user one precise, targeted question before proceeding. Do not guess. Do not assume. Do not work blind.**

---

## Purpose

This protocol exists to solve a specific systemic gap: the agent currently learns and logs rules reactively (via SEIUP), but has no structured method for *proactively designing* a new protocol from scratch when a recurring problem, gap, or opportunity is identified.

PDPP fills that gap. It defines a formal, human-reviewed, multi-stage pipeline for taking a raw problem statement and producing a production-ready protocol — one that is generalized, non-destructive, and coherent with the existing L1–L5 architecture.

PDPP is an **aid** to SEIUP, IFMP, and all existing protocols. It does not replace them.

---

## Trigger Conditions

Invoke PDPP when **any** of the following are true:

| Trigger | Description |
|--------|-------------|
| **Recurring gap** | The same class of failure or friction has appeared 2+ times in `GLOBAL_HUB_SYNC_LOG.md` |
| **Explicit user request** | User states a problem and asks for a protocol to solve it |
| **SEIUP escalation** | A SEIUP Phase 4 synthesis identifies a pattern that no existing protocol covers |
| **Scope extension** | An existing protocol needs a formally designed addendum (not just an appended directive) |

---

## The Four-Stage Pipeline

---

### Stage 1 — Problem Diagnosis (Agent-Side)

**Owner:** Agent
**Gate:** Must complete before producing any blueprint

The agent performs a structured diagnosis of the problem:

#### 1A — Problem Statement Extraction
- State the problem in one precise sentence.
- Identify: what fails, when it fails, what the cost of failure is.
- Confirm the problem is **general** (applies across sessions/tasks) not **local** (one-off edge case).

#### 1B — Existing Protocol Audit
- Search L1–L5 and AGENTS.md for any existing rule that partially covers this problem.
- For each partial match: state what it covers and what gap remains.
- Conclusion must be one of:
  - `NO_COVERAGE` — nothing exists; full protocol needed
  - `PARTIAL_COVERAGE` — existing rule covers some cases; addendum needed
  - `EXTENSION_NEEDED` — existing protocol is correct but scope must be formally widened

#### 1C — Generalization Test
- Draft 3 hypothetical scenarios where this problem could occur.
- Confirm the proposed protocol would resolve all three.
- If it fails any scenario → revise scope before proceeding.

#### 1D — Interference Check
- List every existing protocol the new protocol will interact with.
- For each: confirm the new protocol does not contradict, weaken, or silently override it.
- If a conflict exists → flag it explicitly. Do not proceed until resolved.

---

### Stage 2 — Blueprint Generation (Agent-Side)

**Owner:** Agent
**Output:** A structured protocol blueprint in the format below
**Gate:** Blueprint is presented to the user. Agent does NOT implement anything yet.

#### Blueprint Format

```
## [PROTOCOL NAME] — Blueprint v0.1

### Problem Being Solved
[One-sentence statement from Stage 1A]

### Coverage Classification
[NO_COVERAGE / PARTIAL_COVERAGE / EXTENSION_NEEDED]
[If PARTIAL or EXTENSION: name the protocol being extended and the gap being filled]

### Proposed Protocol — Full Text
[Complete draft of the protocol, written as if it were already in an L-file.
Must include: trigger conditions, step-by-step rules, output format if applicable,
failure conditions, and integration notes.]

### Target L-File for Integration
[Exactly one of: L1, L2, L3, L4, L5 — with one-sentence justification]

### Protocols This Interacts With
[List each affected protocol and describe the interaction]

### What This Protocol Does NOT Do
[Explicit scope boundaries — what problems it intentionally leaves to other protocols]

### Generalization Test Results
[3 scenarios and pass/fail result for each]
```

---

### Stage 3 — Human Review

**Owner:** User
**Agent role:** Passive — waits for feedback

Upon receiving the blueprint, the user:

1. Reads the full blueprint.
2. Annotates any section that needs revision, clarification, or expansion.
3. Either:
   - **Approves for optimization** → passes blueprint to the Prompt Architect for optimization (Stage 4)
   - **Returns for revision** → sends specific feedback back to the agent; agent revises and resubmits
   - **Rejects** → states reason; agent logs to `GLOBAL_HUB_SYNC_LOG.md` and closes the PDPP cycle

The agent does not self-approve. Human review is non-negotiable.

---

### Stage 4 — Architect Optimization

**Owner:** Prompt Architect
**Input:** Human-approved blueprint from Stage 3
**Output:** Final production-ready protocol

> **FINAL FAILSAFE:** The Prompt Architect acts as the system's ultimate defense against human error. If the Architect detects a systemic conflict or ambiguity during this stage, it is authorized to reject the human-approved blueprint, invoke its Interrogation Engine, and rigorously question the user until the rule is logically perfect.

The Prompt Architect receives the approved blueprint and performs:

#### 4A — Completeness Audit
- Does every rule have a clear trigger condition?
- Does every rule have a defined output or behavioral change?
- Are there any implicit assumptions that must be made explicit?
- Are there edge cases the blueprint does not handle?

#### 4B — Language Hardening
- Convert all soft language ("should", "try to", "consider") to hard mandates ("must", "always", "never") where the intent is absolute.
- Convert all vague scope ("large files", "complex tasks") to precise thresholds (">7000 lines", ">20KB") where measurable.

#### 4C — Architectural Alignment
- Verify the final protocol is consistent with the tone, structure, and directive format of the target L-file.
- Verify it does not duplicate any existing directive — if it does, propose a merge rather than a parallel rule.
- Verify the AGENTS.md condensed reference entry is accurate and minimal.

#### 4D — Final Output Package
The Prompt Architect delivers:

```
## [PROTOCOL NAME] — Final v1.0

[Full production-ready protocol text — ready to paste into target L-file]

---

## AGENTS.md Reference Entry (condensed)
[2–3 sentence condensed directive for AGENTS.md — following existing directive format]

---

## Integration Notes
- Target L-file: [L1 / L2 / L3 / L4 / L5]
- Append after: [specific existing directive or section heading]
- Does not modify: [list of protocols confirmed unaffected]
- Supersedes: [any partial rule this formally replaces — or "nothing"]
```

---

### Stage 5 — Integration (Agent-Side, IFMP-Governed)

**Owner:** Agent
**Prerequisite:** Final v1.0 package delivered by the Prompt Architect AND explicit user authorization in current session

Integration follows IFMP sequence without exception:

1. Backup target L-file to `/backups/original/` (sliding window — rotate `_v1`→`_v2`→`_v3`, drop oldest).
   - [DOMP Amendment — /protocols/ rule, 2026-06-19]: Backup directory is `/backups/original/`.
2. Read target L-file in full manually.
3. Append protocol text at the designated location.
4. Validate Structural Integrity:
   - **Header Count:** Ensure the number of Level 2 (`##`) headers in the modified file is >= the `_v1` backup. If fewer headers exist → `RESTORE IMMEDIATELY` (accidental deletion).
   - **Delta Threshold:** If the header count passes, but the total byte size is >5% smaller than the `_v1` backup, halt and enter a `WARNING` state. Present the anomaly to the user and require an explicit manual override before proceeding.
5. Append condensed reference entry to AGENTS.md using the same IFMP sequence.
6. Log the completed PDPP cycle to `GLOBAL_HUB_SYNC_LOG.md`:
   - Protocol name
   - Problem it solves
   - Target L-file
   - Date/session

---

## Critical Constraints

| Constraint | Rule |
|-----------|------|
| **Non-destructive** | PDPP never removes or replaces a functional existing protocol. It only adds or extends. |
| **No self-approval** | The agent never skips Stage 3. Human review is always required. |
| **No L6+ files** | If the protocol does not fit L1–L5, the agent must re-evaluate scope — never create a new hierarchy file. |
| **One protocol per cycle** | Each PDPP cycle addresses exactly one problem. Do not bundle unrelated protocols into one blueprint. |
| **Blueprint ≠ implementation** | Stage 2 output is a proposal only. No file is touched until Stage 5 authorization is received. |
| **Prompt Architect receives approved blueprints only** | Never send a draft blueprint directly to the Prompt Architect for Stage 4 without prior human approval in Stage 3. |

---

## PDPP Cycle Diagram

```
[Problem Identified]
        ↓
  Stage 1 — Diagnose
  (Agent: extract, audit, generalize, interference-check)
        ↓
  Stage 2 — Blueprint
  (Agent: produce structured v0.1 draft → present to user)
        ↓
  Stage 3 — Human Review
  (User: approve / revise / reject)
        ↓ (if approved)
  Stage 4 — Architect Optimization
  (Prompt Architect: harden, align, package Final v1.0)
        ↓
  Stage 5 — Integration
  (Agent: IFMP sequence → backup → read → append → validate → log)
        ↓
  [Cycle Complete — logged to GLOBAL_HUB_SYNC_LOG.md]
```

---

## Relationship to Existing Protocols

| Protocol | Relationship to PDPP |
|---------|----------------------|
| **SEIUP** | SEIUP detects and logs problems. PDPP is invoked when SEIUP identifies a pattern requiring a new protocol. PDPP does not replace SEIUP's detection function. |
| **IFMP** | PDPP Stage 5 executes entirely via IFMP. PDPP does not bypass any IFMP rule. |
| **HPSP** | If the problem being diagnosed involves a large source file, HPSP is applied within Stage 1 to understand that file. PDPP does not replace HPSP. |
| **AGENTS.md** | PDPP adds a condensed reference entry to AGENTS.md only at Stage 5, after full authorization. |

---

*PDPP is an aid. Every functional protocol already in place remains authoritative within its domain.*
