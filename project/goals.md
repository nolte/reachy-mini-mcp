# Vision

`reachy-mini-mcp` is the nolte portfolio's Model Context Protocol (MCP) server
for the Reachy Mini robot. It wraps the Pollen Reachy Mini daemon behind a thin
REST interface and exposes it over MCP, so any MCP-capable LLM frontend (Claude
Desktop, Claude Code, Cursor) can read robot state and trigger motion without
generating ad-hoc Python. It ships as a Docker container over stdio transport,
and it writes a per-invocation audit trail. The canonical specification lives in
the `claude-reachy-mini` plugin.

## Outcomes

- **O-1** — MCP clients read Reachy Mini state and trigger its behaviours over a
  stable MCP tool interface, without generating ad-hoc Python. _(audience: MCP clients)_
- **O-2** — Reachy Mini owners and developers control the robot through any
  MCP-capable LLM frontend they already use. _(audience: Reachy Mini owners / developers)_
- **O-3** — the maintainer evolves the exposed tool surface safely, with
  daemon-reachability checks and a per-invocation audit trail. _(audience: Repository maintainer)_
