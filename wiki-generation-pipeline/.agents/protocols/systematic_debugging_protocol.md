# Systematic Root-Cause Debugging Protocol

## Purpose
To prevent the agent from entering a "Guess and Check" loop when encountering failing tests or runtime errors. This protocol mathematically guarantees root-cause isolation by forbidding speculative patching and enforcing probe-based verification.

## Trigger
This protocol MUST be executed immediately if a test fails or an error occurs 2+ times in a row after a code change was made.

## Phase 1: SEIUP Error Tracking (Detection)
1. Log the error in `error_tracking.json` using the standard SEIUP format.
2. If the Error ID matches a previously logged error, the "Guess and Check" loop is officially detected. Proceed to Phase 2.

## Phase 2: The 7-Step Isolation Framework

### Step 1: Freeze and Read
- **STOP making code changes.**
- Re-read the FULL error output, not just the truncated snippet.
- Identify: what was *expected* vs what *actually happened*. State this as a one-line delta.

### Step 2: Reproduce Minimally
- Reduce the failing case to the smallest possible reproduction: fewest lines, fewest dependencies, fewest inputs.
- If minimization is expensive, binary-search it by commenting out half the logic.

### Step 3: Form a Single Falsifiable Hypothesis
- State ONE specific hypothesis (e.g., "function X returns None when input list is empty").
- It must be falsifiable with one targeted check.

### Step 4: Verify Before Fixing (The Probe)
- Write a probe: a `print()`, `console.log()`, or `assert` statement that confirms or denies the hypothesis directly.
- Run ONLY that probe. **Do not bundle the probe with a speculative fix.**
- If the probe disproves the hypothesis, return to Step 3. Do not "fix" something unconfirmed.

### Step 5: Trace Backward From Failure Point
- Once the immediate cause is confirmed (e.g., "X is None"), do not stop. Ask *why* X is None. Walk the call chain backward.
- Stop only when you hit a genuine boundary/edge case in input data, or an actual logic error in assumptions.

### Step 6: Make the Smallest Correct Fix
- The fix should map 1:1 to the confirmed root cause. No broad defensive changes.
- Do NOT wrap failing lines in try/except blocks to suppress errors unless the exception is genuinely expected and recoverable.

### Step 7: Confirm With Regression Check
- Re-run the minimal reproduction case to confirm the fix.
- Re-run the broader test suite to ensure adjacent behavior wasn't broken.

## Escalation Path
If the bug is still unresolved after 2 full passes through Phase 2:
1. Re-state the problem from scratch in one paragraph.
2. Check upstream dependencies, configs, or environment differences.
3. Search project history for regressions.
4. If blocked, document all falsifiable hypotheses tried and ruled out in a `handoff.md` file before terminating or requesting help.
