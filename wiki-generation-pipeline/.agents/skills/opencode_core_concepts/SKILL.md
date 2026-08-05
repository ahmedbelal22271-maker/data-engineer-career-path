---
name: opencode Core Concepts
description: Foundational understanding of opencode — what it is, its architecture, the two operational modes (Plan vs Auto), session lifecycle, project structure, and how skills/rules/instructions/agents/tools relate. Trigger on "what is opencode", "how does opencode work", "opencode architecture", or conceptual overview questions.
---

## 1. What is opencode?
- Agentic AI coding assistant that runs in the terminal
- Combines LLMs with tools (file read/write, shell execution, web search, subagent delegation)
- Performs software engineering tasks autonomously or interactively

## 2. Architecture
- Stateless per-turn: each conversation turn is independent, no state across sessions
- State lives in files on disk (code, config, plans)
- Session starts by reading opencode.json, loading instructions/skills/rules, then launching TUI or executing script

## 3. Two Operational Modes
- **Plan Mode** (READ-ONLY): analyzes, explores, proposes but never modifies files. For high-risk/complex/unclear tasks.
- **Auto Mode** (READ-WRITE): full tool access. For routine/well-understood tasks.
- How to switch: `/plan` command in TUI, `--subagent` flag

## 4. Project Structure
```
.opencode/
  rules/        # Always/Ask/Never rule files
  plans/        # Plan files for Plan Mode
  node_modules/ # Dependencies
  package.json  # Project metadata
opencode.json   # Main config (or opencode.jsonc)
```

## 5. Skills vs Rules vs Instructions vs Agents

| Mechanism | Scope | Persistence | When to use |
|-----------|-------|-------------|-------------|
| AGENTS.md | Entire project | File on disk | Always-on behavioral rules |
| .opencode/rules/ | Tool-level | File on disk | Per-tool permissions |
| skills/SKILL.md | Task-triggered | File on disk | Specialized knowledge on demand |
| Inline | Single turn | Sent in message | One-off tasks |
| Subagents | Single task | Created per task | Delegating work |
| MCP tools | External service | Config entry | Databases, APIs, external systems |

## 6. How Skills Work
- Skills have YAML frontmatter with `name` and `description`
- The `description` is used for trigger matching — when a user's request semantically matches, the skill loads
- Skills inject specialized instructions into context
- Cross-reference: see also `opencode_skills_framework` skill for details

## 7. Tips
- Long instruction files consume context window — keep lean
- Rules cannot be overridden by the model
- Use Plan Mode for anything destructive or unclear
- Use Auto Mode for routine work

## Full Documentation
For the complete official opencode documentation on core concepts, see `full_docs.md` in this directory. It contains exhaustive coverage of architecture, modes, session lifecycle, project structure, TUI, Server, Share, Zen, Web, SSH, Go SDK, SDK, and ecosystem.

## Cross-References
- [opencode_cli_commands](../opencode_cli_commands/SKILL.md)
- [opencode_configuration](../opencode_configuration/SKILL.md)
- [opencode_tools_catalog](../opencode_tools_catalog/SKILL.md)
- [opencode_skills_framework](../opencode_skills_framework/SKILL.md)
- [opencode_decision_trees](../opencode_decision_trees/SKILL.md)
