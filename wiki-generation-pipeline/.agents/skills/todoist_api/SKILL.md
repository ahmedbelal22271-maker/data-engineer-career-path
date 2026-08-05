---
name: todoist-api
description: Use the Todoist REST API v1 and Sync API to programmatically manage tasks, projects, sections, comments, labels, reminders, and workspaces. Also covers OAuth authentication, the Todoist CLI, and MCP server setup. Use this skill whenever the user wants to integrate with Todoist, automate task management, build Todoist-powered tools, or query/manipulate their Todoist data via API.
---

# Todoist REST API v1 — Skill Reference

Base URL: `https://api.todoist.com/api/v1/`

## Authentication

Every request requires an `Authorization: Bearer <token>` header. Obtain tokens via:

### Personal Token
From Todoist Settings → Integrations. Simplest for personal use.

### OAuth Authorization Code Flow
1. Redirect user to `https://app.todoist.com/oauth/authorize?client_id=<id>&scope=<scopes>&state=<secret>&response_type=code`
2. User authorizes, redirected to your `redirect_uri` with `?code=<auth_code>&state=<secret>`
3. Exchange code: `POST https://api.todoist.com/oauth/access_token` with `client_id`, `client_secret`, `code`, `redirect_uri`

**Scopes:** `task:add`, `data:read`, `data:read_write` (includes task:add + data:read), `data:delete`, `project:delete`, `backups:read`

### Refresh Tokens
New apps get 1-hour access tokens + refresh tokens. Refresh via `POST https://api.todoist.com/oauth/access_token` with `grant_type=refresh_token`, `refresh_token=...`, `client_id`, `client_secret`.

- Refresh tokens rotate on each use. Store the new one from every response.
- 60-second grace window for network retries (same replacement access token returned, no new refresh_token).
- Outside grace window, replay detection revokes ALL tokens for that user+app.

### Dynamic Client Registration (RFC 7591)
`POST https://api.todoist.com/oauth/register` — JSON body with `redirect_uris`, `client_name`, `scope`, `grant_types`, etc. No auth required, rate limited. Returns `client_id` with `tdd_` prefix and `client_secret`.

### OAuth Client ID Metadata Document
Public clients (SPAs, MCP servers) can skip registration entirely by hosting a JSON metadata document at an HTTPS URL and passing that URL as `client_id` on the authorization request. Requires PKCE.

### Revoke Tokens
- `DELETE /api/v1/access_tokens?client_id=<id>&client_secret=<secret>&access_token=<token>`
- `POST /api/v1/revoke` (RFC 7009) — requires HTTP Basic auth with client credentials

### Migrate Personal Token to OAuth
`POST /api/v1/access_tokens/migrate_personal_token`

---

## REST API Endpoints

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | Get all tasks (supports filtering by `project_id`, `section_id`, `label`, `filter`) |
| POST | `/tasks` | Create a task |
| GET | `/tasks/{task_id}` | Get a task |
| POST | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| POST | `/tasks/{task_id}/close` | Close a task |
| POST | `/tasks/{task_id}/reopen` | Reopen a task |
| POST | `/tasks/{task_id}/move` | Move a task to a different section/project |
| POST | `/tasks/quick` | Quick add a task (natural language) |
| GET | `/tasks/filter` | Get tasks by filter string |
| GET | `/tasks/completed/by_completion_date` | Completed tasks grouped by completion date |
| GET | `/tasks/completed/by_due_date` | Completed tasks grouped by due date |
| GET | `/tasks/completed/stats` | Completed task stats |

**Task parameters:** `content` (required), `project_id`, `section_id`, `parent_id`, `order`, `label_ids`, `priority` (1-4), `due_string`, `due_date`, `due_datetime`, `due_lang`, `assignee_id`, `assigner_id`, `duration`, `duration_unit`, `description`

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects` | Get all projects |
| POST | `/projects` | Create a project |
| GET | `/projects/{project_id}` | Get a project |
| POST | `/projects/{project_id}` | Update a project |
| DELETE | `/projects/{project_id}` | Delete a project |
| POST | `/projects/{project_id}/archive` | Archive a project |
| POST | `/projects/{project_id}/unarchive` | Unarchive a project |
| POST | `/projects/{project_id}/join` | Join a shared project |
| GET | `/projects/{project_id}/collaborators` | Get project collaborators |
| GET | `/projects/search` | Search projects |
| GET | `/projects/permissions` | Get project role permissions |
| GET | `/projects/archived` | Get archived projects |

### Sections
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sections` | Get all sections |
| POST | `/sections` | Create a section |
| GET | `/sections/{section_id}` | Get a section |
| POST | `/sections/{section_id}` | Update a section |
| DELETE | `/sections/{section_id}` | Delete a section |
| POST | `/sections/{section_id}/archive` | Archive a section |
| POST | `/sections/{section_id}/unarchive` | Unarchive a section |
| GET | `/sections/search` | Search sections |

### Comments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/comments` | Get comments (filter by `task_id` or `project_id`) |
| POST | `/comments` | Create a comment |
| GET | `/comments/{comment_id}` | Get a comment |
| POST | `/comments/{comment_id}` | Update a comment |
| DELETE | `/comments/{comment_id}` | Delete a comment |

### Labels
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/labels` | Get all labels |
| POST | `/labels` | Create a label |
| GET | `/labels/{label_id}` | Get a label |
| POST | `/labels/{label_id}` | Update a label |
| DELETE | `/labels/{label_id}` | Delete a label |
| GET | `/labels/search` | Search labels |
| GET | `/labels/shared` | Get shared labels |
| POST | `/labels/shared/rename` | Rename a shared label |
| POST | `/labels/shared/remove` | Remove shared label occurrences |

### Reminders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reminders` | Get all reminders |
| POST | `/reminders` | Create a reminder |
| GET | `/reminders/{reminder_id}` | Get a reminder |
| POST | `/reminders/{reminder_id}` | Update a reminder |
| DELETE | `/reminders/{reminder_id}` | Delete a reminder |

### Location Reminders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/location_reminders` | Get all location reminders |
| POST | `/location_reminders` | Create a location reminder |
| GET | `/location_reminders/{reminder_id}` | Get a location reminder |
| POST | `/location_reminders/{reminder_id}` | Update a location reminder |
| DELETE | `/location_reminders/{reminder_id}` | Delete a location reminder |

### Folders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/folders` | Get all folders |
| POST | `/folders` | Create a folder |
| GET | `/folders/{folder_id}` | Get a folder |
| POST | `/folders/{folder_id}` | Update a folder |
| DELETE | `/folders/{folder_id}` | Delete a folder |

### Workspaces
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workspaces` | Get all workspaces |
| POST | `/workspaces` | Create a workspace |
| GET | `/workspaces/{workspace_id}` | Get a workspace |
| POST | `/workspaces/{workspace_id}` | Update a workspace |
| DELETE | `/workspaces/{workspace_id}` | Delete a workspace |
| POST | `/workspaces/join` | Join a workspace (via invite code) |
| POST | `/workspaces/logo` | Update workspace logo |
| GET | `/workspaces/users` | Get workspace users |
| GET | `/workspaces/plan_details` | Get workspace plan details |
| GET | `/workspaces/invitations` | Get invitations |
| GET | `/workspaces/invitations/all` | Get all invitations |
| PUT | `/workspaces/invitations/{invite_code}/accept` | Accept invitation |
| PUT | `/workspaces/invitations/{invite_code}/reject` | Reject invitation |
| POST | `/workspaces/invitations/delete` | Delete invitation |
| GET | `/workspaces/{workspace_id}/projects/active` | Get active workspace projects |
| GET | `/workspaces/{workspace_id}/projects/archived` | Get archived workspace projects |
| POST | `/workspaces/{workspace_id}/users/invite` | Invite users to workspace |
| POST | `/workspaces/{workspace_id}/users/{user_id}` | Update workspace user role |
| DELETE | `/workspaces/{workspace_id}/users/{user_id}` | Remove workspace user |

### Templates
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/templates/import_into_project_from_template_id` | Import template by ID |
| POST | `/templates/import_into_project_from_file` | Import template from file |
| POST | `/templates/create_project_from_file` | Create project from template file |
| GET | `/templates/file` | Export template as file |
| GET | `/templates/url` | Export template as URL |

### Uploads
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/uploads` | Upload a file |
| DELETE | `/uploads` | Delete an upload |

### User
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/user` | Get user info |
| GET | `/user/productivity_stats` | Get productivity stats |
| PUT | `/notification_setting` | Update notification settings |

### Activities
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/activities` | Get activity logs |

### Backups
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/backups` | Get backup list (requires `backups:read` scope) |
| GET | `/backups/download` | Download a backup (requires `data:read_write` scope) |

### Emails
| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/emails` | Get or create email alias |
| DELETE | `/emails` | Disable email integration |

### ID Mappings
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/id_mappings/{obj_name}/{obj_ids}` | Map old IDs to new IDs (for v9 migration) |

### Billing
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payments/cancel_plan_with_redirect_to_stripe` | Cancel plan |
| POST | `/payments/get_subscription_info` | Get subscription info |
| POST | `/payments/reactivate_plan` | Reactivate plan |

---

## Sync API

**Endpoint:** `POST https://api.todoist.com/api/v1/sync`  
**Content-Type:** `application/x-www-form-urlencoded`

The Sync API is the primary way first-party clients keep data in sync. Supports batch read/write in a single HTTP request and incremental sync.

### Reading Resources
```
sync_token=*&resource_types=["all"]
```
- `sync_token`: `*` for full sync, or a token from a previous response for incremental sync
- `resource_types`: JSON array of resource types: `labels`, `projects`, `items` (tasks), `notes` (task comments), `sections`, `filters`, `reminders`, `reminders_location`, `locations`, `user`, `live_notifications`, `collaborators`, `user_settings`, `notification_settings`, `user_plan_limits`, `completed_info`, `stats`, `workspaces`, `workspace_users`, `workspace_filters`, `view_options`, `project_view_options_defaults`, `role_actions`. Use `"all"` for everything. Prefix with `-` to exclude (e.g. `-projects`).

### Writing Resources
```
commands=[{"type":"<command_type>","temp_id":"<uuid>","uuid":"<uuid>","args":{...}}]
```
- `type`: Command type (e.g. `item_add`, `project_add`, `section_add`, etc.)
- `temp_id`: Temporary ID for new resources (referenced by subsequent commands in same batch)
- `uuid`: Unique command UUID for idempotency and result mapping

### Sync Commands Reference
Common command types: `item_add`, `item_update`, `item_delete`, `item_move`, `item_complete`, `item_uncomplete`, `item_close`, `project_add`, `project_update`, `project_delete`, `project_archive`, `project_unarchive`, `section_add`, `section_update`, `section_delete`, `section_archive`, `section_unarchive`, `section_move`, `label_add`, `label_update`, `label_delete`, `filter_add`, `filter_update`, `filter_delete`, `reminder_add`, `reminder_update`, `reminder_delete`, `note_add`, `note_update`, `note_delete`, `collaborator_add`, `collaborator_delete`, `live_notification_set_last_read`, `live_notification_mark_read`, `live_notification_mark_unread`, etc.

### Response
```json
{
  "sync_token": "...",
  "sync_status": {"<uuid>": "ok"},
  "temp_id_mapping": {"<temp_id>": "<real_id>"},
  "full_sync": true,
  "full_sync_date_utc": "..."
}
```
- `sync_status`: Maps each command uuid to `"ok"` or an error object
- `temp_id_mapping`: Maps temporary IDs to real server-assigned IDs
- `full_sync`: Whether this is a full (true) or incremental (false) sync

### Resource Fields (Sync API)

**Item (task):** `id`, `project_id`, `section_id`, `content`, `description`, `due` (date object), `duration`, `duration_unit`, `priority` (1-4), `parent_id`, `child_order`, `labels` (label IDs), `assignee_id`, `assigner_id`, `responsible_uid`, `collapsed`, `is_deleted`, `is_completed`, `in_history`, `date_added`, `date_completed`, `checked`, `added_by_uid`, `user_id`, `day_order`, `sync_id`

**Project:** `id`, `name`, `color`, `parent_id`, `child_order`, `collapsed`, `shared`, `is_deleted`, `is_archived`, `is_favorite`, `view_style`, `inbox_project`, `team_inbox`, `workspace_id`, `user_id`, `description`, `is_shared`, `is_selected`

**Section:** `id`, `project_id`, `order`, `name`, `collapsed`, `is_deleted`, `is_archived`, `is_favorite`, `added_by_uid`, `workspace_id`, `sync_id`, `section_order`, `description`

**Note (comment):** `id`, `posted_uid`, `project_id` (or `item_id`), `content`, `file_attachment`, `uids_to_notify`, `is_deleted`, `posted_at`, `reactions`

**Label:** `id`, `name`, `color`, `item_order`, `is_deleted`, `is_favorite`

**Reminder:** `id`, `notify_uid`, `item_id`, `service`, `type` (`relative`/`absolute`), `due`, `minute_offset`, `name`, `loc_lat`, `loc_long`, `loc_trigger`, `is_deleted`

---

## Pagination

REST endpoints that return lists support cursor-based pagination:
- `limit` (query param, default varies by endpoint)
- `cursor` (returned as `next_cursor` in responses when `has_more` is true)

Send `GET /api/v1/tasks?limit=50` → response includes `next_cursor` if more results exist → `GET /api/v1/tasks?limit=50&cursor=<next_cursor>`

Activity log pagination: uses `offset` and `limit` instead of cursor.

---

## Due Dates & Deadlines

### Due Date Formats
- **Full-day:** `{"date": "2025-12-01"}`
- **Floating with time:** `{"date": "2025-12-01T12:00:00"}`
- **With timezone:** `{"date": "2025-12-01T13:00:00Z", "timezone": "Europe/Madrid", "string": "ev day at 13", "lang": "en", "is_recurring": false}`

### Deadlines (separate from due dates)
`{"date": "2025-12-01"}` — a hard deadline distinct from the due date field. Passed in `deadline` on task create/update or `args.deadline` in Sync commands.

---

## Webhooks

Webhook configuration via Todoist App Management Console. Events are sent as POST to your callback URL with JSON body containing event type, user_id, event_data, version, and timestamp. Includes `event_data_extra` for additional context.

---

## Request Limits

- Rate limits apply per user/endpoint. 429 responses include `Retry-After` header.
- Sync API has separate command limits (number of commands per request and per minute).
- Refer to the `Retry-After` header or `error_extra.retry_after` field for backoff timing.

---

## Error Handling

### REST API Errors
Standard HTTP status codes: 200 (success), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 429 (rate limited), 500 (server error), 503 (service unavailable).

Error body format:
```json
{
  "error_tag": "UNAUTHORIZED",
  "error_code": 477,
  "error": "Unauthorized",
  "http_code": 401,
  "error_extra": { "retry_after": 3, "event_id": "<hash>" }
}
```

### Sync API Errors
Errors per command in `sync_status` object. Common error fields: `error_tag` (machine-readable), `error_code`, `error`, `http_code`, `error_extra`. Error codes like `15` (invalid temporary id), `20` (invalid argument value). Non-retryable commands return 400-level `http_code` in sync_status — do not retry them.

---

## Todoist CLI

Install: `npm install -g @doist/todoist-cli`
Auth: `td auth login`

Common commands:
- `td add "task content #project"` — Quick add task
- `td today` — Show today's tasks
- `td inbox` — Show inbox
- `td task list [--project "Name"]` — List tasks
- `td project list` — List projects

Shell completions: `td completion install [bash|zsh|fish]`

---

## Todoist MCP

**Primary URL:** `https://ai.todoist.net/mcp`  
**Transport:** Streamable HTTP

Setup:
- **Claude Desktop:** Settings → Connectors → Add custom connector → enter URL + OAuth
- **Cursor:** Add to `mcp.json` with `npx -y mcp-remote https://ai.todoist.net/mcp`
- **Claude Code CLI:** `claude mcp add --transport http todoist https://ai.todoist.net/mcp`
- **VS Code:** Command Palette → MCP: Add Server → Type HTTP → enter URL
- **Other:** `npx -y mcp-remote https://ai.todoist.net/mcp`

MCP response format includes three representations: stringified JSON (`content[0]`), human-readable summary (last content item), and `structuredContent` (parsed JSON object for MCP spec 2025-03-26+ clients).
