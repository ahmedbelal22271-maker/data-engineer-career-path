# Hypothesis-Driven API Reversing: Safe Probing of Undocumented Interfaces

## The Problem With Default Agent Behavior

When an agent encounters an undocumented function, class, or API with no README or type hints, the default failure mode is **confident hallucination**: it pattern-matches against similar APIs it's seen before and guesses argument names/types/order, then either fails loudly (best case) or — worse — succeeds in calling the function with semantically wrong arguments that produce no error but silently incorrect behavior. The fix is to treat the unknown API the same way a scientist treats an unknown system: through structured, minimally invasive, falsifiable probing.

## Core Principle: Probe Before You Use, in an Isolated Harness

Never make the first call to an unknown API as part of the actual task. Always build a small, disposable, isolated script (the "test harness") whose only purpose is to learn the API's actual contract — separate from the main codebase and separate from any process with real side effects (real network calls, real database writes, real file mutations).

## Step 1: Static Reconnaissance Before Any Execution

Before running anything, exhaust the free, zero-risk sources of information:
- **Inspect the source directly**, if available (even compiled/minified code can reveal parameter names via introspection — e.g., Python's `inspect.signature()`, `help()`, or reading the `.pyi` stub file if one exists).
- **Check the type system**, if any exists (TypeScript `.d.ts` files, Python type hints, Java/C# method signatures via reflection) — these often exist even when prose documentation doesn't.
- **Search for usage examples** in the same codebase (other call sites of the same function), in the library's own test suite (often the best "documentation" available), or in its CHANGELOG/commit history for the function's introduction.
- **Check the error messages the library itself produces** — many libraries validate arguments internally and will state the expected type/shape in a raised exception, which is free signal obtainable without correct usage.

Only proceed to active probing once static recon is exhausted and genuine unknowns remain.

## Step 2: Build the Isolated Harness

Requirements for the harness:
- It must run in a context where failure is cheap — a throwaway script, not the production call site. Use a sandboxed/temp environment, a test database, a mock network layer, or a dry-run/sandbox flag if the API offers one.
- It must isolate the single unknown call — no surrounding business logic, no unrelated setup that could confound which input caused which output.
- It must capture *all* output, not just the return value — stdout, stderr, exceptions, and (if possible) any side-channel state changes (did a file get created? a global counter increment?).

```python
# harness.py — disposable, isolated
import traceback

def probe(label, fn, *args, **kwargs):
    print(f"--- {label} ---")
    try:
        result = fn(*args, **kwargs)
        print(f"OK: {result!r}")
        return result
    except Exception as e:
        print(f"FAIL: {type(e).__name__}: {e}")
        traceback.print_exc()
        return None
```

## Step 3: Form a Falsifiable Hypothesis Before Each Probe

Exactly as in root-cause debugging, never probe randomly. Before each call, state explicitly: "I believe this function takes a positional `path` argument and an optional keyword `mode` defaulting to read." Then design the *minimum* probe that would confirm or deny that specific belief — not a maximal probe that exercises five guesses at once (if it fails, you won't know which guess was wrong).

## Step 4: Probe in Order of Increasing Risk

1. **Introspection calls first** (zero risk, no actual invocation): `inspect.signature(fn)`, `fn.__doc__`, `dir(obj)`, reflection APIs. These often answer the question outright without ever calling the function.
2. **Calls with obviously-invalid/empty input** next, specifically to read the validation error (which frequently states the expected shape): calling with `None`, an empty dict, or zero arguments and reading what the library complains about.
3. **Calls with a minimal plausible guess**, on the smallest/safest possible input (e.g., a 1-row dummy dataset, not real production data; a throwaway temp file, not a real one).
4. **Calls that could mutate state** only after the above have established the safe call shape — and only against a sandboxed/disposable target (a temp DB, a mock endpoint), never the real system, until the contract is confirmed.

Never skip ahead to step 4 to "save time" — the entire point of the ordering is that earlier steps are strictly cheaper to get wrong.

## Step 5: One Variable at a Time

If a call fails and there are multiple plausible reasons (wrong arg order? wrong type? missing required kwarg?), change exactly one variable per subsequent probe. Changing several guesses simultaneously after a failure means a success afterward is uninterpretable — you won't know which of the several changes was the actual fix, and the "confirmed contract" you walk away with may be wrong in a way that resurfaces later.

## Step 6: Differentiate "Errored" From "Wrong But Silent"

The most dangerous outcome of probing isn't an exception — it's a call that returns successfully with semantically incorrect behavior (e.g., passing a string where a list was expected, and the library silently treats the string as a single-character list). To catch this:
- Always inspect the *actual returned value/state*, not just whether an exception was raised.
- Where possible, probe with deliberately distinctive input (e.g., a uniquely identifiable sentinel string) so that any silent mishandling is visible in the output rather than blending in with plausible-looking real data.
- If the API has observable side effects, verify the side effect matches expectation (e.g., if probing a "create record" function, query the record back afterward rather than trusting that "no exception" means "created correctly").

## Step 7: Record the Confirmed Contract, Not Just the Working Call

Once a call succeeds with verified-correct behavior, don't just keep the one working invocation — document the actual contract you've now confirmed:

```markdown
## Confirmed: `library.process(data, options=None)`
- `data`: must be a list of dicts, NOT a DataFrame (confirmed via probe 4 — DataFrame
  input silently converted to list of column names, which is wrong)
- `options`: optional dict; confirmed defaults applied when omitted (probe 2);
  unknown keys are silently ignored, NOT validated (probe 6) — typo'd option
  keys will not raise an error
- Returns: list of result dicts, same length as input `data`
- Side effects: none observed (no file/network writes during probe 5)
```

This confirmed-contract block becomes reusable knowledge for the rest of the task (and is exactly the kind of "Confirmed Facts" entry that belongs in the agent's persistent context summary rather than being re-derived later).

## Step 8: Promote Sentinel Probes Into Regression Guards

If the unknown API is going to be used repeatedly through the remainder of the task, keep the minimal probe script that confirmed its contract as a standalone smoke test, not just a disposable scratch file. If the library is later upgraded or the environment changes, re-running this probe cheaply re-validates the assumption rather than silently trusting a contract confirmed under different conditions.

## Common Pitfalls

| Pitfall | Why it's dangerous |
|---|---|
| Probing directly against production data/systems "since it's just a quick test" | Side effects from a wrong-guess probe (a write, a send, a delete) are not actually reversible just because the call was "exploratory" |
| Assuming an API matches a similar-looking API's contract from a different library | Surface-similar APIs (e.g., two different `connect()` functions) frequently differ exactly in the undocumented details that matter |
| Treating "no exception raised" as "correct usage confirmed" | Many APIs fail silently on bad input rather than validating strictly |
| Guessing keyword argument names from convention rather than confirming them | Typo'd or wrong kwargs are silently absorbed by `**kwargs`-based signatures in many languages, producing no error at all |
| Discarding the probe harness after one successful call | Loses the reusable confirmed-contract documentation and the regression-guard value for later |

## Summary Heuristic

Before calling an unfamiliar API for real: can you state, in one sentence, the specific evidence (not assumption) that confirms each argument's type, required/optional status, and the function's actual side effects? If any part of that sentence is "I'm assuming," you haven't finished probing — go back to Step 3 with a hypothesis that targets exactly that gap.
