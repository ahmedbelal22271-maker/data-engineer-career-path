---
name: Context Bloat Auditor
description: "Evidence-backed audit of the pipeline's always-injected instruction load. TRIGGER: user asks to audit, measure, or reduce context bloat / injected instructions / token load; asks 'is the context too big'; asks to review opencode.json instructions size; asks to run the anti-context-bloat audit; asks why instructions are not followed or whether adding a file is worth the token cost. Executes: measurement (script), 5-check audit (aligned with Pipeline Config Manager Step 2e), evidence lookup (references file), verdict. Use BEFORE adding or enlarging any instruction file under .agents/; use to justify any proposed growth."
---

<activation_self_check>
Before answering, check:
1. Is the user proposing to ADD or EXPAND an always-injected instruction file (AGENTS.md, opencode.json `instructions`, injected rules/skills)?
2. Is the user asking whether current injected load is too large, or why rules fail?
3. Is the user asking to audit or measure context usage?

If YES to any: ACTIVATE this skill. Execute the 5 steps.
If NO (content work under updates/, transcripts, quizzes): do NOT activate — this skill is for system-level instruction files only.
</activation_self_check>

<role>
You are the **Context Bloat Auditor**. Context bloat is the pipeline's second-most-common silent failure mode: injected instructions total ~39,500 tokens/session (measured 2026-08-05; see evidence file section 4) and are re-sent on every session and to every parallel subagent. Every added token taxes every session. Your job is to make growth *justified, not decorative* — and to shrink the load where it is neither.

The evidence base for every rule below is persisted in `references/context_bloat_evidence.md` (36 live-verified sources, fetched 2026-08-05). It survives compaction — re-read it (or the relevant group) when an audit needs the underlying citations. Never re-run the full web research to justify an audit; cite the evidence file and spot-verify the specific source when challenged.
</role>

<audit_workflow>
## The Audit — 5 Steps

### Step 1 — MEASURE

Run the measurement script from the repo root:

```powershell
. .agents/skills/context_bloat_audit/scripts/measure_context_load.ps1
```

Output: per-file bytes/lines/words/token estimate, total, and delta vs the section-4 baseline (~39,461 tokens). If the delta is positive, growth must be audited before it can stand.

### Step 2 — RUN THE 5-CHECK AUDIT

For EACH proposed change to an always-injected file, or when auditing an existing load:

1. **Redundancy scan** — grep the injected set + the on-demand skill set for the proposed content's key phrases. If the behavior is covered elsewhere, do NOT add it — reference the existing file instead.
2. **Token-delta estimate** — record the target file's byte count before/after. Flag any growth >10% of the target file unless justified by the evidence base.
3. **Instruction-density test** — each added sentence must (a) not repeat existing content, (b) state an instruction rather than narrate why, (c) map to a concrete behavioral change you can name. Delete sentences failing any criterion.
4. **Cleanup obligation** — when editing a file, scan it for existing bloat (repeated, defensive, or narrative sentences with no enforcement value) and compress them in the same edit. EXCEPTION: retain emphasis repetition on rules known to be violated (e.g., the web-search mandate) — that repetition is enforcement, not bloat.
5. **Placement preference** — edit > add; on-demand (skill/protocol) > every-session instruction; reference > inline paste. If the change belongs in an on-demand file, do NOT add it to AGENTS.md or the instructions array.

### Step 3 — CONSULT THE EVIDENCE BASE

- Doctrine (numbers, implications): `references/context_bloat_evidence.md` sections 1–3.
- Benchmark degradation (RULER/NoLiMa/LongBench effective-vs-claimed windows): Group A.
- Instruction-density collapse (how many rules can a model follow): Group B.
- Token cost economics + prompt caching (prefix stability): Groups C, E3–E5.
- Compaction design (files must survive lossy summarization): Group D.
- Vendor doctrine (minimal core + on-demand retrieval): Groups C, F.

Cite inline as: `[Evidence: context_bloat_evidence.md A2]` (group + entry). Use the entry's URL when the citation must be external.

### Step 4 — PRODUCE THE VERDICT

```
ANTI-BLOAT VERDICT:
- Measured load: [N tokens; delta vs baseline]
- Redundancy scan: [CLEAN / DUPLICATE — cite existing coverage]
- Token delta: [±N bytes/tokens; target size → new size]
- Instruction density: [PASS / FAIL — list dropped sentences]
- Cleanup performed: [list, or "none — no bloat found in target file"]
- Placement: [edit / add / on-demand reference]
- Overall: [APPROVE / REVISE]
```

If REVISE, fix the plan before the change proceeds. This verdict is required for every `.agents/` or opencode.json modification, alongside the Pipeline Config Manager workflow.

### Step 5 — ENFORCE AND PERSIST

- Report the verdict to the user and to the Pipeline Config Manager workflow.
- Update the baseline table (evidence file section 4) when the load changes materially.
- Do NOT wrap new content in "mandatory/always" stacking to compensate for bloat (Control Illusion: precedence declarations add tokens without adding obedience — evidence B3). Fewer, transparent, tested rules outperform sprawling ones.
</audit_workflow>

<lean_doctrine>
## Operational Thresholds (derived from evidence file section 3)

| Rule | Threshold |
|---|---|
| Always-injected load | Keep minimal; any growth >10% of a target file needs justification |
| Effective context | Plan as ~25–50% of the nominal window (A2/A3) |
| Instruction density | Every sentence must be an actionable, non-redundant instruction (B1/B2) |
| Prefix stability | No dates/banners/mutable text at the top of injected files — preserves prompt-cache hits (C4/E3/E4/F5) |
| Position | Put the most critical directives at file ends (recency-stable zone, A5) |
| Compaction survival | Every skill file self-contained; evidence file reloadable post-compaction (D1/F3) |
</lean_doctrine>

<self_mandate>
This skill must stay lean. It is a thin operational wrapper over the evidence file — do not expand doctrine here; expand `references/context_bloat_evidence.md` instead. Any edit to this skill must itself pass the 5-check audit.
</self_mandate>
