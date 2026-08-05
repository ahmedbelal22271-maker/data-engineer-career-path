# OpenCode Tools Catalog — Complete Official Documentation

> **Source:** https://opencode.ai/tools — retrieved July 2026

---

## Overview

OpenCode provides a standard set of built-in tools that the AI can use to interact with your codebase and system. Tools are the bridge between the AI's reasoning and real-world actions.

---

## The 12 Built-in Tools

### 1. `bash` — Execute Shell Commands

Runs arbitrary shell commands in your terminal. The primary tool for compilation, testing, package management, git operations, and system interaction.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `command` | `string` | Yes | The shell command to execute |
| `timeout` | `number` | No | Timeout in ms (default: 120000) |
| `workdir` | `string` | No | Working directory (default: project root) |

**Behavior:**
- Commands run in the project root by default
- Supports PowerShell 7+ (`pwsh`) on Windows
- Captures stdout and stderr
- Timeout prevents runaway commands
- The agent should explain non-obvious commands before running them

**Best practices:**
- Chain sequential commands with `&&`
- Use `workdir` instead of `cd` inside commands
- Run independent commands in parallel (single message with multiple tool calls)
- Prefer full cmdlet names on Windows (PowerShell)
- Always verify directory existence before creating files

---

### 2. `read` — Read Files

Reads a file's contents or lists a directory. Returns content with line numbers for precise referencing.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | `string` | Yes | Absolute path to the file |
| `offset` | `number` | No | Line number to start from (1-indexed) |
| `limit` | `number` | No | Max lines to read (default: 2000) |

**Behavior:**
- Returns up to 2000 lines by default
- Lines are prefixed with `<line_number>: <content>`
- Lines >2000 characters are truncated
- Can read image files and PDFs as attachments
- Use `offset` for large files to read specific sections

**Best practices:**
- Read multiple files in parallel when possible
- Use larger windows (100+ lines) to avoid narrow context
- Avoid repeated small slices (30-line chunks) — read larger sections
- Use `grep` to find specific content in large files first

---

### 3. `write` — Write Files

Creates a new file or overwrites an existing file entirely.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | `string` | Yes | Absolute path to the file |
| `content` | `string` | Yes | Complete file content |

**Behavior:**
- Overwrites the file completely (not a partial edit)
- For existing files, you MUST read them first
- Creates parent directories if they don't exist
- Prefer editing existing files over rewriting

**Best practices:**
- ALWAYS prefer `edit` over `write` for existing files
- Only use `write` for brand-new files or complete rewrites
- Read the file first before writing to it
- Never write sensitive data (keys, passwords) to files

---

### 4. `edit` — Edit Files

Performs targeted string replacements in files. Much more efficient than rewriting entire files.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | `string` | Yes | Absolute path to the file |
| `oldString` | `string` | Yes | Exact text to find and replace |
| `newString` | `string` | Yes | Replacement text (must differ from oldString) |
| `replaceAll` | `boolean` | No | Replace all occurrences (default: false) |

**Behavior:**
- Requires exact string matching (including indentation)
- Fails if `oldString` is not found
- Fails if `oldString` matches multiple locations (unless `replaceAll`)
- You MUST read the file before editing
- `replaceAll` replaces every occurrence of the string

**Best practices:**
- Always read the file first
- Provide enough surrounding context in `oldString` to make it unique
- Use `replaceAll` for renaming variables/functions across a file
- Prefer editing existing files — never write when edit will do

---

### 5. `glob` — Find Files by Pattern

Fast file pattern matching. Works with any codebase size.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pattern` | `string` | Yes | Glob pattern (e.g., `**/*.ts`, `src/**/*.tsx`) |
| `path` | `string` | No | Directory to search in (default: workspace root) |

**Behavior:**
- Returns matching file paths
- Supports `**` for recursive matching
- Supports `*` for single-level wildcards
- Supports `{a,b}` for alternatives
- Case-sensitive on Linux/macOS, case-insensitive on Windows

**Examples:**
- `**/*.js` — all JavaScript files recursively
- `src/components/**/*.tsx` — all TSX files in components
- `*.{ts,tsx}` — all TypeScript files at one level
- `**/package.json` — all package.json files

**Best practices:**
- Use `glob` to find files by name, `grep` to find by content
- Combine with `read` to examine matched files
- Use in parallel with other searches for comprehensive discovery

---

### 6. `grep` — Search File Contents

Fast content search using regular expressions across a codebase.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pattern` | `string` | Yes | Regex pattern to search for |
| `path` | `string` | No | Directory to search (default: workspace root) |
| `include` | `string` | No | File pattern to include (e.g., `*.js`) |

**Behavior:**
- Returns file paths and line numbers with matching lines
- Supports full regex syntax
- Use `include` to filter by file type
- For simple searches, prefer `grep` tool; for counting, use `rg` via bash

**Best practices:**
- Use `grep` for content search, `glob` for filename search
- Use `include` to narrow search to specific file types
- For complex searches, use ripgrep (`rg`) via bash tool
- Search for function names, class names, variable references

---

### 7. `web_search` — Search the Web

Performs real-time web searches. Essential for looking up documentation, finding solutions, and verifying current information.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | `string` | Yes | Search query |
| `numResults` | `number` | No | Number of results (default: 8) |

**Behavior:**
- Returns search results with titles, URLs, and snippets
- Can scrape content from specific URLs
- Supports live crawling when cached content is unavailable
- Current year is automatically applied to searches

**Search types (when available):**
- `auto` — balanced search (default)
- `fast` — quick results
- `deep` — comprehensive search

**Best practices:**
- Use for looking up current API documentation
- Use for verifying library versions and compatibility
- Use for finding solutions to specific error messages
- Group related searches into batch queries for efficiency

---

### 8. `web_fetch` — Fetch URL Content

Fetches and extracts content from a specific URL. Converts to markdown by default.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | `string` | Yes | URL to fetch (must be fully-formed) |
| `format` | `string` | No | Output format: `"markdown"` (default), `"text"`, `"html"` |
| `timeout` | `number` | No | Timeout in seconds (max: 120) |

**Behavior:**
- HTTP URLs are automatically upgraded to HTTPS
- Content is converted to the requested format
- Large pages may be summarized
- Read-only — does not modify anything

**Best practices:**
- Use when you need to read a specific documentation page
- Use `web_search` first to find relevant URLs, then `web_fetch` to read them
- Prefer `web_search` over `web_fetch` for general lookups

---

### 9. `task` — Delegate to Subagents

Launches a new agent to handle complex, multistep tasks autonomously.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `description` | `string` | Yes | Short task description (3-5 words) |
| `prompt` | `prompt` | Yes | Detailed task instructions |
| `subagent_type` | `string` | Yes | Agent type: `general` or `explore` |
| `task_id` | `string` | No | Resume a previous task |
| `command` | `string` | No | Command that triggered this task |

**Agent types:**

| Type | Use Case |
|------|----------|
| `general` | Complex multi-step tasks, research, code changes |
| `explore` | Fast codebase exploration, file finding, code search |

**Behavior:**
- Each invocation starts with a fresh context (unless resuming)
- Agent returns a single message with results
- Results are not directly visible to the user — relay them
- Use parallel task invocations for independent work

**Best practices:**
- Use `explore` for finding files, `general` for complex work
- Be extremely detailed in prompts — the agent has no context
- Don't duplicate work the agent is handling
- Use `task_id` to resume long-running work

**When NOT to use:**
- Reading a specific file → use `read`
- Finding a file by name → use `glob`
- Searching code for a pattern → use `grep`

---

### 10. `question` — Ask the User

Prompts the user for input during execution. Used to clarify requirements, get decisions, and confirm approaches.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `questions` | `array` | Yes | Array of question objects |
| `questions[].question` | `string` | Yes | The question text |
| `questions[].header` | `string` | Yes | Short label (max 30 chars) |
| `questions[].options` | `array` | No | Available choices |
| `questions[].multiple` | `boolean` | No | Allow multiple selections |

**Behavior:**
- Presents choices to the user
- Returns answers as arrays
- Supports single and multiple selection
- Can add a custom "Type your own answer" option

**Best practices:**
- Use when implementation choices need user input
- Don't ask obvious questions — check the codebase first
- Limit options to clear, actionable choices
- Recommend the best option when possible

---

### 11. `todowrite` — Task Management

Creates and maintains a structured task list for the current coding session.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `todos` | `array` | Yes | Array of task objects |
| `todos[].content` | `string` | Yes | Brief task description |
| `todos[].status` | `string` | Yes | `"pending"`, `"in_progress"`, `"completed"`, `"cancelled"` |
| `todos[].priority` | `string` | Yes | `"high"`, `"medium"`, `"low"` |

**Behavior:**
- Tracks progress in real time
- Only ONE task can be `in_progress` at a time
- Mark `completed` only after actual work is done
- Preserves user-provided commands verbatim

**When to use:**
- 3+ distinct steps or actions
- Non-trivial work benefiting from planning
- Multiple tasks from the user
- New instructions arrive

**When NOT to use:**
- Single straightforward task
- Purely informational/conversational
- 2-3 simple tool calls for one step

---

### 12. `skill` — Load Specialized Skills

Loads a specialized skill file to inject domain-specific instructions and context into the current conversation.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | `string` | Yes | Skill name from available_skills list |

**Behavior:**
- Injects the full SKILL.md content into context
- Available skills are listed in the system prompt
- Each skill provides specialized instructions for its domain
- Skills are loaded permanently for the session

**Best practices:**
- Load skills when the task matches their description
- Check if a skill is already in context before loading
- Prefer skills over ad-hoc instructions for repeated patterns
- Don't load skills that aren't relevant to the current task

---

## Tool Selection Matrix

| Task | Recommended Tool(s) |
|------|---------------------|
| Read a specific file | `read` |
| Find files by name | `glob` |
| Search code for patterns | `grep` |
| Modify existing file | `edit` |
| Create new file | `write` |
| Run tests/commands | `bash` |
| Look up documentation | `web_search` → `web_fetch` |
| Complex multi-step work | `task` (general) |
| Explore codebase structure | `task` (explore) or `glob` + `read` |
| Get user input | `question` |
| Track progress | `todowrite` |
| Domain-specific work | `skill` → then use tools |

---

## Tool Permission Modes

### Bypass Mode

All tools execute without confirmation. Fast but risky.

```json
{ "permission": "bypass" }
```

### Default Mode

Read-only tools auto-execute. Write tools ask for confirmation.

### Rules Mode

Fine-grained control via `tools.always`, `tools.never`, and `tools.ask` in config.

```json
{
  "tools": {
    "always": ["read", "glob", "grep", "web_search", "web_fetch"],
    "ask": ["write", "edit", "bash"],
    "never": []
  }
}
```

### Preserve State

Remember permission decisions across sessions:

```json
{
  "tools": {
    "preserve": {
      "bash": true,
      "write": true
    }
  }
}
```

---

## Custom Tools via MCP

Extend the built-in tools with MCP servers. Each MCP server can provide additional tools.

```json
{
  "mcp": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-github"]
    }
  }
}
```

The tools from MCP servers appear alongside built-in tools and follow the same permission model.

---

## Custom Tools via `tools.command`

Define simple command-based tools directly in config:

```json
{
  "tools": {
    "command": {
      "run-tests": {
        "description": "Run the project test suite",
        "command": "npm test",
        "timeout": 120000
      },
      "lint": {
        "description": "Run the linter",
        "command": "npm run lint"
      }
    }
  }
}
```

These custom tools are available to the AI like any other tool.

---

## Multi-Tool Workflows

The most effective workflows use multiple tools in sequence:

1. **Explore → Understand → Implement**
   - `glob` (find files) → `read` (examine) → `edit`/`write` (implement)

2. **Research → Apply**
   - `web_search` (find docs) → `web_fetch` (read page) → `edit` (apply knowledge)

3. **Search → Verify → Fix**
   - `grep` (find issue) → `read` (understand context) → `edit` (fix)

4. **Parallel Discovery**
   - Multiple `glob`/`grep` calls in one message → `read` matches → `edit`

---

## Tool Call Best Practices

1. **Batch independent calls** — Send multiple tool calls in one message when they're independent
2. **Read before editing** — Always read a file before modifying it
3. **Explain non-obvious commands** — Tell the user what a bash command does before running it
4. **Prefer specific tools** — Use `grep` for content search, `glob` for filenames, `read` for specific files
5. **Verify before committing** — Check `git status` and `git diff` before any commit
6. **Use workdir for bash** — Don't `cd` inside commands; use the `workdir` parameter
7. **Check parent dirs before creating** — Verify the parent directory exists before writing new files
