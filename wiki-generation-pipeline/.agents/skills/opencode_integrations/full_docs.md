# OpenCode Integrations — Complete Official Documentation

> **Source:** https://opencode.ai/mcp-servers — https://opencode.ai/lsp — https://opencode.ai/github — https://opencode.ai/gitlab — https://opencode.ai/ide — https://opencode.ai/share — https://opencode.ai/zen — https://opencode.ai/web — https://opencode.ai/server — retrieved July 2026

---

## Overview

OpenCode integrates with external systems through MCP servers, LSP, GitHub/GitLab, IDE plugins, SSH, and its built-in server. These integrations extend OpenCode's capabilities beyond local file editing.

---

## MCP (Model Context Protocol) Servers

MCP is a standard protocol for connecting AI assistants to external data sources and tools. OpenCode supports both stdio and SSE transports.

### Configuration

In `opencode.json`:

```json
{
  "mcp": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-filesystem"]
    },
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-github"],
      "env": {
        "GITHUB_TOKEN": "env:GITHUB_TOKEN"
      }
    },
    "remote-server": {
      "type": "sse",
      "url": "http://localhost:8080/sse"
    }
  }
}
```

### Transport Types

#### stdio Transport

Runs the MCP server as a child process. Communication happens via stdin/stdout.

```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@anthropic-ai/mcp-server-name"],
  "env": {}
}
```

#### SSE Transport (Server-Sent Events)

Connects to a remote MCP server via HTTP.

```json
{
  "type": "sse",
  "url": "http://localhost:8080/sse"
}
```

### MCP Server Management CLI

```bash
# List configured servers
opencode mcp list

# Test a connection
opencode mcp test filesystem

# Add a server interactively
opencode mcp add

# Remove a server
opencode mcp remove my-server
```

### Popular MCP Servers

| Server | Purpose | Package |
|--------|---------|---------|
| Filesystem | Read/write local files | `@anthropic-ai/mcp-filesystem` |
| GitHub | GitHub API access | `@anthropic-ai/mcp-github` |
| PostgreSQL | Database queries | `@anthropic-ai/mcp-postgres` |
| Slack | Slack API access | `@anthropic-ai/mcp-slack` |
| Brave Search | Web search | `@anthropic-ai/mcp-brave-search` |
| Google Drive | Google Drive access | `@anthropic-ai/mcp-gdrive` |
| Memory | Persistent key-value store | `@anthropic-ai/mcp-memory` |
| Puppeteer | Browser automation | `@anthropic-ai/mcp-puppeteer` |

### MCP Tool Permissions

MCP tools follow the same permission model as built-in tools:

```json
{
  "tools": {
    "always": ["mcp.filesystem.read_file"],
    "ask": ["mcp.github.create_issue"],
    "never": []
  }
}
```

### Custom MCP Server

Create your own MCP server using the MCP SDK:

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

const server = new Server(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "my_tool",
      description: "Does something useful",
      inputSchema: {
        type: "object",
        properties: {
          input: { type: "string" }
        }
      }
    }
  ]
}));
```

---

## LSP (Language Server Protocol)

OpenCode can connect to Language Servers for code intelligence: autocompletion, go-to-definition, diagnostics, and refactoring.

### Configuration

```json
{
  "lsp": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "languages": ["typescript", "typescriptreact"]
    },
    "python": {
      "command": "pylsp",
      "languages": ["python"]
    },
    "go": {
      "command": "gopls",
      "languages": ["go"]
    },
    "rust": {
      "command": "rust-analyzer",
      "languages": ["rust"]
    }
  }
}
```

### LSP Features

When an LSP server is configured, OpenCode gains:

- **Diagnostics** — Real-time error and warning detection
- **Go to definition** — Navigate to symbol definitions
- **Find references** — Locate all usages of a symbol
- **Autocomplete** — Code completions in the AI's context
- **Hover** — Type information and documentation
- **Code actions** — Quick fixes and refactoring suggestions

### Language Support

| Language | Server | Install |
|----------|--------|---------|
| TypeScript/JavaScript | `typescript-language-server` | `npm i -g typescript-language-server` |
| Python | `pylsp` | `pip install python-lsp-server` |
| Go | `gopls` | `go install golang.org/x/tools/gopls@latest` |
| Rust | `rust-analyzer` | Via rustup component |
| Java | `jdtls` | Eclipse JDT LS |
| C/C++ | `clangd` | Via LLVM |

---

## GitHub Integration

OpenCode integrates deeply with GitHub for PR reviews, issue management, and CI/CD.

### Configuration

Via MCP server:

```json
{
  "mcp": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-github"],
      "env": {
        "GITHUB_TOKEN": "env:GITHUB_TOKEN"
      }
    }
  }
}
```

### GitHub Features

#### PR Review

- Review pull requests with AI analysis
- Comment on specific lines
- Suggest code changes
- Approve/request changes

#### Issue Management

- Read and create issues
- Add labels and milestones
- Link issues to commits
- Auto-close issues via commit messages

#### Actions Integration

- Trigger workflows from OpenCode
- Read workflow logs
- Monitor CI/CD pipelines

### @ Issue Mentions

```bash
@issue #42 what's the status of this bug?
@issue #123 implement the feature described here
```

### @ PR Mentions

```bash
@pr #56 review this pull request
@pr #56 what tests are failing?
```

---

## GitLab Integration

Similar to GitHub integration but for GitLab instances.

### Configuration

Via MCP server or custom configuration:

```json
{
  "mcp": {
    "gitlab": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-gitlab"],
      "env": {
        "GITLAB_TOKEN": "env:GITLAB_TOKEN",
        "GITLAB_URL": "https://gitlab.com"
      }
    }
  }
}
```

### GitLab Features

- Merge request reviews
- Issue management
- Pipeline monitoring
- Wiki access

---

## IDE Plugins

### VS Code Extension

OpenCode integrates with VS Code via the OpenCode extension.

**Features:**
- Run OpenCode commands from the VS Code command palette
- View AI responses in a dedicated panel
- Inline code suggestions
- Terminal integration
- Diff view for AI changes

**Install:**
1. Open VS Code Extensions panel
2. Search for "OpenCode"
3. Install and configure

### JetBrains Plugin

Works with IntelliJ IDEA, WebStorm, PyCharm, and other JetBrains IDEs.

**Features:**
- AI assistant panel
- Code completion integration
- Refactoring suggestions
- Terminal integration

### Extension Configuration

```json
{
  "ide": {
    "vscode": {
      "enabled": true,
      "panel_position": "side"
    },
    "jetbrains": {
      "enabled": true
    }
  }
}
```

---

## OpenCode Server

Run OpenCode as a background server with a REST API.

### Starting the Server

```bash
# Default port (8080)
opencode server

# Custom port
opencode server --port 9090

# With authentication
opencode server --port 8080 --auth
```

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/sessions` | List sessions |
| `POST` | `/sessions` | Create session |
| `GET` | `/sessions/:id` | Get session |
| `POST` | `/sessions/:id/messages` | Send message |
| `GET` | `/sessions/:id/events` | SSE event stream |
| `GET` | `/config` | Get configuration |

### Server Configuration

```json
{
  "server": {
    "port": 8080,
    "host": "0.0.0.0",
    "auth": {
      "type": "apikey",
      "key": "env:OPENCODE_SERVER_KEY"
    },
    "cors": {
      "origins": ["http://localhost:3000"]
    }
  }
}
```

### Authentication

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

Include the API key in requests:

```bash
curl -H "Authorization: Bearer $OPENCODE_SERVER_KEY" \
  http://localhost:8080/sessions
```

### Server-Sent Events (SSE)

Stream events in real time:

```javascript
const events = new EventSource(
  'http://localhost:8080/sessions/abc123/events',
  { headers: { 'Authorization': `Bearer ${apiKey}` } }
);

events.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

---

## OpenCode Share

Share terminal sessions as interactive replays.

### Configuration

```json
{
  "share": {
    "enabled": true,
    "privacy": "private"
  }
}
```

### Sharing Workflow

1. Run your session in OpenCode
2. When done, use `/export` to export the session
3. Share the exported file
4. Recipients can replay the session step-by-step

### Privacy Settings

| Setting | Description |
|---------|-------------|
| `private` | Only you can view shared sessions |
| `team` | Team members with the link can view |
| `public` | Anyone with the link can view |

---

## OpenCode SSH

Remote sessions over SSH.

### Configuration

```bash
# Connect to remote
opencode ssh user@host

# Custom port
opencode ssh -p 2222 user@host

# With project path
opencode ssh user@host:/path/to/project
```

### Remote Setup

On the remote machine:

```bash
# Install OpenCode
curl -fsSL https://opencode.ai/install | bash

# Start in server mode
opencode server --port 8080
```

### SSH Tunnel

```bash
# Create SSH tunnel
ssh -L 8080:localhost:8080 user@host

# Then connect locally
opencode --dir /local/path
```

---

## OpenCode Web

Browser-based interface for OpenCode sessions.

### Configuration

```json
{
  "web": {
    "enabled": true,
    "port": 3000
  }
}
```

### Accessing the Web UI

1. Start the server: `opencode server --port 8080`
2. Open browser to `http://localhost:8080`
3. Authenticate if required
4. Start interacting

---

## ACP (Agent Communication Protocol)

Agent-to-agent communication for multi-agent workflows.

### Configuration

```json
{
  "acp": {
    "enabled": true,
    "peers": [
      {
        "name": "code-reviewer",
        "url": "http://localhost:8081",
        "capabilities": ["review", "analyze"]
      }
    ]
  }
}
```

---

## Cross-Integration Workflows

### GitHub → OpenCode → GitHub

1. `@issue #42` — Pull issue context into OpenCode
2. Implement the fix using AI assistance
3. `git commit` and `git push` via bash tool
4. Create PR via GitHub MCP integration
5. AI reviews the PR and posts comments

### VS Code → OpenCode → VS Code

1. Select code in VS Code
2. Run "OpenCode: Explain Selection" from command palette
3. AI explains the code in the OpenCode panel
4. Apply suggested changes back to VS Code

### CI/CD → OpenCode Server

1. GitHub Action triggers on PR
2. Calls OpenCode Server REST API
3. AI reviews the code changes
4. Posts review comments back to the PR
