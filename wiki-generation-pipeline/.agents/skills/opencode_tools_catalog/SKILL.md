---
name: opencode Tools Catalog
description: Complete reference for all 12 built-in opencode tools — bash, read, edit, write, glob, grep, web_search, web_fetch, task, question, todowrite, skill. Every parameter with schema, when-to-use guidance, behavioral rules, best practices, and a selection matrix. Also covers custom tools via MCP and tool configuration. Trigger on "which tool", "tool parameters", "tool X isn't working", "how do I use the X tool", or tool selection questions.
---

# opencode Tools Catalog

Complete reference for all 12 built-in tools, their parameters, behavioral rules, and usage patterns.

---

## 1. Tool Invocation Overview

- Tools are called by the **AI model**, not directly by users.
- The AI chooses which tool to invoke based on the user's task and each tool's description.
- Tool availability is controlled by **config** (`tools.allow` / `tools.deny`) and **permission rules**.
- Tools run in the user's local environment — they have access to the filesystem, shell, and network.
- Every tool call is subject to the project's permission policies. Restricted tools may require user approval.
- The model can call multiple tools in parallel when calls are independent.

---

## 2. Complete Tool Catalog

### bash

Execute a shell command via the system terminal.

| Parameter  | Required | Default    | Description                                      |
|------------|----------|------------|--------------------------------------------------|
| `command`  | yes      | —          | The shell command string to execute              |
| `timeout`  | no       | `120000`   | Timeout in milliseconds                          |
| `workdir`  | no       | cwd        | Working directory to run the command in          |

**When to use:** git operations, package managers (npm/pip/cargo), running tests, compilation, Docker, any task requiring a shell.

**Security:** Subject to permission policies and rules. On Windows the shell is PowerShell 7+.

**Notes:**
- Output is truncated at 2000 lines or 51200 bytes — use `Read` or `Grep` on the output file for large results.
- Prefer `workdir` over `cd` inside the command string.
- Chain independent commands with `&&`. Use `;` only when failure of an earlier command is acceptable.
- Use full cmdlet names on Windows (`Get-ChildItem` not `gci`).
- Quote file paths containing spaces with double quotes.

---

### read

Read a file's contents or list a directory's entries.

| Parameter  | Required | Default    | Description                                      |
|------------|----------|------------|--------------------------------------------------|
| `filePath` | yes      | —          | Absolute path to the file or directory           |
| `offset`   | no       | `1`        | 1-indexed line number to start reading from      |
| `limit`    | no       | `2000`     | Maximum number of lines to return                |

**When to use:** Understanding code, reading config files, listing directory contents, inspecting build output.

**Notes:**
- Lines longer than 2000 characters are truncated.
- Returns up to 2000 lines by default; use `offset` and `limit` to paginate through large files.
- Call in parallel when reading multiple files simultaneously.
- Can read image files and PDFs as attachments.

---

### edit

Perform an exact string replacement in a file.

| Parameter    | Required | Default | Description                                         |
|--------------|----------|---------|-----------------------------------------------------|
| `filePath`   | yes      | —       | Absolute path to the file                           |
| `oldString`  | yes      | —       | The exact text to find and replace                  |
| `newString`  | yes      | —       | The replacement text                                |
| `replaceAll` | no       | `false` | Replace every occurrence instead of just the first  |

**When to use:** Targeted modifications, renaming identifiers, fixing specific bugs, updating configuration values.

**Rules:**
- You **must** `read` the file in the same session before editing.
- Fails if `oldString` is not found in the file.
- Fails if `oldString` matches multiple locations — provide more surrounding context or use `replaceAll`.
- Prefer editing over writing — only use `write` for full file rewrites.
- Preserve exact indentation (tabs/spaces) from the file when constructing `oldString`.

---

### write

Create a new file or overwrite an existing one completely.

| Parameter  | Required | Default | Description                                     |
|------------|----------|---------|-------------------------------------------------|
| `filePath` | yes      | —       | Absolute path to the file                       |
| `content`  | yes      | —       | The full content to write                       |

**When to use:** Creating new files, complete file rewrites, generating code, writing tests, producing documentation.

**Rules:**
- You **must** `read` the file first if it already exists.
- Prefer `edit` for modifications to existing files — only use `write` for full rewrites.
- Never proactively create documentation or README files unless explicitly requested.

---

### glob

Find files by name pattern using glob syntax.

| Parameter | Required | Default | Description                                       |
|-----------|----------|---------|---------------------------------------------------|
| `pattern` | yes      | —       | Glob pattern (e.g. `**/*.ts`, `src/**/test_*`)    |
| `path`    | no       | cwd     | Directory to search in                            |

**When to use:** Finding files by extension, name, or directory structure. Faster than `bash find` for simple lookups.

**Notes:**
- Use `**` for recursive matching.
- Returns full file paths.
- Run multiple globs in parallel when searching for different patterns.

---

### grep

Search file contents using regular expressions.

| Parameter | Required | Default | Description                                       |
|-----------|----------|---------|---------------------------------------------------|
| `pattern` | yes      | —       | Regular expression to search for                  |
| `path`    | no       | cwd     | Directory to search in                            |
| `include` | no       | —       | File pattern filter (e.g. `*.js`, `*.{ts,tsx}`)  |

**When to use:** Finding function definitions, imports, usages, error messages, hardcoded values, or any content pattern across a codebase.

**Notes:**
- Returns file paths with line numbers and matching lines.
- For counting matches, use `rg` via `bash` instead.
- Always prefer `grep` over `bash Select-String` for content search.

---

### web_search

Perform a real-time web search.

| Parameter            | Required | Default  | Description                                     |
|----------------------|----------|----------|-------------------------------------------------|
| `query`              | yes      | —        | Search query string                             |
| `numResults`         | no       | `8`      | Number of results to return                     |
| `livecrawl`          | no       | `fallback` | `"fallback"` or `"preferred"`                 |
| `type`               | no       | `auto`   | `"auto"`, `"fast"`, or `"deep"`                |
| `contextMaxCharacters` | no     | `10000`  | Max characters per result for LLM context       |

**When to use:** Current events, documentation lookup, package version checks, API references, troubleshooting recent issues.

**Notes:**
- Always include the current year in queries for recent information.
- Use `type: "deep"` for comprehensive research, `type: "fast"` for quick answers.

---

### web_fetch

Fetch content from a URL and return it in a structured format.

| Parameter | Required | Default      | Description                                      |
|-----------|----------|--------------|--------------------------------------------------|
| `url`     | yes      | —            | Fully-formed URL (http upgraded to https)        |
| `format`  | no       | `"markdown"` | `"markdown"`, `"text"`, or `"html"`             |
| `timeout` | no       | —            | Timeout in seconds (max 120)                     |

**When to use:** Reading API documentation, fetching specific web pages, downloading structured data.

**Notes:**
- Read-only — does not modify any files.
- Content may be summarized if very large.

---

### task

Delegate work to a specialized subagent.

| Parameter       | Required | Default | Description                                      |
|-----------------|----------|---------|--------------------------------------------------|
| `description`   | yes      | —       | Brief task label (3–5 words)                     |
| `prompt`        | yes      | —       | Detailed instructions for the subagent           |
| `subagent_type` | yes      | —       | One of: `explore`, `general`, `code`, `architect`, `debug`, `frontend`, `ask` |
| `command`       | no       | —       | Optional shell command for the subagent          |

**When to use:** Parallel exploration of multiple codebase areas, delegating complex isolated subtasks, delegating research.

**Notes:**
- Subagents have their own tool access and run independently.
- Use `explore` for read-only codebase investigation, `code` for file modifications, `debug` for diagnostics.
- The parent agent must verify subagent output.

---

### question

Ask the user for input or a decision.

| Parameter  | Required | Default | Description                                      |
|------------|----------|---------|--------------------------------------------------|
| `questions`| yes      | —       | Array of question objects                        |

Each question object:
| Field      | Required | Default | Description                                      |
|------------|----------|---------|--------------------------------------------------|
| `question` | yes      | —       | The question text                                |
| `header`   | yes      | —       | Short label (max 30 chars)                       |
| `options`  | no       | —       | Array of `{ label, description }`                |
| `multiple` | no       | `false` | Allow multiple selections                        |

**When to use:** Gathering user preferences, clarifying ambiguity, getting decisions before proceeding.

**Best practice:** Batch all questions into a single call rather than asking one at a time.

---

### todowrite

Maintain a structured task list for tracking multi-step work.

| Parameter | Required | Default | Description                                      |
|-----------|----------|---------|--------------------------------------------------|
| `todos`   | yes      | —       | Array of todo objects                            |

Each todo object:
| Field      | Required | Default   | Description                                      |
|------------|----------|-----------|--------------------------------------------------|
| `content`  | yes      | —         | Task description                                 |
| `status`   | no       | `pending` | `pending`, `in_progress`, `completed`, `cancelled` |
| `priority` | no       | `medium`  | `high`, `medium`, `low`                          |

**When to use:** Tracking multi-step work, planning ahead, showing progress to the user.

**Rules:** Maintain exactly **one** `in_progress` item at a time.

---

### skill

Load a specialized skill into the current conversation context.

| Parameter | Required | Default | Description                                      |
|-----------|----------|---------|--------------------------------------------------|
| `name`    | yes      | —       | Skill name matching its YAML frontmatter `name`  |

**When to use:** When the user's request matches a skill's trigger description. The skill's `description` field in frontmatter determines when it should be loaded.

**Notes:**
- Loading a skill injects its full instructions and references into context.
- Use this at the start of a task that matches a skill domain.

---

## 3. Tool Selection Matrix

| Task                                  | Best Tool   | Why                                          |
|---------------------------------------|-------------|----------------------------------------------|
| Find file by name or extension        | `glob`      | Fast glob pattern matching                   |
| Find text across files                | `grep`      | Regex content search with line numbers        |
| Read a specific file                  | `read`      | Structured output with line numbers and paging |
| Create a new file                     | `write`     | Single call, full content                    |
| Modify part of a file                 | `edit`      | Precise replacement, no full rewrite needed  |
| Run a shell command                   | `bash`      | Only way to execute system commands          |
| Search the web                        | `web_search`| Real-time indexed search                     |
| Fetch a specific URL                  | `web_fetch` | Structured content retrieval                 |
| Delegate a subtask                    | `task`      | Parallel execution, specialized subagents    |
| Ask the user a question               | `question`  | Structured input with options                |
| Track progress on multi-step work     | `todowrite` | Persistent structured task list              |
| Load domain expertise                 | `skill`     | Injects specialized instructions into context|

---

## 4. Multi-Tool Workflow Patterns

| Goal                                | Recommended Sequence                          |
|-------------------------------------|-----------------------------------------------|
| Understand a feature                | `glob` → `grep` → `read`                      |
| Fix a bug                           | `grep` → `read` → `edit` → `bash` (test)      |
| Add a new file                      | `glob` → `read` → `write`                     |
| Refactor a function                 | `grep` → `read` → `edit` → `edit` → `bash`   |
| Research and implement              | `web_search` → `web_fetch` → `write` → `bash` |
| Explore an unknown codebase         | `glob` → `read` → `todowrite`                 |
| Complex multi-file change           | `todowrite` → `task` → `bash` (verify)        |
| Debug a failing test                | `bash` (run test) → `grep` → `read` → `edit`  |
| Add a dependency                    | `web_search` → `bash` (install) → `read` → `edit` |

---

## 5. Custom Tools

Custom tools extend the built-in set via configuration:

- **MCP servers** expose tools over the Model Context Protocol — any MCP-compatible server can register tools that appear in the model's tool list alongside built-ins.
- **`tools` config field** in `opencode.json` lets you define tools directly with:
  - `name` — tool identifier
  - `description` — what the tool does (used by the model for selection)
  - `parameters` — JSON Schema for the tool's parameters
  - `handler` — the script or command that executes when the tool is called

Custom tools are subject to the same permission rules as built-in tools. They appear in the model's available tool list and are selected the same way — by matching the task to the tool description.

---

## 6. Tool Configuration

### Allow / Deny Lists

Control which tools are available to the model:

```jsonc
{
  "tools": {
    "allow": ["bash", "read", "edit", "write", "glob", "grep"],
    "deny": ["web_search", "web_fetch"]
  }
}
```

- `tools.allow` — whitelist; only listed tools are available.
- `tools.deny` — blacklist; listed tools are unavailable even if otherwise allowed.

### Permission Rules

Rules provide finer-grained control over individual tools:

- Restrict `bash` commands by pattern (e.g., block `rm -rf`).
- Require approval for `write` to sensitive paths.
- Auto-approve `read` and `glob` (typically safe, read-only).

### Permission Modes

The approval flow for tool calls depends on the permission mode:

- **`ask`** — prompt the user before every restricted tool call.
- **`auto`** — approve automatically based on rules.
- **`strict`** — deny anything not explicitly allowed.

---

## Full Documentation
For the complete official opencode tools documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of all 12 tools, parameters, permission modes, custom tools, MCP tools, and multi-tool workflows.

**Cross-references:**
- **opencode_configuration** — how `tools.allow` / `tools.deny` and `tools.custom` are configured in `opencode.json`.
- **opencode_rules_permissions** — permission rules that control per-tool approval behavior.
- **opencode_agents_subagents** — using the `task` tool for subagent delegation and orchestration.
- **opencode_decision_trees** — decision trees for selecting the right tool for any task.
