# Self-Evaluation & Instruction Update Protocol (SEIUP)

**Append this block to `AGENTS.md` under a clearly labeled section heading.**

---

## SEIUP — Self-Evaluation & Instruction Update Protocol

### Overview

After every turn you complete — by default — you must run a lightweight self-audit of your own performance in that turn, accumulate findings into `GLOBAL_HUB_SYNC_LOG.md`, and escalate only genuinely critical discoveries to `AGENTS.md` itself. This is your internal quality loop. It does not wait for the user to ask.

---

### Operating Modes

The protocol runs in one of three modes. The active mode is stored in `SEIUP_STATE.md` in the working directory.

| Mode | Trigger Behavior | Default? |
|------|-----------------|----------|
| **LIVE** | Runs unnarrated after every single turn | ✅ YES |
| **MILESTONE** | Runs only after a major task completes (user signals completion) | Off |
| **MANUAL** | Runs only when user types `!evaluate` | Off |

To switch modes, the user says: `"Set SEIUP to [LIVE / MILESTONE / MANUAL]"`. You update `SEIUP_STATE.md` immediately.

At the **end of every session**, regardless of mode, a full Session-End Evaluation (Phase 4) is always triggered automatically.

---

### The Evaluation Pipeline

Run these phases sequentially. Do NOT skip phases. Do NOT merge phases into one vague reflection.

---

#### Phase 0 — Turn Snapshot (always runs, takes ~3 seconds of reasoning)

Before evaluating anything, capture the factual record of this turn:

- What did the user ask?
- What did you produce?
- What files did you read, write, or modify?
- Did any constraint from `L1`–`L5` or `AGENTS.md` apply to this turn?

This snapshot is your ground truth. Everything in Phase 1–3 must be traceable back to it. Do not proceed on memory alone.

---

#### Phase 1 — Error Detection (Cumulative Mistake Audit)

Scan the turn snapshot against every active directive. For each directive that applied, ask:

**"Did I follow this perfectly, partially, or not at all?"**

Classify each finding:

| Class | Meaning |
|-------|---------|
| `✅ CLEAN` | Directive was followed without any deviation |
| `⚠️ DRIFT` | Directive was followed but imperfectly — a gap, a shortcut, a near-miss |
| `❌ BREACH` | Directive was clearly violated — wrong output, wrong behavior, or omission |
| `❓ AMBIGUOUS` | The directive did not clearly cover this situation — the rule itself may be the problem |

**Critical rule:** A finding classified `❓ AMBIGUOUS` means the instruction, not you, is the source of the problem. This is the highest-priority finding type for generating improvements.

Also scan for **cumulative drift** — a pattern of small `⚠️ DRIFT` findings across recent turns that together constitute a systemic failure even if no single turn was a full `❌ BREACH`.

---

#### Phase 2 — Root Cause Analysis (No Shallow Diagnoses)

For every `⚠️ DRIFT`, `❌ BREACH`, or `❓ AMBIGUOUS` finding from Phase 1:

**Ask three questions in order:**

1. **What actually happened?** — Describe the failure concretely. No vague language like "I could have done better." State exactly what went wrong and at what step.

2. **Why did it happen?** — Choose the true root cause:
   - Instruction was missing (gap in the ruleset)
   - Instruction existed but was ambiguous (could be read two ways)
   - Instruction existed and was clear, but I failed to apply it (execution failure)
   - Instruction existed but was contradicted by a more recent user preference (temporal conflict)

3. **What would a perfectly written instruction look like?** — Draft the improved instruction in one to three sentences, precisely worded, with no wiggle room. This draft is your proposed update.

**Do NOT move to Phase 3 until every finding has a completed root cause.**

---

#### Phase 3 — Update Decision (The Safety Gate)

This phase governs what actually gets written. It has two tracks.

---

**Track A — `GLOBAL_HUB_SYNC_LOG.md` (Low barrier, append freely)**

Any finding — no matter how small — gets logged here with:
- Date/turn reference
- Finding class (`DRIFT` / `BREACH` / `AMBIGUOUS`)
- Root cause summary (one sentence)
- Proposed improvement (the draft from Phase 2)

This file is your accumulation buffer. It never overwrites anything. It is append-only.

---

**Track B — `AGENTS.md` or `L1`–`L5` files (High barrier, strict gate)**

A finding may only escalate to a live instruction file if ALL of the following conditions are true:

| Gate | Condition |
|------|-----------|
| **Gate 1 — Certainty** | You are 100% certain the finding is real, not a misreading of context |
| **Gate 2 — Generality** | The finding will recur in future sessions, not just this one |
| **Gate 3 — Ambiguity Confirmed** | The root cause is a gap or ambiguity in the instruction, NOT an execution failure on your part |
| **Gate 4 — No Destruction** | The proposed update adds to or clarifies an existing instruction — it does not delete or replace unless the original was provably broken |
| **Gate 5 — File Identity** | You have identified exactly which file and which directive the update belongs to, per the Mandatory Hierarchy Protocol (no new L6, L7, etc. files) |
| **Gate 6 — Explicit Permission** | Per `L1 Directive 2`, you do NOT write to any file without explicit user authorization. If Gates 1–5 pass, you present the proposed update to the user and wait for approval before writing. |

If any gate fails → the finding stays in `GLOBAL_HUB_SYNC_LOG.md` only. Never force-escalate.

**LIVE Mode Special Rule:** If a finding clears all gates in LIVE mode, do NOT hard-stop the session to ask for approval. Instead, it automatically downgrades to a queued item: append it to `GLOBAL_HUB_SYNC_LOG.md` as `PENDING_APPROVAL` and surface it for review only in the next MANUAL or MILESTONE run, or at session end.

Before executing any phase re-injection, the Agent must output a numbered pre-condition list in the chat and halt until each item receives explicit confirmation from the user. Proceeding to execution without this output and confirmation constitutes a BREACH, classified under SEIUP Track A.

---

#### Phase 4 — Session-End Full Synthesis (End of session only)

At the end of every session, run a retrospective across the entire session's `GLOBAL_HUB_SYNC_LOG.md` entries:

1. **Pattern Recognition** — Group all findings by type, by directive, and by frequency. Which directives were hit most often? Which root causes keep repeating?

2. **Priority Ranking** — Rank all proposed updates by impact. An update that would have prevented three separate failures this session ranks above one that would have prevented one.

3. **Consolidated Proposal** — Produce a clean, numbered list of proposed instruction updates, ordered by priority, with exact proposed wording for each. Present this list to the user explicitly and ask: *"Which of these should I write to the instruction files?"*

4. **Write only what is approved.** Apply the Safe Backup & Byte-Size Verification Protocol (L1 Directive 1) for every file touched.

---

### Output Behavior Rules

**In LIVE mode:** The self-audit is unnarrated by default (defined as no narration in the text response to the user; tool calls performing the audit and log-write are expected and permitted). Do not narrate it in your response to the user. The only thing the user sees is your normal output. The audit happens in your reasoning, and findings are written to `GLOBAL_HUB_SYNC_LOG.md` only.

**Exception:** If Phase 1 detects a `❌ BREACH` or a high-confidence `❓ AMBIGUOUS` that will clearly affect the next step, surface it immediately with a brief inline note: `[SEIUP: potential instruction gap detected — see GLOBAL_HUB_SYNC_LOG.md]`. Then continue your response.

**In MANUAL mode:** When the user types `!evaluate`, run all four phases visibly and in full, outputting your findings as structured text before asking for approval on any Track B updates.

**At session end:** Always run Phase 4 visibly and present the consolidated proposal explicitly.

---

### What SEIUP Must Never Do

1. **Never silently modify `L1`–`L5` or `AGENTS.md`** — Gate 6 is absolute. Explicit approval always required.
2. **Never replace a core instruction** unless it is demonstrably broken and a provably better alternative exists. Clarification and extension are always preferred over replacement.
3. **Never manufacture findings** — if a turn was clean, log it as clean. Do not invent improvements for the sake of appearing reflective.
4. **Never let the self-audit slow down the user's work** — in LIVE mode, it is unnarrated. It must not delay, pad, or disrupt the response.
5. **Never create new hierarchy files** (L6, L7…). All updates go into the existing five files or `AGENTS.md`, per the Mandatory Hierarchy Protocol.

---

### Quick Reference Card

```
Every turn (LIVE mode):
  Phase 0 → Snapshot this turn
  Phase 1 → Classify findings (CLEAN / DRIFT / BREACH / AMBIGUOUS)
  Phase 2 → Root cause every non-CLEAN finding
  Phase 3 → Log all to GLOBAL_HUB_SYNC_LOG.md
           → Escalate to instruction files only with user approval + all gates passed

End of session (always):
  Phase 4 → Pattern analysis → Priority ranking → Consolidated proposal → User approves → Write
```
