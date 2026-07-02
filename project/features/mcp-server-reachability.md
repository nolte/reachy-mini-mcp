---
id: F-1
title: MCP server reachability
status: done
roadmap_item: R-1
sprint: 1
created: 2026-07-02
ended: 2026-07-02
verifies_sprint_value: acceptance-1
consistency_check:
  performed_at: 2026-07-02
  agent_version: manual-fallback (retroactive; feature-consistency-reviewer not run cross-repo)
  findings:
    - kind: clean
      target: project/features/
      resolution: proceed
      evidence: "project/features/ empty (first decomposition); no feature-to-feature overlap possible."
    - kind: prior-art
      target: the shipped health_check tool
      resolution: proceed
      evidence: "The MCP server skeleton and health_check tool already exist; F-1 documents the reachability contract, it does not build new tools."
---

## Description

F-1 is the mission-verifying feature for reachy-mini-mcp's minimal MVP: a
reachable MCP server. An MCP client connects to the server over stdio transport
and invokes the `health_check` tool, which probes Pollen daemon reachability and
local audit-log writability. The contract is met when the client receives a
result and the invocation is audited. This holds against the shipped skeleton,
so the feature is recorded `done` as part of the retroactive MVP reconciliation
(issue nolte/claude-shared#262).

## Acceptance criteria

- [x] **acceptance-1** An MCP client connects to the server over stdio and the
  `health_check` tool returns a Pollen-daemon-reachability result. _(This is the
  sprint value verifier.)_
- [x] **acceptance-2** Every tool invocation writes a per-invocation entry to the
  local audit log.
- [x] **acceptance-3** The server ships as a Docker container runnable over stdio
  transport.

## Test hooks

- **acceptance-1** — `health_check` invocation against a running container with a
  reachable daemon — passing (skeleton).
- **acceptance-2** — inspect the audit log after an invocation — passing.
- **acceptance-3** — `docker build` and stdio launch — passing.

## Consistency notes

Retroactive documentation feature: the MCP server skeleton and `health_check`
predate the planning suite. No new implementation is introduced; the feature
exists so the mission's `verifies_via: F-1:acceptance-1` and sprint 1's
`value_statement` resolve to a real acceptance criterion. The behaviour tool
tiers are the post-MVP roadmap item R-2.

## References

- `project/portfolio.yml` capability `reachy-mini-mcp-server`
- `AUDIENCES.md` audiences "MCP clients", "Reachy Mini owners / developers"
- `README.md` (the MCP server skeleton and `health_check` tool)
