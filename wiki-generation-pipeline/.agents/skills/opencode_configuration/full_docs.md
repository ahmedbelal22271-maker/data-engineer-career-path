# OpenCode Configuration Reference — Complete Official Documentation

> **Source:** https://opencode.ai/config — retrieved July 2026
> **Schema:** https://opencode.ai/config.json

---

## Overview

OpenCode is configured through `opencode.json` (or `opencode.jsonc` with comments). The config file lives at your project root and controls models, providers, tools, permissions, MCP servers, skills, and more.

**Config is optional.** OpenCode works out of the box with sensible defaults.

---

## Config File Locations

OpenCode searches in this order (first match wins):

1. `.opencode/config.json` — project-level (highest priority)
2. `opencode.json` — project root
3. `~/.config/opencode/config.json` — user-level (lowest priority)

---

## Config Resolution

When merging configs from multiple sources:

- **Objects** are recursively merged (project overrides user)
- **Arrays** are replaced entirely (not merged)
- **Scalars** use the most specific value found
- **Environment variables** resolve at read time using `env:VAR_NAME` syntax

---

## All Configuration Fields

### `$schema`

Type: `string` | Optional

Provides IDE autocompletion and validation. Points to the OpenCode JSON schema.

```json
{
  "$schema": "https://opencode.ai/config.json"
}
```

### `instructions`

Type: `string[]` | Optional | Default: `[]`

Files loaded into every session. These provide behavioral guidance and context to the AI. Supports file paths relative to the config file.

```json
{
  "instructions": ["AGENTS.md", "docs/standards.md", ".opencode/rules/*.md"]
}
```

**Glob patterns supported:** `"*.md"` matches all .md files in the directory.

### `tools`

Type: `object` | Optional

Controls which tools are available and their behavior.

#### `tools.always`

Type: `string[]` | Optional

Tools that are always available without asking for permission.

```json
{
  "tools": {
    "always": ["read", "glob", "grep", "web_search"]
  }
}
```

#### `tools.never`

Type: `string[]` | Optional

Tools that are never available, even if requested.

```json
{
  "tools": {
    "never": ["bash"]
  }
}
```

#### `tools.ask`

Type: `string[]` | Optional

Tools that require user confirmation before executing.

```json
{
  "tools": {
    "ask": ["write", "edit"]
  }
}
```

#### `tools.preserve`

Type: `Record<string, boolean>` | Optional

Preserves tool state between sessions. When set to `true`, the tool remembers its last permission decision.

```json
{
  "tools": {
    "preserve": {
      "bash": true,
      "write": false
    }
  }
}
```

#### `tools.command`

Type: `Record<string, object>` | Optional

Custom tool definitions. Each key is a tool name, and the value defines the command.

```json
{
  "tools": {
    "command": {
      "run-tests": {
        "description": "Run the project test suite",
        "command": "npm test",
        "timeout": 120000
      }
    }
  }
}
```

### `model`

Type: `object` | Optional

Configures which AI models to use.

#### `model.primary`

Type: `string` | Optional

The main model for reasoning, planning, and editing. Format: `provider/model-name`.

```json
{
  "model": {
    "primary": "anthropic/claude-sonnet-4-6"
  }
}
```

#### `model.big`

Type: `string` | Optional

The model used for large codebase exploration and search. Optimized for speed and large context windows.

```json
{
  "model": {
    "big": "anthropic/claude-sonnet-4-6"
  }
}
```

### `provider`

Type: `Record<string, ProviderConfig>` | Optional

Configures AI providers. Each key is a provider name.

```json
{
  "provider": {
    "anthropic": {
      "name": "anthropic",
      "apiKey": "env:ANTHROPIC_API_KEY"
    },
    "openai": {
      "name": "openai",
      "apiKey": "env:OPENAI_API_KEY"
    },
    "opencode": {
      "name": "opencode",
      "apiKey": "env:OPENCODE_API_KEY"
    }
  }
}
```

**Provider fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Display name |
| `apiKey` | `string` | API key (use `env:VAR` for env vars) |
| `apiUrl` | `string` | Custom API base URL |
| `models` | `object[]` | Override available models |

### `mode`

Type: `string` | Optional | Default: `"auto"`

The default operational mode. Options: `"plan"`, `"auto"`.

```json
{
  "mode": "plan"
}
```

Override at runtime with `/mode` in TUI or `--mode` on CLI.

### `permission`

Type: `string` | Optional | Default: `"default"`

Permission mode for tool execution. Options: `"bypass"`, `"default"`, `"rules"`.

```json
{
  "permission": "bypass"
}
```

### `logLevel`

Type: `string` | Optional | Default: `"info"`

Logging verbosity. Options: `"debug"`, `"info"`, `"warn"`, `"error"`.

```json
{
  "logLevel": "debug"
}
```

### `theme`

Type: `object` | Optional

UI theme configuration for the TUI.

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

**Theme tokens:** `background`, `text`, `accent`, `success`, `error`, `warning`, `info`, `muted`, `border`, `selection`, `highlight`, `dim`

### `keybindings`

Type: `object` | Optional

Custom keyboard shortcuts for the TUI.

```json
{
  "keybindings": {
    "send": "enter",
    "cancel": "ctrl+c",
    "model_picker": "ctrl+k",
    "help": "?"
  }
}
```

### `mcp`

Type: `Record<string, McpServerConfig>` | Optional

Model Context Protocol (MCP) servers for extending tool capabilities.

```json
{
  "mcp": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-filesystem"],
      "env": {}
    },
    "remote-server": {
      "type": "sse",
      "url": "http://localhost:8080/sse"
    }
  }
}
```

**MCP server fields:**

| Field | Type | Description |
|-------|------|-------------|
| `type` | `"stdio"` \| `"sse"` | Transport type |
| `command` | `string` | Command to run (stdio) |
| `args` | `string[]` | Command arguments (stdio) |
| `url` | `string` | Server URL (SSE) |
| `env` | `Record<string, string>` | Environment variables |
| `disabled` | `boolean` | Disable without removing |

### `skill`

Type: `Record<string, SkillConfig>` | Optional

Custom skill definitions for the project.

```json
{
  "skill": {
    "docs": {
      "path": ".opencode/skills/docs",
      "description": "Documentation generation",
      "trigger": "use when generating or updating documentation"
    },
    "testing": {
      "path": ".opencode/skills/testing",
      "description": "Test generation and execution",
      "trigger": "use when writing or running tests"
    }
  }
}
```

**Skill fields:**

| Field | Type | Description |
|-------|------|-------------|
| `path` | `string` | Path to skill directory (relative to config) |
| `description` | `string` | Human-readable description |
| `trigger` | `string` | When to activate the skill |

### `agent`

Type: `Record<string, AgentConfig>` | Optional

Custom agent definitions. Each agent has its own model, tools, and behavior.

```json
{
  "agent": {
    "reviewer": {
      "model": "anthropic/claude-opus-4-6",
      "tools": ["read", "glob", "grep"],
      "instructions": ["docs/review-checklist.md"]
    }
  }
}
```

**Agent fields:**

| Field | Type | Description |
|-------|------|-------------|
| `model` | `string` | Model to use for this agent |
| `tools` | `string[]` | Tools available to this agent |
| `instructions` | `string[]` | Additional instruction files |
| `permission` | `string` | Permission mode override |

### `network`

Type: `object` | Optional

Network configuration for proxies, TLS, and retries.

```json
{
  "network": {
    "proxy": "http://proxy.example.com:8080",
    "tls": {
      "insecure": false,
      "ca": "/path/to/ca-cert.pem"
    },
    "retries": {
      "max": 3,
      "backoff": "exponential"
    }
  }
}
```

### `server`

Type: `object` | Optional

Configuration for the OpenCode Server (background mode).

```json
{
  "server": {
    "port": 8080,
    "auth": {
      "type": "apikey",
      "key": "env:OPENCODE_SERVER_KEY"
    }
  }
}
```

### `share`

Type: `object` | Optional

Terminal session sharing configuration.

```json
{
  "share": {
    "enabled": true,
    "privacy": "private"
  }
}
```

### `zen`

Type: `object` | Optional

Zen (minimal) mode configuration.

```json
{
  "zen": {
    "enabled": false
  }
}
```

### `subagent`

Type: `object` | Optional

Subagent behavior configuration.

```json
{
  "subagent": {
    "depth": 3
  }
}
```

**Note:** The `subagent_depth` field was not recognized in v1.17.20. Check your version for support.

---

## Supported Providers

| Provider | Models | Config Key |
|----------|--------|------------|
| Anthropic | Claude Opus/Sonnet/Haiku | `anthropic` |
| OpenAI | GPT-4o, o1, o3 | `openai` |
| Google | Gemini 2.5 Pro/Flash | `google` |
| AWS Bedrock | Claude, Llama via Bedrock | `bedrock` |
| Azure OpenAI | GPT-4o via Azure | `azure` |
| GCP Vertex AI | Gemini via Vertex | `vertex` |
| Ollama | Local models | `ollama` |
| OpenRouter | Multi-provider routing | `openrouter` |
| Custom (OpenAI-compatible) | Any compatible endpoint | `custom` |

---

## Environment Variables

All config values can be overridden via environment variables with the `OPENCODE_` prefix:

| Variable | Config Equivalent |
|----------|-------------------|
| `OPENCODE_API_KEY` | `provider.*.apiKey` |
| `OPENCODE_MODEL` | `model.primary` |
| `OPENCODE_PROVIDER` | Provider selection |
| `OPENCODE_MODE` | `mode` |
| `OPENCODE_LOG_LEVEL` | `logLevel` |
| `OPENCODE_CONFIG_DIR` | Config directory |
| `OPENCODE_SESSION_DIR` | Session storage |

---

## Config Validation

OpenCode validates your config on startup. Common validation errors:

| Error | Cause | Fix |
|-------|-------|-----|
| Unknown property | Unsupported field for your version | Remove the field |
| Invalid model format | Model name not in `provider/model` format | Fix the model string |
| Missing API key | Provider needs authentication | Set the API key |
| Invalid MCP config | Missing required fields | Check MCP server config |

Use `opencode config --validate` to check your config without starting OpenCode.

---

## Example Configs

### Minimal (just set a model)

```json
{
  "model": {
    "primary": "anthropic/claude-sonnet-4-6"
  }
}
```

### Multi-provider

```json
{
  "provider": {
    "anthropic": {
      "apiKey": "env:ANTHROPIC_API_KEY"
    },
    "openai": {
      "apiKey": "env:OPENAI_API_KEY"
    }
  },
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "big": "openai/gpt-4o"
  }
}
```

### With MCP and Skills

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md"],
  "model": {
    "primary": "anthropic/claude-sonnet-4-6"
  },
  "mcp": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-github"]
    }
  },
  "skill": {
    "custom-tool": {
      "path": ".opencode/skills/custom-tool",
      "description": "Custom project tool",
      "trigger": "use for project-specific operations"
    }
  }
}
```

### Enterprise (with network and auth)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "anthropic": {
      "apiKey": "env:ANTHROPIC_API_KEY"
    }
  },
  "network": {
    "proxy": "env:HTTP_PROXY",
    "tls": {
      "ca": "/etc/ssl/certs/company-ca.pem"
    }
  },
  "permission": "rules",
  "tools": {
    "always": ["read", "glob", "grep"],
    "ask": ["write", "edit", "bash"]
  },
  "server": {
    "port": 8080,
    "auth": {
      "type": "apikey",
      "key": "env:OPENCODE_SERVER_KEY"
    }
  }
}
```
