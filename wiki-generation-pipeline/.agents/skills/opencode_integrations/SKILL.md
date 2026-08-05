---
name: opencode Integrations
description: Complete reference for connecting opencode to external systems — MCP (Model Context Protocol) server configuration with SSE and stdio transports, ACP (Agent Communication Protocol) for agent-to-agent communication, LSP (Language Server Protocol) for language intelligence, GitHub integration (PR review, issues, Actions), IDE plugins (VS Code, JetBrains), opencode Share, opencode Server, Zen mode, and SSH remote sessions. Trigger on "MCP", "ACP", "LSP", "GitHub", "integration", "IDE", "VS Code", "JetBrains", "plugin", "remote", "Share", "Server", "SSH", or "Zen" questions.
---

# opencode Integrations

## 1. MCP (Model Context Protocol)

Connect opencode to external tools and services.

### Server Configuration

Full annotated example:

```jsonc
{
  "mcp_servers": [
    {
      "name": "database",
      "url": "http://localhost:3000/mcp",
      "transport": "sse",
      "tools": ["query", "migrate"],
      "headers": {
        "Authorization": "Bearer ${MCP_TOKEN}"
      }
    },
    {
      "name": "local-service",
      "transport": "stdio",
      "command": "node",
      "args": ["./mcp-server/index.js"],
      "tools": ["*"]
    }
  ]
}
```

Fields: name, url, transport (sse/stdio), tools (allowlist), headers (for SSE), command+args (for stdio).

### MCP CLI

```
opencode mcp list
opencode mcp add db http://...
opencode mcp remove db
opencode mcp test db
opencode mcp start local
opencode mcp stop local
```

### MCP Tool Interface

MCP tools appear alongside built-in tools. AI can call them like any other tool. Return structured data.

## 2. ACP (Agent Communication Protocol)

Agent-to-agent communication protocol.

- Agent discovery: find agents by capability
- Message passing: structured format between agents
- Task delegation: delegate subtasks, await results
- Result aggregation: parent collects and synthesizes
- Used internally by the `task` tool and `--subagent` flag

## 3. LSP (Language Server Protocol)

- Syntax-aware completions
- Go to definition
- Find references
- Diagnostics (errors, warnings)
- LSP servers detected from project config (tsconfig.json, .vscode/settings.json)
- File viewer uses LSP for syntax highlighting and navigation

## 4. GitHub Integration

- PR review: `opencode run scripts/review_pr.md`
- Issue triage: `@issue <n>` in TUI
- GitHub Actions: use `opencode run` in workflows
- Show a sample GitHub Actions workflow YAML:

```yaml
name: opencode Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: opencode run scripts/review_pr.md --yes --output-format json
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- Authentication via GITHUB_TOKEN or gh CLI

## 5. IDE Integration

### VS Code

- opencode extension for VS Code
- Open files from VS Code in opencode
- Send selections to opencode
- View results in VS Code
- Ctrl+Shift+P → opencode: Open

### JetBrains

- Plugin from Marketplace
- Tool windows, keybindings, editor integration

## 6. opencode Share

Share conversations and results:

```
opencode run task.md --output-format html --save share.html
opencode publish share.html
```

## 7. opencode Server

Run as a networked service:

```
opencode server start --port 8080
opencode server start --port 8080 --tls-cert cert.pem --tls-key key.pem
```

Features: REST API for tasks, WebSocket streaming, MCP endpoint, team management with RBAC, usage metrics

## 8. SSH Remote Sessions

```
opencode ssh user@remote-server "explain the project"
opencode ssh dev-server -- bash "run deploy script"
```

Flags: --port, --user, --key, --forward-agent

## 9. Zen Mode

Minimalist mode for focused work:

- Hides all UI chrome
- Shows only chat panel
- `/zen` to toggle
- `--zen` flag on startup

---

### Full Documentation
For the complete official opencode integrations documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of MCP servers, LSP, ACP, GitHub/GitLab, IDE plugins, Server, Share, Web, SSH, and cross-integration workflows.

### Cross-references

- **opencode_cli_commands** — mcp, ssh commands
- **opencode_configuration** — mcp_servers config
- **opencode_agents_subagents** — ACP for subagents
- **opencode_tools_catalog** — MCP tools
