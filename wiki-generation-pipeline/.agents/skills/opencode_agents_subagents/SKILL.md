---
name: opencode Agents & Subagents
description: Complete reference for opencode's subagent architecture — all 7 built-in agent types (general, code, architect, explore, debug, frontend, ask), their code names, default tool access, configuration in opencode.json, the task tool handoff protocol, --subagent CLI flag usage, agent-specific instructions, and concurrency. Trigger on "subagent", "agent type", "delegation", "which agent", "task tool", or multi-agent workflow questions.
---

## 1. Overview

opencode uses a subagent architecture where the main session AI delegates tasks to specialized subagents. Each subagent is an independent execution context with its own model selection, tool permissions, system instructions, and context window. The main agent orchestrates by spawning subagents via the `task` tool, collecting their results, and continuing its own reasoning.

This separation of concerns enables:
- Specialized tool access per task type
- Independent context windows (no cross-contamination)
- Parallel execution of independent subtasks
- Model tiering (use cheaper/faster models for simple subtasks)

## 2. Built-in Agent Types

| Agent | Code | Default Tools | Best For |
|-------|------|---------------|----------|
| general | `general` | All tools | Default agent, fallback for everything. Used when no specific agent matches the task. |
| code | `code` | All except `web_search`/`web_fetch` | Feature implementation, refactoring, bug fixes. Focused on local codebase work. |
| architect | `architect` | `read`/`glob`/`grep`/`question`/`todowrite`/`task`/`web` | System design, planning, architectural decisions. Design-only mode — no write access. |
| explore | `explore` | `read`/`glob`/`grep`/`bash` | Quick searches, finding files, understanding codebase structure. Lightweight and fast. |
| debug | `debug` | All tools | Root cause analysis, error investigation, debugging sessions. Full access to reproduce issues. |
| frontend | `frontend` | All tools (specialized for UI) | HTML/CSS/JS/React work, visual design, UI components. Skills-aware for frontend patterns. |
| ask | `ask` | `web_search`/`web_fetch`/`read`/`glob`/`grep` | Q&A, documentation lookup, research, learning. No write or execute — read-only investigation. |

## 3. Agent Configuration in opencode.json

Agents are configured under the `"agents"` key in `opencode.json`. Each entry uses the agent code name as its key and overrides specific properties.

```jsonc
{
  "agents": {
    "code": {
      // Model alias — references a model in "models" section
      "model": "reasoning",
      // Tool access overrides
      "tools": { "allow": ["*"], "deny": ["web_search"] },
      // Custom instruction files loaded into agent context
      "instructions": [".agents/code_standards.md"],
      // Token budget for this agent's responses
      "max_tokens": 16384,
      // Temperature override for generation
      "temperature": 0.3
    },
    "explore": {
      "model": "fast",
      // Explicit allowlist — only these tools are available
      "tools": { "allow": ["read", "glob", "grep", "bash"] },
      "max_tokens": 4096,
      "temperature": 0.5
    },
    "frontend": {
      "model": "reasoning",
      // Skills loaded automatically when this agent is spawned
      "skills": [".agents/skills/html_css_generation/SKILL.md"]
    }
  }
}
```

**Field reference:**

- **model** — References an alias defined in the `"models"` section. Controls which LLM powers the agent (see opencode_models_providers).
- **tools** — Object with `allow` (whitelist) and `deny` (blacklist) arrays. `"allow": ["*"]` grants all tools; explicit lists restrict access. Deny takes precedence over allow.
- **instructions** — Array of file paths loaded as system instructions when the agent starts. Used for project-specific rules and standards.
- **max_tokens** — Maximum tokens in the agent's response. Controls output length budget.
- **temperature** — Float controlling randomness. Lower values produce more deterministic output; higher values increase creativity.
- **skills** — Array of skill file paths loaded into the agent's context. Skills provide domain-specific knowledge and workflows (see opencode_skills_framework).

## 4. Subagent Handoff Protocol (task Tool)

The `task` tool is the mechanism for delegating work from the main agent to a subagent.

**Handoff steps:**

1. Main agent creates a task with a clear description, a self-contained prompt, and the `subagent_type` (agent code name).
2. The system spawns the subagent as a new execution context with its own tool access, model, and instructions.
3. The subagent executes independently — it can read files, run tools, and produce output without parent interference.
4. The subagent returns a single result message to the parent.
5. The parent agent receives the result and continues its reasoning.

**Best practices:**

- **Be self-contained** — The subagent has no access to the parent's conversation history. Include all necessary context in the prompt.
- **Set explicit output expectations** — Tell the subagent exactly what format and content you need back.
- **Don't delegate trivial work** — The tool call and context setup have overhead. For single-file reads or simple lookups, do it directly.
- **Parallelize independent subtasks** — Spawn multiple subagents simultaneously when tasks don't depend on each other. Results are merged by the parent.

## 5. --subagent CLI Flag

The `--subagent` flag starts an opencode session with a specific agent type:

```bash
# Start with explore agent for codebase investigation
opencode --subagent explore "find all API routes in the project"

# Start with architect for design review
opencode --subagent architect "review the database schema and suggest improvements"

# Start with ask agent for research
opencode --subagent ask "what is Apache Spark and how does it compare to Hadoop?"
```

This is useful for one-off tasks where you know which agent type is most appropriate, bypassing the main agent's routing decision.

## 6. Agent Concurrency

- **Configuration** — Set via `agent_concurrency` in `opencode.json`. Controls the maximum number of subagents that can run simultaneously.
- **Shared context** — Parallel subagents share the parent's context but not each other's. Each gets a snapshot of the parent's state at spawn time.
- **Independent execution** — Subtasks that don't depend on each other run simultaneously. The parent can issue multiple `task` calls in one step.
- **Result merging** — When parallel subagents complete, their results are collected and presented to the parent agent for synthesis.

## 7. Agent-Specific Instructions

Each agent can have custom instructions loaded via the `instructions` field in its configuration. When a subagent is spawned, it receives its configured instructions as part of its system context.

Instructions can reference:
- Project-specific coding standards and conventions
- Domain knowledge files
- Custom workflow rules
- Skill files via the `skills` field

This means a `code` agent can have strict linting rules injected, while an `architect` agent gets system design guidelines — all configured per-agent in `opencode.json`.

## 8. Architect and Explore Tool Restrictions

**Architect agent** — By default has no write or execute access. This enforces a design-only mode where the architect can read the codebase, analyze structure, and produce plans without accidentally modifying files. Tools like `bash`, `write`, and `edit` are excluded from its default set.

**Explore agent** — Restricted to lightweight, read-only tools (`read`, `glob`, `grep`, `bash` with caveats). This ensures fast responses and prevents any state mutations during investigation. It is optimized for speed — searching, locating, and summarizing.

These restrictions are design choices that prevent accidental modifications and ensure agents operate within their intended scope. They can be overridden in `opencode.json` configuration if needed.

## Full Documentation
For the complete official opencode agents and subagents documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of all 7 agent types, configuration, task tool handoff, CLI flags, concurrency, and agent-specific instructions.

**Cross-references:**
- **opencode_configuration** — Model alias definitions referenced by agent `model` fields
- **opencode_tools_catalog** — Full tool catalog including `task` tool specification
- **opencode_models_providers** — Model selection strategies for per-agent tiering
- **opencode_skills_framework** — Skill loading mechanism used by agent `skills` field
- **opencode_decision_trees** — Decision flowchart for selecting the right agent type
