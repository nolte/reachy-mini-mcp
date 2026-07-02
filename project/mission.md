---
mission_statement: "reachy-mini-mcp gives MCP clients and Reachy Mini owners one MCP server that exposes the Pollen Reachy Mini daemon over a stable tool interface, so any MCP-capable LLM frontend can read robot state and trigger motion without generating ad-hoc Python."
relevant_outcomes: [O-1, O-2, O-3]
audiences:
  - MCP clients
  - Reachy Mini owners / developers
  - Repository maintainer
verifies_via: F-1:acceptance-1
time_bound:
  kind: mvp_completion
mvp_status: achieved
created: 2026-07-02
revised_at: null
---

## Statement

`reachy-mini-mcp` gives MCP clients and Reachy Mini owners one MCP server that
exposes the Pollen Reachy Mini daemon over a stable tool interface, so any
MCP-capable LLM frontend can read robot state and trigger motion without
generating ad-hoc Python.

- **Specific** — the statement names *what* (an MCP server wrapping the Pollen
  daemon) and *for whom* (MCP clients, Reachy Mini owners, and the maintainer,
  resolved in `audiences`).
- **Measurable** — `verifies_via: F-1:acceptance-1`: an MCP client connects over
  stdio and the `health_check` tool returns a daemon-reachability result.
- **Achievable** — the minimum viable product is the reachable server skeleton;
  roadmap item R-1 is `mvp: true`, `detail: fine`, `target_sprint: 1`. The
  richer behaviour tools (R-2) are post-MVP.
- **Relevant** — `relevant_outcomes: [O-1, O-2, O-3]`, each resolving to an
  outcome in `project/goals.md`.
- **Time-bound** — `time_bound: { kind: mvp_completion }`; the bound is the
  moment the reachable-skeleton MVP is recorded as achieved.

## Audiences

- **MCP clients** — the MVP delivers a reachable MCP server over stdio transport
  that a client connects to and queries with the `health_check` tool; the richer
  behaviour tools follow post-MVP.
- **Reachy Mini owners / developers** — the MVP delivers a single container they
  run to expose their robot's daemon over MCP, so they drive it from an
  MCP-capable LLM frontend instead of writing ad-hoc Python.
- **Repository maintainer** — the MVP delivers a skeleton with daemon-reachability
  checks and a per-invocation audit trail, so the maintainer can add tool tiers
  on a safe, observable base.

## Verification

The mission is verified by feature **F-1 — MCP server reachability**, acceptance
criterion 1: *"An MCP client connects to the server over stdio and the
`health_check` tool returns a Pollen-daemon-reachability result."* This is the
`verifies_sprint_value` criterion for sprint 0001 and holds against the shipped
skeleton, so the minimal MVP is recorded as `achieved`.

## Source

- **Audience artefact**: `AUDIENCES.md` at the `reachy-mini-mcp` repository root
  (consulted at its current develop tip); the three `audiences` entries are the
  two primary direct-consumer/operator audiences plus the maintainer.
- **Outcomes referenced**: O-1, O-2, O-3 from `project/goals.md`.
- **Authored by**: the `mission-define` cascade (issue nolte/claude-shared#262
  mission-authoring backfill), 2026-07-02. The MVP is modelled as the minimal
  reachable skeleton (already shipped), so R-1 is recorded `status: done` and
  `mvp_status` opens at `achieved`; the behaviour tool tiers are tracked as the
  post-MVP roadmap item R-2 (`mvp: false`).
