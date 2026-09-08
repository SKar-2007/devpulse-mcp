#!/usr/bin/env python3
"""DevPulse MCP — Hackathon Deck (v2, less template-y)"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Colors ───────────────────────────────────────────────────────────────
BG        = RGBColor(0x11, 0x13, 0x18)
SURFACE   = RGBColor(0x1A, 0x1D, 0x24)
CODE_BG   = RGBColor(0x0D, 0x10, 0x17)
CYAN      = RGBColor(0x56, 0xD4, 0xE5)
GREEN     = RGBColor(0x6A, 0xDB, 0x95)
AMBER     = RGBColor(0xF0, 0xC5, 0x4B)
RED       = RGBColor(0xE0, 0x6C, 0x75)
PURPLE    = RGBColor(0xC6, 0x78, 0xDD)
WHITE     = RGBColor(0xE5, 0xE5, 0xE5)
GRAY      = RGBColor(0x7A, 0x82, 0x8E)
DIM       = RGBColor(0x50, 0x56, 0x62)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

def bg(s):
    f = s.background.fill; f.solid(); f.fore_color.rgb = BG

def rect(s, l, t, w, h, fill=SURFACE, border=None, bw=1):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if border: sh.line.color.rgb = border; sh.line.width = Pt(bw)
    else: sh.line.fill.background()
    return sh

def rrect(s, l, t, w, h, fill=SURFACE, border=None):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if border: sh.line.color.rgb = border; sh.line.width = Pt(1)
    else: sh.line.fill.background()
    return sh

def txt(s, l, t, w, h, text, sz=16, c=WHITE, b=False, a=PP_ALIGN.LEFT, font="Consolas"):
    tb = s.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = text
    p.font.size = Pt(sz); p.font.color.rgb = c; p.font.bold = b; p.font.name = font
    p.alignment = a
    return tb

def mono_block(s, l, t, w, h, lines, sz=11, title=None, title_c=CYAN):
    """code block with optional title"""
    if title:
        rect(s, l, t, w, Inches(0.35), fill=CYAN)
        txt(s, l+Inches(0.15), t+Inches(0.02), w, Inches(0.3), title, sz=11, c=BG, b=True, font="Consolas")
        t += Inches(0.35)
    rect(s, l, t, w, Inches(len(lines)*0.22+0.3), fill=CODE_BG)
    for i, line in enumerate(lines):
        txt(s, l+Inches(0.15), t+Inches(0.1+i*0.22), w-Inches(0.3), Inches(0.22),
            line, sz=sz, c=GREEN, font="Consolas")

def bullet_list(s, l, t, w, h, items, sz=14, c=WHITE, bc=CYAN):
    tb = s.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.space_after = Pt(4)
        r = p.add_run(); r.text = "→ "; r.font.size = Pt(sz); r.font.color.rgb = bc; r.font.name = "Consolas"; r.font.bold = True
        r2 = p.add_run(); r2.text = item; r2.font.size = Pt(sz); r2.font.color.rgb = c; r2.font.name = "Consolas"

# ══════════════════════════════════════════════════════════════════════════
# 1 — TITLE
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(1), Inches(1.8), Inches(11), Inches(0.6),
    "$ devpulse serve --transport stdio", sz=20, c=GREEN, font="Consolas")
txt(sl, Inches(1), Inches(2.6), Inches(11), Inches(1.2),
    "DevPulse MCP", sz=52, b=True, c=WHITE, font="Consolas")
txt(sl, Inches(1), Inches(3.9), Inches(11), Inches(0.7),
    "An MCP server that gives Cursor, Claude Code, and Windsurf\nthe ability to see Docker, Postgres, Snowflake, Git, and your test suite.",
    sz=18, c=GRAY)
rect(sl, Inches(1), Inches(5.4), Inches(4), Pt(2), fill=CYAN)
txt(sl, Inches(1), Inches(5.6), Inches(6), Inches(0.4),
    "Hackathon 2026", sz=13, c=DIM)

# ══════════════════════════════════════════════════════════════════════════
# 2 — THE PROBLEM (real talk)
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "What actually happens when AI writes your code", sz=28, b=True, c=WHITE)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=RED)

# left side: the actual pain
mono_block(sl, Inches(0.8), Inches(1.5), Inches(6.5), Inches(0),
    [
        "// 9:41 AM — Cursor writes a new API endpoint",
        "// 9:42 AM — You run it locally",
        "// 9:42 AM — Container crashes immediately",
        "//",
        "// You: ...what happened?",
        "// Cursor: \"The code looks correct to me.\"",
        "//",
        "// (It's a missing DB column. Cursor can't see that.)",
    ], sz=11, title="The real workflow")

txt(sl, Inches(0.8), Inches(4.5), Inches(6.5), Inches(0.5),
    "AI editors are great at writing code. They're blind to everything else.",
    sz=16, c=AMBER, b=True)

# right side: the specific failures
rrect(sl, Inches(7.8), Inches(1.5), Inches(5), Inches(5.2), border=RED)
txt(sl, Inches(8.0), Inches(1.6), Inches(4.6), Inches(0.4),
    "What AI can't see right now", sz=16, b=True, c=RED)
items = [
    "Docker container logs (crash loops, OOM kills)",
    "Database schema (missing columns, type mismatches)",
    "Snowflake warehouse state (tables, views, pipeline errors)",
    "System resources (CPU throttling, disk full)",
    "Git history (who broke what, when, why)",
    "Test results (it wrote the test, but it fails)",
    "Visual errors (UI bugs, broken layouts — AI is text-only)",
    "Stack traces (filtered to YOUR code, not node_modules)",
]
bullet_list(sl, Inches(8.0), Inches(2.2), Inches(4.6), Inches(4.0),
            items, sz=13, c=GRAY, bc=RED)

txt(sl, Inches(0.8), Inches(5.5), Inches(11.7), Inches(0.5),
    "Every context switch to terminal = 5-15 minutes lost. Multiply by 10-20 times per day.",
    sz=14, c=DIM)

# ══════════════════════════════════════════════════════════════════════════
# 3 — WHAT IS MCP (technical but clear)
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "Model Context Protocol — the missing layer", sz=28, b=True, c=WHITE)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=CYAN)

# protocol explanation
txt(sl, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.0),
    "MCP is a protocol that lets AI editors discover and call tools\n"
    "exposed by external servers. Think of it like a plugin system,\n"
    "but standardized — one server works in Cursor, Claude Code,\n"
    "Windsurf, Zed, and any future editor that adopts MCP.\n\n"
    "The AI doesn't need to know HOW to query Docker or Postgres.\n"
    "It just sees a list of tools with descriptions and schemas.\n"
    "It calls them like function calls.", sz=15, c=GRAY)

# actual protocol message
mono_block(sl, Inches(7.0), Inches(1.5), Inches(5.8), Inches(0),
    [
        '// What Cursor sends to our server:',
        '{',
        '  "method": "tools/list",',
        '  "params": {}',
        '}',
        '',
        '// What we return:',
        '{',
        '  "tools": [',
        '    {',
        '      "name": "get_container_logs",',
        '      "description": "Fetch logs from a Docker container",',
        '      "inputSchema": {',
        '        "type": "object",',
        '        "properties": {',
        '          "container": {"type": "string"},',
        '          "lines": {"type": "integer", "default": 100}',
        '        }',
        '      }',
        '    }',
        '  ]',
        '}',
    ], sz=10, title="MCP protocol exchange")

txt(sl, Inches(0.8), Inches(5.5), Inches(5.5), Inches(0.5),
    "Transport: stdio (local) or SSE (network). One binary, any editor.",
    sz=14, c=CYAN, b=True)

# ══════════════════════════════════════════════════════════════════════════
# 4 — TOOL: Docker Logs
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "Tool: get_container_logs", sz=28, b=True, c=CYAN)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=CYAN)

# what it does
txt(sl, Inches(0.8), Inches(1.5), Inches(5.5), Inches(1.5),
    "Streams stdout/stderr from any Docker container on your machine.\n"
    "AI can see crash-loop logs, startup errors, and runtime exceptions\n"
    "without leaving the chat. Supports filtering by log level and time range.",
    sz=14, c=GRAY)

# actual Go implementation
mono_block(sl, Inches(0.8), Inches(3.2), Inches(5.8), Inches(0),
    [
        'func (t *DockerLogsTool) Execute(ctx context.Context,',
        '    args map[string]any) (any, error) {',
        '',
        '    container := args["container"].(string)',
        '    lines := args["lines"].(int)',
        '',
        '    reader, err := t.client.ContainerLogs(ctx,',
        '        container, Docker.ContainerLogsOptions{',
        '            ShowStdout: true,',
        '            ShowStderr: true,',
        '            Tail:       fmt.Sprintf("%d", lines),',
        '        })',
        '    if err != nil {',
        '        return nil, fmt.Errorf("container not found: %w", err)',
        '    }',
        '    defer reader.Close()',
        '',
        '    // Parse multiplexed stream, return clean text',
        '    return io.ReadAll(reader)',
        '}',
    ], sz=10, title="Go — Docker Engine API via dockerode")

# what AI sees
mono_block(sl, Inches(7.0), Inches(1.5), Inches(5.8), Inches(0),
    [
        '// What Cursor sees when it calls this tool:',
        '',
        'Output from get_container_logs("auth-api", 50):',
        '',
        '2026-09-08T10:23:01Z ERROR: migration failed',
        '  relation "users" column "role" does not exist',
        '2026-09-08T10:23:01Z INFO  shutting down',
        '2026-09-08T10:23:02Z ERROR: exit status 1',
        '',
        '// AI now KNOWS the exact error.',
        '// No copy-paste. No terminal. No guessing.',
    ], sz=11, title="Tool output → AI prompt context")

# ══════════════════════════════════════════════════════════════════════════
# 5 — TOOL: DB Schema
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "Tool: inspect_db_schema", sz=28, b=True, c=GREEN)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=GREEN)

txt(sl, Inches(0.8), Inches(1.5), Inches(5.5), Inches(1.2),
    "Connects to any local Postgres/SQLite/MySQL and dumps the full schema\n"
    "— tables, columns, types, constraints, indices, foreign keys.\n"
    "AI generates accurate ORM models and migrations from real schema state.",
    sz=14, c=GRAY)

# SQL query it runs
mono_block(sl, Inches(0.8), Inches(2.9), Inches(5.8), Inches(0),
    [
        '-- What we actually query (Postgres):',
        '',
        'SELECT',
        '  c.table_name,',
        '  c.column_name,',
        '  c.data_type,',
        '  c.is_nullable,',
        '  pgd.description AS column_comment',
        'FROM information_schema.columns c',
        'LEFT JOIN pg_catalog.pg_statio_all_tables st',
        '  ON c.table_schema = st.schemaname',
        '  AND c.table_name = st.relname',
        'LEFT JOIN pg_catalog.pg_description pgd',
        '  ON pgd.objoid = st.relid',
        '  AND pgd.objsubid = c.ordinal_position',
        'WHERE c.table_schema = \'public\'',
        'ORDER BY c.table_name, c.ordinal_position;',
    ], sz=10, title="PostgreSQL — schema introspection")

# what AI gets
mono_block(sl, Inches(7.0), Inches(1.5), Inches(5.8), Inches(0),
    [
        '// Tool output formatted for LLM context:',
        '',
        'SCHEMA: public',
        '',
        'TABLE: users',
        '  id          SERIAL      PRIMARY KEY',
        '  email       VARCHAR(255) NOT NULL UNIQUE',
        '  name        VARCHAR(100)',
        '  created_at  TIMESTAMP   DEFAULT NOW()',
        '',
        'TABLE: orders',
        '  id          SERIAL      PRIMARY KEY',
        '  user_id     INTEGER     REFERENCES users(id)',
        '  total       DECIMAL(10,2)',
        '  status      VARCHAR(20) DEFAULT \'pending\'',
        '',
        '// AI generates migrations that actually match reality.',
    ], sz=11, title="Tool output → AI sees real DB state")

# ══════════════════════════════════════════════════════════════════════════
# 6 — TOOL: Git Context
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "Tools: GitPulse suite", sz=28, b=True, c=PURPLE)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=PURPLE)

# Three tools side by side
tools_data = [
    ("get_recent_diff_context", CYAN,
     "Packages uncommitted diffs into\nLLM-friendly context. Shows what\nchanged, where, and why (commit msgs)."),
    ("find_expert_for_file", GREEN,
     "Git blame + commit history analysis.\nTells the AI who last touched this code\nand what decisions were made."),
    ("check_breaking_changes", AMBER,
     "Compares your feature branch against\nmain. Warns the AI before it refactors\na function that 12 other files depend on."),
]

for i, (name, clr, desc) in enumerate(tools_data):
    x = Inches(0.8 + i * 4.1)
    rrect(sl, x, Inches(1.5), Inches(3.7), Inches(2.5), border=clr)
    txt(sl, x+Inches(0.2), Inches(1.6), Inches(3.3), Inches(0.4),
        name, sz=14, b=True, c=clr, font="Consolas")
    txt(sl, x+Inches(0.2), Inches(2.1), Inches(3.3), Inches(1.8),
        desc, sz=13, c=GRAY)

# git commands we run
mono_block(sl, Inches(0.8), Inches(4.3), Inches(11.7), Inches(0),
    [
        '# get_recent_diff_context runs:',
        'git diff --cached          # staged changes',
        'git diff                   # unstaged changes',
        'git log --oneline -5       # recent commits for context',
        '',
        '# find_expert_for_file runs:',
        'git blame --line-porcelain src/auth/middleware.go | head -20',
        'git log --follow --format="%h %an %s" -- src/auth/middleware.go',
        '',
        '# check_breaking_changes runs:',
        'git diff main...HEAD -- src/api/   # what changed in your branch',
    ], sz=10, title="Under the hood — real git commands")

# ══════════════════════════════════════════════════════════════════════════
# 7 — TOOL: Test Runner
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "Tools: TestRig suite", sz=28, b=True, c=AMBER)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=AMBER)

txt(sl, Inches(0.8), Inches(1.5), Inches(11.5), Inches(1.0),
    "run_targeted_tests: Runs pytest/jest/vitest on files related to what the AI just modified.\n"
    "parse_failure_stacktrace: Filters out node_modules frames, extracts the actual assertion failure,\n"
    "and formats it so the AI can self-heal without human intervention.",
    sz=14, c=GRAY)

# test execution
mono_block(sl, Inches(0.8), Inches(2.9), Inches(5.8), Inches(0),
    [
        'func (t *TestRunnerTool) Execute(ctx context.Context,',
        '    args map[string]any) (any, error) {',
        '',
        '    files := args["files"].([]string)',
        '    runner := args["runner"] // "pytest"|"jest"|"vitest"',
        '',
        '    // Build targeted test command',
        '    cmd := exec.CommandContext(ctx, runner,',
        '        "--tb=short", "--no-header",',
        '        fmt.Sprintf("%s...", files[0]))',
        '',
        '    output, err := cmd.CombinedOutput()',
        '    // Parse failures, strip irrelevant frames',
        '    return formatForLLM(output, err), nil',
        '}',
    ], sz=10, title="Go — subprocess test execution")

# stack trace parsing
mono_block(sl, Inches(7.0), Inches(1.5), Inches(5.8), Inches(0),
    [
        '// Raw pytest output (what AI would normally see):',
        'FAILED tests/test_auth.py::test_login - AssertionError',
        '  assert response.status == 200',
        '  E       assert 401 == 200',
        '  /venv/lib/python3.11/site-packages/.../models.py:42',
        '  /src/auth/middleware.py:15  # ← actual problem',
        '',
        '// What we feed the AI (filtered):',
        'TEST FAILURE: test_login',
        '  Expected: 200, Got: 401',
        '  File: src/auth/middleware.py, line 15',
        '  Root cause hint: auth check rejecting valid token',
    ], sz=10, title="Stack trace → filtered for LLM")

# ══════════════════════════════════════════════════════════════════════════
# 8 — TOOL: Snowflake Schema
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "Tool: inspect_snowflake_schema", sz=28, b=True, c=CYAN)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=CYAN)

txt(sl, Inches(0.8), Inches(1.5), Inches(5.5), Inches(1.2),
    "Same pattern as Postgres, targeting Snowflake's INFORMATION_SCHEMA.\n"
    "AI can see warehouse tables, views, columns, and data types.\n"
    "Critical for teams running production data pipelines on Snowflake.",
    sz=14, c=GRAY)

mono_block(sl, Inches(0.8), Inches(2.9), Inches(5.8), Inches(0),
    [
        '-- Snowflake schema introspection:',
        'SELECT',
        '  t.table_schema,',
        '  t.table_name,',
        '  t.table_type,',
        '  c.column_name,',
        '  c.data_type,',
        '  c.is_nullable,',
        '  c.comment AS column_comment',
        'FROM information_schema.tables t',
        'JOIN information_schema.columns c',
        '  ON t.table_catalog = c.table_catalog',
        '  AND t.table_schema = c.table_schema',
        '  AND t.table_name = c.table_name',
        'WHERE t.table_schema != \'INFORMATION_SCHEMA\'',
        'ORDER BY t.table_schema, t.table_name, c.ordinal_position;',
    ], sz=10, title="Snowflake — INFORMATION_SCHEMA query")

mono_block(sl, Inches(7.0), Inches(1.5), Inches(5.8), Inches(0),
    [
        '// Tool output for LLM:',
        '',
        'WAREHOUSE: ANALYTICS_DB.PUBLIC',
        '',
        'VIEW: daily_revenue',
        '  date          DATE',
        '  revenue       DECIMAL(12,2)',
        '  region        VARCHAR(50)',
        '',
        'TABLE: user_events',
        '  event_id      VARCHAR(36)  PRIMARY KEY',
        '  user_id       INTEGER',
        '  event_type    VARCHAR(100)',
        '  created_at    TIMESTAMP_TZ',
        '',
        '// AI can now write queries against your real data model.',
    ], sz=11, title="Tool output → AI sees Snowflake state")

# Snowflake connection details
txt(sl, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.5),
    "Connects via gosnowflake driver. Reads SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD from env.",
    sz=13, c=DIM)

# ══════════════════════════════════════════════════════════════════════════
# 9 — TOOL: Cloudinary Screenshots
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "Tool: capture_error_screenshot", sz=28, b=True, c=AMBER)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=AMBER)

txt(sl, Inches(0.8), Inches(1.5), Inches(5.5), Inches(1.5),
    "When a UI bug happens, text logs aren't enough.\n"
    "This tool captures a screenshot of the active window/screen,\n"
    "uploads it to Cloudinary, and returns the URL to the AI.\n"
    "AI can now 'see' broken layouts, missing elements, visual regressions.",
    sz=14, c=GRAY)

mono_block(sl, Inches(0.8), Inches(3.2), Inches(5.8), Inches(0),
    [
        'func (t *ScreenshotTool) Execute(ctx context.Context,',
        '    args map[string]any) (any, error) {',
        '',
        '    // macOS screencapture (non-interactive)',
        '    cmd := exec.CommandContext(ctx, "screencapture",',
        '        "-x",  // no camera sound',
        '        "-m",  // monitor (full screen)',
        '        "/tmp/error_screenshot.png")',
        '    if err := cmd.Run(); err != nil {',
        '        return nil, err',
        '    }',
        '',
        '    // Upload to Cloudinary',
        '    url, err := t.cloudinary.Upload(ctx,',
        '        "/tmp/error_screenshot.png",',
        '        "devpulse-errors")',
        '    if err != nil {',
        '        return nil, err',
        '    }',
        '',
        '    return map[string]any{',
        '        "screenshot_url": url,',
        '        "note": "AI can reference this URL for visual context",',
        '    }, nil',
        '}',
    ], sz=10, title="Go — screencapture + Cloudinary upload")

mono_block(sl, Inches(7.0), Inches(1.5), Inches(5.8), Inches(0),
    [
        '// What the AI sees:',
        '',
        'capture_error_screenshot() →',
        '{',
        '  "screenshot_url":',
        '    "https://res.cloudinary.com/devpulse/image/upload/v1/errors/screenshot_2026.png",',
        '  "note": "AI can reference this URL',
        '          for visual context"',
        '}',
        '',
        '// Cursor can now say:',
        '"I can see the sidebar is missing in the',
        ' screenshot. The nav component is not',
        ' rendering. Let me check the CSS."',
    ], sz=10, title="Tool output → AI gets visual context")

txt(sl, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.5),
    "Cloudinary free tier: 25GB storage, 25GB bandwidth/mo. More than enough for hackathon + daily dev use.",
    sz=13, c=DIM)

# ══════════════════════════════════════════════════════════════════════════
# 10 — LIVE DEMO
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "Live demo — the whole loop", sz=28, b=True, c=WHITE)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=GREEN)

txt(sl, Inches(0.8), Inches(1.4), Inches(11.5), Inches(0.5),
    "Scenario: \"The API returns 500, fix it\" — developer does nothing except describe the problem.",
    sz=15, c=AMBER, b=True)

# Chat-style conversation
chat_lines = [
    (">>> Developer:", "The user API is returning 500. Fix it.", WHITE, False),
    (">>> Cursor:", "Let me investigate. I'll check the container logs.", CYAN, False),
    ("", "[Cursor calls get_container_logs(\"user-api\", 50)]", DIM, False),
    ("", "→ ERROR: column \"role\" does not exist in table \"users\"", RED, False),
    ("", "", WHITE, False),
    (">>> Cursor:", "The DB schema is missing a column. Let me check.", CYAN, False),
    ("", "[Cursor calls inspect_db_schema()]", DIM, False),
    ("", "→ users table: id, email, name, created_at (no 'role' column)", AMBER, False),
    ("", "", WHITE, False),
    (">>> Cursor:", "Found it. I'll create the migration and fix the middleware.", CYAN, False),
    ("", "→ Generated: ALTER TABLE users ADD COLUMN role VARCHAR(20)", GREEN, False),
    ("", "→ Fixed: src/auth/middleware.py:15 — role column reference", GREEN, False),
    ("", "", WHITE, False),
    ("", "[Cursor calls run_targeted_tests(\"src/auth/\")]", DIM, False),
    ("", "→ 3 tests passed, 0 failures", GREEN, False),
    ("", "", WHITE, False),
    (">>> Cursor:", "One more thing — let me check if this affects Snowflake.", CYAN, False),
    ("", "[Cursor calls inspect_snowflake_schema()]", DIM, False),
    ("", "→ Snowflake users table also missing 'role' — flagging for sync", AMBER, False),
    ("", "", WHITE, False),
    (">>> Cursor:", "Fixed. Migration, middleware, tests pass, Snowflake flagged.", CYAN, True),
]

for i, (who, what, clr, bold) in enumerate(chat_lines):
    y = Inches(2.0 + i * 0.36)
    if who:
        txt(sl, Inches(0.8), y, Inches(1.5), Inches(0.35), who, sz=12, c=clr, b=bold, font="Consolas")
        txt(sl, Inches(2.3), y, Inches(10), Inches(0.35), what, sz=12, c=clr, b=bold, font="Consolas")
    else:
        txt(sl, Inches(2.3), y, Inches(10), Inches(0.35), what, sz=12, c=clr, b=bold, font="Consolas")

txt(sl, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.5),
    "Total time: ~30 seconds.  Context switches: 0.  Human intervention: 0.",
    sz=14, c=GREEN, b=True)

# ══════════════════════════════════════════════════════════════════════════
# 9 — COMPETITIVE LANDSCAPE
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "What exists vs what we're building", sz=28, b=True, c=WHITE)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=CYAN)

# comparison table
headers = ["Tool / Server", "Docker", "DB Schema", "Snowflake", "Git", "Tests", "Visual", "Status"]
col_widths = [2.2, 0.8, 1.0, 1.0, 0.8, 0.8, 0.8, 1.0]
col_x = [0.8]
for w in col_widths[:-1]:
    col_x.append(col_x[-1] + w)

# header row
rect(sl, Inches(0.8), Inches(1.5), Inches(8.4), Inches(0.4), fill=CYAN)
for i, h in enumerate(headers):
    txt(sl, Inches(col_x[i]), Inches(1.52), Inches(col_widths[i]), Inches(0.35),
        h, sz=10, c=BG, b=True, font="Consolas")

rows = [
    ["mcp-server-docker", "✓", "✗", "✗", "✗", "✗", "✗", "Partial"],
    ["mcp-server-sqlite", "✗", "✓(sqlite)", "✗", "✗", "✗", "✗", "Partial"],
    ["mcp-snowflake-mcp", "✗", "✗", "✓", "✗", "✗", "✗", "Partial"],
    ["mcp-git-context", "✗", "✗", "✗", "✓", "✗", "✗", "Partial"],
    ["DevPulse (ours)", "✓", "✓", "✓", "✓", "✓", "✓", "Full"],
]

row_colors = [GRAY, GRAY, GRAY, GRAY, GREEN]
for r, (row, rc) in enumerate(zip(rows, row_colors)):
    y = Inches(2.0 + r * 0.45)
    bg_fill = SURFACE if r < 4 else RGBColor(0x15, 0x2E, 0x1A)
    rect(sl, Inches(0.8), y, Inches(8.4), Inches(0.42), fill=bg_fill)
    for c, val in enumerate(row):
        clr = rc if val == "✓" or r == 4 else (RED if val == "✗" else GRAY)
        txt(sl, Inches(col_x[c]), y+Inches(0.02), Inches(col_widths[c]), Inches(0.35),
            val, sz=10, c=clr, b=(r==4), font="Consolas")

txt(sl, Inches(0.8), Inches(4.5), Inches(11.5), Inches(1.0),
    "Nobody has built a single MCP server that covers Docker + DB + Snowflake + Git + Tests + Visual.\n"
    "Existing servers are single-purpose. We're the unified layer.\n"
    "Plus Cloudinary integration gives AI something no other server has: the ability to SEE.",
    sz=15, c=GRAY)

# ══════════════════════════════════════════════════════════════════════════
# 10 — TECH STACK + SAFETY
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)
txt(sl, Inches(0.8), Inches(0.4), Inches(6), Inches(0.6),
    "Stack and safety", sz=28, b=True, c=WHITE)
rect(sl, Inches(0.8), Inches(1.1), Inches(3), Pt(2), fill=CYAN)

# left: stack
rrect(sl, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.2), border=CYAN)
txt(sl, Inches(1.0), Inches(1.6), Inches(5.4), Inches(0.4),
    "Built with", sz=16, b=True, c=CYAN)

stack_items = [
    "Go + mcp-go SDK — fast, single binary, easy Docker API integration",
    "Docker Engine API via dockerode — container logs, restart, inspect",
    "pg driver + information_schema queries — Postgres schema introspection",
    "gosnowflake driver — Snowflake INFORMATION_SCHEMA queries",
    "Cloudinary REST API — screenshot upload, error visualization",
    "macOS screencapture — non-interactive window/screen capture",
    "Git CLI subprocess calls — blame, diff, log (no libgit2 dependency)",
    "pytest / jest / vitest via subprocess — run tests without API coupling",
    "stdio transport — zero config, works in any terminal",
]
bullet_list(sl, Inches(1.0), Inches(2.2), Inches(5.4), Inches(4.0),
            stack_items, sz=13, c=GRAY, bc=CYAN)

# right: safety
rrect(sl, Inches(7.0), Inches(1.5), Inches(5.8), Inches(5.2), border=RED)
txt(sl, Inches(7.2), Inches(1.6), Inches(5.4), Inches(0.4),
    "Safety guards", sz=16, b=True, c=RED)

safety_items = [
    "No destructive operations without explicit user confirmation",
    "restart_service requires --confirm flag from human",
    "DB queries are read-only (SELECT only, no mutations)",
    "Git operations never push, never force-push, never amend",
    "Container logs are read-only — we don't exec into containers",
    "All tool calls logged locally for audit trail",
]
bullet_list(sl, Inches(7.2), Inches(2.2), Inches(5.4), Inches(4.0),
            safety_items, sz=13, c=GRAY, bc=RED)

# ══════════════════════════════════════════════════════════════════════════
# 11 — CLOSING
# ══════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(prs.slide_layouts[6]); bg(sl)

txt(sl, Inches(1), Inches(1.5), Inches(11), Inches(1.0),
    "DevPulse MCP", sz=48, b=True, c=WHITE, font="Consolas")
txt(sl, Inches(1), Inches(2.8), Inches(11), Inches(0.7),
    "AI editors can finally see what's actually running.",
    sz=22, c=GRAY)

rect(sl, Inches(1), Inches(3.8), Inches(3), Pt(2), fill=CYAN)

txt(sl, Inches(1), Inches(4.3), Inches(11), Inches(0.5),
    "One server. Any editor. Docker. Postgres. Snowflake. Git. Tests. Screenshots. Done.",
    sz=18, c=CYAN, font="Consolas")

txt(sl, Inches(1), Inches(5.5), Inches(11), Inches(0.5),
    "github.com/your-team/devpulse-mcp", sz=14, c=DIM, font="Consolas")

txt(sl, Inches(1), Inches(6.2), Inches(11), Inches(0.5),
    "Questions?", sz=28, c=WHITE)

# ── Save ─────────────────────────────────────────────────────────────────
out = "/Users/shamina/Desktop/Tmsl/DevPulse_MCP_Pitch.pptx"
prs.save(out)
print(f"Saved: {out}")
