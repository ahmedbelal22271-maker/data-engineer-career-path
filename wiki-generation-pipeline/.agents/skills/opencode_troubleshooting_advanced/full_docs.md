# OpenCode Troubleshooting & Advanced Features — Complete Official Documentation

> **Source:** https://opencode.ai/troubleshooting — https://opencode.ai/network — https://opencode.ai/enterprise — https://opencode.ai/windows-wsl — https://opencode.ai/plugins — https://opencode.ai/sdk — https://opencode.ai/ecosystem — retrieved July 2026

---

## Troubleshooting

### API Errors

#### 401 Unauthorized

**Cause:** Invalid or missing API key.

**Fix:**
```json
{
  "provider": {
    "anthropic": {
      "apiKey": "env:ANTHROPIC_API_KEY"
    }
  }
}
```

```bash
export ANTHROPIC_API_KEY="your-actual-key"
```

#### 429 Rate Limited

**Cause:** Too many requests to the provider.

**Fix:**
- Wait and retry
- Switch to a different provider
- Implement exponential backoff in config:
```json
{
  "network": {
    "retries": {
      "max": 5,
      "backoff": "exponential"
    }
  }
}
```

#### 500/502/503 Server Error

**Cause:** Provider-side issue.

**Fix:**
- Retry after a short delay
- Check provider status page
- Switch to a backup provider

#### Model Not Found

**Cause:** Incorrect model name or provider not configured.

**Fix:**
- Verify model name format: `provider/model-name`
- Check provider is configured in `opencode.json`
- Ensure API key is valid for that provider

---

### Tool Failures

#### `edit` — oldString Not Found

**Cause:** The text to replace doesn't match exactly.

**Fix:**
- Read the file first to get exact content
- Copy the exact string including whitespace
- Use more context to make the match unique

#### `write` — Permission Denied

**Cause:** File system permissions or write protection.

**Fix:**
- Check file permissions
- Verify the directory exists
- Check for read-only filesystem

#### `bash` — Command Not Found

**Cause:** The command isn't installed or not in PATH.

**Fix:**
- Install the required tool
- Use absolute path
- Check PATH in the shell environment

#### `bash` — Timeout

**Cause:** Command took longer than the timeout (default: 120s).

**Fix:**
```json
{
  "tools": {
    "command": {
      "long-task": {
        "command": "npm run build",
        "timeout": 300000
      }
    }
  }
}
```

#### `glob` — No Results

**Cause:** Pattern doesn't match any files.

**Fix:**
- Check the glob pattern syntax
- Verify the search path exists
- Use `*` instead of `**` for single-level search

---

### Configuration Errors

#### Unknown Property

**Cause:** Config field not supported in your OpenCode version.

**Fix:** Remove the field or check the schema for your version:
```bash
opencode config --validate
```

#### Invalid JSON

**Cause:** Malformed JSON in config file.

**Fix:**
- Check for trailing commas
- Verify all brackets are closed
- Use a JSON validator

#### Circular Reference

**Cause:** Config file references itself.

**Fix:** Remove circular references in config.

---

### TUI Issues

#### TUI Not Rendering

**Cause:** Terminal doesn't support required features.

**Fix:**
- Use a modern terminal (iTerm2, Alacritty, Kitty, Windows Terminal)
- Ensure terminal size is at least 80×24
- Check true color support

#### Colors Look Wrong

**Cause:** Terminal doesn't support true color.

**Fix:**
- Enable true color in terminal settings
- Use a theme with 256-color fallback
- Switch to a terminal with true color support

#### Input Not Working

**Cause:** Terminal input mode conflict.

**Fix:**
- Press `Escape` then try again
- Check for conflicting keybindings
- Restart the terminal

---

### Session Issues

#### Session Not Found

**Cause:** Session was deleted or ID is incorrect.

**Fix:**
```bash
# List available sessions
opencode sessions

# Resume most recent
opencode --resume
```

#### Session Corrupted

**Cause:** Session file was modified or corrupted.

**Fix:**
- Delete the corrupted session
- Start a new session
- Check session storage directory permissions

#### Export Fails

**Cause:** Session too large or disk full.

**Fix:**
- Export to clipboard instead of file
- Clear old sessions
- Check disk space

---

## Network Configuration

### Proxy Configuration

```json
{
  "network": {
    "proxy": "http://proxy.example.com:8080"
  }
}
```

Or via environment variable:

```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

### TLS Configuration

```json
{
  "network": {
    "tls": {
      "insecure": false,
      "ca": "/path/to/ca-cert.pem",
      "cert": "/path/to/client-cert.pem",
      "key": "/path/to/client-key.pem"
    }
  }
}
```

### Custom CA Certificate

For corporate environments with custom CAs:

```json
{
  "network": {
    "tls": {
      "ca": "/etc/ssl/certs/company-root-ca.pem"
    }
  }
}
```

### Retry Configuration

```json
{
  "network": {
    "retries": {
      "max": 3,
      "backoff": "exponential",
      "initial_delay": 1000,
      "max_delay": 30000
    }
  }
}
```

### Timeout Configuration

```json
{
  "network": {
    "timeout": {
      "connect": 10000,
      "read": 60000,
      "total": 120000
    }
  }
}
```

---

## Enterprise Features

### Audit Logging

Log all AI interactions for compliance:

```json
{
  "enterprise": {
    "audit_log": {
      "enabled": true,
      "path": "/var/log/opencode/audit.jsonl",
      "events": [
        "session.create",
        "session.message",
        "tool.execute",
        "file.modify"
      ]
    }
  }
}
```

### SSO (Single Sign-On)

```json
{
  "enterprise": {
    "sso": {
      "provider": "okta",
      "domain": "company.okta.com",
      "client_id": "env:OKTA_CLIENT_ID"
    }
  }
}
```

### RBAC (Role-Based Access Control)

```json
{
  "enterprise": {
    "rbac": {
      "enabled": true,
      "roles": {
        "admin": {
          "permissions": ["*"]
        },
        "developer": {
          "permissions": ["read", "edit", "bash:tests", "bash:build"]
        },
        "viewer": {
          "permissions": ["read"]
        }
      }
    }
  }
}
```

### Data Classification

```json
{
  "enterprise": {
    "data_classification": {
      "enabled": true,
      "levels": ["public", "internal", "confidential", "restricted"],
      "default_level": "internal"
    }
  }
}
```

---

## Windows & WSL

### Windows Support

OpenCode works natively on Windows:

- **Terminal:** Windows Terminal, PowerShell, CMD
- **Shell:** PowerShell 7+ recommended
- **Path style:** Use `C:\path\to\file` format

### WSL2 Support

Full Linux compatibility via WSL2:

```bash
# Install in WSL
curl -fsSL https://opencode.ai/install | bash

# Run from WSL
opencode
```

### Windows-Specific Issues

#### Path Length Limits

Windows has a 260-character path limit. Enable long paths:

```powershell
# Run as Administrator
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
```

#### Line Endings

Ensure consistent line endings:

```json
{
  "tools": {
    "preserve": {
      "bash": true
    }
  }
}
```

Or in `.gitattributes`:

```
* text=auto eol=lf
```

#### Permission Model

Windows uses ACLs instead of Unix permissions. The permission system works the same way but underlying enforcement differs.

---

## Plugins

OpenCode supports plugins for extending functionality.

### Plugin Structure

```
.opencode/plugins/
├── my-plugin/
│   ├── plugin.json         # Plugin manifest
│   ├── index.js            # Plugin entry point
│   └── package.json        # Dependencies
```

### Plugin Manifest

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My custom plugin",
  "hooks": {
    "pre-session": "onSessionStart",
    "post-message": "onMessage"
  }
}
```

### Plugin API

Plugins can hook into:

- **Session lifecycle** — Create, start, end sessions
- **Message events** — Pre/post message processing
- **Tool calls** — Pre/post tool execution
- **Config** — Extend configuration

---

## SDK

The OpenCode SDK provides programmatic access to the core engine.

### Go SDK

```go
import "github.com/opencode-ai/opencode/pkg/client"

c := client.New(client.Config{
    Provider: "anthropic",
    Model:    "claude-sonnet-4-6",
})

session, _ := c.CreateSession(ctx)
response, _ := c.SendMessage(ctx, session.ID, "hello")
```

### REST API SDK

```javascript
const response = await fetch('http://localhost:8080/sessions', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${apiKey}` },
  body: JSON.stringify({ model: 'anthropic/claude-sonnet-4-6' })
});
```

---

## Ecosystem

### Community Skills

The OpenCode community shares skills via:

- **GitHub repos** — Fork and use others' skills
- **Skill registry** — Publish and discover skills
- **Discord** — Share and discuss skills

### Community Plugins

Extend OpenCode with community plugins:

- **Database connectors** — MongoDB, Redis, DynamoDB
- **Cloud providers** — AWS, GCP, Azure integrations
- **DevOps tools** — Terraform, Kubernetes, Ansible
- **Communication** — Slack, Discord, Teams integrations

---

## Debug Mode

Enable debug logging for troubleshooting:

```bash
# Via environment variable
OPENCODE_LOG_LEVEL=debug opencode

# Via config
{
  "logLevel": "debug"
}

# Via CLI flag
opencode --verbose
```

Debug output includes:
- Tool calls and results
- API requests and responses
- Config loading
- Session management
- Error stack traces

---

## Performance Optimization

### Token Usage

Monitor token consumption:

```bash
# Export session with token counts
opencode --json run "explain codebase" | jq '.usage'
```

### Context Window Management

- Clear sessions when switching tasks
- Use plan mode for exploration (less overhead)
- Choose appropriately-sized models for each slot
- Minimize unnecessary file reads

### Response Time

- Use faster models for the `big` slot
- Reduce context window size
- Use zen mode for background execution
- Minimize MCP server round-trips

---

## Common Workflows

### Fresh Start

```bash
# Clear all sessions
opencode sessions --clear

# Start fresh
opencode
```

### Resume Work

```bash
# List sessions
opencode sessions

# Resume specific session
opencode --session-id abc123
```

### Debug a Problem

```bash
# Enable debug logging
OPENCODE_LOG_LEVEL=debug opencode

# Run with verbose output
opencode --verbose run "debug this error"
```

### Export for Sharing

```bash
# Export as Markdown
opencode --json run "explain this" | jq -r '.session' > session.md
```
