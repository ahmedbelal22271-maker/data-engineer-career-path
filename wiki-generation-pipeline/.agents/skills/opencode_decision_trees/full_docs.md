# OpenCode Decision Trees — Complete Official Documentation

> **Source:** https://opencode.ai — compiled from all documentation pages — retrieved July 2026

---

## Overview

This skill provides structured decision logic for choosing the optimal approach when using OpenCode. Each decision tree covers a specific selection problem.

---

## Decision Tree 1: Mode Selection

**Start:** What do you need to do?

```
Need to EXPLORE or PLAN?
├── Yes → PLAN MODE
│   ├── Just reading/searching? → opencode (default)
│   ├── Want to design an approach? → opencode plan
│   └── Need to understand codebase? → opencode run --subagent explore
│
└── No → Need to IMPLEMENT or EXECUTE?
    ├── Yes → AUTO MODE
    │   ├── Implement a feature? → opencode (default, auto)
    │   ├── Run a specific task? → opencode run "task description"
    │   ├── Execute a plan? → opencode execute
    │   └── Run in background/CI? → opencode --zen run "task"
    │
    └── Not sure → Start with PLAN MODE, switch to AUTO when ready
```

**Rules:**
- Start in plan mode when exploring unfamiliar code
- Switch to auto mode when ready to implement
- Use `--zen` for non-interactive execution
- Use `--subagent explore` for fast codebase search

---

## Decision Tree 2: Agent Selection

**Start:** What type of work?

```
Code exploration / searching?
├── Yes → EXPLORE AGENT
│   ├── Find files by pattern? → glob tool (direct)
│   ├── Search code content? → grep tool (direct)
│   └── Understand structure? → task(subagent_type: "explore")
│
├── Code writing / implementation? → GENERAL or CODE AGENT
│   ├── Simple edit? → general (default)
│   ├── Complex feature? → general with detailed prompt
│   └── Code-heavy refactor? → task(subagent_type: "code")
│
├── Debugging / fixing? → DEBUG AGENT
│   ├── Known error? → general with error context
│   ├── Investigating? → task(subagent_type: "debug")
│   └── Performance issue? → task(subagent_type: "debug")
│
├── Architecture / design? → ARCHITECT AGENT
│   ├── System design? → task(subagent_type: "architect")
│   └── Tech evaluation? → task(subagent_type: "architect")
│
├── Frontend / UI? → FRONTEND AGENT
│   ├── Build component? → task(subagent_type: "frontend")
│   └── Style/CSS? → task(subagent_type: "frontend")
│
└── Just asking? → ASK AGENT
    ├── Question about code? → general (default)
    └── Documentation lookup? → task(subagent_type: "ask")
```

---

## Decision Tree 3: Tool Selection

**Start:** What do you need to do?

```
Need to READ something?
├── Specific file? → read tool
├── Find files by name? → glob tool
├── Search file contents? → grep tool
├── Read a URL? → web_fetch tool
└── Read multiple files? → parallel read calls

Need to WRITE something?
├── New file? → write tool
├── Modify existing file? → edit tool (ALWAYS prefer over write)
├── Rename across files? → edit with replaceAll
└── Run a build/test? → bash tool

Need to SEARCH?
├── Files by pattern? → glob tool
├── Code by content? → grep tool
├── Web search? → web_search tool
└── Specific URL content? → web_fetch tool

Need to EXECUTE?
├── Shell command? → bash tool
├── Run tests? → bash (npm test, pytest, etc.)
├── Git operations? → bash (git commands)
└── Package management? → bash (npm, pip, etc.)

Need to DELEGATE?
├── Complex multi-step? → task(subagent_type: "general")
├── Codebase exploration? → task(subagent_type: "explore")
└── Resume previous? → task(task_id: "id")

Need USER INPUT?
├── Choice to make? → question tool
├── Confirmation? → question tool
└── Preference? → question tool

Need to TRACK PROGRESS?
├── Multiple steps? → todowrite tool
└── Single step? → no tracking needed
```

---

## Decision Tree 4: Model Selection

**Start:** What's your priority?

```
Quality / reasoning?
├── Yes → Claude Opus 4 or Claude Sonnet 4
│   ├── Anthropic available? → anthropic/claude-opus-4-6
│   ├── Bedrock? → bedrock/anthropic.claude-opus-4-6
│   └── Vertex? → vertex/claude-opus-4
│
├── Speed? → GPT-4o-mini or Gemini Flash
│   ├── OpenAI? → openai/gpt-4o-mini
│   └── Google? → google/gemini-2.5-flash
│
├── Cost? → Smaller models
│   ├── Cheapest? → openai/gpt-4o-mini
│   └── Local? → ollama/llama3
│
├── Privacy? → Local models
│   ├── Ollama? → ollama/llama3
│   └── Bedrock (VPC)? → bedrock models
│
└── Context window? → Gemini or Claude
    ├── Huge codebase? → google/gemini-2.5-pro (1M tokens)
    └── Standard? → anthropic/claude-sonnet-4-6 (200K)
```

**Primary model:** Use the strongest model available for reasoning and editing.

**Big model:** Use a fast, cost-effective model for search and exploration.

---

## Decision Tree 5: Integration Selection

**Start:** What system do you need to connect?

```
Version control?
├── GitHub? → GitHub MCP server
├── GitLab? → GitLab MCP server
└── Local git only? → bash tool (git commands)

External data?
├── Database? → Database MCP server (Postgres, MongoDB)
├── Cloud storage? → Cloud MCP server (S3, GCS)
├── API? → web_fetch or custom MCP server
└── Knowledge base? → Memory MCP server

IDE integration?
├── VS Code? → VS Code extension
├── JetBrains? → JetBrains plugin
└── Terminal only? → TUI (default)

Remote access?
├── Remote server? → SSH integration
├── Team access? → Server mode + Share
└── CI/CD? → Zen mode + Server API

Code intelligence?
├── Autocomplete? → LSP server
├── Diagnostics? → LSP server
└── Refactoring? → LSP server
```

---

## Decision Tree 6: Output Format Selection

**Start:** Who is the audience?

```
Human reading?
├── Interactive? → TUI (default)
├── Documentation? → Markdown export
└── Presentation? → Formatted Markdown with code blocks

Machine processing?
├── Script automation? → JSON output (--json)
├── CI/CD pipeline? → Zen mode + quiet output
└── API integration? → Server REST API

 archival?
├── Session record? → JSON export
├── Sharing? → Share feature
└── Debugging? → Debug log export
```

---

## Decision Tree 7: Permission Strategy

**Start:** What's your risk tolerance?

```
Maximum speed, trust AI?
├── Yes → BYPASS MODE
│   └── permission: "bypass"
│
├── Balanced? → DEFAULT MODE
│   └── permission: "default"
│   ├── Read auto-execute
│   ├── Write ask confirmation
│   └── Destructive ask confirmation
│
├── Maximum control? → RULES MODE
│   └── permission: "rules"
│   ├── Define allow/deny lists
│   ├── Per-command granularity
│   └── Preserve decisions as needed
│
└── Enterprise / regulated? → POLICIES
    ├── Audit logging
    ├── RBAC
    └── Data classification
```

---

## Decision Tree 8: Instructions Strategy

**Start:** What do you need to teach the AI?

```
Global behavioral rules?
├── Yes → AGENTS.md (or instructions in opencode.json)
│   ├── Always apply? → instructions array
│   └── Project-specific? → AGENTS.md at root
│
Domain expertise?
├── Yes → SKILLS
│   ├── Single domain? → skill in .opencode/skills/
│   ├── Multiple domains? → multiple skills
│   └── Load on demand? → skill tool
│
Security constraints?
├── Yes → RULES
│   ├── File protection? → .opencode/rules/
│   ├── Command restrictions? → rules with never/ask
│   └── Behavioral requirements? → rules with always
│
External data access?
├── Yes → MCP SERVERS
│   ├── GitHub? → github MCP
│   ├── Database? → database MCP
│   └── Custom? → custom MCP server
│
Tool extensions?
├── Yes → CUSTOM TOOLS
│   ├── Simple command? → tools.command in config
│   └── Complex integration? → MCP server
```

---

## Decision Tree 9: Error Recovery

**Start:** What failed?

```
API error (401/429/500)?
├── 401 → Check API key → Fix in provider config
├── 429 → Rate limited → Wait + retry or switch provider
├── 500 → Server error → Retry or check status
└── Model not found → Check model name format

Tool failure?
├── edit not found → Read file first, match exact string
├── bash timeout → Increase timeout or simplify command
├── write permission → Check file permissions
└── glob no results → Check pattern syntax

TUI issue?
├── Not rendering → Check terminal compatibility
├── Colors wrong → Enable true color support
└── Input stuck → Press Escape, restart

Session issue?
├── Not found → List sessions, resume or create new
├── Corrupted → Delete and create new
└── Export fails → Export to clipboard instead

Config issue?
├── Unknown property → Remove unsupported field
├── Invalid JSON → Fix syntax errors
└── Model not loading → Check provider + API key
```

---

## Common Scenarios Quick Reference

| Scenario | Recommended Approach |
|----------|---------------------|
| "Explain this code" | `read` the file, then explain in chat |
| "Fix this bug" | `read` error context, `edit` to fix |
| "Add a feature" | Plan mode first, then auto mode to implement |
| "Run my tests" | `bash` tool with test command |
| "Find all TODOs" | `grep` for "TODO" pattern |
| "Review this PR" | `@pr #123` mention or GitHub MCP |
| "Write documentation" | Load relevant skill, use templates |
| "Optimize this query" | Load domain skill, use expertise |
| "Deploy to production" | Use `ask` for confirmation, then `bash` |
| "What does this function do" | `read` the file, explain in chat |
| "Refactor this module" | Plan mode for design, auto mode for execution |
| "Create a new project" | `bash` for scaffolding, `write` for files |
| "Debug a memory leak" | Debug agent via `task` |
| "Set up CI/CD" | Load DevOps skill, use `bash` for commands |
| "Migrate a database" | Plan mode, domain skill, careful `bash` execution |
