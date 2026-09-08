# HACKATHON SPECIFICATION: CLI DEV GUARDIAN & WORKFLOW TOOL

## OVERVIEW
A high-performance Terminal User Interface (TUI) and CLI tool designed to solve local development workflow friction, hung processes, and multi-service log chaos.

## CORE FEATURE ARCHITECTURE

### 1. INTELLIGENT PORT & PROCESS GUARDIAN (GhostBuster / PortSentry)
- **Real-time Port Radar**: Scans active listening ports commonly used in modern dev stacks (3000, 5000, 8080, 5432, 27017, 6379).
- **Parent-Child Process Mapping**: Visualizes full process trees (e.g., node -> npm -> next-server) so you know exactly what is running behind a port.
- **One-Key Interactive Process Reaper**: Fuzzy-search or select hanging zombie processes to terminate them safely (graceful SIGTERM first, SIGKILL escalation).
- **Safety Shield**: Hardcoded protections for OS-level processes (SSH, Systemd, Xorg, etc.) to prevent accidental system crashes.

### 2. ENVIRONMENT VARIABLE & CONFIG DRIFT SYNC (EnvPulse)
- **Health Inspection**: Audits active environment variables in real time against `.env.example` or team schemas for missing keys, malformed strings, or expired API tokens.
- **Hot-Reloading Shell Context**: Detects `.env` modifications on disk and syncs context across open terminal sessions without requiring manual restarts.
- **Secret Masking**: Obfuscates sensitive tokens while letting developers diff variable structures across local, staging, and production configs.

### 3. MULTI-SERVICE LOG AGGREGATOR & FAST FIX LAUNCHER (BuildPulse)
- **Split-Pane Terminal Stream**: Aggregates stdout/stderr from concurrent microservices (Frontend, Backend, DB, Workers) into color-coded, searchable panels.
- **Instant Stack-Trace Isolator**: Parses runtime exceptions, extracts the broken file path and line number, and ignores irrelevant node_modules frame bloat.
- **One-Keystroke Code Jump**: Pressing `e` on a stack trace directly opens the targeted source file at the exact broken line inside Cursor / VS Code / Neovim.

## TECHNICAL STACK RECOMMENDATIONS
- **Language**: Go (Bubbletea + Lipgloss) OR Python (Textual + Rich) OR Node.js (Blessed-contrib)
- **System Utilities**: System calls via `psutil`, `/proc` parsing, or `lsof` bindings.

## PPT SLIDE DECK OUTLINE (FOR EARLY SUBMISSION)

### Slide 1: Title & Vision
- Title: DevGuardian CLI
- Subtitle: The Ultimate Terminal Operating System for High-Speed Engineers

### Slide 2: The Problem
- Developer time lost to `EADDRINUSE`, invisible background zombie servers, lost error logs, and manually hunting PIDs in terminal windows.

### Slide 3: The Unified CLI Solution
- Live TUI combining process management, environment sync, and error log routing into one binary.

### Slide 4: Technical Architecture
- Low-overhead system process polling, IPC event monitoring, and terminal render engines.

### Slide 5: Live Demo Workflow (2-Minute Plan)
- Trigger port conflict -> Clean process with TUI -> Hot-sync broken `.env` -> Auto-jump to error location in IDE.

### Slide 6: Execution Roadmap (8-Hour Hackathon Scope)
- Hour 0-2: Port scanner & Process signal handlers.
- Hour 2-5: TUI Layouts, log stream parsing & IDE deep-linking.
- Hour 5-7: Polish, keyboard shortcuts, error handling.
- Hour 7-8: Final pitch prep & live demo rehearsal.
