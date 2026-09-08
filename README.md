# DevPulse MCP

> An MCP server that gives Cursor, Claude Code, and Windsurf the ability to see Docker, Postgres, Snowflake, Git, and your test suite.

AI editors are great at writing code. They're blind to everything else — Docker crash loops, missing DB columns, broken Snowflake schemas, visual UI bugs. DevPulse fixes that with one MCP server.

---

## Why

```
9:41 AM — Cursor writes a new API endpoint
9:42 AM — Container crashes immediately
9:42 AM — Cursor: "The code looks correct to me."
           (It's a missing DB column. Cursor can't see that.)
```

Every context switch to terminal = 5-15 minutes lost. 10-20 times per day.

## What DevPulse Does

DevPulse exposes 9 tools via the Model Context Protocol. Your AI editor discovers them automatically and calls them like function calls — no copy-paste, no terminal, no guessing.

### DevOps Bridge

| Tool | Description |
|------|-------------|
| `get_container_logs` | Stream stdout/stderr from any Docker container |
| `inspect_db_schema` | Full Postgres/SQLite/MySQL schema introspection |
| `inspect_snowflake_schema` | Snowflake INFORMATION_SCHEMA queries |
| `get_system_health` | CPU, RAM, disk usage warnings |
| `restart_service` | Restart Docker containers (with confirmation) |

### GitPulse

| Tool | Description |
|------|-------------|
| `get_recent_diff_context` | Package diffs into LLM-friendly context |
| `find_expert_for_file` | Git blame + commit history analysis |
| `check_breaking_changes` | Compare branch against main for breaking changes |

### TestRig

| Tool | Description |
|------|-------------|
| `run_targeted_tests` | Run pytest/jest/vitest on modified files |
| `parse_failure_stacktrace` | Filter stack traces for AI consumption |

### Visual Debug

| Tool | Description |
|------|-------------|
| `capture_error_screenshot` | Screenshot → Cloudinary → URL for AI |

## Demo

```
>>> Developer: The user API is returning 500. Fix it.
>>> Cursor: Let me check the container logs.
    [calls get_container_logs("user-api", 50)]
    → ERROR: column "role" does not exist in table "users"
>>> Cursor: DB schema is missing a column.
    [calls inspect_db_schema()]
    → users: id, email, name, created_at (no 'role' column)
>>> Cursor: Found it. Creating migration + fixing middleware.
    → ALTER TABLE users ADD COLUMN role VARCHAR(20)
    → Fixed: src/auth/middleware.py:15
    [calls run_targeted_tests("src/auth/")]
    → 3 tests passed, 0 failures
>>> Cursor: Fixed. Done.
```

## Quick Start

### Prerequisites

- Go 1.21+
- Docker (running)
- PostgreSQL or Snowflake (optional)

### Install

```bash
git clone https://github.com/SKar-2007/devpulse-mcp.git
cd devpulse-mcp
go build -o devpulse
```

### Run

```bash
./devpulse --transport stdio
```

### Connect to Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "devpulse": {
      "command": "/path/to/devpulse",
      "args": ["--transport", "stdio"]
    }
  }
}
```

### Connect to Claude Code

Add to Claude Code MCP config:

```json
{
  "mcpServers": {
    "devpulse": {
      "command": "/path/to/devpulse",
      "args": ["--transport", "stdio"]
    }
  }
}
```

## Configuration

### PostgreSQL

```bash
export PGHOST=localhost
export PGPORT=5432
export PGUSER=postgres
export PGDATABASE=myapp
export PGPASSWORD=yourpassword
```

### Snowflake

```bash
export SNOWFLAKE_ACCOUNT=your_account
export SNOWFLAKE_USER=your_user
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_DATABASE=ANALYTICS
export SNOWFLAKE_SCHEMA=PUBLIC
```

### Cloudinary

```bash
export CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

## Architecture

```
┌─────────────┐     stdio/SSE     ┌──────────────────┐
│  AI Editor   │ ◄──────────────► │  DevPulse MCP    │
│  (Cursor,    │                   │  Server (Go)     │
│  Claude,     │                   │                  │
│  Windsurf)   │                   │  ┌────────────┐  │
└─────────────┘                   │  │ DevOps     │──┼──► Docker API
                                  │  │ Bridge     │──┼──► PostgreSQL
                                  │  │            │──┼──► Snowflake
                                  │  ├────────────┤  │
                                  │  │ GitPulse   │──┼──► Git CLI
                                  │  ├────────────┤  │
                                  │  │ TestRig    │──┼──► pytest/jest
                                  │  ├────────────┤  │
                                  │  │ Visual     │──┼──► screencapture
                                  │  │ Debug      │──┼──► Cloudinary
                                  │  └────────────┘  │
                                  └──────────────────┘
```

## Tech Stack

- **Go** + [mcp-go](https://github.com/mark3labs/mcp-go) SDK
- **Docker Engine API** via dockerode
- **gosnowflake** driver
- **pg** driver + information_schema
- **Cloudinary** REST API
- **Git** CLI subprocess calls
- **pytest / jest / vitest** via subprocess
- **stdio** transport (zero config)

## Safety

- DB queries are **read-only** (SELECT only)
- Git operations **never push, force-push, or amend**
- `restart_service` requires explicit user confirmation
- `capture_error_screenshot` is non-interactive
- All tool calls logged locally for audit trail

## License

MIT

---

Built at Hackathon 2026
