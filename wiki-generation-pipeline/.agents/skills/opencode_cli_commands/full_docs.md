# OpenCode CLI Commands & Flags — Complete Official Documentation

> **Source:** https://opencode.ai — retrieved July 2026

---

## Main Entry Point

The `opencode` command is the primary entry point. Running `opencode` with no arguments starts the interactive TUI in the current directory.

```bash
opencode [flags]
```

---

## Global Flags

These flags apply to all commands:

| Flag | Short | Description |
|------|-------|-------------|
| `--dir` | `-d` | Change to this directory before starting |
| `--quiet` | `-q` | Suppress TUI output (useful for scripting) |
| `--verbose` | `-v` | Enable verbose logging |
| `--help` | `-h` | Show help for any command |
| `--version` | | Print the version string |
| `--config` | `-c` | Path to config file (default: auto-discovered) |
| `--json` | `-j` | Output in JSON format (where applicable) |
| `--pretty` | | Pretty-print JSON output (default: true) |
| `--no-pretty` | | Disable pretty-printing |

---

## Commands

### `opencode` (default)

Start the interactive TUI. This is the default command when no subcommand is specified.

```bash
# Start in current directory
opencode

# Start in a specific directory
opencode --dir /path/to/project
```

### `opencode run`

Run a task non-interactively. Opens a session, sends the prompt, executes tools, and streams the response to stdout.

```bash
# Run a task
opencode run "explain this codebase"

# Pipe input
cat README.md | opencode run "summarize this"

# Resume a session
opencode run --resume
```

**Flags:**

| Flag | Short | Description |
|------|-------|-------------|
| `--session-id` | `-s` | Resume an existing session by ID |
| `--resume` | | Resume the most recent session |
| `--model` | `-m` | Override the primary model |
| `--provider` | `-p` | Override the provider |
| `--mode` | | Override the mode (plan/auto) |
| `--permission` | | Override permission mode |
| `--subagent` | `-a` | Run as a specific agent type |

**Subagent delegation:**

```bash
# Run as a code-focused agent
opencode run --subagent code "optimize this function"

# Run as a debug agent
opencode run --subagent debug "find the memory leak"
```

### `opencode plan`

Create and manage plans. In Plan Mode, you explore the codebase, design an approach, and then execute it.

```bash
# Start planning
opencode plan "refactor the authentication module"

# Plan from a file
cat task.txt | opencode plan
```

### `opencode execute`

Execute a previously created plan. Switches to Auto mode and implements the approved approach.

```bash
# Execute the current plan
opencode execute

# Execute with a specific model
opencode execute --model anthropic/claude-opus-4-6
```

### `opencode config`

Manage configuration. Shows current config, validates it, and helps set values.

```bash
# Show current config
opencode config

# Validate config
opencode config --validate

# Show a specific value
opencode config --get model.primary

# Set a value
opencode config --set model.primary "anthropic/claude-sonnet-4-6"
```

### `opencode init`

Initialize OpenCode in the current directory. Creates the `opencode.json` config file and the `.opencode/` directory.

```bash
# Initialize with defaults
opencode init

# Initialize with a template
opencode init --template basic
```

### `opencode install`

Install OpenCode or update to the latest version.

```bash
# Install/update
opencode install

# Check for updates
opencode install --check
```

### `opencode publish`

Publish a skill or plugin to the OpenCode registry.

```bash
# Publish a skill
opencode publish --skill my-skill

# Publish a plugin
opencode publish --plugin my-plugin
```

### `opencode check`

Run health checks on the system. Verifies that all dependencies are installed and configured correctly.

```bash
# Run all checks
opencode check

# Check specific component
opencode check --provider anthropic
```

### `opencode completion`

Generate shell completion scripts.

```bash
# Bash
opencode completion bash >> ~/.bashrc

# Zsh
opencode completion zsh >> ~/.zshrc

# Fish
opencode completion fish > ~/.config/fish/completions/opencode.fish

# PowerShell
opencode completion powershell >> $PROFILE
```

### `opencode mcp`

Manage MCP servers. Add, remove, list, and test MCP server connections.

```bash
# List configured MCP servers
opencode mcp list

# Test a connection
opencode mcp test filesystem

# Add a server interactively
opencode mcp add

# Remove a server
opencode mcp remove my-server
```

### `opencode ssh`

Start an SSH session to a remote OpenCode instance.

```bash
# Connect to remote
opencode ssh user@host

# Connect with specific port
opencode ssh -p 2222 user@host
```

### `opencode update`

Update OpenCode to the latest version.

```bash
# Update
opencode update

# Check current version
opencode --version
```

---

## Output Formatters

OpenCode supports multiple output formats for scripting and automation:

### Default Format

Human-readable output with colors and formatting. Used by default in interactive mode.

### JSON Format (`--json`)

Machine-readable JSON output. Useful for piping to other tools or processing in scripts.

```bash
opencode --json run "list all TODO comments"
```

### Quiet Format (`--quiet`)

Minimal output, suppressing the TUI. Useful for background execution and CI/CD pipelines.

```bash
opencode --quiet run "run tests"
```

### Pretty JSON (`--pretty`)

Formatted JSON with indentation (default when `--json` is used). Disable with `--no-pretty`.

---

## Piping & stdin

OpenCode supports piping input from other commands:

```bash
# Pipe file content
cat src/main.go | opencode run "review this code"

# Pipe command output
git diff | opencode run "explain these changes"

# Pipe multiple files
find src -name "*.go" | xargs cat | opencode run "find code smells"
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 3 | Network/Provider error |
| 4 | Permission denied |
| 5 | Session error |

---

## Environment Variables

All OpenCode CLI behavior can be configured via environment variables:

| Variable | Description |
|----------|-------------|
| `OPENCODE_API_KEY` | API key for the default provider |
| `OPENCODE_MODEL` | Override the primary model |
| `OPENCODE_PROVIDER` | Override the provider |
| `OPENCODE_MODE` | Override the mode (plan/auto) |
| `OPENCODE_LOG_LEVEL` | Set log level (debug/info/warn/error) |
| `OPENCODE_CONFIG_DIR` | Custom config directory path |
| `OPENCODE_SESSION_DIR` | Custom session storage path |
| `OPENCODE_ZEN` | Enable zen mode (1/true/yes) |
| `OPENCODE_QUIET` | Enable quiet mode (1/true/yes) |

**Provider precedence:** CLI flags > environment variables > config file > defaults.
