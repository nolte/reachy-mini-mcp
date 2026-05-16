# reachy-mini-mcp

[![CI](https://github.com/nolte/reachy-mini-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/nolte/reachy-mini-mcp/actions/workflows/ci.yml)
[![Release Drafter](https://github.com/nolte/reachy-mini-mcp/actions/workflows/release-drafter.yml/badge.svg)](https://github.com/nolte/reachy-mini-mcp/actions/workflows/release-drafter.yml)
[![Docs](https://github.com/nolte/reachy-mini-mcp/actions/workflows/release-cd-deliver-docs.yml/badge.svg)](https://github.com/nolte/reachy-mini-mcp/actions/workflows/release-cd-deliver-docs.yml)
[![Docker](https://github.com/nolte/reachy-mini-mcp/actions/workflows/release-cd-deliver-docker.yml/badge.svg)](https://github.com/nolte/reachy-mini-mcp/actions/workflows/release-cd-deliver-docker.yml)

Model Context Protocol (MCP) server for [Reachy Mini](https://github.com/pollen-robotics/reachy_mini) — a thin REST wrapper around the Pollen daemon, exposed over MCP so any MCP-capable LLM frontend (Claude Desktop, Claude Code, Cursor) can read robot state and trigger motion without generating ad-hoc Python.

**Distribution form:** Docker container, stdio transport.

The canonical specification lives in the `claude-reachy-mini` plugin repo under `spec/reachy-mini/mcp-server/de.md` (German, canonical) and `en.md` (translation). The operational bootstrap counterpart is `spec/claude/mcp-server-bootstrap/de.md`.

## Status

Initial skeleton. Tier-1 / Tier-2 / Tier-3 tools are not yet implemented — only a `health_check` tool that probes daemon reachability and local audit-log writability.

## Build

```bash
docker build -t reachy-mini-mcp:dev .
```

## Run (stdio transport)

```bash
docker run --rm -i \
  --network host \
  -v "$HOME/.cache/reachy-mini-mcp:/home/mcp/.cache/reachy-mini-mcp" \
  reachy-mini-mcp:dev
```

`--network host` is the simplest way to reach a Pollen daemon listening on `127.0.0.1:8000` of the host. On macOS or Windows, replace it with `-e REACHY_MINI_DAEMON_URL=http://host.docker.internal:8000` and drop `--network host`.

## MCP client configuration

Example for Claude Desktop (macOS path: `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "reachy-mini": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--network", "host",
        "-v", "/Users/you/.cache/reachy-mini-mcp:/home/mcp/.cache/reachy-mini-mcp",
        "reachy-mini-mcp:dev"
      ]
    }
  }
}
```

## Environment variables

| Variable | Default | Meaning |
|---|---|---|
| `REACHY_MINI_DAEMON_URL` | `http://127.0.0.1:8000` | Pollen-daemon base URL the server talks to. Per spec, the default must never point at a non-localhost address. |
| `XDG_CACHE_HOME` | `/home/mcp/.cache` (in the container) | Parent of the `reachy-mini-mcp/` audit-log directory. |

## Local development without Docker

```bash
uv sync
uv run python -m reachy_mini_mcp
```
