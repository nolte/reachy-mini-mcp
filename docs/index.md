# reachy-mini-mcp

Model Context Protocol (MCP) server for [Reachy Mini](https://github.com/pollen-robotics/reachy_mini) — a thin REST wrapper around the Pollen daemon, exposed over MCP so any MCP-capable LLM frontend (Claude Desktop, Claude Code, Cursor) can read robot state and trigger motion without generating ad-hoc Python.

The canonical product specification lives in the `claude-reachy-mini` plugin repository under `spec/reachy-mini/mcp-server/`. This site documents the implementation that follows from that spec.

## Status

Initial skeleton. Tier-1 / Tier-2 / Tier-3 tools are not yet implemented — only a `health_check` tool that probes daemon reachability and local audit-log writability.

## Quickstart

```bash
docker build -t reachy-mini-mcp:dev .
docker run --rm -i \
  --network host \
  -v "$HOME/.cache/reachy-mini-mcp:/home/mcp/.cache/reachy-mini-mcp" \
  reachy-mini-mcp:dev
```

See [the README](https://github.com/nolte/reachy-mini-mcp/blob/main/README.md) for MCP-client wiring and environment variables.
