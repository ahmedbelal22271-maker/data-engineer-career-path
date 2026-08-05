---
name: opencode Models & Providers
description: Complete reference for all supported AI providers in opencode — Anthropic, OpenAI, Google/Gemini, AWS Bedrock, Azure OpenAI, GCP Vertex AI, Ollama (local), OpenRouter, and custom OpenAI-compatible endpoints. Covers model config fields, thinking/effort parameters, provider-specific authentication patterns, model selection strategy, and fallback configuration. Trigger on "model", "provider", "API key", "which model", "change model", "Opus", "Sonnet", "Haiku", "GPT", "Gemini", "Ollama", or model configuration questions.
---

# opencode Models & Providers

## 1. Model Configuration in opencode.json

Full example with all fields:

```jsonc
{
  "models": {
    "default": {
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "max_tokens": 8192,
      "temperature": 0.7,
      "api_key": "${ANTHROPIC_API_KEY}"
    }
  }
}
```

## 2. Model Config Fields

| Field | Description |
|-------|-------------|
| `provider` | One of: `anthropic`, `openai`, `google`, `aws_bedrock`, `azure`, `gcp_vertex`, `ollama`, `openrouter`, `custom` |
| `model` | Model name string (provider-specific) |
| `max_tokens` | Maximum output tokens |
| `temperature` | `0.0`–`1.0` |
| `api_key` | Supports `${ENV_VAR}` syntax |
| `base_url` | Custom endpoint URL |
| `thinking` | `{ "type": "adaptive" }` (default for newer Claude models), `{ "type": "enabled", "budget_tokens": 4096 }` (extended thinking, deprecated for new models), `{ "type": "disabled" }` |
| `effort` | `"low"` \| `"medium"` \| `"high"` \| `"max"` — token efficiency control. `"medium"` is default. |
| `description` | Human-readable label for model picker |

## 3. Provider Reference

### Anthropic

```jsonc
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "api_key": "${ANTHROPIC_API_KEY}"
}
```

Models: `claude-sonnet-4-20250514`, `claude-opus-4-20250514`, `claude-haiku-4-20250514`, `claude-sonnet-4.6`, `claude-fable-5`.

Key field: `api_key`.

### OpenAI

```jsonc
{
  "provider": "openai",
  "model": "gpt-4o",
  "api_key": "${OPENAI_API_KEY}",
  "base_url": "https://api.openai.com/v1"
}
```

Models: `gpt-4o`, `gpt-4o-mini`, `o1`, `o3`.

Fields: `api_key`, `base_url`.

### Google (Gemini)

```jsonc
{
  "provider": "google",
  "model": "gemini-2.5-pro",
  "api_key": "${GEMINI_API_KEY}"
}
```

Models: `gemini-2.0-flash`, `gemini-2.5-pro`, `gemini-1.5-pro`.

Fields: `api_key`.

### AWS Bedrock

```jsonc
{
  "provider": "aws_bedrock",
  "model": "anthropic.claude-sonnet-4-20250514",
  "aws_access_key": "${AWS_ACCESS_KEY_ID}",
  "aws_secret_key": "${AWS_SECRET_ACCESS_KEY}",
  "aws_region": "us-east-1"
}
```

Models: `anthropic.claude-sonnet-4-20250514`, `anthropic.claude-opus-4-20250514`, `anthropic.claude-haiku-4-20250514`, `anthropic.claude-fable-5`.

Fields: `aws_access_key`, `aws_secret_key`, `aws_region`.

### Azure OpenAI

```jsonc
{
  "provider": "azure",
  "model": "gpt-4o",
  "api_key": "${AZURE_OPENAI_API_KEY}",
  "base_url": "https://your-resource.openai.azure.com",
  "deployment": "your-deployment-name"
}
```

Models: `gpt-4o`, `gpt-4o-mini`, `o1`, `o3` (via deployment).

Fields: `api_key`, `base_url`, `deployment`.

### GCP Vertex AI

```jsonc
{
  "provider": "gcp_vertex",
  "model": "claude-sonnet-4-20250514",
  "gcp_project": "your-project-id",
  "gcp_region": "us-central1",
  "gcp_credentials": "${GCP_CREDENTIALS_PATH}"
}
```

Models: `claude-sonnet-4-20250514`, `claude-opus-4-20250514`, `claude-haiku-4-20250514`, `claude-fable-5`, `gemini-2.0-flash`, `gemini-2.5-pro`.

Fields: `gcp_project`, `gcp_region`, `gcp_credentials`.

### Ollama (Local)

```jsonc
{
  "provider": "ollama",
  "model": "llama3",
  "base_url": "http://localhost:11434"
}
```

Models: `llama3`, `qwen`, `mistral`, `codellama`, `deepseek-coder`, or any model pulled locally.

Fields: `base_url` (default `http://localhost:11434`).

### OpenRouter

```jsonc
{
  "provider": "openrouter",
  "model": "anthropic/claude-sonnet-4",
  "api_key": "${OPENROUTER_API_KEY}"
}
```

Models: `anthropic/claude-sonnet-4`, `anthropic/claude-opus-4`, `openai/gpt-4o`, `google/gemini-2.5-pro`, `meta-llama/llama-3`, `mistralai/mistral-large`.

Fields: `api_key`.

### Custom (OpenAI-compatible)

```jsonc
{
  "provider": "custom",
  "model": "my-model",
  "base_url": "https://my-custom-endpoint.com/v1",
  "api_key": "${CUSTOM_API_KEY}"
}
```

Works with any OpenAI-compatible API.

Fields: `base_url`, `api_key`.

## 4. Model Selection Strategy

| Criterion | Recommended Model | Rationale |
|-----------|-------------------|-----------|
| Complex reasoning, architecture | Claude Opus / Fable 5 | Best at deep analysis |
| Day-to-day coding | Claude Sonnet 4.6 | Best balance of speed/quality/cost |
| Quick tasks, exploration | Claude Haiku | Fastest, cheapest |
| Large context windows | Gemini 2.5 Pro | 1M+ token context |
| Offline/private | Ollama (Llama 3, Qwen) | Runs locally |
| Cost-sensitive | GPT-4o-mini, Claude Haiku | Lowest cost |
| Maximum output length | Claude Opus (16K tokens) | Largest output |

## 5. Fallback Models

Configure in case primary is unavailable:

```jsonc
{
  "model_fallback": true,
  "models": {
    "primary": { "provider": "anthropic", "model": "claude-sonnet-4-20250514" },
    "fallback": { "provider": "openai", "model": "gpt-4o" }
  }
}
```

## 6. Model Picker in TUI

- `Ctrl+/` to open
- Shows: model name, provider, token usage, context limit, estimated cost, latency
- Type to filter, Enter to switch

## Full Documentation
For the complete official opencode models and providers documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of all 9 providers, model config fields, thinking/effort parameters, Zen mode, Go SDK, and provider precedence.

**Cross-references:**
- `opencode_configuration` — models in config
- `opencode_agents_subagents` — per-agent model selection
- `opencode_decision_trees` — model selection decisions
