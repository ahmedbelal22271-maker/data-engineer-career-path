# OpenCode Agents & Subagents — Complete Official Documentation

> **Source:** https://opencode.ai/agents — retrieved July 2026

---

## Overview

OpenCode uses a multi-agent architecture. The **primary agent** handles most work, while specialized **subagents** are delegated specific tasks. Each agent has its own tools, model, and behavioral instructions.

---

## Agent Types

### 1. General Agent (Default)

The general-purpose agent handles most tasks: code editing, file management, research, debugging, and conversation.

**Default tools:** All 12 built-in tools (bash, read, write, edit, glob, grep, web_search, web_fetch, task, question, todowrite, skill)

**Use for:** Everything that doesn't require a specialized agent.

---

### 2. Code Agent

Optimized for code-heavy tasks: writing functions, implementing features, code review.

**Default tools:** read, write, edit, glob, grep, bash

**Use for:** Implementing features, writing code, refactoring.

---

### 3. Architect Agent

Focused on system design, architecture decisions, and high-level planning.

**Default tools:** read, glob, grep, web_search, web_fetch, question

**Use for:** Designing systems, planning architecture, evaluating tradeoffs.

---

### 4. Explore Agent

Fast codebase exploration. Uses the `big` model for rapid search across large codebases.

**Default tools:** read, glob, grep

**Use for:** Finding files, understanding code structure, answering questions about the codebase.

**Key behavior:** The explore agent is invoked via the `task` tool with `subagent_type: "explore"`. It has a fresh context and relies on detailed prompts.

---

### 5. Debug Agent

Specialized for diagnosing and fixing bugs. Focuses on error analysis and root cause identification.

**Default tools:** read, glob, grep, bash, edit

**Use for:** Investigating errors, analyzing stack traces, fixing bugs.

---

### 6. Frontend Agent

Specialized for frontend/UI work: HTML, CSS, React, Vue, and visual design.

**Default tools:** read, write, edit, glob, grep, bash

**Use for:** Building UI components, styling, frontend architecture.

---

### 7. Ask Agent

Information-only agent. Reads and searches but never modifies files.

**Default tools:** read, glob, grep, web_search, web_fetch

**Use for:** Answering questions, providing explanations, documentation lookup.

---

## Subagent Architecture

### Task Tool Handoff

The primary agent delegates work to subagents via the `task` tool:

```json
{
  "description": "Find auth middleware",
  "prompt": "Search for all files containing authentication middleware in the src/ directory. List each file path, the middleware function name, and what it validates. Be thorough — check for JWT, session, API key, and OAuth patterns.",
  "subagent_type": "explore"
}
```

### Subagent Invocation Pattern

1. Primary agent identifies work suitable for a subagent
2. Primary agent calls `task` with a detailed prompt
3. Subagent executes autonomously with fresh context
4. Subagent returns a single result message
5. Primary agent relays the result to the user

### Fresh Context

Each subagent invocation starts with a **fresh context**. The subagent has no knowledge of the parent conversation. The prompt must be completely self-contained:

- Include all relevant file paths
- Include the specific question or task
- Include any constraints or requirements
- Don't assume the subagent knows what the parent discussed

### Resuming Tasks

Use `task_id` to resume a previous subagent session:

```json
{
  "description": "Continue code review",
  "prompt": "Continue reviewing the remaining files in src/models/",
  "subagent_type": "explore",
  "task_id": "previous-task-id-here"
}
```

---

## Subagent Configuration

### Config-Based Agent Definitions

Define custom agents in `opencode.json`:

```json
{
  "agent": {
    "reviewer": {
      "model": "anthropic/claude-opus-4-6",
      "tools": ["read", "glob", "grep"],
      "instructions": ["docs/review-checklist.md"]
    },
    "security-auditor": {
      "model": "anthropic/claude-sonnet-4-6",
      "tools": ["read", "glob", "grep", "web_search"],
      "instructions": [".opencode/rules/security.md"]
    }
  }
}
```

### Agent Fields

| Field | Type | Description |
|-------|------|-------------|
| `model` | `string` | Model for this agent |
| `tools` | `string[]` | Available tools |
| `instructions` | `string[]` | Additional instruction files |
| `permission` | `string` | Permission mode override |

---

## Subagent CLI Flag

Use `--subagent` to run as a specific agent type:

```bash
# Run as code agent
opencode run --subagent code "implement the login form"

# Run as explore agent
opencode run --subagent explore "find all API endpoints"

# Run as debug agent
opencode run --subagent debug "investigate the timeout error"
```

---

## Concurrency

OpenCode supports concurrent subagent execution:

- Multiple `task` calls in a single message run in parallel
- Each subagent operates independently
- Results are collected and returned to the primary agent
- The primary agent waits for all parallel tasks to complete before proceeding

```python
# Pseudocode — this runs both tasks in parallel:
task(explore, "find all database queries")
task(explore, "find all API routes")
# Both complete before primary agent continues
```

---

## Agent-Specific Instructions

Each agent can have its own instruction files. These are loaded on top of the global instructions.

```json
{
  "agent": {
    "debugger": {
      "instructions": [
        "docs/debugging-playbook.md",
        ".opencode/rules/debug-rules.md"
      ]
    }
  }
}
```

Agent-specific instructions take precedence over global instructions when there's a conflict.

---

## When to Use Each Agent

| Scenario | Recommended Agent |
|----------|-------------------|
| Implement a new feature | `code` or `general` |
| Fix a specific bug | `debug` |
| Understand codebase structure | `explore` |
| Design system architecture | `architect` |
| Review code quality | `general` with review instructions |
| Build UI components | `frontend` |
| Answer a question | `ask` |
| Complex multi-step task | `general` |
| Fast codebase search | `explore` |

---

## Best Practices

1. **Be specific in prompts** — Subagents have no context; include everything they need
2. **Use explore for search** — It's optimized for fast codebase exploration
3. **Use general for complex work** — It has access to all tools
4. **Parallelize independent tasks** — Send multiple `task` calls in one message
5. **Resume long tasks** — Use `task_id` to continue interrupted work
6. **Match agent to task** — Don't use a sledgehammer for a nail
