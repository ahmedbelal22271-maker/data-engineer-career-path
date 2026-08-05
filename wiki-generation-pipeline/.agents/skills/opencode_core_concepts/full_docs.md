# OpenCode Core Concepts — Complete Official Documentation

> **Source:** https://opencode.ai — retrieved July 2026

---

## What is OpenCode

OpenCode is a terminal-based AI coding agent. It runs in your terminal, connects to any LLM provider, and uses natural language to help you write, debug, and ship code. It is a self-contained binary with a built-in terminal UI (TUI), native tool integrations, and an extensible plugin system.

OpenCode combines three things into one cohesive system:

- A reasoning engine (LLM) that understands your codebase
- A set of tools for searching, editing, and running code
- A structured set of instructions that tell it how to behave

The CLI serves as the primary entry point. The core engine is built on a modular architecture with pluggable components for different features and integrations.

**Core design principles:**

- Terminal-native — built for the terminal, not as an afterthought
- LLM-agnostic — works with any provider
- Tool-first — always has access to a standard set of tools
- Extensible — supports plugins, skills, and MCP servers
- Fast — optimized for performance

---

## Architecture

### Lattice Architecture

OpenCode uses a lattice architecture for session management. The lattice consists of nodes (states) and edges (transitions) that represent the possible paths through a conversation. This provides a robust, verifiable system for managing complex interactions.

The architecture is built on immutable message graphs that enable deterministic replay. Each session maintains an immutable log of all events (messages, tool calls, tool results, snapshots). The UI renders directly from this event log.

### Event System

OpenCode uses a typed event system for communication. Events are the primary mechanism for decoupling components and enabling flexible composition. Events flow through a central bus that routes them to registered handlers.

### File I/O

OpenCode provides a file I/O layer that handles reading, writing, and watching files. It includes safety checks for sensitive files (`.env`, `credentials.json`, `id_rsa`) and respects `.gitignore` patterns. File operations are atomic with backup support.

### Session Management

Sessions persist conversations across restarts. Each session maintains a log of events that the UI renders. Sessions can be exported, imported, and resumed. The `opencode run` command can start new sessions or resume existing ones.

---

## Two Modes

### Plan Mode

In Plan Mode, OpenCode cannot make any changes to your files. It reads, searches, and analyzes your code but cannot write, edit, or execute anything. Use this when you want to explore options, understand a codebase, or design an approach before committing to changes.

Plan mode provides read-only access. It can read files, search code, check git status, and analyze architecture, but cannot modify files, execute commands, or interact with Git.

### Auto Mode

In Auto Mode, OpenCode can read, write, and execute. It makes changes, runs commands, and iterates until the task is done. Use this when you want OpenCode to implement the solution directly.

Auto mode provides full access. It can read files, search code, modify files, execute shell commands, create new files, and manage Git operations.

You control the mode through the `mode` key in `opencode.json`. The default mode is `auto`. You can override the mode at any time with `/mode` in the TUI or `--mode` on the CLI. The current mode displays in the footer bar.

```json
{
  "mode": "plan"
}
```

When you finish a plan, the `/task` command automatically switches to Auto mode to execute the approved plan.

---

## Session Lifecycle

Sessions are the fundamental unit of work in OpenCode. Each session maintains a complete event log that the UI renders. Sessions persist across restarts and can be exported, imported, and resumed.

Key characteristics:
- Each session has a unique ID
- The event log is immutable — new events are appended
- Sessions can be resumed with `opencode run --resume`
- Sessions can be exported for sharing or debugging

---

## Model Selection

OpenCode uses two different configurations for two different jobs:

1. **Primary model** — the main reasoning engine, handles planning, editing, and orchestration. Best results with strong models like GPT-4o, Claude Sonnet/Opus, Gemini 2.5 Pro.
2. **Big model** — specialized for codebase exploration. Excels at searching large codebases quickly. Best with models optimized for speed and large context windows.

Configure models in `opencode.json`:

```json
{
  "provider": {
    "opencode": {
      "name": "opencode",
      "apiKey": "env:OPENCODE_API_KEY"
    }
  },
  "model": {
    "big": "opencode/big-pickle"
  }
}
```

**Provider precedence:** CLI flags > environment variables > config files > defaults. Model configuration precedence follows the same order.

---

## Project Structure

A typical OpenCode project:

```
my-project/
├── .opencode/
│   ├── config.json         # Project configuration
│   └── skills/             # Project-specific skills
├── opencode.json           # Project config (root)
├── src/                    # Your source code
├── tests/                  # Your tests
└── README.md
```

The `.opencode/` directory contains project-specific configurations and skills. The `opencode.json` file at the root is the main project configuration.

---

## Environment Variables

OpenCode uses a standardized environment variable scheme. All environment variables follow the `OPENCODE_` prefix convention.

Key variables:
- `OPENCODE_API_KEY` — API key for the default provider
- `OPENCODE_LOG_LEVEL` — Logging level (debug, info, warn, error)
- `OPENCODE_SESSION_DIR` — Custom directory for session storage
- `OPENCODE_CONFIG_DIR` — Custom directory for config files

---

## Quick Start

```bash
# Install
curl -fsSL https://opencode.ai/install | bash

# Start in current directory
opencode

# Start with a task
opencode run "implement user authentication"

# Resume a session
opencode run --resume
```

The TUI launches immediately. Press `?` to see all keybindings. Type your task in the input box and press Enter.

---

## The opencode.json Config File

Every OpenCode project has an `opencode.json` at the root. This file defines everything: models, agents, tools, permissions, MCP servers, and how they work together.

There are two styles:

1. **Simple mode** — use built-in defaults with minimal configuration
2. **Advanced mode** — override defaults and add custom configurations

The config is optional. OpenCode works out of the box with sensible defaults.

### Minimal Config

```json
{
  "model": {
    "big": "anthropic/claude-sonnet-4-6"
  }
}
```

### Full Config Example

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md", "docs/standards.md"],
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "big": "anthropic/claude-sonnet-4-6"
  },
  "provider": {
    "anthropic": {
      "name": "anthropic",
      "apiKey": "env:ANTHROPIC_API_KEY"
    }
  },
  "tools": {
    "preserve": {
      "bash": true
    }
  },
  "mcp": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-filesystem"]
    }
  },
  "skill": {
    "docs": {
      "path": ".opencode/skills/docs",
      "description": "Documentation generation",
      "trigger": "use when generating docs"
    }
  }
}
```

### Config File Locations

OpenCode searches for config files in this order:

1. `.opencode/config.json` (project-level, highest priority)
2. `opencode.json` (project root)
3. `~/.config/opencode/config.json` (user-level)

### Config Resolution

When merging configs from multiple sources:

- **Objects** are recursively merged (project overrides user)
- **Arrays** are replaced entirely (not merged)
- **Scalars** use the most specific value found
- **Environment variables** resolve at read time

---

## OpenCode TUI (Terminal UI)

The TUI is OpenCode's primary interface. It provides a visual workspace for interacting with the AI assistant directly in your terminal.

### Launching the TUI

```bash
# Start in current directory
opencode

# Start in a specific directory
opencode --dir /path/to/project

# Resume a session
opencode --resume
```

### Layout

The TUI is divided into distinct zones:

1. **Header** — Shows project name, model, and session info
2. **Messages** — The conversation view (scrollable)
3. **Input** — Where you type your messages
4. **Footer** — Mode indicator and key hints

### Commands

Commands are accessed with `/` in the input box:

- `/help` — Show all available commands
- `/model` — Switch the active model
- `/mode` — Switch between plan and auto modes
- `/clear` — Clear the current session
- `/export` — Export session to clipboard or file
- `/diff` — Show file changes in the session
- `/file` — Browse files in the project
- `/search` — Search for text in the project
- `/undo` — Undo the last file change
- `/redo` — Redo the last undone change
- `/task` — Start a new task
- `/quit` — Exit the TUI

### @ Mentions

Reference content directly in your input:

- `@filename` — Attach a file as context
- `@url` — Fetch and attach URL content
- `@issue` — Reference a GitHub issue
- `@pr` — Reference a pull request
- `@diff` — Show the current diff
- `@selection` — Reference selected text
- `@clipboard` — Paste clipboard content

### Keybindings

| Key | Action |
|-----|--------|
| `?` | Toggle help overlay |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+L` | Clear screen |
| `Up/Down` | Navigate message history |
| `Enter` | Send message |
| `Shift+Enter` | New line in input |
| `Ctrl+K` | Open model picker |
| `Tab` | Switch focus between panes |

The TUI also supports vim-style navigation in certain contexts.

### File Viewer

The TUI has a built-in file viewer accessible via the `/file` command. It supports syntax highlighting and allows you to browse your project's file structure without leaving the terminal.

### Diff View

The `/diff` command shows a side-by-side or unified diff of all file changes made during the current session. This provides full visibility into what OpenCode has modified.

### Settings Panel

The settings panel lets you change model, provider, and mode settings without leaving the TUI. Access it with `/setting` or the gear icon in the footer.

### Themes

OpenCode supports customizable color themes. Configure via the `/theme` command or in `opencode.json`:

```json
{
  "theme": {
    "name": "opencode",
    "colors": {
      "background": "#0e1419",
      "text": "#e5e1e8",
      "accent": "#2471e2",
      "success": "#299d2c",
      "error": "#e0294b",
      "warning": "#ff9500",
      "info": "#1a8cda"
    }
  }
}
```

The TUI renders all colors using ANSI 24-bit true color. If your terminal does not support true color, OpenCode automatically degrades to the nearest available palette.

---

## OpenCode Server

OpenCode can run as a background server, providing a REST API for programmatic access. This is useful for IDE integrations, automation, and custom tooling.

### Starting the Server

```bash
opencode server --port 8080
```

### REST API

The server exposes endpoints for:

- Session management (create, list, resume, export)
- Message submission
- Configuration retrieval
- Event streaming (SSE)
- Health checks

### Authentication

The server supports optional API key authentication:

```json
{
  "server": {
    "auth": {
      "type": "apikey",
      "key": "env:OPENCODE_SERVER_KEY"
    }
  }
}
```

---

## OpenCode Share

OpenCode Share allows you to share terminal sessions as interactive replays. When enabled, others can view and step through your session, seeing every command, output, and AI interaction.

### Configuration

```json
{
  "share": {
    "enabled": true
  }
}
```

### Privacy by Default

- Sessions are private unless explicitly shared
- No data is sent to external servers unless you opt in
- You control what gets shared and for how long

---

## OpenCode Zen

Zen is OpenCode's minimal mode. It hides the TUI and runs purely in the background, streaming output directly to your terminal. Useful for CI/CD pipelines and automated workflows.

### Configuration

```json
{
  "zen": {
    "enabled": true
  }
}
```

Or use the `--zen` flag:

```bash
opencode --zen run "run all tests and fix failures"
```

---

## OpenCode Web

OpenCode Web provides a browser-based interface for interacting with your OpenCode sessions. It mirrors the TUI functionality but in a web browser.

---

## OpenCode SSH

OpenCode supports remote sessions over SSH. This allows you to run OpenCode on a remote machine while interacting with it from your local terminal.

---

## OpenCode Go

OpenCode is written in Go. The Go SDK is available for building custom tooling and extensions. The SDK provides access to the core OpenCode engine, including:

- LLM provider abstraction
- Tool execution framework
- Session management
- Event system

---

## OpenCode SDK

The OpenCode SDK provides programmatic access to OpenCode's core functionality. Use it to build custom integrations, IDE plugins, or automation tools.

### Key Capabilities

- Start and manage sessions
- Submit messages and receive responses
- Access tool results
- Configure providers and models
- Stream events in real time

---

## Ecosystem

The OpenCode ecosystem includes:

- **Plugins** — Extend functionality via custom plugins
- **Skills** — Domain-specific instruction sets
- **MCP Servers** — Connect to external data sources and tools
- **LSP Integration** — Language Server Protocol for code intelligence
- **IDE Plugins** — VS Code and JetBrains extensions
- **GitHub Integration** — PR reviews, issue management, Actions triggers
- **Community** — Growing ecosystem of shared skills and plugins

---

## Troubleshooting

### Common Issues

**"Model not found"**
- Verify the provider and model name in `opencode.json`
- Check that your API key is set correctly
- Ensure the provider is available in your region

**"Tool execution failed"**
- Check tool permissions in `opencode.json`
- Verify the tool is available in the current mode
- Check for network connectivity issues

**"Session not found"**
- Verify the session exists with `opencode sessions`
- Check the session storage directory
- Try creating a new session

**TUI rendering issues**
- Ensure your terminal supports true color
- Try a different terminal emulator
- Check terminal size (minimum 80x24)

**Slow performance**
- Use a faster model for the `big` slot
- Reduce context window usage
- Check network latency to the provider

**"Permission denied"**
- Check the permission rules in your config
- Verify file system permissions
- Review the permissions section in the docs

### Debug Mode

Enable debug logging to diagnose issues:

```bash
OPENCODE_LOG_LEVEL=debug opencode
```

Or in config:

```json
{
  "logLevel": "debug"
}
```
