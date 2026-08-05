---
name: opencode CLI Commands & Flags
description: Complete reference for every opencode CLI command and flag. Covers main entry point, global flags, and all 12 commands: init, config, run, plan, execute, install, publish, check, completion, mcp, ssh, update. Also includes output formatters. Trigger on "how to run opencode", "opencode command", "CLI flag", or any question about a specific command like "opencode run" or "opencode config".
---

# opencode CLI — Complete Command Reference

## Overview

The opencode CLI is the primary interface for interacting with opencode. It provides a rich TUI (terminal user interface) for interactive sessions, a non-interactive command mode for automation, and a comprehensive set of subcommands for configuration, installation, publishing, and administration.

---

## 1. Main Entry Point

```
opencode [flags]
```

Starts an interactive TUI session. If input is piped from stdin, it is read as a prompt and executed non-interactively.

### Default behavior

- When run without arguments and stdin is a TTY, launches the interactive TUI.
- When stdin is piped, reads the entire input and treats it as a prompt.
- Global flags can modify session behavior (model, permission, output format, etc.).

### Basic usage

```bash
# Start interactive TUI session
opencode

# Run with a specific model
opencode --model claude-sonnet-4-20250514

# Pipe a prompt from stdin
echo "Explain the architecture" | opencode

# Pipe a task file
cat task.md | opencode --model claude-sonnet-4-20250514
```

---

## 2. Global Flags

Global flags are available on the main `opencode` entry point and most subcommands.

| Flag | Description |
|------|-------------|
| `--config <path>`, `-c <path>` | Path to the opencode configuration file. Defaults to `.opencode.jsonc` or `.opencode.json` in the project root. |
| `--model <name>` | Specify the model to use for the session. Overrides any model set in config. |
| `--subagent <name>` | Specify a subagent to use for the session. Subagents are pre-configured agent definitions. |
| `--output-format <format>` | Output format for results. One of: `terminal`, `json`, `jsonl`, `json-stream`, `markdown`, `html`, `file`, `edit`. Defaults to `terminal`. |
| `--verbose`, `-v` | Enable verbose logging. Repeat for increased verbosity (`-vv`, `-vvv`). |
| `--quiet`, `-q` | Suppress all output except results. Errors still print to stderr. |
| `--yes`, `-y` | Auto-approve all permission requests. Use with caution in automation. |
| `--no` | Decline all permission requests automatically. |
| `--permission <policy>` | Set permission mode. Values: `default` (ask per operation), `accept-all` (same as `--yes`), `reject-all` (same as `--no`). |
| `--allow-read <patterns>` | Comma-separated glob patterns for read permission auto-approval. Overrides permission checks for matching file reads. |
| `--allow-write <patterns>` | Comma-separated glob patterns for write permission auto-approval. Overrides permission checks for matching file writes. |
| `--allow-exec <patterns>` | Comma-separated glob patterns for command execution permission auto-approval. Overrides permission checks for matching commands. |
| `--help`, `-h` | Show help text for the command or subcommand. |
| `--version` | Print the opencode version and exit. |
| `--timeout <seconds>` | Maximum session duration in seconds before forced termination. Default is unlimited. |
| `--max-iterations <n>` | Maximum number of tool-use iterations before the session terminates. Prevents runaway loops. |

### Flag precedence

1. Command-line flags (highest priority)
2. Configuration file values (`.opencode.jsonc`)
3. Environment variables (`OPENCODE_MODEL`, `OPENCODE_CONFIG`, etc.)
4. Default values (lowest priority)

---

## 3. Command Reference

### opencode init

```
opencode init [directory]
```

Creates a new opencode project by generating the `.opencode/` directory structure and a starter configuration file.

**Flags:**

| Flag | Description |
|------|-------------|
| `--force`, `-f` | Overwrite existing files without prompting. |
| `--template <name>` | Use a specific project template. Built-in templates: `default`, `minimal`, `full`. |
| `--yes`, `-y` | Auto-approve all prompts. |

**Generated structure:**

```
.opencode/
├── opencode.jsonc          # Main configuration
├── rules/                  # Custom rules
├── skills/                 # Custom skills
└── agents/                 # Agent definitions
```

**Examples:**

```bash
# Initialize in current directory
opencode init

# Initialize in a specific directory
opencode init ./my-project

# Force re-initialization with minimal template
opencode init --force --template minimal --yes
```

---

### opencode config

```
opencode config <action> [key] [value]
```

Manages opencode configuration settings. Supports reading, writing, listing, editing, and validating configuration values.

**Actions:**

| Action | Description |
|--------|-------------|
| `get <key>` | Retrieve a specific configuration value. Dot notation supported (e.g., `model.vision`). |
| `set <key> <value>` | Set a configuration value. Creates parent keys if they do not exist. |
| `list` | List all configuration values in a tree view. |
| `edit` | Open the configuration file in the default editor. |
| `validate` | Validate the configuration file for correctness. Reports errors and warnings. |

**Flags:**

| Flag | Description |
|------|-------------|
| `--global` | Operate on the global (user-level) configuration instead of the local project config. |

**Examples:**

```bash
# Get the current model setting
opencode config get model

# Set the model
opencode config set model claude-sonnet-4-20250514

# Set a nested property
opencode config set model.vision true

# List all configuration
opencode config list

# Edit configuration in default editor
opencode config edit

# Validate configuration
opencode config validate

# Set a global default model
opencode config set model claude-sonnet-4-20250514 --global

# View global configuration
opencode config list --global
```

**Configuration file locations:**

- **Project**: `./.opencode.jsonc` or `./.opencode.json`
- **Global**: `~/.config/opencode/opencode.jsonc` (Linux/macOS), `%APPDATA%\opencode\opencode.jsonc` (Windows)

---

### opencode run

```
opencode run <file> [args...]
```

Runs a task script file non-interactively. This is the primary command for automation, CI/CD pipelines, and scheduled tasks. The file contains markdown with instructions and optionally frontmatter for configuration.

**Flags:**

| Flag | Description |
|------|-------------|
| `--model <name>` | Override the model for this run. |
| `--subagent <name>` | Use a specific subagent for this run. |
| `--output-format <format>` | Output format for results. |
| `--yes`, `-y` | Auto-approve all permission requests. |
| `--allow-read <patterns>` | Glob patterns for auto-approved file reads. |
| `--allow-write <patterns>` | Glob patterns for auto-approved file writes. |
| `--allow-exec <patterns>` | Glob patterns for auto-approved command execution. |
| `--timeout <seconds>` | Maximum execution time. |
| `--save` | Save the run output to a file in `.opencode/runs/`. Filename is auto-generated from the task name and timestamp. |
| `--save <path>` | Save the run output to a specific path. |

**Task script format:**

```markdown
---
model: claude-sonnet-4-20250514
subagent: coder
---

# Task: Deploy to Production

Run the deployment script and verify the service health endpoint.

1. Execute `deploy.sh --env prod`
2. Run health check against `https://api.example.com/health`
3. Report the status
```

**Examples:**

```bash
# Run a task script
opencode run scripts/deploy.md

# Run with auto-approval and save output
opencode run scripts/deploy.md --yes --save

# Run with specific model and output format
opencode run scripts/audit.md --model claude-sonnet-4-20250514 --output-format json

# Pass arguments to the task script
opencode run scripts/release.md v2.1.0 --yes

# Run in CI with restricted permissions
opencode run tests/validate.md \
  --allow-read "src/**" \
  --allow-write "test-results/**" \
  --allow-exec "npm test"
```

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | Success — task completed without errors |
| 1 | Error — task failed or encountered an unhandled error |
| 2 | Permission denied — task required permissions that were not granted |
| 130 | Interrupted — task was terminated by SIGINT (Ctrl+C) |
| 137 | Killed — task was terminated by SIGKILL (timeout or OOM) |

---

### opencode plan

```
opencode plan [description]
```

Starts a Plan Mode session. Plan Mode is a structured workflow where opencode first formulates a detailed plan before executing any actions. The plan is presented to the user for approval before execution begins.

**Flags:**

| Flag | Description |
|------|-------------|
| `--execute`, `-e` | Automatically execute the plan after it is approved (skip the manual approval step). |
| `--save` | Save the generated plan to a file (`.opencode/plans/` by default). |
| `--save <path>` | Save the plan to a specific path. |
| `--model <name>` | Override the model for planning. |

**Examples:**

```bash
# Start plan mode with a description
opencode plan "Refactor the authentication module to use JWT"

# Plan and auto-execute
opencode plan "Set up CI/CD pipeline" --execute

# Plan and save for later review
opencode plan "Migrate database schema" --save migration-plan.md

# View the plan file
cat .opencode/plans/migration-plan.md
```

**Plan output format:**

The plan is structured as a markdown document with:
- **Objective**: The high-level goal
- **Steps**: Ordered list of actions with details
- **Files affected**: List of files that will be created, modified, or deleted
- **Risks**: Potential issues and rollback strategies

---

### opencode execute

```
opencode execute <plan-file>
```

Executes a previously saved plan file. This allows plans to be reviewed, shared, and executed at a later time or in a different environment.

**Flags:**

| Flag | Description |
|------|-------------|
| `--model <name>` | Override the model for execution. |
| `--step` | Execute the plan one step at a time, pausing between steps for confirmation. |
| `--yes`, `-y` | Auto-approve all steps in the plan. |

**Examples:**

```bash
# Execute a saved plan
opencode execute .opencode/plans/migration-plan.md

# Execute step by step with manual confirmation
opencode execute .opencode/plans/deploy-plan.md --step

# Execute with auto-approval
opencode execute .opencode/plans/refactor-plan.md --yes
```

**Plan validation:**

`opencode execute` validates the plan file format before execution. If the plan is malformed or references files that no longer exist, it reports errors and aborts.

---

### opencode install

```
opencode install <source>
```

Installs agents, skills, rules, or plugins from various sources. Supports installing from the opencode registry, GitHub repositories, local file paths, and direct URLs.

**Sources:**

| Source Format | Example |
|---------------|---------|
| Registry name | `opencode install opencode/coder` |
| GitHub repo | `opencode install github:username/repo` |
| Local path | `opencode install ./path/to/package` |
| URL | `opencode install https://example.com/package.tar.gz` |

**Flags:**

| Flag | Description |
|------|-------------|
| `--from <source>` | Explicitly specify the source type: `registry`, `github`, `path`, `url`. Usually auto-detected. |
| `--version <version>` | Install a specific version (semver). Defaults to latest. |
| `--global` | Install globally (available across all projects). |
| `--file <path>` | Install from a local archive file (`.tar.gz`, `.zip`). |

**Examples:**

```bash
# Install an agent from the registry
opencode install opencode/coder

# Install a specific version
opencode install opencode/coder --version 1.2.0

# Install from GitHub
opencode install github:my-org/my-agent

# Install from a local path
opencode install ./dist/my-skill

# Install globally
opencode install opencode/auditor --global

# Install from a URL
opencode install https://registry.opencode.ai/packages/analyst.tar.gz
```

**Install locations:**

| Scope | Location |
|-------|----------|
| Project | `.opencode/agents/`, `.opencode/skills/`, `.opencode/rules/` |
| Global | `~/.config/opencode/agents/`, `~/.config/opencode/skills/`, `~/.config/opencode/rules/` |

---

### opencode publish

```
opencode publish [path]
```

Publishes an agent, skill, or rule package to the opencode registry or a custom registry. The path should point to a directory containing a valid package with an `opencode.jsonc` manifest.

**Flags:**

| Flag | Description |
|------|-------------|
| `--registry <url>` | Publish to a custom registry URL instead of the default. |
| `--public` | Publish as a public package (visible to everyone). |
| `--private` | Publish as a private package (visible only to the owner). |
| `--version <version>` | Override the version specified in the manifest. |
| `--dry-run` | Validate the package without actually publishing. |

**Examples:**

```bash
# Publish the current directory
opencode publish

# Publish a specific package directory
opencode publish ./dist/my-agent

# Publish to a custom registry
opencode publish --registry https://my-registry.example.com

# Publish as private
opencode publish --private

# Validate without publishing
opencode publish --dry-run
```

**Package requirements:**

A valid package must have:
- `opencode.jsonc` with `name`, `version`, `type` (agent/skill/rule)
- A `README.md` describing the package
- All required files for the package type

---

### opencode check

```
opencode check [path]
```

Validates opencode configuration, skills, rules, and agent definitions for correctness. Reports errors, warnings, and suggestions.

**Flags:**

| Flag | Description |
|------|-------------|
| `--config` | Check only the configuration file. |
| `--skills` | Check only skill definitions. |
| `--rules` | Check only rule definitions. |
| `--verbose`, `-v` | Show detailed validation output including warnings. |
| `--fix` | Automatically fix common issues when possible. |

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | No issues found |
| 1 | Errors found (configuration is invalid) |

**Examples:**

```bash
# Check entire project configuration
opencode check

# Check only skills
opencode check --skills

# Check with verbose output
opencode check --verbose

# Check and auto-fix issues
opencode check --fix

# Check a specific directory
opencode check ./my-project
```

**Validation checks:**

- Configuration file syntax (JSON/JSONC parsing)
- Required fields presence
- File path references validity
- Skill trigger conditions syntax
- Rule pattern format correctness
- Agent definition completeness
- Duplicate definitions

---

### opencode completion

```
opencode completion <shell>
```

Generates shell completion scripts for opencode CLI commands. The generated script can be sourced in the shell's init file to enable tab completion.

**Supported shells:**

- `bash`
- `zsh`
- `fish`
- `powershell`

**Examples:**

```bash
# Generate bash completions
opencode completion bash > /etc/bash_completion.d/opencode

# Generate zsh completions
opencode completion zsh > /usr/local/share/zsh/site-functions/_opencode

# Generate fish completions
opencode completion fish > ~/.config/fish/completions/opencode.fish

# Generate PowerShell completions
opencode completion powershell > $PROFILE.CurrentDirectoryCurrentHost
```

**Source in shell config:**

```bash
# .bashrc or .zshrc
source /etc/bash_completion.d/opencode
```

```powershell
# PowerShell $PROFILE
opencode completion powershell | Out-String | Invoke-Expression
```

---

### opencode mcp

```
opencode mcp <action> [args]
```

Manages MCP (Model Context Protocol) servers. MCP servers provide additional tools and resources to the model during sessions.

**Actions:**

| Action | Description |
|--------|-------------|
| `list` | List all configured MCP servers and their status. |
| `add <name> <command> [args...]` | Add a new MCP server configuration. |
| `remove <name>` | Remove an MCP server configuration. |
| `test <name>` | Test connectivity to an MCP server. |
| `start <name>` | Start a configured MCP server. |
| `stop <name>` | Stop a running MCP server. |

**Flags:**

| Flag | Description |
|------|-------------|
| `--global` | Operate on global MCP configuration (available across all projects). |

**Examples:**

```bash
# List all MCP servers
opencode mcp list

# Add a new MCP server
opencode mcp add my-server "node" "server.js"

# Add a global MCP server
opencode mcp add my-server "node" "server.js" --global

# Remove an MCP server
opencode mcp remove my-server

# Test connectivity
opencode mcp test my-server

# Start a server
opencode mcp start my-server

# Stop a server
opencode mcp stop my-server
```

**MCP server configuration:**

MCP servers are defined in the configuration file under the `mcpServers` key:

```jsonc
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "${OPENCODE_MCP_API_KEY}"
      }
    }
  }
}
```

---

### opencode ssh

```
opencode ssh <host> [command]
```

Connects to a remote host via SSH and allows opencode to interact with the remote environment. This enables the model to read files, execute commands, and perform operations on remote servers.

**Flags:**

| Flag | Description |
|------|-------------|
| `--port <port>` | SSH port to connect to (default: 22). |
| `--user <username>` | SSH username. If omitted, uses the current system username. |
| `--key <path>` | Path to an SSH private key file. If omitted, uses defaults from `~/.ssh/`. |
| `--forward-agent` | Forward the local SSH agent to the remote host. |

**Examples:**

```bash
# Connect to a remote host
opencode ssh deploy@example.com

# Connect on a non-standard port with a specific key
opencode ssh example.com --port 2222 --user admin --key ~/.ssh/deploy-key

# Run commands on the remote host in an opencode session
opencode ssh staging.example.com

# Enable agent forwarding
opencode ssh prod.example.com --forward-agent

# Execute a specific command and exit
opencode ssh server.example.com "tail -100 /var/log/app.log"
```

**Remote session behavior:**

- File operations read/write over SFTP
- Command execution over SSH
- Permission model applies to remote operations as well
- When used with `opencode run`, the task file executes in the remote context

---

### opencode update

```
opencode update [version]
```

Updates opencode to the specified version or the latest available version. Automatically downloads and installs the update.

**Flags:**

| Flag | Description |
|------|-------------|
| `--channel <channel>` | Update channel: `stable`, `beta`, or `nightly`. Defaults to `stable`. |
| `--yes`, `-y` | Auto-confirm the update. |

**Channels:**

| Channel | Description |
|---------|-------------|
| `stable` | Production-ready releases. Recommended for most users. |
| `beta` | Pre-release builds with new features. May have bugs. |
| `nightly` | Daily builds from the latest development branch. Unstable. |

**Examples:**

```bash
# Update to the latest stable version
opencode update

# Update to a specific version
opencode update 1.5.0

# Update to the latest beta
opencode update --channel beta

# Update to nightly
opencode update --channel nightly

# Auto-confirm update
opencode update --yes
```

---

### opencode version

```
opencode version
```

Prints the current opencode version and optionally detailed version information.

**Flags:**

| Flag | Description |
|------|-------------|
| `--json` | Output version information in JSON format. |
| `--verbose`, `-v` | Show detailed version information including build date, commit hash, Go version, and platform. |

**Examples:**

```bash
# Print version
opencode version

# Print detailed version
opencode version --verbose

# Print version as JSON
opencode version --json
```

**JSON output example:**

```json
{
  "version": "1.5.0",
  "commit": "a1b2c3d4e5f6",
  "buildDate": "2026-06-15T10:30:00Z",
  "goVersion": "go1.22.0",
  "os": "linux",
  "arch": "amd64",
  "channel": "stable"
}
```

---

### opencode help

```
opencode help [command]
```

Displays help information for any opencode command. If no command is specified, shows the top-level help.

**Examples:**

```bash
# Show top-level help
opencode help

# Show help for a specific command
opencode help run

# Show help for config subcommand
opencode help config

# Alternative: use --help flag
opencode run --help
```

---

## 4. Piped Input

opencode supports reading prompts from stdin. When input is piped, opencode runs non-interactively and processes the piped content as the prompt.

### Basic piping

```bash
# Pipe a simple prompt
echo "Explain the concept of eventually consistent databases" | opencode

# Pipe a prompt with model selection
echo "Refactor this function for better performance" | opencode --model claude-sonnet-4-20250514

# Pipe a file
cat deploy-instructions.md | opencode
```

### Piping with configuration

```bash
# Pipe with auto-approval and json output
echo "List all TODO comments in src/" | opencode --yes --output-format json

# Pipe a complex task with permission rules
cat audit-task.md | opencode \
  --model claude-sonnet-4-20250514 \
  --yes \
  --allow-read "src/**" \
  --allow-exec "npm run audit"
```

### Piping and saving results

```bash
# Save results to a file
echo "Generate a test plan for the API" | opencode --save test-plan.md

# Pipe commands through opencode
npm test 2>&1 | opencode "Analyze these test failures and suggest fixes"
```

---

## 5. Formatters & Output

The `--output-format` flag controls how opencode formats its output. This is critical for CI/CD integration and programmatic use.

| Format | Description | Best For |
|--------|-------------|----------|
| `terminal` | Rich terminal output with ANSI colors, progress indicators, and interactive elements. | Interactive sessions. |
| `json` | Single JSON object with the complete result. Includes `result`, `toolCalls`, `metadata`. | CI/CD, programmatic consumption. |
| `jsonl` | Newline-delimited JSON. One JSON object per line, streamed in real time. | Real-time log processing. |
| `json-stream` | Streaming JSON array. Writes JSON objects as they are produced. | Large outputs, pipelines. |
| `markdown` | Pure Markdown output without ANSI formatting. | Documentation generation, file output. |
| `html` | HTML-rendered output with syntax highlighting. | Web display, reports. |
| `file` | Writes output directly to the filesystem. Creates or overwrites files as directed by the model. | File generation tasks. |
| `edit` | Applies edits to existing files. Returns structured edit operations (search/replace blocks). | Automated refactoring. |

### Format details

**terminal** (default): Full TUI experience. Includes spinners, progress bars, color-coded diffs, and interactive prompts. Not suitable for piping or automation.

**json**: Complete structured output. The result is a JSON object with:
- `result`: The final answer or output
- `toolCalls`: Array of all tool invocations made during the session
- `metadata`: Session metadata (model used, duration, token counts)
- `errors`: Any errors encountered (empty if successful)

**jsonl**: Useful for real-time processing. Each line is a complete JSON object representing a single event (tool call, result, error).

**json-stream**: Similar to jsonl but wrapped as a JSON array. Compatible with streaming parsers.

**markdown**: Strips all ANSI escape codes and TUI elements. Produces clean Markdown suitable for writing to `.md` files.

**html**: Generates a standalone HTML page with rendered output, syntax highlighting for code blocks, and responsive styling.

**file**: The model writes directly to disk. Useful for scripts that generate configuration files, reports, or source code.

**edit**: Returns structured search/replace edit blocks. Designed for integration with code editors and refactoring tools.

---

## 6. CI/CD Integration

opencode is designed for seamless integration into CI/CD pipelines. The combination of `opencode run`, `--output-format json`, and exit codes enables automated workflows.

### Basic CI pipeline

```yaml
# GitHub Actions example
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run code audit
        run: |
          opencode run .opencode/tasks/audit.md \
            --yes \
            --output-format json \
            --allow-read "src/**" \
            --save audit-results.json
      - name: Check results
        run: |
          if [ $? -eq 0 ]; then
            echo "Audit passed"
          else
            echo "Audit failed"
            exit 1
          fi
```

### Parsing JSON output in scripts

```bash
#!/bin/bash
# Run and parse JSON output
output=$(opencode run task.md --yes --output-format json 2>/dev/null)

# Extract the result
result=$(echo "$output" | jq -r '.result')
# Extract metadata
model=$(echo "$output" | jq -r '.metadata.model')
tokens=$(echo "$output" | jq -r '.metadata.totalTokens')

echo "Model: $model"
echo "Tokens used: $tokens"
echo "Result: $result"
```

### Exit code handling

```bash
# Check exit code in CI
opencode run deploy.md --yes --allow-exec "deploy.sh"
exit_code=$?

case $exit_code in
  0) echo "Deployment successful" ;;
  1) echo "Deployment failed" >&2 ;;
  2) echo "Permission denied" >&2 ;;
  130) echo "Deployment interrupted" >&2 ;;
  137) echo "Deployment timed out" >&2 ;;
esac

exit $exit_code
```

### Scheduled tasks with cron

```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/project && opencode run .opencode/tasks/daily-maintenance.md --yes --save
```

### Environment variables for automation

| Variable | Description |
|----------|-------------|
| `OPENCODE_MODEL` | Default model to use |
| `OPENCODE_CONFIG` | Path to config file |
| `OPENCODE_HOME` | Override home directory for global config |
| `OPENCODE_MCP_*` | Custom environment variables forwarded to MCP servers |

---

## Full Documentation
For the complete official opencode CLI documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of all commands, flags, output formatters, CI/CD integration, and environment variables.

## Cross-References

- **Configuration reference**: `opencode_configuration` — detailed documentation of all configuration options in `.opencode.jsonc`
- **TUI customization**: `opencode_tui_customization` — theming, keybindings, layout customization for the interactive TUI
- **Decision trees**: `opencode_decision_trees` — flowcharts and decision matrices for selecting the right command, flag, agent, model, and output format based on task requirements
