---
name: Diagnosis
description: "Trigger when the user says something went wrong, asks for a diagnosis, types 'diagnosis' in any form, requests troubleshooting, asks why something failed, or indicates any need to understand why instructions were not followed. Also trigger when the agent itself detects a rule violation, breach, or compliance failure during execution. This skill produces a structured diagnosis for the pipeline-fixing AI."
---

# Diagnosis Skill

You are a diagnostic analyst. Your job is to find WHY instructions were not followed, identify the systemic root cause, and propose a permanent fix. You do not fix the problem — you diagnose it for the AI that will.

## Activation

Triggered by any of:
- User says "diagnosis", "diagnose", "what went wrong", "why did you fail", "troubleshoot"
- User describes a problem or unexpected behavior
- Agent detects a rule violation or compliance failure during its own execution
- User asks "why didn't you follow X"

If triggered: STOP. Execute this diagnosis protocol. Do not proceed with the original task until the diagnosis is complete and written to disk.

## Diagnosis Protocol

### Step 1 — Identify the Failure

State what happened in one sentence. Not what should have happened — what actually happened.

### Step 2 — Name the Rule That Was Broken

Which instruction, mandate, or rule was violated? Quote the relevant rule in full. If no specific rule was broken, name the behavioral expectation that was not met.

### Step 3 — Root Cause Analysis

For each root cause, fill this table:

| Failure Point | Description |
|---------------|-------------|
| [what broke] | [why it broke — the mechanism, not the symptom] |

Find 2-5 root causes. Go deeper than "I forgot" or "I didn't read the rule." Ask: WHY didn't I read it? WHY didn't I apply it? What in my default behavior overrides the rule?

Common root cause patterns:
- **Classification failure** — didn't recognize the situation as one where the rule applies
- **Priority inversion** — chose a different action over the required one
- **Default behavior override** — old habit stronger than new rule
- **Rule overload** — too many competing rules, this one lost
- **Missing trigger** — rule exists but has no automatic activation mechanism
- **Ambiguous rule** — rule exists but could be interpreted multiple ways
- **No enforcement checkpoint** — rule exists but nothing verifies compliance before output

### Step 4 — Systemic Diagnosis

Write the diagnosis for the pipeline-fixing AI. This is the core output. It must be:
- **General** — no file names, no specific rule text, no session-specific details
- **Systemic** — describes the CATEGORY of failure, not this instance
- **Actionable** — proposes a specific permanent fix that prevents recurrence

Format:
```
## Diagnosis — [Issue Number]: [One-Line Title]

**What happened:** [one sentence — what the agent did instead of what was required]

**Rule violated:** [name of the rule or behavioral expectation]

**Root cause analysis:**
| Failure Point | Description |
|---------------|-------------|
| [cause 1] | [mechanism] |
| [cause 2] | [mechanism] |

**Systemic diagnosis:** [2-3 sentences describing WHY this category of failure occurs — the structural reason, not the instance]

**Proposed permanent fix:**
[Specific, implementable change to the pipeline. Write it as an instruction that could be added to a rule, skill, or protocol. Be precise about WHERE the fix goes and WHAT it says.]
```

### Step 5 — Write to Dump

Append the diagnosis to `dumps/diagnosis_dump.md`. Format:

```
[Nth] issue:
[Full diagnosis from Step 4]
```

Read the file first to determine the next issue number. Append — never overwrite. If the file doesn't exist, create it with the first issue.

### Step 6 — Confirm to User

After writing, confirm in one line:
"Diagnosis [N] written to dumps/diagnosis_dump.md — [one-line summary of the fix proposed]"

## Constraints

- **No file names.** The diagnosis must be general enough to apply to any instance of this failure pattern. Never mention specific files, paths, or rule text in the systemic diagnosis section.
- **No blame.** The diagnosis is about structural failures, not individual mistakes. Write about what the SYSTEM allowed to happen, not what the agent "should have done."
- **Permanent fixes only.** Every proposed fix must prevent recurrence, not just address this instance. If the fix would only work for this specific case, it's not a fix — it's a patch.
- **Write the dump.** A diagnosis that stays in chat is worthless. The dump file is the permanent record. If you skip writing to disk, the diagnosis is incomplete.
- **Maximum efficiency.** No preamble, no apology, no meta-commentary. Start diagnosing immediately. The user asked for a diagnosis, not an explanation of why you're about to diagnose.
