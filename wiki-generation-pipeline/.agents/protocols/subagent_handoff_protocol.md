# Subagent Handoff Protocol (Context Compression)

## Purpose
When a parent agent spawns a subagent (or hands off a task), the receiving agent has none of the parent's accumulated context. Dumping the full conversation history is a massive waste of tokens and context limits. The goal of a handoff document is **maximum decision-relevant density, minimum token count**.

## Trigger
This protocol MUST be followed every time the `invoke_subagent` tool is used. The parent agent must create a `handoff.md` file in the workspace or artifact directory, and the prompt to the subagent MUST point to this file.

## Core Principle: Write State, Not Narrative
A handoff doc must read like a structured snapshot, not a diary. Narrative history ("First I tried X, then Y...") wastes tokens recounting dead ends. The subagent needs to know *what is true right now* and *what has already been ruled out*.

## Required `handoff.md` Structure

```markdown
# Handoff: <task name>

## Objective
<One or two sentences. The actual goal, not the means.>

## Current State
<What exists right now, factually. File paths, current values, what's already been built/changed. Not what was attempted — what IS true now.>

## Constraints
<Hard requirements the solution must satisfy. APIs that must be used, versions, performance requirements, things explicitly out of scope.>

## Ruled Out
<Approaches already tried and confirmed NOT to work, with the one-line reason why. This is the highest-value section per token — it prevents the subagent from re-doing failed work.>

## Next Step
<The single most concrete next action. Not a list of options — a decision. If there's genuine ambiguity, state the ambiguity explicitly.>

## Key Files / Locations
<Exact paths, line numbers, function names. Avoid vague references like "the parser module" — use the literal path.>

## Open Risks
<Anything that could silently break downstream. Edge cases noticed but not yet handled, assumptions made that haven't been verified.>
```

## Density Techniques (Token Optimization)
1. **Replace prose with structured fragments:** 
   - *Bad:* "I looked into the auth flow and found token logic is broken."
   - *Good:* `auth/refresh.py:84` — refresh loop doesn't check expiry.
2. **Use file:line references instead of pasted code:** Do not paste full function bodies into the handoff. The subagent has filesystem access. Provide paths and line numbers.
3. **Collapse exploration into conclusions:** If 10 tool calls confirmed a bug, do not list the 10 calls. List the conclusion: "Bug confirmed in `compute_total()`".
4. **Use explicit negative space:** State what was deliberately NOT done so the subagent doesn't assume it was overlooked. ("Did not refactor cache layer - out of scope").

## Multi-Hop Handoffs
If a task chains through multiple subagents (A → B → C), each handoff MUST be regenerated fresh at each hop, summarizing the *current* state. Do not simply forward an old handoff, as the context will be stale.
