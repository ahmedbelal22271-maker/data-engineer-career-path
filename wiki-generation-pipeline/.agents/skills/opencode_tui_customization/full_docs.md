# OpenCode TUI & Customization — Complete Official Documentation

> **Source:** https://opencode.ai/tui — https://opencode.ai/themes — https://opencode.ai/keybinds — retrieved July 2026

---

## Overview

OpenCode's Terminal User Interface (TUI) is the primary interaction mode. It provides a visual workspace for conversing with the AI, viewing code changes, browsing files, and managing sessions — all within your terminal.

---

## Launching the TUI

```bash
# Start in current directory
opencode

# Start in a specific directory
opencode --dir /path/to/project

# Resume a session
opencode --resume

# Resume specific session
opencode run --session-id <id>
```

---

## Layout

The TUI is divided into distinct zones:

```
┌─────────────────────────────────────────────┐
│  Header: Project name | Model | Session ID  │
├─────────────────────────────────────────────┤
│                                             │
│  Messages Area (scrollable conversation)    │
│                                             │
│  [User message]                             │
│  [AI response with code blocks]             │
│  [Tool output]                              │
│  [File diff]                                │
│                                             │
├─────────────────────────────────────────────┤
│  Input Box: Type your message here...       │
├─────────────────────────────────────────────┤
│  Footer: [auto] [anthropic/claude] [?]      │
└─────────────────────────────────────────────┘
```

### Header

Displays:
- **Project name** — The current workspace
- **Model** — Active model (e.g., `anthropic/claude-sonnet-4-6`)
- **Session ID** — Current session identifier
- **Mode** — Current mode (`auto` or `plan`)

### Messages Area

The scrollable conversation view. Shows:
- User messages (your input)
- AI responses (text, code blocks, explanations)
- Tool outputs (command results, file reads)
- File diffs (changes made)
- System messages (loading, errors)

### Input Box

Where you type messages. Supports:
- Multi-line input (Shift+Enter for new lines)
- @ mentions (file references, URLs)
- / commands (slash commands)
- Paste from clipboard

### Footer

Displays:
- Current mode (`auto` / `plan`)
- Active model
- Help indicator (`?` for keybindings)

---

## Commands

Commands are accessed with `/` in the input box:

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/model` | Switch the active model |
| `/mode` | Switch between plan and auto modes |
| `/clear` | Clear the current session |
| `/export` | Export session to clipboard or file |
| `/diff` | Show file changes in the session |
| `/file` | Browse files in the project |
| `/search` | Search for text in the project |
| `/undo` | Undo the last file change |
| `/redo` | Redo the last undone change |
| `/task` | Start a new task |
| `/setting` | Open settings panel |
| `/theme` | Change the color theme |
| `/copy` | Copy last response to clipboard |
| `/save` | Save session to file |
| `/quit` | Exit the TUI |

### Command Details

#### `/model`
Opens the model picker. Select from configured models. Changes take effect immediately.

#### `/mode`
Toggles between `plan` and `auto` modes:
- **plan** — Read-only, no file changes
- **auto** — Full access, can edit and execute

#### `/export`
Export options:
- **Clipboard** — Copy session as Markdown
- **File** — Save session to a `.md` file
- **JSON** — Export as structured JSON

#### `/diff`
Shows a unified or side-by-side diff of all file changes made during the session.

#### `/file`
Opens the file browser. Navigate your project's file tree with arrow keys and Enter to view files.

#### `/undo` / `/redo`
Undo or redo file changes made by the AI. Supports multiple levels.

#### `/task`
Creates a new task context. Useful for starting fresh work within the same session.

---

## @ Mentions

Reference content directly in your input:

| Mention | Description | Example |
|---------|-------------|---------|
| `@filename` | Attach a file as context | `@src/main.go explain this` |
| `@url` | Fetch and attach URL content | `@https://docs.example.com/api review this API` |
| `@issue` | Reference a GitHub issue | `@issue #42 fix this bug` |
| `@pr` | Reference a pull request | `@pr #123 review this PR` |
| `@diff` | Show the current diff | `@diff what changed?` |
| `@selection` | Reference selected text | Select text, then `@selection explain this` |
| `@clipboard` | Paste clipboard content | `@clipboard debug this code` |

### File Mentions

```bash
# Reference a specific file
@src/auth/login.ts how does this work?

# Reference multiple files
@src/auth/login.ts @src/auth/middleware.ts compare these

# Reference with line numbers
@src/main.go:42 what does this function do?
```

### URL Mentions

```bash
# Fetch a documentation page
@https://docs.python.org/3/library/json.html show me how to parse JSON

# Fetch a GitHub file
@https://github.com/user/repo/blob/main/README.md summarize this
```

---

## Keybindings

### Global Keybindings

| Key | Action |
|-----|--------|
| `?` | Toggle help overlay |
| `Ctrl+C` | Cancel current operation / Exit |
| `Ctrl+L` | Clear screen |
| `Ctrl+K` | Open model picker |
| `Tab` | Switch focus between panes |
| `Escape` | Close overlay / Cancel |

### Message Navigation

| Key | Action |
|-----|--------|
| `Up` | Previous message in history |
| `Down` | Next message in history |
| `Page Up` | Scroll up in messages |
| `Page Down` | Scroll down in messages |
| `Home` | Scroll to top of conversation |
| `End` | Scroll to bottom of conversation |

### Input Editing

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Shift+Enter` | New line in input |
| `Ctrl+A` | Move to beginning of line |
| `Ctrl+E` | Move to end of line |
| `Ctrl+U` | Clear current line |
| `Ctrl+W` | Delete word backward |
| `Ctrl+K` | Delete to end of line |
| `Ctrl+R` | Search command history |

### Vim Mode

When vim mode is enabled (via keybinding config):

| Key | Action |
|-----|--------|
| `Escape` | Enter normal mode |
| `i` | Enter insert mode |
| `dd` | Delete line |
| `yy` | Yank (copy) line |
| `p` | Paste |
| `u` | Undo |
| `Ctrl+r` | Redo |

---

## File Viewer

The TUI has a built-in file viewer accessible via the `/file` command.

### Features

- **Syntax highlighting** — Color-coded code for many languages
- **Line numbers** — Reference specific lines
- **File tree** — Navigate project structure
- **Search** — Find text within files
- **Multiple tabs** — View multiple files simultaneously

### Navigation

- Arrow keys to move through the file tree
- Enter to open a file
- `q` to close the file viewer
- `/` to search within the open file

---

## Diff View

The `/diff` command shows changes made during the session.

### Unified Diff

Default view showing changes in a single column:

```diff
--- a/src/auth.ts
+++ b/src/auth.ts
@@ -10,7 +10,9 @@
 function authenticate(token) {
-  return verify(token);
+  if (!token) return null;
+  return verify(token);
 }
```

### Side-by-Side Diff

Toggle with `s` in the diff view:

```
│ Original          │ Modified           │
│ function auth(t)  │ function auth(t) { │
│   return ver(t);  │   if (!t) return null; │
│                   │   return ver(t);   │
```

---

## Settings Panel

Access with `/setting` or the gear icon in the footer.

### Available Settings

- **Model** — Switch primary model
- **Provider** — Change AI provider
- **Mode** — Toggle plan/auto
- **Theme** — Change color theme
- **Font size** — Adjust text size
- **Word wrap** — Toggle word wrapping

---

## Themes

OpenCode supports customizable color themes.

### Built-in Themes

| Theme | Description |
|-------|-------------|
| `opencode` | Default dark theme |
| `light` | Light theme for bright terminals |
| `monokai` | Monokai-inspired colors |
| `dracula` | Dracula theme |
| `solarized` | Solarized Dark |

### Theme Configuration

Via the `/theme` command or in `opencode.json`:

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
      "info": "#1a8cda",
      "muted": "#6e7681",
      "border": "#30363d",
      "selection": "#264f78",
      "highlight": "#ff9e64",
      "dim": "#484f58"
    }
  }
}
```

### Theme Tokens

| Token | Description |
|-------|-------------|
| `background` | Main background color |
| `text` | Default text color |
| `accent` | Highlights, links, active elements |
| `success` | Success messages, pass indicators |
| `error` | Error messages, fail indicators |
| `warning` | Warnings, caution indicators |
| `info` | Informational messages |
| `muted` | Secondary text, comments |
| `border` | Panel borders, separators |
| `selection` | Selected text background |
| `highlight` | Search matches, highlights |
| `dim` | Dimmed text, inactive elements |

### Custom Theme Creation

Create a theme file at `~/.config/opencode/themes/my-theme.json`:

```json
{
  "name": "my-theme",
  "colors": {
    "background": "#1a1b26",
    "text": "#c0caf5",
    "accent": "#7aa2f7",
    "success": "#9ece6a",
    "error": "#f7768e",
    "warning": "#e0af68",
    "info": "#7dcfff",
    "muted": "#565f89",
    "border": "#3b4261",
    "selection": "#283457",
    "highlight": "#ff9e64",
    "dim": "#565f89"
  }
}
```

---

## Keybinding Configuration

Customize keybindings in `opencode.json`:

```json
{
  "keybindings": {
    "send": "enter",
    "cancel": "ctrl+c",
    "new_line": "shift+enter",
    "model_picker": "ctrl+k",
    "help": "?",
    "clear": "ctrl+l",
    "scroll_up": "page_up",
    "scroll_down": "page_down",
    "command_mode": "/"
  }
}
```

### Available Binding Targets

| Target | Default | Description |
|--------|---------|-------------|
| `send` | `enter` | Send the current message |
| `cancel` | `ctrl+c` | Cancel current operation |
| `new_line` | `shift+enter` | Insert newline in input |
| `model_picker` | `ctrl+k` | Open model selection |
| `help` | `?` | Toggle help overlay |
| `clear` | `ctrl+l` | Clear the screen |
| `scroll_up` | `page_up` | Scroll messages up |
| `scroll_down` | `page_down` | Scroll messages down |
| `command_mode` | `/` | Enter command mode |

---

## Terminal Compatibility

### Requirements

- **Terminal:** Any modern terminal (iTerm2, Alacritty, Kitty, Windows Terminal, WezTerm, Ghostty)
- **Minimum size:** 80 columns × 24 rows
- **Color support:** 256 colors minimum, true color (24-bit) recommended

### True Color Support

OpenCode uses ANSI 24-bit true color. If your terminal doesn't support it, colors automatically degrade to the nearest available palette.

### Windows Specifics

- Use Windows Terminal or WezTerm for best results
- PowerShell 7+ recommended
- WSL2 works with all Linux terminal features

---

## Session Export Formats

### Markdown Export

```markdown
# Session: 2024-01-15 authentication refactor

## User
Fix the login bug in auth.ts

## Assistant
I found the issue... [code blocks, explanations]

## Tool: bash
$ npm test
All tests passed
```

### JSON Export

```json
{
  "session_id": "abc123",
  "created_at": "2024-01-15T10:30:00Z",
  "model": "anthropic/claude-sonnet-4-6",
  "messages": [
    {
      "role": "user",
      "content": "Fix the login bug",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "I found the issue...",
      "tool_calls": [...]
    }
  ]
}
```

---

## Performance Optimization

- **Reduce context** — Clear sessions that are no longer relevant
- **Use plan mode** — Faster for exploration (no tool execution overhead)
- **Use zen mode** — No TUI rendering for background execution
- **Choose fast models** — Use speed-optimized models for the `big` slot
- **Minimize file reads** — Use grep to find specific content first
