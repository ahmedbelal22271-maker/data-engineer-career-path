---
name: opencode Configuration Reference
description: Complete reference for opencode.json/opencode.jsonc — every configuration field, its type, description, behavioral implications, and examples. Covers $schema, instructions, system_prompt, tools, models, agents, hooks, notifications, custom_keys, theme, keybindings, rules, skills, permissions, network, mcp_servers, output_formats, and more. Trigger on "configure opencode", "opencode.json", "config setup", "how to set up opencode", or any config field question.
---

# opencode Configuration Reference

## 1. File Location & Schema

opencode looks for a configuration file named `opencode.json` or `opencode.jsonc` (JSON with comments) at the project root. If not found, it searches upward through parent directories. The config file defines how opencode behaves in that project — model selection, tools, agents, hooks, permissions, and more.

To enable IDE autocompletion and validation, add:

```jsonc
"$schema": "https://opencode.ai/config.json"
```

## 2. Complete Configuration Example

```jsonc
{
  "$schema": "https://opencode.ai/config.json",

  // --- Instructions ---
  "instructions": [
    ".opencode/instructions/system.md",
    ".opencode/instructions/coding.md"
  ],

  // --- System Prompt Override ---
  "system_prompt": "You are an expert software engineer. Respond concisely.",

  // --- Tools ---
  "tools": {
    "allow": ["*"],
    "deny": []
  },

  // --- Models ---
  "models": {
    "default": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "max_tokens": 8192,
      "temperature": 0.7
    },
    "reasoning": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "max_tokens": 16384,
      "thinking": {
        "type": "enabled",
        "budget_tokens": 4096
      },
      "effort": "high"
    },
    "fast": {
      "provider": "anthropic",
      "model": "claude-haiku-4-20250514",
      "max_tokens": 4096,
      "temperature": 0.3
    },
    "local": {
      "provider": "openai",
      "model": "gpt-4o-mini",
      "base_url": "http://localhost:1234/v1",
      "api_key": "${LOCAL_API_KEY}",
      "max_tokens": 4096
    }
  },

  // --- Agents ---
  "agents": {
    "code": {
      "model": {
        "provider": "anthropic",
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 16384
      },
      "tools": {
        "allow": ["*"],
        "deny": ["web_search", "web_fetch"]
      },
      "instructions": [".opencode/agents/code.md"]
    },
    "explore": {
      "model": {
        "provider": "anthropic",
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 8192
      },
      "tools": {
        "allow": ["*"],
        "deny": ["write", "edit"]
      },
      "instructions": [".opencode/agents/explore.md"]
    }
  },

  // --- Hooks ---
  "hooks": {
    "pre_tool": ["echo \"Running tool: $TOOL_NAME\""],
    "post_tool": ["echo \"Tool completed: $TOOL_NAME\""],
    "pre_command": ["echo \"Executing: $COMMAND\""],
    "post_command": ["echo \"Command finished: $COMMAND\""],
    "on_startup": ["echo \"Session started\""],
    "on_shutdown": ["echo \"Session ended\""]
  },

  // --- Notifications ---
  "notifications": {
    "on_completion": true,
    "on_error": true,
    "provider": "desktop"
  },

  // --- Custom Keys ---
  "custom_keys": [
    {
      "key": "ctrl+shift+p",
      "command": "opencode.project",
      "description": "Open project selector"
    }
  ],

  // --- Theme ---
  "theme": "dark-plus",

  // --- Keybindings ---
  "keybindings": ".opencode/keybindings.json",

  // --- Rules ---
  "rules": ".opencode/rules",

  // --- Skills ---
  "skills": {
    "paths": [".agents/skills"]
  },

  // --- Permissions ---
  "permissions": {
    "mode": "default",
    "policies": ".opencode/permissions.json"
  },

  // --- Network ---
  "network": {
    "proxy": "http://proxy.company.com:8080",
    "timeout": 60000,
    "retry_count": 3,
    "retry_delay": 1000
  },

  // --- MCP Servers ---
  "mcp_servers": [
    {
      "name": "filesystem",
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    {
      "name": "custom-api",
      "transport": "sse",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${MCP_TOKEN}"
      },
      "tools": ["read-db", "query-data"]
    }
  ],

  // --- Output Formats ---
  "output_formats": ["terminal", "markdown"],

  // --- Misc ---
  "hide_hints": false,
  "verbose": true,
  "skip_confirm": false,
  "auto_execute": false,
  "agent_concurrency": 3,
  "log_level": "info",
  "log_file": ".opencode/logs/session.log"
}
```

## 3. Complete Field Reference

### `$schema`

- **Type:** `string` (optional)
- **Description:** URL pointing to the opencode JSON Schema for IDE autocompletion and validation.
- **Behavioral implications:** No runtime effect. Helps editors provide inline documentation, type checking, and error highlights while editing the config file.
- **Example:**
  ```jsonc
  "$schema": "https://opencode.ai/config.json"
  ```

### `instructions`

- **Type:** `string[]` (required)
- **Description:** Array of file paths to instruction/markdown files. Each file is read and concatenated into the system prompt in order. These files contain behavioral directives, conventions, and constraints for the model.
- **Behavioral implications:** Instruction files consume context window tokens — keep them lean. They are injected before any system_prompt text. Changes take effect on next session.
- **Example:**
  ```jsonc
  "instructions": [
    ".opencode/instructions/system.md",
    ".opencode/instructions/coding.md"
  ]
  ```

### `system_prompt`

- **Type:** `string` (optional)
- **Description:** Additional text appended after instructions in the system prompt. Can override or supplement behavior defined in instruction files.
- **Behavioral implications:** Appended after instruction files. Useful for short, session-specific overrides without creating a new instruction file.
- **Example:**
  ```jsonc
  "system_prompt": "Always ask before running destructive commands."
  ```

### `tools`

- **Type:** `object` (optional) — `{ allow: string[], deny: string[] }`
- **Description:** Controls which tools the model can call. `"allow": ["*"]` permits all built-in tools. Specific tool names can be allowed or denied individually.
- **Behavioral implications:** Deny overrides allow. If a tool is in both arrays, it is denied. Restricting tools changes the model's capabilities and can force it to use alternative approaches.
- **Tool names:** `bash`, `read`, `edit`, `write`, `glob`, `grep`, `web_search`, `web_fetch`, `task`, `question`, `todowrite`, `skill`
- **Example:**
  ```jsonc
  "tools": {
    "allow": ["bash", "read", "edit", "write", "glob", "grep"],
    "deny": ["web_search", "web_fetch"]
  }
  ```

### `models`

- **Type:** `object` (required)
- **Description:** Named model configurations. At minimum, a `"default"` key is required — this model is used unless another is explicitly selected. Each model config defines provider, model name, and optional parameters.
- **Behavioral implications:** The default model handles all requests unless another model is specified by an agent or explicitly chosen. Multiple models enable task routing (e.g., cheap model for fast tasks, reasoning model for complex ones).
- **Fields per model config:**

  | Field | Type | Required | Description |
  |-------|------|----------|-------------|
  | `provider` | `string` | yes | `"anthropic"`, `"openai"`, `"google"`, `"aws_bedrock"`, `"gcp_vertex"`, `"azure"`, `"ollama"`, `"open_compatible"` |
  | `model` | `string` | yes | Model ID (e.g., `"claude-sonnet-4-20250514"`) |
  | `max_tokens` | `integer` | no | Maximum output tokens |
  | `temperature` | `number` | no | Sampling temperature (0.0–1.0) |
  | `api_key` | `string` | no | Supports `${ENV_VAR}` syntax for environment variables |
  | `base_url` | `string` | no | Custom API endpoint (required for ollama, open_compatible) |
  | `thinking` | `object` | no | `{ type: "adaptive"\|"enabled"\|"disabled", budget_tokens: integer }` |
  | `effort` | `string` | no | `"low"`, `"medium"`, `"high"`, `"max"` — for supported providers |
  | `description` | `string` | no | Human-readable label for UI display |

- **Example:**
  ```jsonc
  "models": {
    "default": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "max_tokens": 8192
    },
    "reasoning": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "max_tokens": 16384,
      "thinking": { "type": "enabled", "budget_tokens": 4096 },
      "effort": "high"
    }
  }
  ```

### `agents`

- **Type:** `object` (optional)
- **Description:** Defines subagent configurations that can be invoked for specialized tasks. Each agent can specify its own model, tool permissions, instruction files, and parameter overrides. Agents inherit from the default model if not specified.
- **Behavioral implications:** Agents enable role-specific behavior — e.g., a "code" agent with full tool access and a "explore" agent that can read but not write. Agent instructions are injected alongside base instructions. Agent tool allow/deny lists merge with the top-level tools config.
- **Fields per agent:**

  | Field | Type | Description |
  |-------|------|-------------|
  | `model` | `object` | Model config (same schema as models entry) |
  | `tools` | `object` | Tool allow/deny overrides specific to this agent |
  | `instructions` | `string[]` | Additional instruction files for this agent |
  | `max_tokens` | `integer` | Per-agent token limit override |
  | `temperature` | `number` | Per-agent temperature override |
  | `skills` | `string[]` | Paths to SKILL.md files for this agent |

- **Example:**
  ```jsonc
  "agents": {
    "code": {
      "model": { "provider": "anthropic", "model": "claude-sonnet-4-20250514" },
      "tools": { "allow": ["*"], "deny": ["web_search"] },
      "instructions": [".opencode/agents/code.md"]
    }
  }
  ```

### `hooks`

- **Type:** `object` (optional)
- **Description:** Lifecycle hooks that execute shell commands at specific points in opencode's execution flow. Hooks run synchronously — the session waits for completion before proceeding.
- **Behavioral implications:** Pre-tool hooks run before every tool call; post-tool hooks run after. Can be used for logging, metrics, validation, or environment setup. Failed hooks do not block execution by default.
- **Hook types:**

  | Hook | Trigger | Available Variables |
  |------|---------|-------------------|
  | `pre_tool` | Before each tool call | `$TOOL_NAME`, `$TOOL_INPUT` |
  | `post_tool` | After each tool call | `$TOOL_NAME`, `$TOOL_OUTPUT`, `$TOOL_EXIT_CODE` |
  | `pre_command` | Before each bash command | `$COMMAND` |
  | `post_command` | After each bash command | `$COMMAND`, `$EXIT_CODE` |
  | `on_startup` | Session start | — |
  | `on_shutdown` | Session end | — |

- **Example:**
  ```jsonc
  "hooks": {
    "pre_tool": ["echo \"[$TOOL_NAME] starting\""],
    "post_tool": ["echo \"[$TOOL_NAME] exit: $TOOL_EXIT_CODE\""]
  }
  ```

### `notifications`

- **Type:** `object` (optional)
- **Description:** Configures desktop or webhook notifications for session events.
- **Behavioral implications:** When enabled, opencode sends OS-level desktop notifications (or webhook POST requests) on completion or error. Useful for long-running tasks.
- **Example:**
  ```jsonc
  "notifications": {
    "on_completion": true,
    "on_error": true,
    "provider": "desktop",
    "webhook_url": "https://hooks.example.com/opencode"
  }
  ```

### `custom_keys`

- **Type:** `array` of `object` (optional)
- **Description:** Custom keyboard shortcuts for the TUI interface. Each entry maps a key combination to a command.
- **Behavioral implications:** Overrides default keybindings when conflicts occur. Only active in TUI mode.
- **Example:**
  ```jsonc
  "custom_keys": [
    {
      "key": "ctrl+shift+p",
      "command": "opencode.project",
      "description": "Open project selector"
    }
  ]
  ```

### `theme`

- **Type:** `string` (optional)
- **Description:** Theme name or path to a custom theme file for the TUI. Built-in themes include `"dark-plus"`, `"light-plus"`, `"catppuccin"`, `"nord"`, `"monokai"`.
- **Behavioral implications:** Only affects TUI appearance. Custom themes can be loaded from file paths or npm packages.
- **Example:**
  ```jsonc
  "theme": "catppuccin-mocha"
  ```

### `keybindings`

- **Type:** `string` (optional)
- **Description:** Path to a custom keybindings JSON file. Allows full remapping of all TUI keyboard shortcuts.
- **Behavioral implications:** Overrides all default keybindings. File should follow opencode's keybindings schema.
- **Example:**
  ```jsonc
  "keybindings": ".opencode/keybindings.json"
  ```

### `rules`

- **Type:** `string` (optional)
- **Description:** Path to the rules directory. Defaults to `.opencode/rules/`. Rules are markdown files that define behavioral constraints and permissions.
- **Behavioral implications:** Rules are loaded and enforced at session start. Changing rules requires a new session. See the rules/permissions reference for rule format.
- **Example:**
  ```jsonc
  "rules": ".opencode/custom-rules"
  ```

### `skills`

- **Type:** `object` (optional)
- **Description:** Configures skill directories. An object with `paths` (array of directories scanned recursively for `**/SKILL.md`) and/or `urls` (remote skill lists). **Not an array** — the array form was used in opencode <1.x versions and is no longer valid. Using `"skills": [...]` will cause an initialization error.
- **Behavioral implications:** Skills are loaded at session start and are available to the model. They appear in the system prompt and can be triggered by the skill tool.
- **Example:**
  ```jsonc
  "skills": {
    "paths": [".agents/skills"]
  }
  ```

### `permissions`

- **Type:** `object` (optional)
- **Description:** Controls the permissions mode and policy file path.
- **Behavioral implications:** `"bypass"` skips all permission checks. `"non-bypass"` requires user confirmation for every operation. `"default"` uses the standard permission model. The policies file defines granular allow/deny rules for paths, tools, and commands.
- **Modes:**

  | Mode | Behavior |
  |------|----------|
  | `"default"` | Standard permission checks; sensitive operations require confirmation |
  | `"bypass"` | All operations proceed without confirmation (use with caution) |
  | `"non-bypass"` | Every operation requires explicit user confirmation |

- **Example:**
  ```jsonc
  "permissions": {
    "mode": "default",
    "policies": ".opencode/permissions.json"
  }
  ```

### `network`

- **Type:** `object` (optional)
- **Description:** Network configuration for API calls to LLM providers.
- **Behavioral implications:** Applies to all outbound HTTP requests from opencode. Timeout and retry settings affect reliability. Proxy is used for both API calls and web fetch/search tools.
- **Example:**
  ```jsonc
  "network": {
    "proxy": "http://proxy.company.com:8080",
    "custom_headers": { "X-Correlation-Id": "${CORRELATION_ID}" },
    "timeout": 60000,
    "retry_count": 3,
    "retry_delay": 1000
  }
  ```

### `mcp_servers`

- **Type:** `array` of `object` (optional)
- **Description:** Model Context Protocol servers that provide additional tools and capabilities to the model. Supports both SSE (remote) and stdio (local) transports.
- **Behavioral implications:** MCP tools are merged with built-in tools and are available to the model in every session. Useful for database access, file system operations, API integrations, and custom tooling.
- **Fields per server:**

  | Field | Type | Required | Description |
  |-------|------|----------|-------------|
  | `name` | `string` | yes | Unique identifier for the server |
  | `transport` | `string` | yes | `"sse"` or `"stdio"` |
  | `url` | `string` | for sse | SSE endpoint URL |
  | `command` | `string` | for stdio | Executable command to start the server |
  | `args` | `string[]` | no | Arguments for the command |
  | `headers` | `object` | no | HTTP headers for SSE transport |
  | `tools` | `string[]` | no | Filter to only expose specific tools from this server |

- **Example:**
  ```jsonc
  "mcp_servers": [
    {
      "name": "fs",
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  ]
  ```

### `output_formats`

- **Type:** `string[]` (optional)
- **Description:** Controls the output format(s) for model responses.
- **Behavioral implications:** Multiple formats can be specified (e.g., terminal + markdown). Certain formats enable structured output for CI/CD pipelines.
- **Options:** `"terminal"`, `"json"`, `"jsonl"`, `"json-stream"`, `"markdown"`, `"html"`, `"file"`, `"edit"`
- **Example:**
  ```jsonc
  "output_formats": ["json", "file"]
  ```

### `hide_hints`

- **Type:** `boolean` (optional, default: `false`)
- **Description:** Hides usage hints and tips shown at session start and during interactions.
- **Example:**
  ```jsonc
  "hide_hints": true
  ```

### `verbose`

- **Type:** `boolean` (optional, default: `false`)
- **Description:** Enables verbose logging output, including tool input/output details and internal state.
- **Example:**
  ```jsonc
  "verbose": true
  ```

### `skip_confirm`

- **Type:** `boolean` (optional, default: `false`)
- **Description:** Skips confirmation prompts for non-destructive operations.
- **Example:**
  ```jsonc
  "skip_confirm": true
  ```

### `auto_execute`

- **Type:** `boolean` (optional, default: `false`)
- **Description:** Automatically executes bash commands without user confirmation. Use with caution.
- **Example:**
  ```jsonc
  "auto_execute": true
  ```

### `agent_concurrency`

- **Type:** `integer` (optional, default varies)
- **Description:** Maximum number of concurrent agent invocations. Limits parallel subagent execution.
- **Example:**
  ```jsonc
  "agent_concurrency": 5
  ```

### `log_level`

- **Type:** `string` (optional, default: `"info"`)
- **Description:** Logging verbosity level. Options: `"error"`, `"warn"`, `"info"`, `"debug"`, `"trace"`.
- **Example:**
  ```jsonc
  "log_level": "debug"
  ```

### `log_file`

- **Type:** `string` (optional)
- **Description:** Path to write session logs to. Supports `${ENV_VAR}` in path.
- **Example:**
  ```jsonc
  "log_file": ".opencode/logs/${SESSION_ID}.log"
  ```

## Full Documentation
For the complete official opencode configuration documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of every config field, provider configs, MCP config, network config, enterprise features, and example configurations.

**Cross-references:**
- **opencode_cli_commands** — the `config` command for viewing/editing config from the CLI
- **opencode_rules_permissions** — rule file format, permission policy syntax, and evaluation order
- **opencode_models_providers** — supported providers, model IDs, API key setup, and provider-specific notes
- **opencode_agents_subagents** — agent architecture, subagent handoff protocol, and agent-specific configuration
- **opencode_integrations** — MCP server development, community servers, and integration patterns
- **opencode_tui_customization** — theme creation, custom keybindings, and TUI layout configuration
