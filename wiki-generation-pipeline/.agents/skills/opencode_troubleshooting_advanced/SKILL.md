---
name: opencode Troubleshooting & Advanced Features
description: Complete reference for diagnosing and resolving opencode issues — API errors (401/429/500), token limits, tool failures (edit oldString not found, write not read first, bash permission denied), config validation errors, network/proxy issues, Windows/WSL specifics, session hangs, debug mode, recovery procedures. Also covers advanced features: Verifier (test runner config), Network config (proxy, TLS, retry), Enterprise features (audit log, SSO, RBAC, usage reporting), plugins, and SDK. Trigger on "error", "troubleshoot", "debug", "opencode is broken", "API error", "token limit", "Windows", "WSL", "enterprise", "audit log", "SSO", "RBAC", "plugin", "SDK", or failure/diagnosis questions.
---

# opencode Troubleshooting & Advanced Features

## 1. Common API Errors

| Error | Likely Cause | Solution |
|---|---|---|
| 401 Unauthorized | Invalid/missing API key | Check `api_key` env var or config |
| 429 Too Many Requests | Rate limited | Add delay, reduce concurrency, check plan |
| 500 Internal Server Error | Provider outage | Retry with fallback model |
| 403 Forbidden | Key lacks permission | Check key permissions |
| RateLimitError | Token quota exceeded | Wait, use cheaper model, upgrade |

## 2. Token Limits

**Problem:** `max_tokens` exceeded or context too large.

**Solutions:**
- Reduce `max_tokens` in config
- Split work into smaller tasks
- Use `opencode run` for isolated runs
- Reduce instructions file size
- Use Haiku or Sonnet for exploration, Opus only for complex reasoning

## 3. Tool Failures

| Error | Solution |
|---|---|
| `edit` "oldString not found" | Read file first, match exact content including whitespace |
| `edit` "multiple matches" | Add more surrounding context or use `replaceAll: true` |
| `bash` "command not found" | Install the tool or use a different approach |
| `bash` "permission denied" | `chmod +x` or check file existence |
| `read` "file not found" | Check path, use `glob` to find the file |
| `write` "did not read file first" | Read the file before writing |

## 4. Config Validation Errors

- **"Invalid config"**: Run `opencode config validate` to diagnose.
- **"Missing default model"**: Add a `"default"` model entry to your config.
- **"Circular instructions"**: Remove circular `instructions` references between agents.
- **"Skill not found"**: Check the skill path exists and is installed. Run `opencode skill install` if needed.

## 5. Network Issues

- **API timeout**: Increase `timeout` in network config (default 30000ms).
- **Proxy errors**: Verify proxy URL format and authentication credentials.
- **SSL/TLS errors**: Set `insecure: true` for testing or provide a CA certificate.
- **DNS failures**: Check DNS resolution, try using the provider's IP directly.

## 6. Windows / WSL Specific Issues

- **Path separator**: Windows uses `\`, WSL uses `/`. opencode normalizes most paths automatically.
- **Line endings**: Windows CRLF vs WSL LF. The `edit` tool requires exact match — use LF in both environments.
- **PowerShell**: opencode uses PowerShell on Windows. Syntax differs — `Get-ChildItem` not `ls`, `Set-Content` not `>`.
- **WSL paths**: Windows paths (`C:\Users\...`) must translate to `/mnt/c/Users/...`. Use `wslpath` for conversion.
- **WSL integration**: opencode works inside WSL. File path translation between Windows and WSL paths is needed for cross-filesystem operations.

## 7. Session Hangs or Slow Performance

- **Large context**: Reduce instructions files, prune conversation history.
- **Model overload**: Switch to a faster model (Sonnet > Opus).
- **Tool explosion**: AI making too many tool calls — check prompt specificity and constraints.
- **Network latency**: Check API connection quality, try a different provider or region.
- **Rate limiting**: Add delays between requests, reduce concurrent agent count.

## 8. Debug Mode

```
opencode --verbose
opencode run task.md --verbose
```

**Log levels:** `debug`, `info`, `warn`, `error`

```jsonc
{
  "log_level": "debug",
  "log_file": ".opencode/logs/session.log"
}
```

## 9. Recovery Procedures

1. **Hung session**: Press `Ctrl+C`, re-prompt with clearer, more constrained instructions.
2. **Corrupted config**: Run `opencode config validate`, then `opencode config edit` to fix.
3. **Permission loop**: Use `--yes` flag or adjust `permission_mode` in config.
4. **Model errors**: Switch models with `Ctrl+/` during session or restart with `--model`.
5. **Lost work**: Use `/save` to persist state, or check `.opencode/logs/` for session history.

---

# Advanced Features

## 10. Verifier (Test Runner)

Automated verification checks after every tool execution:

```jsonc
{
  "verifier": {
    "enabled": true,
    "scripts": ["npm run lint", "npm run typecheck", "npm test"],
    "auto_fix": true,
    "on_failure": "prompt"    // "prompt" | "abort" | "retry"
  }
}
```

**Behavior:** When enabled, after each file change the specified scripts run. If all pass → continue. If any fail → behavior depends on `on_failure`:
- `"prompt"`: Ask user how to proceed
- `"abort"`: Stop the session
- `"retry"`: Auto-retry the failed operation

Per-agent verifier configuration is also supported — each agent can have its own scripts and `on_failure` policy.

## 11. Network Configuration

```jsonc
{
  "network": {
    "proxy": "http://proxy.company.com:8080",
    "no_proxy": ["localhost", "*.internal.com"],
    "custom_headers": { "X-API-Key": "${CUSTOM_HEADER_KEY}" },
    "timeout": 30000,
    "retry_count": 3,
    "retry_delay": 1000,
    "tls": {
      "ca_cert": "/path/to/ca.pem",
      "insecure": false
    }
  }
}
```

## 12. Enterprise Features

### Audit Log

```jsonc
{
  "enterprise": {
    "audit_log": {
      "enabled": true,
      "path": "/var/log/opencode/audit.jsonl",
      "events": ["tool_call", "file_change", "command", "session_start", "session_end"]
    }
  }
}
```

### SSO / SAML

```jsonc
{
  "enterprise": {
    "sso": {
      "provider": "okta",
      "saml_url": "https://company.okta.com/saml",
      "certificate": "/path/to/saml.cert"
    }
  }
}
```

### RBAC (Role-Based Access Control)

```jsonc
{
  "enterprise": {
    "rbac": {
      "roles": {
        "developer": {
          "tools": ["*"],
          "models": ["default"]
        },
        "reviewer": {
          "tools": ["read", "glob", "grep"],
          "models": ["default"]
        }
      }
    }
  }
}
```

### Usage Reporting

```jsonc
{
  "enterprise": {
    "reporting": {
      "enabled": true,
      "endpoint": "https://analytics.company.com/api/usage",
      "interval_hours": 24
    }
  }
}
```

## 13. opencode Plugins

Extend opencode with:
- **Custom formatters** for specialized output
- **Additional tools** beyond the built-in set
- **Provider adapters** for custom AI backends
- **UI extensions** for the terminal interface

Develop plugins using the opencode SDK.

## 14. opencode SDK

Programmatic API for integrating opencode into your own tools and workflows:

```typescript
import { opencode } from 'opencode-sdk';

const result = await opencode.run({
  prompt: "explain this code",
  model: "claude-sonnet-4-20250514",
  tools: ["read", "glob", "grep"]
});
```

**Use cases:**
- Custom tool development
- MCP server creation
- Plugin authoring
- CI/CD pipeline integration

## 15. Ecosystem

opencode integrates with:

| Category | Examples |
|---|---|
| **Version Control** | Git, GitHub, GitLab |
| **Package Managers** | npm, pip, cargo, go |
| **Databases** | Via MCP servers |
| **CI/CD** | GitHub Actions, GitLab CI, Jenkins |
| **Editors** | VS Code, JetBrains, Vim/Neovim |
| **AI Providers** | Anthropic, OpenAI, Google, AWS, Azure, GCP, Ollama, OpenRouter |

## Full Documentation
For the complete official opencode troubleshooting and advanced features documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of API errors, tool failures, config issues, network config, enterprise features, Windows/WSL, plugins, SDK, and ecosystem.

### Cross-References

- `opencode_configuration` — Network, verifier, and model config details
- `opencode_rules_permissions` — Enterprise RBAC rules and permission modes
- `opencode_integrations` — Ecosystem connections and third-party integrations
- `opencode_cli_commands` — `config validate`, `--verbose`, and other CLI flags
- `opencode_tools_catalog` — Full tool reference including error messages
