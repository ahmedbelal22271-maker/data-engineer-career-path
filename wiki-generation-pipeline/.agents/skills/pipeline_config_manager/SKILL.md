---
name: Pipeline Config Manager
description: "Loads when the user expresses ANY intent to change, add, remove, or reconfigure ANY system file under .agents/ — including AGENTS.md, rules, skills, protocols, workflows, root-level files (brain.md, aim.md, init prompts), opencode.json, registers, or injection templates. Also triggers for audits of current pipeline configuration state, token budget analysis, or config reviews. This is the default entry point for ANY system-file modification — if the user wants to change how the pipeline behaves, this skill handles the full workflow: plan mode entry, config state analysis, mandatory web research, structured plan-agent prompt, orchestrator-subagent adversarial debate (self-critique → independent positions → bidirectional cross-critique → structured rebuttal → convergence verification → failure recovery), clarification, and a final implementation plan with both-analyses presentation and resolution trail."
---

<activation_self_check>
Before processing ANY system file modification, verify:
1. Loaded via `skill` tool (not read directly or injected via instructions)?
2. User modifying a file under `.agents/` or `opencode.json`?
3. Plan Mode entered before any changes?

ALL YES → proceed. ANY NO → HALT. Load via `skill(name: "Pipeline Config Manager")` and re-read.

Not loaded via skill tool → BREACH. HALT and report: "Must be loaded via skill tool for .agents/ modifications."

Skipped Step 4 (stress-test) → HALT. Stress-test mandatory even for one-line edits. Run it.

Skipped Step 4a (orchestrator self-critique) → HALT. Orchestrator MUST critically analyze its own demand before engaging the sub-agent. Self-critique is the foundation of the debate — without it, the orchestrator has no independent position and defaults to accepting the sub-agent's framing.

Skipped Step 4g (failure recovery) → HALT. When sub-agent fails, orchestrator MUST follow the Failure Recovery Protocol — classify the failure, retry once if transient, escalate to user if terminal. Self-debating or inventing what the sub-agent "would have said" is FORBIDDEN.

Skipped Step 2d (web research) for instruction file modification → HALT. Web search is MANDATORY before modifying any `.agents/` file. Only trivial edits (typo fixes, formatting) are exempt. Document search queries and findings.

Skipped Step 5 (clarifying questions + final plan) → HALT. Never implement without presenting plan to user first.
</activation_self_check>

# Pipeline Config Manager

**You are the plan agent.** This skill gives you a rigid 5-step workflow. You do NOT spawn a "plan agent" — you ARE the plan agent. You are also a critical thinker with your own sophisticated analysis — you do not passively accept the sub-agent's framing. The only subagent you spawn is the explore subagent for the adversarial debate in Step 4.

---

## System File Taxonomy

| # | File Type | Location | Load Mechanism | Index File | Blast Radius |
|---|-----------|----------|----------------|------------|-------------|
| 1 | AGENTS.md | `.agents/AGENTS.md` | Every session (via instructions) | None | EVERY session |
| 2 | Rules | `.agents/rules/*.md` | Every session (if in instructions array) | None | EVERY session |
| 3 | Skills | `.agents/skills/*/SKILL.md` | On-demand (skill tool) | `.agents/skills/index.md` | Only when invoked |
| 4 | Protocols | `.agents/protocols/*.md` | On-demand (manual read) | `.agents/protocols/index.md` | Only when invoked |
| 5 | Workflows | `.agents/workflows/*.md` | On-demand (manual reference) | None | Only when invoked |
| 6 | Root-level files | `.agents/brain.md`, `aim.md`, `init*.md` | Varies (init injection, session bootstrap) | None | EVERY session |
| 7 | Injection templates | `.agents/injection_templates/*.md` | On-demand (CCMP invocation) | None | Only when invoked |
| 8 | Registers | `.agents/registers/*.md` | On-demand (manual reference) | None | Only when invoked |
| 9 | opencode.json | Project root (not under .agents/) | Always (config loaded by runtime) | N/A | EVERY session |

---

## Trigger Conditions

Activates on any natural-language request implying "I want to alter what opencode knows, loads, or follows."

| Intent | Examples |
|--------|----------|
| Adding behavior | "add a mandate that...", "make a rule that...", "we need a new instruction for..." |
| Modifying behavior | "modify the rule about...", "change the instruction that...", "the current rule about X is wrong" |
| Removing behavior | "remove the rule about...", "we don't need the instruction for...", "stop loading the skill that..." |
| Creating skills | "I need a skill for...", "turn this into a skill..." |
| Creating protocols | "add a new protocol for...", "we need a protocol that..." |
| Editing root files | "update brain.md", "change the init prompt", "modify aim.md" |
| Config changes | "update opencode.json", "change what loads at session start" |
| Auditing | "what's currently loaded?", "review our instructions" |
| Behavioral gaps | "I need [X] to happen automatically", "the agent keeps forgetting to..." |

---

## Mandatory Workflow — 5 Steps

This workflow is rigid. Every step must complete before the next begins.

### Step 1 — Enter Plan Mode

Declare plan mode before any file reading or modification:

```
PLAN MODE: ACTIVE
Objective: [one-sentence summary]
Scope: [which files/systems affected]
File type: [which of the 9 types from taxonomy]
```

Ambiguous request → ask for clarification BEFORE declaring plan mode. Plan mode requires a clear objective.

Once declared, file reading is permitted for composing Step 3's Context and Config state fields.

### Step 2 — Analyze opencode.json Config State

Read `opencode.json` at project root. Record current state:

```
CONFIG STATE SUMMARY:
- Instructions loaded: [N] files
  1. [path] — [purpose]
  2. [path] — [purpose]
  ...
- Skills paths: [directories listed]
- Agents config: [present/absent]
- Total estimated tokens: ~[X]

Does the proposed change affect this config?
- YES → what type: [add/remove instruction / config edit]
- NO → proceed with file-only change
```

#### Step 2d — Web Research (MANDATORY for instruction file modifications)

Before modifying ANY instruction file under `.agents/` (AGENTS.md, rules, skills, workflows, root-level files, opencode.json), you MUST execute live web searches and document the findings. This is not optional — most problems have already been solved, and skipping search means reinventing the wheel with your training data alone.

**Required searches (at minimum):**
1. Search for `[topic] best practices [current year]` — find what the community recommends
2. Search for `[tool/framework] agent instructions patterns` — find proven instruction patterns
3. Check at least ONE authoritative source: official documentation, vendor blog, or community reference with community validation (upvotes/stars)

**Required documentation (append to Step 2):**
```
WEB SEARCH LOG:
- Query 1: "[exact query]" → [source found: URL or "no relevant results"]
- Query 2: "[exact query]" → [source found: URL or "no relevant results"]
- Authoritative source checked: [URL] — [what it confirmed or contradicted]
- Findings applied: [list specific changes made to the plan based on search results]
- Search NOT performed: [if truly trivial edit, state why — e.g., "typo fix, no design decision involved"]
```

**Verification checkpoint:** Before proceeding to Step 3, confirm at least ONE search was executed and documented. If no search was performed and no trivial-edit exception applies, HALT and run the search.

**Exception — truly trivial edits only:** Typo fixes, formatting changes, and whitespace corrections do not require web search. State "TRIVIAL EDIT EXCEPTION" and proceed.

#### Step 2e — Anti-Context-Bloat Audit (MANDATORY for instruction file modifications)

Context bloat degrades reasoning (LLM attention budget depletes per token; "context rot" degrades performance as input length grows; "lost-in-the-middle" drops accuracy 30%+ when instructions sit mid-context) and multiplies cost (the system prompt is the largest fixed cost, paid on every call; every injected token is re-sent to every session and every parallel subagent). Sources: [AWS Well-Architected AGENTCOST02-BP02](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentcost02-bp02.html), [IETF draft-chang-agent-token-efficient](https://datatracker.ietf.org/doc/draft-chang-agent-token-efficient/02), [Lean System Prompts (AgenticSkillset)](https://agenticskillset.org/en/topics/lean-system-prompts/), [Zylos Research context management](https://zylos.ai/research/2026-01-19-llm-context-management). This pipeline's injected instructions total ~158 KB (~39,500 tokens/session, measured 2026-08-05; full baseline in `context_bloat_audit/references/context_bloat_evidence.md` section 4) — every addition is a tax on every session.

Before finalizing the plan, run all five checks:

1. **Redundancy scan** — grep the injected instruction set (opencode.json `instructions`) for the proposed content's key phrases. If the behavior is already covered elsewhere, do NOT add it — reference the existing file instead.
2. **Token-delta estimate** — record the target file's byte count before/after the change and report the delta in the plan. Flag any growth >10% of the target file unless the plan justifies it.
3. **Instruction-density test** — each added sentence must (a) not repeat existing content, (b) state an instruction rather than narrate why, (c) map to a concrete behavioral change you can name. Delete sentences that fail any criterion.
4. **Cleanup obligation** — when editing a file, scan it for existing bloat (repeated, defensive, or narrative sentences with no enforcement value) and compress them in the same edit. EXCEPTION: retain emphasis repetition on rules known to be violated (e.g., the web-search mandate) — that repetition is enforcement, not bloat, and removing it risks regressions.
5. **Placement preference** — edit > add; on-demand (skill/protocol) > every-session instruction; reference > inline paste. If the change belongs in an on-demand file, do not add it to AGENTS.md or the instructions array.

Produce the verdict before proceeding to Step 3:

```
ANTI-BLOAT VERDICT:
- Redundancy scan: [CLEAN / DUPLICATE — cite the existing coverage]
- Token delta: [±N bytes/tokens; current target size → new size]
- Instruction density: [PASS / FAIL — list dropped sentences]
- Cleanup performed: [list, or "none — no bloat found in target file"]
- Placement: [edit / add / on-demand reference]
- Overall: [APPROVE / REVISE]
```

If overall is REVISE, fix the plan before proceeding. This audit applies to the current file being edited AND to future files: the behavior is permanent.

### Step 3 — Write the Structured Prompt

Fill every field with specificity. Vague fields produce vague plans.

```
I need to [add/modify/remove] a [file type] to [file path].

Context: [what this pipeline does, what the file is for, what triggers it]
Config state: [from Step 2 — what's currently loaded, config impact]

My demand: [exactly what you want implemented]
```

- `[add/modify/remove]` — exact operation
- `[file type]` — one of: rule, skill, protocol, workflow, root-file, register, injection-template, config, or "AGENTS.md"
- `[file path]` — target file, or "new file at [path]"
- `Context` — pipeline purpose, file purpose, trigger conditions, why it exists
- `Config state` — from Step 2. Include only if change affects config.
- `My demand` — exactly what you want. Be precise. Leave nothing to interpretation.

### Step 4 — Orchestrator-Subagent Adversarial Debate

**This is a structured debate between two co-equal critical thinkers — you (the orchestrator) and the sub-agent. You are NOT a passive recipient of the sub-agent's feedback. You are an equal participant with your own sophisticated critical analysis. The sub-agent is NOT the authority — both of you challenge each other until genuine resolution is reached.**

**4a. Orchestrator Self-Critique (MANDATORY — before spawning anything)**

Before engaging the sub-agent, you MUST critically analyze your own demand. This is not optional — it is the foundation of the debate. You must have a sophisticated, defensible position BEFORE the sub-agent sees anything.

Write your self-critique using this structure:

```
ORCHESTRATOR POSITION:
- Demand: [your exact demand from Step 3]
- File choice rationale: [why this file type and path, not alternatives]
- Blast radius assessment: [which sessions/agents affected, token impact]
- Minimum viable change: [what's the smallest change that achieves the goal]

ORCHESTRATOR KNOWN WEAKNESSES:
1. [strongest objection to your approach — what could be wrong]
2. [second-strongest objection]
3. [assumption you're making that might be invalid]

ORCHESTRATOR PRE-EMPTIVE RESPONSES:
- If sub-agent challenges [weakness 1]: [your evidence-based counter]
- If sub-agent challenges [weakness 2]: [your evidence-based counter]
```

**Why this exists:** An orchestrator that hasn't critically analyzed its own demand cannot engage in a meaningful debate. Without this phase, you default to accepting whatever the sub-agent says — which is exactly the failure mode we're eliminating.

**4b. Independent Position Generation**

Both parties reason independently BEFORE seeing each other's output. This prevents anchoring bias — the first agent's framing must not anchor the second.

- **Orchestrator's position:** Already written in 4a. This is your independent analysis.
- **Sub-agent's position:** Spawn the explore subagent via `task` tool with `subagent_type: "explore"`. The task prompt contains ONLY:
  - The `Context` field from Step 3
  - The `Config state` field from Step 2
  - The user's ORIGINAL raw request (not your demand, not your framing)
  - The instruction: "Produce your independent analysis. What file type and path should be modified? What's the change? What are the risks? What alternatives exist?"
  - **DO NOT include your `My demand` field, your position, or your self-critique.** The sub-agent must reason from the raw problem, not from your solution.

The sub-agent produces its own `SUB-AGENT POSITION` with: recommended file, recommended change, risks, alternatives, blast radius assessment.

**4c. Cross-Critique Round 1**

Now each party receives the other's independent position and challenges it. This is bidirectional — both must challenge, not just the sub-agent.

**Orchestrator's challenge of sub-agent's position:**
Read the sub-agent's output. For each recommendation, ask:
- "Does this conflict with any existing rule, skill, or protocol? Cite specifics."
- "Is the sub-agent's file choice justified, or did it miss a better alternative?"
- "Is the blast radius assessment accurate? What did it miss?"
- "Does the sub-agent's approach achieve the user's goal, or does it solve a different problem?"
- Produce: `ORCHESTRATOR CHALLENGES` (numbered list, each with evidence)

**Sub-agent's challenge of orchestrator's position:**
Send the sub-agent your full `ORCHESTRATOR POSITION` + `ORCHESTRATOR KNOWN WEAKNESSES` from 4a. Add: "Challenge this position. Identify gaps, conflicts with existing rules, wrong assumptions, and alternatives. Be specific — cite rule names, file paths, config entries."

The sub-agent produces: `SUB-AGENT CHALLENGES` (numbered list)

**4d. Rebuttal Round**

Each party responds to the specific challenges raised. No hand-waving — every challenge must be addressed.

**Orchestrator's rebuttal:**
For each `SUB-AGENT CHALLENGE`, you MUST either:
- **Concede:** "Challenge [N] is valid. I revise my position: [how the position changes]."
- **Rebut with evidence:** "Challenge [N] is incorrect because [specific evidence from existing rules/skills/config]. Citing: [exact rule name, file path, line number, or config entry]."

**Sub-agent's rebuttal:**
Send the sub-agent your `ORCHESTRATOR CHALLENGES`. Add: "For each challenge above, either concede and revise your position, or rebut with specific evidence. Cite rule names, file paths, or config entries."

The sub-agent produces: `SUB-AGENT REBUTTALS` (numbered, each marked CONCEDE or REBUT with evidence)

**4e. Convergence Verification**

Convergence requires ALL of the following. If any fail, the debate is not converged:

```
CONVERGENCE CHECKLIST:
□ Both parties agree on exact file type and path
□ Both parties agree on exact change content
□ Both parties agree on config impact (if any)
□ Every SUB-AGENT CHALLENGE has been addressed (conceded or rebutted with evidence)
□ Every ORCHESTRATOR CHALLENGE has been addressed (conceded or rebutted with evidence)
□ No open questions remain
□ Blast radius is agreed upon by both parties
```

**If convergence fails after 2 full rounds (4c + 4d repeated twice):** HALT the debate. Present both positions to the user in Step 5 with a tiebreak request. Do NOT force convergence — deadlocks mean the problem has genuine tradeoffs that require human judgment.

**If convergence succeeds:** Record the final agreed position. Both parties' positions are now the validated design.

**4f. Kill the subagent**

Terminate the subagent. Do not leave it running.

**4g. Failure Recovery Protocol**

If the sub-agent returns empty output, errors, or "no provider available" — do NOT start self-debating. Follow this structured recovery:

```
FAILURE CLASSIFICATION:
- TRANSIENT: sub-agent returned empty or timed out, but the task is well-formed
- TERMINAL: sub-agent failed after retry, or returned nonsensical output
- PARTIAL: sub-agent returned output but with critical gaps (missing analysis steps)

RECOVERY ACTIONS:
TRANSIENT → Retry ONCE with a simplified prompt:
  - Strip non-essential context
  - Keep only: Context field, Config state field, raw user request
  - Add: "CRITICAL: You MUST produce a complete SUB-AGENT POSITION. Do not return empty."
  - If retry succeeds → continue to 4c
  - If retry fails → classify as TERMINAL

TERMINAL → Escalate to user in Step 5:
  - Present YOUR analysis (from 4a) as the sole basis for the plan
  - State: "Sub-agent failed ([error class]). Proceeding with orchestrator-only analysis."
  - Ask user to confirm or adjust
  - Do NOT attempt a third retry — two failures means the task prompt is the problem

PARTIAL → Proceed with sub-agent's partial output:
  - Fill the gaps with your own analysis
  - Note which parts came from the sub-agent vs. your own reasoning
  - Present to user with the gap annotations
```

**FORBIDDEN BEHAVIOR:** If the sub-agent fails, you MUST NOT:
- "Debate yourself" — generating both positions internally and then pretending a debate happened
- Invent what the sub-agent would have said
- Skip the debate entirely and proceed with your own analysis without disclosing the failure
- Keep retrying beyond one retry — repeated failures indicate a prompt problem, not a transient issue

### Step 5 — Ask Clarifying Questions + Return Final Plan

**5a. Clarifying questions**

After killing the subagent, present BOTH the orchestrator's and sub-agent's analyses to the user. Show:
1. **Where they agreed from the start** — consensus points (these are low-risk, high-confidence)
2. **Where they disagreed** — and how the disagreement was resolved (conceded or rebutted)
3. **What the orchestrator conceded** — what the sub-agent's challenge changed in the orchestrator's thinking
4. **What the sub-agent conceded** — what the orchestrator's challenge changed in the sub-agent's thinking
5. **Any remaining open questions** — questions neither party could resolve, requiring user judgment

If Step 4g triggered (sub-agent failed), present your orchestrator-only analysis with the failure disclosure: "Sub-agent failed ([error class]). The following is the orchestrator's independent analysis. Please review and confirm or adjust."

Then ask about ambiguities. Include config-specific questions:

- "Should this be loaded every session (instruction) or on-demand (skill)?"
- "Are you aware this adds ~[X] tokens to every session?" (if adding to instructions)
- "Should any existing instruction be removed to make room?" (if adding to instructions)

Do NOT proceed until user answers all questions.

**5b. Return the final implementation plan**

After convergence and clarification, produce the final deliverable:

```
FINAL IMPLEMENTATION PLAN:

## File Changes
## 1. [FILE PATH] — [ACTION: create/modify/delete]
   - Insertion point: [exact line number, section header, or "new file"]
   - Content: [verbatim content to insert, or exact oldString → newString]

## 2. [FILE PATH] — [ACTION: create/modify/delete]
   - Insertion point: [exact location]
   - Content: [exact content]

## opencode.json Changes (if applicable):
- instructions: [add/remove] "[exact path]" at position [N]
  - Current array: [list current entries]
  - New array: [list with proposed change]
  - Token impact: +~[X] tokens/session (current: ~[Y], new total: ~[Z])
  - Ordering rationale: [why this position]
- skills.paths: [no change / add "[path]"]
- agents: [no change / add/modify]

## Blast Radius:
- [Which sessions/agents affected]
- [Token cost change if any]

## Index Updates Needed:
- [Which index files need updating with exact entries]

## Verification:
1. [exact command or check]
2. [expected result]
```

Present plan to user for approval. If rejected, return to Step 3 with revised demand. Step 4 repeats if change is substantial.

---

## Decision Tree — Where Does This Change Go?

**Every session + hard rule (always/never):** AGENTS.md
**Every session + soft rule:** New .md file in opencode.json instructions array
**Task-specific + repeatable process:** Skill (.agents/skills/*/SKILL.md)
**Task-specific + repeatable process (deprecated):** Protocol (.agents/protocols/*.md)
**Task-specific + one-off process:** Workflow (.agents/workflows/*.md)
**Root files:** brain.md, aim.md, init prompts — special handling

**Config impact:**
- New instruction file → add to instructions array
- New skill directory → skills.paths (auto-discovered, no config change)
- New protocol/workflow → no config change (on-demand)
- New agent → agents object
- Just a file edit → no config change

**Index updates:**
- Skill created → `.agents/skills/index.md`
- Protocol created → `.agents/protocols/index.md`
- AGENTS.md modified → verify references still resolve
- Config modified → verify JSON validity

**Blast radius:**
- opencode.json instructions → EVERY session, ALL agents
- AGENTS.md → EVERY session
- A rule in instructions → EVERY session
- brain.md / init prompts → EVERY session (via initialization)
- A skill → Only when invoked
- A protocol → Only when invoked (deprecated)
- A workflow → Only when invoked
