# CLAUDE.md

AI-collaboration conventions, architecture hints, and command entry points for the `reachy-mini-mcp` repository.

## What this repo is

A Model Context Protocol (MCP) server that wraps the Pollen `reachy-mini` daemon's REST surface so MCP-capable LLM frontends (Claude Desktop, Claude Code, Cursor) can read robot telemetry and trigger motion. Distribution form is a Docker container with stdio transport.

## Canonical specifications

This repository implements specs that live elsewhere; do not redefine them here.

- `claude-reachy-mini/spec/reachy-mini/mcp-server/de.md` — canonical product spec for this MCP server (German is canonical; `en.md` is the translation kept in sync).
- `claude-reachy-mini/spec/claude/mcp-server-bootstrap/de.md` — operational bootstrap spec describing host/daemon expectations.
- `claude-shared/spec/project/project-structure/de.md` — repository layout this repo follows.

When the implementation and the specs disagree, the spec wins. Open a PR against the spec repo before silently diverging here.

## Architecture at a glance

- Python 3.12, single-purpose layout: source under `src/reachy_mini_mcp/`.
- Transport: stdio MCP; the server is launched as `python -m reachy_mini_mcp`.
- Outbound: `httpx` against the Pollen daemon at `REACHY_MINI_DAEMON_URL` (default `http://127.0.0.1:8000`, never a non-localhost address by default per spec).
- Audit log: per-invocation JSONL under `${XDG_CACHE_HOME}/reachy-mini-mcp/`.
- Tiered tool surface (per spec): Tier 1 read-only, Tier 2 motion-safe, Tier 3 motion-active. Current state is skeleton — only `health_check` exists.

## Dependency layout

- Runtime dependencies live in `requirements.txt` (not in `pyproject.toml`'s `[project.dependencies]`, per the project-structure spec).
- Development / test dependencies live in `requirements-dev.txt`. The `-r requirements.txt` chaining directive is forbidden by spec — install both files independently.
- `pyproject.toml` carries distribution metadata (`name`, `version`, `authors`, `urls`) and tooling config (`[tool.ruff]`, `[tool.pytest.ini_options]`) only.

## Command entry points

All reproducible commands flow through Taskfile so local and CI behaviour stay in sync.

| Task | Purpose |
|---|---|
| `task install` | Create `.venv` and install runtime + dev deps via `uv pip install -r`. |
| `task lint` | Run `ruff check` + `ruff format --check`. |
| `task test` | Run `pytest`. |
| `task docs` | Build MkDocs site (`mkdocs build --strict`). |
| `task ci` | Aggregate: lint, test, docs. The CI workflow calls this target. |

The Dockerfile invokes `uv pip install -r requirements.txt` directly so the production image carries only runtime deps.

## Environment variables

| Variable | Default | Meaning |
|---|---|---|
| `REACHY_MINI_DAEMON_URL` | `http://127.0.0.1:8000` | Pollen-daemon base URL. Per spec, the default must never point at a non-localhost address. |
| `XDG_CACHE_HOME` | `/home/mcp/.cache` (in the container) | Parent of the `reachy-mini-mcp/` audit-log directory. |

## Working with AI assistants in this repo

- Prefer Taskfile targets over ad-hoc commands.
- Never write Runtime dependencies into `[project.dependencies]`; the project-structure spec forbids the duplication.
- Touching the daemon-routing surface (`server.py`) requires reviewing the canonical product spec first.
- Source files belong under `src/reachy_mini_mcp/`; tests under `tests/` mirroring the source tree. Never leave Python files loose at the repository root.
