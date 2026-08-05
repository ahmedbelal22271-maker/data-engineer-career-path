# Coursera Course Tracker — Complete Capability Reference

> **Skill:** `coursera_tracker`
> **Location:** `.agents/skills/coursera_tracker/`
> **Auto-discovered:** Yes, via `opencode.json` `skills.paths`
> **Test suite:** 20/20 tests passing

---

## 1. Safety & Compliance Layer

The safety layer is the first thing every operation passes through. It enforces Coursera's robots.txt rules for the `ClaudeBot` user-agent, which is explicitly named in the robots.txt file.

| Capability | Method | Description |
|-----------|--------|-------------|
| URL validation | `validate_access(url)` | Checks every URL against cached robots.txt before any fetch |
| ClaudeBot-specific rules | `_get_rules_for_agent()` | Merges `*` baseline with `ClaudeBot`-specific rules per robots.txt standard |
| Access logging | `_log_access()` | Logs every validation attempt (allowed/denied + reason) to `data/access_log.json` |
| Non-Coursera rejection | `validate()` | Raises `ValueError` for any URL not on `coursera.org` |
| Hardcoded fallback | `_blocked_prefixes` | Backup block list if robots.txt is missing or corrupted |
| Blocked path enumeration | `get_blocked_paths()` | Returns all paths blocked for ClaudeBot |
| Allowed path enumeration | `get_allowed_paths()` | Returns all paths explicitly allowed for ClaudeBot |

### Allowed Paths (ClaudeBot)

| Path Pattern | Purpose |
|-------------|---------|
| `/learn/{slug}` | Course landing pages, syllabi, about sections |
| `/specializations/{slug}` | Specialization overview pages |
| `/professional-certificates/{slug}` | Certificate program pages |
| `/api/utilities/v1/imageproxy` | Image proxy only |

### Blocked Paths (ClaudeBot)

| Path Pattern | Blocked By |
|-------------|-----------|
| `/api/*` | Hardcoded block + robots.txt `*` rule |
| `/lecture/*` | robots.txt `ClaudeBot`-specific rule |
| `/account/*` | Hardcoded block + robots.txt `*` rule |
| `/search` | Hardcoded block + robots.txt `*` rule |
| `/maestro/*` | Hardcoded block + robots.txt `*` rule |
| `/ui/*` | Hardcoded block + robots.txt `*` rule |
| `/signature/voucher/*` | robots.txt `*` rule |
| `/acclaimbadge/*` | robots.txt `*` rule |
| `/voucher/*` | robots.txt `*` rule |
| `/ent-website/*` | robots.txt `*` rule |
| `/learn-perf/*` | robots.txt `*` rule |
| `/specializations-perf/*` | robots.txt `*` rule |
| `/professional-certificates-perf/*` | robots.txt `*` rule |
| `/business/xmlrpc.php` | robots.txt `*` rule |
| `/business/wp-content/uploads/*` | robots.txt `*` rule |
| `/business/search` | robots.txt `*` rule |
| `/business/teams/search` | robots.txt `*` rule |
| `/organizations/*` | robots.txt `*` rule |

### Access Log Format

Every validation attempt is logged to `data/access_log.json`:

```json
{
  "timestamp": "2026-07-13T21:07:00+00:00",
  "url": "https://www.coursera.org/learn/machine-learning",
  "path": "/learn/machine-learning",
  "allowed": true,
  "reason": "matches Allow: /learn/",
  "user_agent": "ClaudeBot"
}
```

Log is capped at 500 entries (oldest evicted automatically).

---

## 2. Course Registration & Management

| Capability | Method | Description |
|-----------|--------|-------------|
| Register new course | `register_course(slug, title, modules)` | Creates tracking record with metadata and module list |
| Auto-fetch metadata | `fetch_public_metadata(slug)` | Fetches title, description, syllabus from `/learn/{slug}` (robots.txt-allowed path) |
| Extract modules from HTML | `extract_modules_from_html(html)` | Parses Coursera course page HTML to extract week/module headings |
| Re-register (update) | `register_course()` on existing slug | Adds new modules without overwriting existing progress |
| Unregister course | `unregister_course(slug)` | Removes course and all its progress data |
| List all courses | `list_courses()` | Returns list of all registered course slugs |

### Usage Examples

```python
tracker = CourseraTracker()

# Register with manual module list
tracker.register_course(
    "machine-learning",
    title="Machine Learning",
    modules=["Linear Regression", "Neural Networks", "Recommender Systems"]
)

# Register with metadata
tracker.register_course(
    "data-science",
    title="Applied Data Science with Python",
    description="University of Michigan",
    modules=["Intro", "Plotting", "Selection", "Fetching", "Processing"]
)

# Update an existing course (adds new modules, keeps existing progress)
tracker.register_course("machine-learning", modules=["Linear Regression", "NN", "RecSys", "Capstone"])
# "Capstone" is added; "Linear Regression", "NN", "RecSys" keep their existing status

# List all tracked courses
courses = tracker.list_courses()
# ["machine-learning", "data-science"]

# Remove a course
tracker.unregister_course("data-science")
```

---

## 3. Progress Tracking

| Capability | Method | Description |
|-----------|--------|-------------|
| Mark module completed | `update_status(slug, module, "completed")` | Sets completion timestamp, optional notes and score |
| Mark module in progress | `update_status(slug, module, "in_progress")` | Tracks active work |
| Mark module skipped | `update_status(slug, module, "skipped", reason)` | Records why it was skipped |
| Reset to pending | `update_status(slug, module, "pending")` | Revert status if needed |
| Add notes | `add_notes(slug, module, notes)` | Append notes without changing status |
| Record scores | `update_status(..., score=92.0)` | Numeric score (0-100) per module |
| Track time spent | `ModuleRecord.time_spent_minutes` | Manual time logging per module |
| Timestamp everything | `registered_at`, `completed_at` | UTC ISO-8601 timestamps on all state changes |

### Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Not yet started (default) |
| `in_progress` | Currently being worked on |
| `completed` | Finished with passing grade or user-confirmed |
| `skipped` | Intentionally skipped (with reason) |

### Usage Examples

```python
# Complete a module with score
tracker.update_status("machine-learning", "Linear Regression", "completed",
                      notes="Passed quiz with 92%", score=92.0)

# Start working on a module
tracker.update_status("machine-learning", "Neural Networks", "in_progress")

# Skip a module
tracker.update_status("machine-learning", "Recommender Systems", "skipped",
                      reason="Not relevant to current project")

# Add notes without changing status
tracker.add_notes("machine-learning", "Neural Networks",
                  "Watched lecture 3 twice, need to review backprop math")
```

### ModuleRecord Fields

```python
ModuleRecord(
    status=ModuleStatus.COMPLETED,    # pending | in_progress | completed | skipped
    notes="Passed quiz with 92%",     # free-form text
    score=92.0,                       # numeric 0-100, optional
    registered_at="2026-07-13T21:00:00+00:00",
    completed_at="2026-07-13T22:30:00+00:00",
    time_spent_minutes=45.0           # manual tracking
)
```

---

## 4. Reporting & Analytics

| Capability | Method | Description |
|-----------|--------|-------------|
| Single course progress | `fetch_progress(slug)` | Returns `ProgressReport` with completion %, counts, next modules |
| All courses progress | `fetch_progress()` | Returns list of `ProgressReport` for every registered course |
| Completion percentage | `CourseRecord.completion_pct` | Auto-calculated (completed / total * 100) |
| Module status counts | `.completed_count`, `.in_progress_count`, `.pending_count`, `.skipped` | Breakdown by status |
| Markdown export | `export_report()` | Full human-readable report with per-course breakdown and overall summary |
| JSON export | `export_json()` | Machine-readable dump of all progress data |
| Next-up suggestions | `suggest_next(slug, limit)` | Prioritizes in-progress modules, then pending in order |

### ProgressReport Object

```python
ProgressReport(
    course_slug="machine-learning",
    title="Machine Learning",
    total_modules=12,
    completed=5,
    in_progress=1,
    pending=6,
    skipped=0,
    completion_pct=41.7,
    next_modules=["Neural Networks", "Recommender Systems"]
)
```

### Markdown Output Example

```markdown
## Machine Learning (machine-learning)
**Progress:** 41.7% (5/12 modules)

- Completed: 5
- In Progress: 1
- Pending: 6

**Next up:**
1. Neural Networks
2. Recommender Systems
```

### Full Export Example

```markdown
# Coursera Progress Report

*Generated: 2026-07-13 21:00 UTC*

## Machine Learning (machine-learning)
**Progress:** 41.7% (5/12 modules)

- Completed: 5
- In Progress: 1
- Pending: 6

**Next up:**
1. Neural Networks
2. Recommender Systems

## Data Science (data-science)
**Progress:** 100.0% (5/5 modules)

- Completed: 5

---

**Overall:** 10/17 modules (58.8%) across 2 courses
```

---

## 5. Adaptive Learning Pathways

| Capability | Method | Description |
|-----------|--------|-------------|
| Smart next-module suggestion | `suggest_next()` | Returns in-progress modules first, then pending in registration order |
| Gap detection | `pending_count` + `suggest_next()` | Identifies modules not yet started |
| Performance-based notes | `ModuleRecord.score` + `.notes` | Store quiz scores and study notes for each module |
| Course comparison | `fetch_progress()` all | See completion % across all courses side-by-side |

### Suggestion Logic

```
suggest_next("machine-learning", limit=3) returns:
  1. In-progress modules (prioritize finishing what's started)
  2. Pending modules (in registration order)
  3. Skipped modules are excluded from suggestions
```

### Usage Examples

```python
# What should I work on next?
next_mods = tracker.suggest_next("machine-learning")
# ["Neural Networks", "Recommender Systems"]

# Get more suggestions
next_mods = tracker.suggest_next("machine-learning", limit=5)
# ["Neural Networks", "Recommender Systems", "Capstone"]

# Compare progress across all courses
all_reports = tracker.fetch_progress()
for report in all_reports:
    print(f"{report.title}: {report.completion_pct}%")
# Machine Learning: 41.7%
# Data Science: 100.0%
# Python for Everybody: 60.0%
```

---

## 6. Data Persistence

| Capability | Method | Description |
|-----------|--------|-------------|
| Auto-save on every change | `_save_state()` | Every `update_status()`, `register_course()`, etc. writes to disk |
| Load on init | `_load_state()` | Restores state from `data/progress.json` on startup |
| Cross-instance persistence | `CourseraTracker(data_dir)` | New instance from same directory picks up all prior state |
| Human-editable JSON | `data/progress.json` | User can manually edit progress file |
| Git-trackable | Plain JSON | Progress file works with version control |
| Export anytime | `export_json()` | Snapshot all data at any point |

### Progress File Schema

```json
{
  "version": 1,
  "updated_at": "2026-07-13T21:00:00+00:00",
  "courses": {
    "machine-learning": {
      "slug": "machine-learning",
      "title": "Machine Learning",
      "description": "Stanford CS229",
      "provider": "Stanford University",
      "url": "https://www.coursera.org/learn/machine-learning",
      "registered_at": "2026-07-13T20:00:00+00:00",
      "modules": {
        "Linear Regression": {
          "status": "completed",
          "notes": "Passed quiz with 92%",
          "score": 92.0,
          "registered_at": "2026-07-13T20:00:00+00:00",
          "completed_at": "2026-07-13T22:00:00+00:00",
          "time_spent_minutes": 45.0
        },
        "Neural Networks": {
          "status": "in_progress",
          "notes": "Watched lecture 3 twice",
          "score": null,
          "registered_at": "2026-07-13T20:00:00+00:00",
          "completed_at": null,
          "time_spent_minutes": 30.0
        }
      }
    }
  }
}
```

---

## 7. Error Handling & Validation

| Capability | Error Type | Trigger | Recovery |
|-----------|-----------|---------|----------|
| Unknown course | `KeyError` | `update_status()` on unregistered slug | Register the course first |
| Unknown module | `KeyError` | `update_status()` on module not in course | Check available modules in error message |
| Invalid status | `ValueError` | Status not in `pending`, `in_progress`, `completed`, `skipped` | Use a valid status string |
| Non-Coursera URL | `ValueError` | `validate_access()` on non-coursera.org URL | Only use Coursera URLs |
| Blocked URL | `PermissionError` | `fetch_public_metadata()` on restricted path | Use local data entry instead |
| Corrupt state file | Graceful fallback | `data/progress.json` has invalid JSON | Starts fresh, logs warning |
| Missing robots.txt | Hardcoded fallback | `scripts/robots.txt` not found | Uses `_blocked_prefixes` backup list |

### Error Message Examples

```
KeyError: "Course not registered: data-science"
KeyError: "Module 'Fake Module' not found in 'machine-learning'. Available modules: ['Linear Regression', 'Neural Networks']"
ValueError: "Invalid status 'bogus'. Must be one of: ['pending', 'in_progress', 'completed', 'skipped']"
PermissionError: "ACCESS DENIED: https://www.coursera.org/api/v1/x is blocked by Coursera's robots.txt."
ValueError: "Non-Coursera URL rejected: https://evil.com/steal. Only coursera.org URLs are within scope."
```

---

## 8. What It Explicitly Does NOT Do

These are hard constraints enforced by design, not limitations to work around.

| Constraint | Reason | Enforcement |
|-----------|--------|-------------|
| No `/api/` access | Blocked by robots.txt for all bots | `RobotsTxtGuard` blocks all `/api/` paths |
| No `/lecture/` access | Blocked by robots.txt for ClaudeBot specifically | Merged `ClaudeBot`-specific Disallow rule |
| No `/account/` access | Blocked — cannot see actual enrolled courses | Hardcoded block + robots.txt |
| No `/search` access | Blocked — cannot search catalog programmatically | Hardcoded block + robots.txt |
| No authentication | Avoids ToS violations from cookie/session replay | No auth code in skill at all |
| No grade scraping | Grades require authenticated account access | Progress is self-reported by user |
| No real-time enrollment check | Would require `/account/` access | User registers courses manually |
| No certificate verification | Not available via public pages | User reports completion manually |
| No form submissions | Robots.txt disallows automated interactions | Skill only reads public pages |
| No rate abuse | Coursera can block IPs for aggressive scraping | Single-threaded, no parallel fetches |

---

## 9. Integration Points

| Integration | How | Use Case |
|------------|-----|----------|
| opencode skill system | Auto-discovered via `skills.paths` in `opencode.json` | Triggers on "Coursera progress", "track courses" |
| Wiki pipeline | Progress data can feed into `updates/` enrichment workflow | Track which course content has been enriched |
| Todoist sync | Progress reports inform task completion | Close Todoist tasks when modules are completed |
| Export to chat | `export_report()` produces paste-ready Markdown | Quick progress check in conversation |
| Export to file | Write `export_json()` output to any path | Backup, sharing, or archival |
| Access log audit | `data/access_log.json` can be reviewed | Verify compliance with robots.txt |
| Manual file editing | `data/progress.json` is human-readable JSON | User can fix entries by hand |

---

## 10. File Structure

```
coursera_tracker/
├── SKILL.md                    # Skill definition and instructions
├── scripts/
│   ├── __init__.py             # Package exports
│   ├── safety.py               # robots.txt enforcement (RobotsTxtGuard)
│   ├── schema.py               # Data models (CourseMetadata, CourseRecord, ModuleRecord, ProgressReport)
│   ├── tracker.py              # Core CourseraTracker class
│   ├── robots.txt              # Cached Coursera robots.txt (fetched 2026-07-13)
│   └── test_tracker.py         # 20-test validation suite
└── data/
    ├── progress.json           # Local progress state (auto-created)
    └── access_log.json         # Access validation audit log (auto-created)
```

---

## 11. Quick Reference Card

### Initialize

```python
from scripts.tracker import CourseraTracker
tracker = CourseraTracker()
```

### Register

```python
tracker.register_course("slug", title="Title", modules=["Mod1", "Mod2"])
```

### Update

```python
tracker.update_status("slug", "Mod1", "completed", notes="Passed", score=95)
```

### Check

```python
report = tracker.fetch_progress("slug")  # single
reports = tracker.fetch_progress()        # all
```

### Suggest

```python
next_mods = tracker.suggest_next("slug", limit=3)
```

### Export

```python
print(tracker.export_report())  # Markdown
data = tracker.export_json()     # JSON
```

### Validate

```python
tracker.validate_access("https://www.coursera.org/learn/ml")  # True
tracker.validate_access("https://www.coursera.org/api/v1/x")  # False
```
