# HACKATHON SPECIFICATION: DEVOPS & CONTEXT MCP LAYER

## OVERVIEW
A Model Context Protocol (MCP) server that connects local AI coding environments (Cursor, Claude Code, Windsurf, Zed) directly to runtime infrastructure, system specs, git history, and testing suites.

## CORE MCP TOOLSET & FEATURES

### 1. LOCAL INFRASTRUCTURE & RUNTIME INSPECTOR (DevOps-Bridge)
- **`get_container_logs`**: Allows AI editors to fetch and inspect stdout/stderr logs from Docker containers when local services fail or crash-loop.
- **`inspect_db_schema`**: Gives the AI instant access to local database tables, indices, and foreign keys (Postgres, SQLite, MySQL) for accurate ORM generation.
- **`get_system_health`**: Exposes CPU, RAM usage, and disk thermals to warn the AI agent if build or compilation failures are caused by resource exhaustion.
- **`restart_service`**: Allows AI agents to directly trigger restarts for local mock API servers or Docker services upon user request.

### 2. CONTEXT-AWARE REPOSITORY & COMMIT LINEAGE (GitPulse)
- **`get_recent_diff_context`**: Supplies uncommitted staged/unstaged diffs formatted specifically for LLM prompt context windows.
- **`find_expert_for_file`**: Analyzes Git blame and commit metadata to identify historical code ownership and summarize past PR decisions.
- **`check_breaking_changes`**: Compares local feature branch methods against the main branch schema to warn the AI before it refactors dependent functions.

### 3. AUTOMATED TEST & COVERAGE ORCHESTRATOR (TestRig)
- **`run_targeted_tests`**: Triggers unit/integration tests (`pytest`, `jest`, `vitest`) specific to modified source files without exiting the AI chat interface.
- **`parse_failure_stacktrace`**: Isolates test assertion failures and automatically formats the stack trace for prompt feeding, enabling continuous self-healing code loops.

## TECHNICAL STACK RECOMMENDATIONS
- **Language**: TypeScript (`@modelcontextprotocol/sdk`) OR Python (`mcp` SDK)
- **Integrations**: Docker Engine API (`dockerode`), PostgreSQL/SQLite native drivers, Git subprocesses.

## PPT SLIDE DECK OUTLINE (FOR EARLY SUBMISSION)

### Slide 1: Title & Vision
- Title: DevPulse MCP
- Subtitle: Giving AI Editors Real-time Perception of Local System Infrastructure

### Slide 2: The Problem
- AI code editors are "runtime blind" - they can write code but cannot see local database schemas, Docker logs, test runner errors, or system memory bottlenecks.

### Slide 3: The MCP Solution
- An open-standard MCP server acting as a bridge between LLMs and local infrastructure.

### Slide 4: Technical Architecture
- MCP Stdio/SSE communication channel connecting AI IDEs to system sockets and local DB drivers.

### Slide 5: Live Demo Workflow (2-Minute Plan)
- Ask Cursor/Claude Code to fix a failing API -> AI automatically queries Docker logs via MCP -> AI inspects local DB schema -> AI runs tests and verifies fix.

### Slide 6: Execution Roadmap (8-Hour Hackathon Scope)
- Hour 0-2: Protocol initialization & Docker/DB socket connectors.
- Hour 2-5: Implement MCP tools (`get_container_logs`, `inspect_db_schema`, `run_targeted_tests`).
- Hour 5-7: Edge-case prompts, safety guards, and IDE connection testing.
- Hour 7-8: Slide deck finalization & live presentation demo script.
