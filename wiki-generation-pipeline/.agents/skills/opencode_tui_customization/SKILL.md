---
name: opencode TUI & Customization
description: Complete reference for opencode's terminal UI — screen layout, all / commands (help, plan, task, clear, model, setting, theme, export, save, undo, redo, diff, file, search, copy, quit), @ mentions (file, web, url, issue, pr, diff, selection, clipboard), keyboard navigation (30+ keybindings including vim mode), model picker, file viewer, diff view, settings panel, scrollback, multi-block editing, theme format (all 20+ tokens), and keybinding configuration. Trigger on "TUI", "keyboard shortcut", "theme", "keybinding", "/ command", "@ mention", "file viewer", "diff view", or interface customization questions.
---

# opencode TUI & Customization

## 1. Opening the TUI
Run `opencode` with no arguments. Your terminal splits into panels — chat on the left, optional side panels on the right. The status bar at the bottom shows the active model, mode, and connection state.

## 2. Screen Layout

```
┌─────────────────────────────────────────────┐
│  opencode  ●  Sonnet 4.6  [Chat]            │  ← Title bar
├──────────────────────┬──────────────────────┤
│                      │  File Viewer         │
│                      │  ┌──────────────────┐│
│   Chat Panel         │  │ src/main.ts      ││
│                      │  │ import { ... }   ││
│   ┌──────────────┐   │  │ function main()  ││
│   │ User: hello  │   │  │   console.log()  ││
│   │ Assistant:   │   │  └──────────────────┘│
│   │ Hi! I can    │   ├──────────────────────┤
│   │ help with... │   │  Diff View           │
│   └──────────────┘   │  ┌─ + added  ───────┐│
│                      │  │ - removed         ││
│                      │  └──────────────────┘│
├──────────────────────┴──────────────────────┤
│ > /model @file src/main.ts What does this   │  ← Input bar
│ do?                                         │
├─────────────────────────────────────────────┤
│  Model: Sonnet 4.6  │  Mode: Ask  │  42%    │  ← Status bar
└─────────────────────────────────────────────┘
```

## 3. / Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help overview |
| `/plan` | Toggle Plan Mode |
| `/task` | Create or focus a task |
| `/clear` | Clear conversation |
| `/model` | Open model picker |
| `/setting` | Open settings panel |
| `/theme` | Switch themes |
| `/export` | Export conversation |
| `/save` | Save to file |
| `/undo` | Undo last action |
| `/redo` | Redo last undone |
| `/diff` | Toggle diff view |
| `/file <path>` | Open file viewer |
| `/search <term>` | Search within conversation |
| `/copy` | Copy last response |
| `/quit` or `/exit` | Exit |

## 4. @ Mentions

| Mention | Description | Example |
|---------|-------------|---------|
| `@file <path>` | Reference file contents | `@file src/main.ts` |
| `@web <query>` | Search web | `@web latest Python version` |
| `@url <url>` | Fetch URL | `@url https://example.com` |
| `@issue <n>` | Reference GitHub issue | `@issue 42` |
| `@pr <n>` | Reference GitHub PR | `@pr 128` |
| `@diff` | Reference current git diff | `@diff` |
| `@selection` | Reference selected text | `@selection` |
| `@clipboard` | Reference clipboard contents | `@clipboard` |

## 5. Keyboard Navigation

| Key | Action |
|-----|--------|
| Up / Down | Navigate history / scroll |
| Left / Right | Horizontal scroll |
| Ctrl+P / Ctrl+N | Previous / next item |
| Ctrl+F / Ctrl+B | Page forward / backward |
| Home / End | Beginning / end |
| Tab | Autocomplete / cycle focus |
| Enter | Submit / select |
| Alt+Enter | Newline in input |
| Escape | Close panel / cancel |
| Ctrl+C | Cancel operation |
| Ctrl+L | Clear screen |
| Ctrl+S | Save |
| Ctrl+Z | Undo |
| Ctrl+Shift+Z | Redo |
| Ctrl+/ | Open model picker |
| Ctrl+O | Open file |
| Ctrl+W | Close file |
| Ctrl+E | Edit file |
| Ctrl+G | Go to line |
| Ctrl+F | Search in file viewer |
| Ctrl+K | Clear conversation |
| Ctrl+Q | Quit |

Vim keybindings (when enabled): `j`/`k`, `gg`/`G`, `w`/`b`, `dd`, `yy`, `p`, `u`, `Ctrl+r`

## 6. Model Picker

- **Open:** `Ctrl+/` or `/model`
- **Shows:** model name, provider, token count, context limit, cost estimate, latency
- **Filter:** type to narrow results
- **Switch:** select with arrows, press Enter
- **Context window:** displays remaining token budget for active conversation

## 7. File Viewer

- **Open via:** `@file`, `@diff`, `/file`, or clicking a file reference
- **Syntax highlighting:** 50+ languages
- **Features:** line numbers, scrollable, searchable (`Ctrl+F`), go-to-line (`Ctrl+G`), selection mode for multi-line copy
- **Tabs:** multiple files open simultaneously (`Ctrl+W` to close)

## 8. Diff View

- **Open via:** `/diff` or `@diff`
- **Formats:** side-by-side (default) or unified
- **Color coding:** green for additions, red for deletions
- **Navigation:** hunk jumping, file-by-file browsing
- **Inline actions:** stage selective changes

## 9. Settings Panel (/setting)

Configurable at runtime:

- **theme** — switch between built-in or custom themes
- **font_size** — 10–24pt
- **tab_width** — 2, 4, or 8
- **word_wrap** — on/off
- **vim_mode** — enable/disable vim keybindings
- **notifications** — on/off
- **output_format** — markdown or plain text
- **permission_mode** — allow/deny for tool execution

## 10. Themes

**Built-in themes:** light, dark, monokai, solarized, dracula, nord, github, one_dark

**Custom theme JSON format:**

```jsonc
{
  "name": "my-theme",
  "type": "dark",
  "background": "#1e1e2e",
  "foreground": "#cdd6f4",
  "cursor": "#f5e0dc",
  "selection": "#45475a",
  "comment": "#6c7086",
  "primary": "#89b4fa",
  "secondary": "#a6e3a1",
  "error": "#f38ba8",
  "warning": "#fab387",
  "info": "#89dceb",
  "success": "#a6e3a1",
  "border": "#45475a",
  "highlight": "#585b70",
  "line_number": "#6c7086",
  "status_bar": {
    "background": "#181825",
    "foreground": "#cdd6f4",
    "mode": "#89b4fa"
  },
  "file_viewer": {
    "background": "#181825",
    "foreground": "#cdd6f4",
    "syntax_string": "#a6e3a1",
    "syntax_keyword": "#cba6f7",
    "syntax_function": "#89b4fa",
    "syntax_type": "#f9e2af",
    "syntax_comment": "#6c7086",
    "syntax_number": "#fab387"
  },
  "diff": {
    "addition": "#a6e3a1",
    "deletion": "#f38ba8",
    "addition_background": "#1e3a2e",
    "deletion_background": "#3a1e1e"
  },
  "chat": {
    "user": "#89b4fa",
    "assistant": "#cdd6f4",
    "system": "#6c7086",
    "thinking": "#f9e2af"
  }
}
```

**Apply via config:** `"theme": ".opencode/themes/my_theme.json"`

## 11. Keybinding Configuration

Custom keybindings use JSON format:

```jsonc
{
  "keybindings": [
    { "key": "ctrl+t", "command": "opencode run scripts/todo.md", "description": "Sync Todoist" },
    { "key": "ctrl+shift+p", "command": "opencode plan", "description": "Open plan mode" },
    { "key": "ctrl+shift+e", "command": "opencode export --format html", "description": "Export as HTML" }
  ],
  "remove_defaults": [],
  "vim_mode": true
}
```

**Apply via config:** `"keybindings": ".opencode/keybindings.json"`

## Full Documentation
For the complete official opencode TUI documentation, see `full_docs.md` in this directory. It contains exhaustive coverage of layout, commands, @ mentions, keybindings, file viewer, diff view, settings, themes, and terminal compatibility.

**Cross-references:**
- `opencode_configuration` — theme and keybinding config in `opencode.json`
- `opencode_cli_commands` — startup flags (`--theme`, `--model`, `--keybindings`)
- `opencode_models_providers` — model picker details and provider setup
