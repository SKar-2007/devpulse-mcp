<p align="center">
  <h1 align="center">⚡ DevPulse MCP</h1>
  <p align="center">
    <strong>The MCP server that gives AI editors eyes.</strong><br>
    Docker logs. Postgres schema. Snowflake. Git history. Test results. Screenshots.<br>
    One server. Any editor. Zero context switches.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/go-1.21+-00ADD8?style=flat-square&logo=go" alt="Go">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/MCP-compatible-blueviolet?style=flat-square" alt="MCP">
  <img src="https://img.shields.io/badge/prs-welcome-brightgreen?style=flat-square" alt="PRs Welcome">
</p>

---

## The Problem

AI code editors are incredible at writing code. They're **completely blind** to what happens when that code runs.

```
9:41 AM — Cursor writes a new API endpoint
9:42 AM — You run it locally. Container crashes immediately.
9:42 AM — Cursor: "The code looks correct to me."
9:42 AM — You, manually: docker logs... oh, missing DB column.
           15 minutes of context switching. Again.
```

This happens **10-20 times per day**. Each switch costs 5-15 minutes. That's **2-5 hours of daily friction** that has nothing to do with building product.

## The Solution

DevPulse is a [Model Context Protocol](https://modelcontextprotocol.io) server that connects your AI editor directly to your runtime infrastructure.

```
┌─────────────┐     stdio/SSE     ┌──────────────────┐
│  AI Editor   │ ◄──────────────► │  DevPulse MCP    │
│  (Cursor,    │                   │  Server          │
│  Claude,     │                   │                  │
│  Windsurf)   │                   │  Docker API      │
└─────────────┘                   │  PostgreSQL      │
                                  │  Snowflake       │
                                  │  Git CLI         │
                                  │  Test Runners    │
                                  │  Cloudinary      │
                                  └──────────────────┘
```

The AI doesn't need to know **how** to query Docker or Postgres. It just sees a list of tools with descriptions. It calls them like function calls.

---

## Features

### 🐳 DevOps Bridge

| Tool | What it does | When you'd use it |
|------|-------------|-------------------|
| `get_container_logs` | Stream stdout/stderr from any Docker container | Container crashes, startup errors |
| `inspect_db_schema` | Full Postgres/SQLite/MySQL schema | Missing columns, type mismatches |
| `inspect_snowflake_schema` | Snowflake INFORMATION_SCHEMA | Data pipeline debugging |
| `get_system_health` | CPU, RAM, disk usage | Build failures from OOM |
| `restart_service` | Restart Docker containers | After fixing a config issue |

### 🧬 GitPulse

| Tool | What it does | When you'd use it |
|------|-------------|-------------------|
| `get_recent_diff_context` | Diffs formatted for LLM context | "What changed recently?" |
| `find_expert_for_file` | Git blame + commit history | "Who wrote this and why?" |
| `check_breaking_changes` | Branch vs main comparison | Before refactoring |

### 🧪 TestRig

| Tool | What it does | When you'd use it |
|------|-------------|-------------------|
| `run_targeted_tests` | pytest/jest/vitest on modified files | After AI writes code |
| `parse_failure_stacktrace` | Filtered, AI-ready stack traces | When tests fail |

### 📸 Visual Debug

| Tool | What it does | When you'd use it |
|------|-------------|-------------------|
| `capture_error_screenshot` | Screenshot → Cloudinary → URL | UI bugs, visual regressions |

---

## Demo

> **Scenario:** "The user API is returning 500. Fix it."

```
>>> Developer: The user API is returning 500. Fix it.

>>> Cursor: Let me investigate. I'll check the container logs.
    [calls get_container_logs("user-api", 50)]
    → ERROR: column "role" does not exist in table "users"

>>> Cursor: The DB schema is missing a column. Let me check.
    [calls inspect_db_schema()]
    → users: id, email, name, created_at (no 'role' column)

>>> Cursor: Found it. I'll create the migration and fix the middleware.
    → ALTER TABLE users ADD COLUMN role VARCHAR(20)
    → Fixed: src/auth/middleware.py:15

    [calls run_targeted_tests("src/auth/")]
    → 3 tests passed, 0 failures

>>> Cursor: One more thing — let me check Snowflake.
    [calls inspect_snowflake_schema()]
    → Snowflake users table also missing 'role' — flagging for sync

>>> Cursor: Fixed. Migration, middleware, tests pass, Snowflake flagged.
```

**Total time: ~30 seconds. Context switches: 0. Human intervention: 0.**

---

## Quick Start

### 1. Install

```bash
git clone https://github.com/SKar-2007/devpulse-mcp.git
cd devpulse-mcp
go build -o devpulse
```

### 2. Run

```bash
./devpulse --transport stdio
```

### 3. Connect your editor

<details>
<summary><strong>Cursor</strong></summary>

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "devpulse": {
      "command": "/absolute/path/to/devpulse",
      "args": ["--transport", "stdio"]
    }
  }
}
```
</details>

<details>
<summary><strong>Claude Code</strong></summary>

Add to Claude Code MCP config:

```json
{
  "mcpServers": {
    "devpulse": {
      "command": "/absolute/path/to/devpulse",
      "args": ["--transport", "stdio"]
    }
  }
}
```
</details>

<details>
<summary><strong>Windsurf</strong></summary>

Add to Windsurf MCP config:

```json
{
  "mcpServers": {
    "devpulse": {
      "command": "/absolute/path/to/devpulse",
      "args": ["--transport", "stdio"]
    }
  }
}
```
</details>

<details>
<summary><strong>Zed</strong></summary>

Add to Zed settings:

```json
{
  "context_servers": {
    "devpulse": {
      "command": "/absolute/path/to/devpulse",
      "args": ["--transport", "stdio"]
    }
  }
}
```
</details>

### 4. Start using it

Open Cursor (or your editor). Ask it to fix something. It will automatically discover and use DevPulse tools.

---

## Configuration

DevPulse works out of the box with Docker. For additional features, set these environment variables:

### Docker (no config needed)

Connects to local Docker socket automatically.

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
export SNOWFLAKE_ACCOUNT=xy12345.us-east-1
export SNOWFLAKE_USER=analyst
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_DATABASE=ANALYTICS
export SNOWFLAKE_SCHEMA=PUBLIC
```

### Cloudinary

```bash
export CLOUDINARY_URL=cloudinary://1234567890:xxxxxxxxxxxxx@your_cloud_name
```

> **Free tier:** 25GB storage, 25GB bandwidth/month. More than enough.

### System Health

```bash
export HEALTH_CHECK_INTERVAL=30   # seconds between checks
export HEALTH_WARN_CPU=80         # CPU % threshold
export HEALTH_WARN_RAM=85         # RAM % threshold
```

---

## How It Works

### 1. Server starts

```
$ ./devpulse --transport stdio
DevPulse MCP server running (stdio transport)
Registered 9 tools:
  - get_container_logs
  - inspect_db_schema
  - inspect_snowflake_schema
  - get_system_health
  - restart_service
  - get_recent_diff_context
  - find_expert_for_file
  - check_breaking_changes
  - run_targeted_tests
  - parse_failure_stacktrace
  - capture_error_screenshot
```

### 2. AI discovers tools

Your editor sends `tools/list` to DevPulse. DevPulse returns all tools with descriptions and JSON schemas.

### 3. AI calls tools

When debugging, the AI calls the appropriate tool. DevPulse executes it and returns results formatted for LLM context.

### 4. AI fixes code

Armed with real infrastructure data, the AI writes correct fixes. First try.

---

## Architecture

```
                    ┌─────────────────────────────────┐
                    │         DevPulse MCP Server      │
                    │              (Go)                 │
                    ├─────────────────────────────────┤
                    │                                  │
  AI Editor ───────►│  ┌────────────┐  ┌───────────┐ │
  (stdio/SSE)       │  │ DevOps     │  │ GitPulse  │ │
                    │  │ Bridge     │  │           │ │
                    │  │            │  │ diff      │ │──► git
                    │  │ logs       │──│──► docker  │ │
                    │  │ schema     │──│──► postgres│ │
                    │  │ snowflake  │──│──► snowflake│ │
                    │  │ health     │──│──► psutil  │ │
                    │  │ restart    │──│──► docker  │ │
                    │  └────────────┘  └───────────┘ │
                    │                                  │
                    │  ┌────────────┐  ┌───────────┐ │
                    │  │ TestRig    │  │ Visual    │ │
                    │  │            │  │ Debug     │ │
                    │  │ run_tests  │──│──► pytest  │ │
                    │  │ parse_trace│  │ capture   │──│──► screencapture
                    │  └────────────┘  │ upload    │──│──► cloudinary
                    │                  └───────────┘ │
                    └─────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Go 1.21+ |
| MCP SDK | [mcp-go](https://github.com/mark3labs/mcp-go) |
| Docker | Engine API via dockerode |
| PostgreSQL | pg driver + information_schema |
| Snowflake | gosnowflake driver |
| Screenshots | macOS screencapture |
| Image upload | Cloudinary REST API |
| Git | CLI subprocess calls |
| Tests | pytest / jest / vitest via subprocess |
| Transport | stdio (local) / SSE (network) |

---

## Safety

DevPulse is designed with safety as a first-class concern:

| Guard | Description |
|-------|-------------|
| 🔒 Read-only DB | All database queries are SELECT only — no mutations |
| 🔒 No force-push | Git operations never push, force-push, or amend |
| 🔒 Confirm restart | `restart_service` requires explicit user confirmation |
| 🔒 No exec | We don't exec into containers — logs only |
| 🔒 Audit trail | All tool calls logged locally for review |
| 🔒 No secrets | API keys stay in env vars, never logged or transmitted |

---

## FAQ

**Q: Does this work with VS Code?**
A: DevPulse uses the MCP protocol. VS Code doesn't support MCP natively yet, but extensions like Continue.dev can bridge the gap.

**Q: Does it send my code to the cloud?**
A: No. Everything runs locally. DevPulse connects to local Docker, local Postgres, local Git. The only external call is Cloudinary (for screenshot uploads, which you can disable).

**Q: What if I don't have Docker/Postgres/Snowflake?**
A: DevPulse works with whatever you have. No Docker? Skip those tools. No Snowflake? Skip that too. The tools are discovered dynamically.

**Q: Can I add custom tools?**
A: Yes. DevPulse is built on the open MCP standard. You can extend it with your own tools.

---

## Contributing

Contributions welcome! Here's how:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-tool`)
3. Commit your changes (`git commit -m 'Add my-tool'`)
4. Push to the branch (`git push origin feature/my-tool`)
5. Open a Pull Request

---

## License

MIT

---

<p align="center">
  Built at Hackathon 2026<br>
  <a href="https://github.com/SKar-2007/devpulse-mcp">github.com/SKar-2007/devpulse-mcp</a>
</p>
