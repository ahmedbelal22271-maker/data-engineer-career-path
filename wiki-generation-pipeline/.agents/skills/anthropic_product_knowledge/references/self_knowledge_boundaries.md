# Agent Self-Knowledge: Capability Boundaries and Graceful Tool-Failure Handling

## The Core Problem

An autonomous agent's internal model of "what I can do" frequently drifts from what's actually true — it may believe a tool exists that was deprecated, assume a context budget that's larger than what's actually available, or assume a capability based on a superficially similar tool it used in a different environment. Left unchecked, this produces **confident capability hallucination**: the agent commits to a plan that assumes it can do something it can't, fails partway through, and the failure surfaces far from its root cause (a wrong assumption made at planning time, not at the point of failure). The fix is treating self-knowledge as something to be actively verified and re-verified, not assumed from training-time priors or past sessions.

## Step 1: Verify Tool Capabilities Before Planning Around Them, Not After

Apply the same discipline used for unknown third-party APIs (see hypothesis-driven probing) to the agent's *own* toolset:

- Before building a multi-step plan that depends on a specific tool behavior, confirm that behavior with a minimal, cheap check rather than assuming it from memory of a previous session or a similar tool elsewhere. Environments change between sessions — a tool that existed yesterday may be reconfigured, rate-limited differently, or removed today.
- Distinguish **tool existence** ("is this capability available to me right now, in this environment") from **tool behavior** ("given that it exists, what exactly does it accept/return"). Both need separate verification — a tool can exist but behave differently than the last-seen version.
- If a task plan requires a chain of capabilities (tool A's output feeding tool B), verify the chain's compatibility explicitly (does A's actual output format match what B actually expects?) rather than assuming compatibility because both tools "sound like" they should compose.

## Step 2: Maintain an Explicit, Current Capability Inventory — Not an Assumed One

Rather than relying on an implicit, fuzzy sense of "what I can probably do," maintain a structured, explicitly current inventory that's checked (not just recalled) at the start of any task that depends on it:

```markdown
## Capability Inventory (verified this session)
- tool: file_write — confirmed available; max single-write size: untested, assume conservative until probed
- tool: web_request — confirmed available; confirmed rate limit: 60/min (hit limit once, backed off)
- tool: code_execution — confirmed available; confirmed timeout: 30s per call (one call timed out at exactly this boundary)
- capability: "persistent memory across sessions" — NOT confirmed; treat as unavailable unless explicitly verified for this environment
```

Entries should be marked by *how* they were confirmed (successful use, explicit documentation, or still-unverified-assumption) — an unverified assumption should never be treated with the same confidence as a directly confirmed behavior. This mirrors the "confirmed contract" pattern from API reversing: write down what's actually been verified, not what seems likely.

## Step 3: Treat Context/Resource Limits as Operational Constraints to Track, Not Estimate

An agent that doesn't actively track its own context/resource consumption will discover a limit only by hitting it mid-task, at the worst possible time (e.g., losing the ability to write a final summary because the budget ran out during execution rather than being reserved for it).

- **Reserve budget for wrap-up before starting, not after** — if there's any chance the task might approach a context or time limit, explicitly reserve a portion of the budget for producing a clean handoff/summary, and treat that reserve as off-limits for the main task work. Discovering the limit only when it's already been exceeded means losing the ability to fail gracefully.
- **Track consumption incrementally**, not just at the end — if a budget is genuinely measurable (token count, time elapsed, number of tool calls used against a quota), check it at natural checkpoints throughout the task, not only when something fails.
- **Don't assume a previous session's observed limit still holds** — limits tied to infrastructure, quotas, or configuration can change between sessions; a limit observed once should be treated as "last known," re-verified if there's any sign it might have changed (e.g., an operation that previously succeeded now behaves differently).

## Step 4: Distinguish Tool Failure Types and Respond Differently to Each

A blanket "retry on any failure" or "give up on any failure" policy is wrong for at least one of the following common cases — failures need to be classified before reacting:

| Failure type | Signal | Correct response |
|---|---|---|
| Transient/infrastructure (network blip, rate limit) | Error message indicates timeout, rate limit, or temporary unavailability | Retry with backoff — but cap retry count; don't loop indefinitely on a failure that isn't actually transient |
| Permission/auth failure | Explicit permission-denied or auth-error response | Do NOT retry the same call unmodified — escalate or request the missing credential/permission; retrying identical unauthorized calls wastes cycles and can trigger lockouts |
| Capability genuinely absent (tool doesn't support the requested operation) | Error indicates unsupported operation, not a transient issue | Stop attempting that specific approach immediately; don't disguise the gap by attempting workarounds that produce a similar-looking but semantically wrong result |
| Malformed request (agent's own input was invalid) | Validation error referencing the specific malformed parameter | Fix the specific malformed input and retry once with the correction — but verify the fix addresses the *stated* error, not a guessed one (see the one-variable-at-a-time principle from systematic debugging) |
| Silent partial success (call returns success but output doesn't match expectation) | No error raised, but output shape/content doesn't match what the task needs | Treat as a failure requiring investigation — never proceed downstream on output that "technically didn't error" but doesn't actually satisfy the need; this is the same "wrong but silent" trap as in API probing |

## Step 5: Never Substitute a Workaround That Silently Changes the Task's Meaning

When a genuinely needed capability is absent, the dangerous failure mode isn't stopping — it's *quietly* substituting a different operation that produces superficially similar output but doesn't actually satisfy the original requirement (e.g., a task that needs precise structured data extraction falling back to an approximate guess when the precise tool is unavailable, without flagging that the result is now approximate).

- If a workaround is used because the ideal tool/capability isn't available, state this explicitly in the output, including what's different about the workaround's guarantees compared to what was originally requested.
- If no reasonable workaround exists, report the specific missing capability rather than returning a degraded result framed as if it fully satisfies the original task — an explicit "I can't do X because Y is unavailable" is more useful downstream than a silently-degraded deliverable that looks complete.

## Step 6: Periodically Re-Verify Assumptions During Long-Running Tasks

Self-knowledge gathered at the start of a long task can go stale by the end of it — environment configuration, available quota, or even tool versions can change mid-task in some systems. For tasks long enough that this is plausible:

- Re-check critical capability assumptions at major checkpoints, not just once at the start.
- If a previously-reliable tool starts behaving differently mid-task, treat this as a signal to re-verify rather than assuming the earlier verification still holds and attributing the new behavior to something else.

## Anti-Patterns

| Anti-pattern | Why it fails |
|---|---|
| Assuming a tool's behavior based on a similarly-named tool from a different system/session | Surface-similar tools frequently differ in exactly the details that matter (rate limits, required parameters, output shape) |
| Treating "no error raised" as equivalent to "succeeded correctly" | Misses silent partial-success failures, which are common and dangerous |
| Retrying every failure with identical input | Wastes cycles on permission/capability failures that retrying cannot fix, and can trigger lockouts on auth failures |
| Discovering a context/resource limit only by exceeding it | Loses the ability to reserve budget for a graceful wrap-up; the failure surfaces at the worst possible time |
| Silently substituting a degraded workaround without disclosing the substitution | Downstream consumers (human or agent) treat a degraded result as if it fully satisfies the original requirement |
| Treating a capability verified once as permanently confirmed for all future sessions | Environments and configurations change; stale assumptions reintroduce the exact hallucination problem this protocol exists to prevent |
