# OpenCode Models & Providers — Complete Official Documentation

> **Source:** https://opencode.ai/providers — https://opencode.ai/models — https://opencode.ai/zen — https://opencode.ai/go — retrieved July 2026

---

## Overview

OpenCode is model-agnostic and provider-agnostic. It works with any LLM provider that offers an OpenAI-compatible API. The model/provider configuration lives in `opencode.json`.

---

## Two Model Slots

OpenCode uses two different model slots:

### Primary Model

The main reasoning engine. Handles planning, editing, conversation, and orchestration.

- **Best with:** Strong reasoning models (GPT-4o, Claude Sonnet/Opus, Gemini 2.5 Pro)
- **Config key:** `model.primary`

### Big Model

Specialized for large codebase exploration. Excels at searching large codebases quickly.

- **Best with:** Models optimized for speed and large context windows
- **Config key:** `model.big`

```json
{
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "big": "anthropic/claude-sonnet-4-6"
  }
}
```

---

## Model Naming Convention

Models follow the format: `provider/model-name`

Examples:
- `anthropic/claude-sonnet-4-6`
- `openai/gpt-4o`
- `google/gemini-2.5-pro`
- `ollama/llama3`

---

## Supported Providers

### Anthropic

Provider: `anthropic`

Models: Claude Opus 4, Claude Sonnet 4, Claude Haiku

```json
{
  "provider": {
    "anthropic": {
      "name": "anthropic",
      "apiKey": "env:ANTHROPIC_API_KEY"
    }
  },
  "model": {
    "primary": "anthropic/claude-sonnet-4-6"
  }
}
```

### OpenAI

Provider: `openai`

Models: GPT-4o, GPT-4o-mini, o1, o1-mini, o3, o3-mini

```json
{
  "provider": {
    "openai": {
      "name": "openai",
      "apiKey": "env:OPENAI_API_KEY"
    }
  },
  "model": {
    "primary": "openai/gpt-4o"
  }
}
```

### Google (Gemini)

Provider: `google`

Models: Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.0 Flash

```json
{
  "provider": {
    "google": {
      "name": "google",
      "apiKey": "env:GOOGLE_API_KEY"
    }
  },
  "model": {
    "primary": "google/gemini-2.5-pro"
  }
}
```

### AWS Bedrock

Provider: `bedrock`

Models: Claude, Llama, Mistral via AWS Bedrock

```json
{
  "provider": {
    "bedrock": {
      "name": "bedrock",
      "region": "us-east-1",
      "accessKeyId": "env:AWS_ACCESS_KEY_ID",
      "secretAccessKey": "env:AWS_SECRET_ACCESS_KEY"
    }
  },
  "model": {
    "primary": "bedrock/anthropic.claude-sonnet-4-6"
  }
}
```

### Azure OpenAI

Provider: `azure`

Models: GPT-4o via Azure OpenAI Service

```json
{
  "provider": {
    "azure": {
      "name": "azure",
      "apiKey": "env:AZURE_OPENAI_API_KEY",
      "apiUrl": "https://your-resource.openai.azure.com/"
    }
  },
  "model": {
    "primary": "azure/gpt-4o"
  }
}
```

### GCP Vertex AI

Provider: `vertex`

Models: Gemini via Google Cloud Vertex AI

```json
{
  "provider": {
    "vertex": {
      "name": "vertex",
      "project": "your-gcp-project",
      "region": "us-central1"
    }
  },
  "model": {
    "primary": "vertex/gemini-2.5-pro"
  }
}
```

### Ollama (Local)

Provider: `ollama`

Models: Any model running locally via Ollama

```json
{
  "provider": {
    "ollama": {
      "name": "ollama",
      "apiUrl": "http://localhost:11434"
    }
  },
  "model": {
    "primary": "ollama/llama3"
  }
}
```

### OpenRouter

Provider: `openrouter`

Models: Multi-provider routing (access to multiple providers through one API)

```json
{
  "provider": {
    "openrouter": {
      "name": "openrouter",
      "apiKey": "env:OPENROUTER_API_KEY"
    }
  },
  "model": {
    "primary": "openrouter/anthropic/claude-sonnet-4-6"
  }
}
```

### Custom (OpenAI-Compatible)

Provider: `custom`

Any provider offering an OpenAI-compatible API endpoint.

```json
{
  "provider": {
    "custom": {
      "name": "custom",
      "apiUrl": "https://your-provider.example.com/v1",
      "apiKey": "env:CUSTOM_API_KEY"
    }
  },
  "model": {
    "primary": "custom/model-name"
  }
}
```

---

## Provider Configuration Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | Yes | Display name |
| `apiKey` | `string` | Yes | API key (use `env:VAR` for env vars) |
| `apiUrl` | `string` | No | Custom API base URL |
| `region` | `string` | No | Cloud region (AWS/GCP) |
| `project` | `string` | No | GCP project ID |
| `accessKeyId` | `string` | No | AWS access key |
| `secretAccessKey` | `string` | No | AWS secret key |
| `models` | `array` | No | Override available models |

---

## Environment Variable Configuration

All provider credentials can be set via environment variables:

| Variable | Provider |
|----------|----------|
| `ANTHROPIC_API_KEY` | Anthropic |
| `OPENAI_API_KEY` | OpenAI |
| `GOOGLE_API_KEY` | Google |
| `AWS_ACCESS_KEY_ID` | AWS Bedrock |
| `AWS_SECRET_ACCESS_KEY` | AWS Bedrock |
| `AZURE_OPENAI_API_KEY` | Azure |
| `OPENROUTER_API_KEY` | OpenRouter |
| `CUSTOM_API_KEY` | Custom provider |

---

## Model Selection Strategy

### Choosing the Primary Model

- **Claude Sonnet/Opus** — Best for complex reasoning, code generation, and multi-step tasks
- **GPT-4o** — Strong all-around, good at following instructions
- **Gemini 2.5 Pro** — Large context window, good for big codebases
- **Local models (Ollama)** — Offline, private, but limited capability

### Choosing the Big Model

- **Claude Sonnet** — Good balance of speed and quality
- **GPT-4o-mini** — Fast and cheap for search tasks
- **Gemini 2.5 Flash** — Optimized for speed

### Cost Optimization

- Use a cheaper model for the `big` slot (search/exploration)
- Use the strongest model for the `primary` slot (reasoning/editing)
- Use Ollama for development and prototyping
- Monitor token usage via session exports

---

## Thinking & Effort Parameters

Some models support reasoning effort configuration:

```json
{
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "thinking": true,
    "effort": "medium"
  }
}
```

**Effort levels:**
- `low` — Fast responses, less thorough reasoning
- `medium` — Balanced (default)
- `high` — Thorough reasoning, more tokens used

---

## Zen Mode

Zen mode is OpenCode's minimal mode. It hides the TUI and runs purely in the background, streaming output directly to your terminal.

### Configuration

```json
{
  "zen": {
    "enabled": true
  }
}
```

Or via CLI flag:

```bash
opencode --zen run "run all tests and fix failures"
```

### Zen Mode Behavior

- No TUI rendering — plain text output to stdout
- Ideal for CI/CD pipelines
- Ideal for scripted automation
- Ideal for background execution
- All tools and permissions still apply

### When to Use Zen

- CI/CD pipelines (GitHub Actions, GitLab CI)
- Automated code review scripts
- Background task execution
- Shell script integration

---

## OpenCode Go SDK

OpenCode is written in Go. The Go SDK provides programmatic access to the core engine.

### Key Capabilities

- **LLM provider abstraction** — Connect to any provider
- **Tool execution framework** — Register and execute custom tools
- **Session management** — Create, resume, export sessions
- **Event system** — Stream events in real time

### SDK Usage

```go
package main

import (
    "context"
    "github.com/opencode-ai/opencode/pkg/client"
)

func main() {
    ctx := context.Background()
    
    // Create a client
    c := client.New(client.Config{
        Provider: "anthropic",
        Model:    "claude-sonnet-4-6",
    })
    
    // Start a session
    session, _ := c.CreateSession(ctx)
    
    // Send a message
    response, _ := c.SendMessage(ctx, session.ID, "explain this codebase")
    
    // Handle response
    fmt.Println(response.Content)
}
```

### SDK Configuration

The SDK reads the same `opencode.json` config file. You can override settings programmatically:

```go
c := client.New(client.Config{
    Provider:  "anthropic",
    Model:     "claude-sonnet-4-6",
    ConfigPath: "./opencode.json",
})
```

---

## Provider Precedence

Configuration values are resolved in this order (highest priority first):

1. CLI flags (`--model`, `--provider`)
2. Environment variables (`OPENCODE_MODEL`, `OPENCODE_PROVIDER`)
3. Config file (`opencode.json`)
4. Defaults

---

## Model Configuration Examples

### Single Provider (Anthropic)

```json
{
  "provider": {
    "anthropic": {
      "apiKey": "env:ANTHROPIC_API_KEY"
    }
  },
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "big": "anthropic/claude-sonnet-4-6"
  }
}
```

### Multi-Provider

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
    "big": "openai/gpt-4o-mini"
  }
}
```

### Local Development (Ollama)

```json
{
  "provider": {
    "ollama": {
      "apiUrl": "http://localhost:11434"
    }
  },
  "model": {
    "primary": "ollama/codellama",
    "big": "ollama/codellama"
  }
}
```

### Enterprise (Bedrock)

```json
{
  "provider": {
    "bedrock": {
      "region": "us-east-1",
      "accessKeyId": "env:AWS_ACCESS_KEY_ID",
      "secretAccessKey": "env:AWS_SECRET_ACCESS_KEY"
    }
  },
  "model": {
    "primary": "bedrock/anthropic.claude-sonnet-4-6"
  }
}
```
