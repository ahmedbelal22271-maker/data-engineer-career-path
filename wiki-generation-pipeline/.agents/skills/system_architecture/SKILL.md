---
name: System Architecture
description: Rules for subagent orchestration, error mitigation, and structural limits.
---

# System Architecture & Parallelization

## Compounding Errors & Mitigation
Because AI models simulate reasoning, they are inherently prone to compounding logical errors over long iterations.
- **Do not loop an AI indefinitely.** Iterative loops accumulate mathematical errors until the system completely derails.
- **Continuation Prompts (Recommended):** Instead of looping, drop the error back to zero. Extract only the verified, clean context, start a brand new session, and pass the clean state forward via a Continuation Prompt.
- **Directed Acyclic Graphs (Alternative):** If you cannot use Continuation Prompts, break complex tasks into strict one-way streets (Step A → Step B → Step C) with NO looping back.

## Prerequisites Before Any Parallelization
Before resorting to parallelization or launching multiple subagents, you **must**:
1. Formulate a deeply considered plan. **Do not parallelize uncertainty.** You multiply errors if you parallelize a bad plan.
2. Confirm the task is parallelizable by nature (genuinely independent sub-tasks).
3. Verify that subagents won't fail due to having a partial view of the problem.

## Fail-Fast Rule
- Monitor subagents closely. If they fail or produce bad work, **abandon parallelization immediately**. Fall back to a single, fully-informed agent.

## Subagent Memory Requirements
Every subagent must hold the core protocols in its system prompt to be valid. You must use platform-native subagent definition tools to ensure they inherit the Core OS Kernel (`AGENTS.md`).

## Append-Only Delta Execution
When safely editing massive datasets in parallel, use an event-sourcing / non-destructive delta log pattern. Parallel direct edits on the same DOM or file structure by different subagents are prohibited to prevent overwrite collisions.

## Safe Script Execution (Blind Execution Ban)
Before running any unfamiliar or custom Python/Node script via the terminal, you **must** use `view_file` to check the source code for `sys.argv` or `argparse` requirements. Blindly guessing script arguments results in syntax errors, wasted tool calls, and execution delays.
