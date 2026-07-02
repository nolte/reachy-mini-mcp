# Roadmap

This file is the work queue governed by `spec/project/roadmap/`. Each entry is a
level-3 heading followed by a `yaml` code block (`id`, `title`, `detail`,
`outcomes`, `target_sprint`, `mvp`, `status`, in that order) and a free-text
body. `roadmap-plan` and `roadmap-refine` own the detail level and the status
lifecycle; do not hand-edit those fields here.

Entries carry monotonically increasing IDs starting at `R-1`, never reused.
Outcome IDs (`O-n` in `goals.md`) are an independent counter.

The MVP is deliberately minimal: a reachable MCP server skeleton. R-1 shipped
before the planning suite and is recorded retroactively as `status: done`. The
behaviour tool tiers (R-2) are post-MVP (`mvp: false`) — named so the boundary
between the minimum reachable surface and the richer tool surface stays visible.

## Phase 1 — Reachable MCP server

### R-1 — MCP server skeleton and health check

```yaml
id: R-1
title: MCP server skeleton and health check
detail: fine
outcomes: [O-1]
target_sprint: 1
mvp: true
status: done
```

The MCP server skeleton: a Docker container over stdio transport that an
MCP client connects to, plus a `health_check` tool that probes Pollen daemon
reachability and local audit-log writability. Capability
`reachy-mini-mcp-server` in `project/portfolio.yml`.

## Phase 2 — Behaviour tools (post-MVP)

### R-2 — Tiered behaviour tools

```yaml
id: R-2
title: Tiered behaviour tools
detail: backlog
outcomes: [O-1, O-2]
target_sprint: null
mvp: false
status: proposed
```

The Tier-1 / Tier-2 / Tier-3 behaviour tools that read richer robot state and
trigger motion. Post-MVP: they expand the reachable skeleton into the full
tool surface. Not required to fulfil the minimum mission.
