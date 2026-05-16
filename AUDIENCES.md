# Audiences — reachy-mini-mcp

<!--
Produced via the `audience-identify` skill, following
spec/project/audience-identification/.
Do not add audiences without first declaring the bounded context below.
-->

## Bounded context

`reachy-mini-mcp` is a local MCP server process (distribution: Docker container,
stdio transport) that exposes a bounded tool inventory over the Model Context
Protocol and routes internally through the **REST API of the Pollen
`reachy-mini` daemon**. Tools are organised in three tiers (Read / Write /
Lifecycle). The canonical product spec lives in the `claude-reachy-mini`
plugin (`spec/reachy-mini/mcp-server/de.md`) — this repository is the
implementation, not the spec.

**Inside the context:**

- The MCP server process itself (source under `src/reachy_mini_mcp/`).
- Tool routes to the daemon, audit log, health check.
- Distribution as a Docker image plus the `.mcp.json` client configuration.
- Reproducibility surface: `Taskfile`, `requirements*.txt`, `pyproject.toml`,
  the CI/CD workflows under `.github/workflows/`.

**Outside the context:**

- The Pollen daemon itself — external REST source, this server only consumes it.
- The `reachy_mini` Python SDK — the MCP server never imports it directly.
- LLM frontends (Claude Desktop, Claude Code, Cursor) — they *consume* the
  server but are not part of its surface.
- Motion composition, choreographies, Hugging-Face app publishing — owned by
  other plugin skills and apps.
- Remote / multi-user operation — explicitly out of scope for v1; the server
  binds localhost-only by default.
- The specs themselves — they live in the `claude-reachy-mini` plugin repo.

## Audiences

Each entry: label, relationship category, interaction surface, expectation,
open questions, `confirmed` or `assumed`, criticality (primary / secondary /
peripheral). Categories marked `none` carry a one-line reason.

### Direct consumers

- **MCP clients** — _category_: direct-consumer · _surface_: stdio MCP
  protocol · _expects_: three-tier tool inventory (Read / Write / Lifecycle),
  MCP-conformant error responses, stable tool names across server versions ·
  _status_: `assumed` · _criticality_: primary
  - Examples: Claude Desktop, Claude Code, Cursor, custom MCP clients.
  - Open questions: which clients have actually been exercised end-to-end
    against this server? Any client-specific quirks (e.g. tool-schema-cache
    invalidation) that warrant per-client guidance?

### Operators

- **Reachy Mini owners / developers** — _category_: operator · _surface_:
  Docker CLI, `.mcp.json` configuration, `REACHY_MINI_DAEMON_URL`
  environment variable · _expects_: reproducible container setup, clear
  daemon-URL convention, readable audit logs under
  `${XDG_CACHE_HOME}/reachy-mini-mcp/` · _status_: `assumed` ·
  _criticality_: primary
  - Open questions: do operators run the daemon on the same host as the
    MCP server, or remotely? The spec defaults to localhost — what fraction
    of operators end up needing the mDNS Wireless override
    (`http://reachy-mini.local:8000`)?
- **Pollen daemon operator** — _category_: operator · _surface_: the daemon's
  REST API on the daemon host · _expects_: that the MCP server is a
  well-behaved consumer that does not overload the daemon and respects the
  app-lock contract · _status_: `assumed` · _criticality_: secondary
  - Often the same physical person as the Reachy Mini owner, but the role
    separation matters when the daemon is deployed by a different actor
    than the MCP-server operator.
  - Open questions: should the server emit any rate-limiting telemetry the
    daemon operator can consume?

### Contributors / maintainers

- **Repository maintainer** — _category_: contributor · _surface_: source
  code, CI/CD, release workflow · _expects_: spec-conformant implementation,
  green quality gate (`task ci`), clear Conventional-Commits history,
  release-drafter-compatible PR titles · _status_: `assumed` ·
  _criticality_: primary
  - Currently: `nolte`.
  - Open questions: when do additional maintainers join? A `MAINTAINERS.md`
    or `CODEOWNERS` policy is not in scope today.
- **`claude-reachy-mini` plugin maintainer** — _category_: contributor ·
  _surface_: cross-repo spec PRs against
  `spec/reachy-mini/mcp-server/{de,en}.md` · _expects_: that this
  implementation follows the spec and that drift is surfaced via a spec PR,
  not silent divergence here · _status_: `assumed` · _criticality_: secondary
  - Open questions: what's the agreed cadence for syncing spec changes into
    this implementation? Is there a formal "spec-bumps-this-repo" trigger?

### Governing parties

- **Pollen Robotics** — _category_: governing-party · _surface_: the daemon's
  documented REST contract · _expects_: that this MCP server only calls
  documented endpoints and synchronises with their release cadence on
  breaking changes · _status_: `assumed` · _criticality_: primary
  - Open questions: does Pollen have plans for an official MCP server? If
    yes, this project should coordinate to avoid two competing servers.
- **Anthropic / MCP spec maintainers** — _category_: governing-party ·
  _surface_: the Model Context Protocol specification · _expects_: protocol
  conformance (request/response shape, error format, tool schema) ·
  _status_: `assumed` · _criticality_: primary
  - Open questions: how does this server signal its capability version in
    the MCP handshake when tool schemas evolve?

### Indirect audiences

- **LLM end users** — _category_: indirect · _surface_: the chat UI of their
  MCP frontend; never the server directly · _expects_: that tool calls are
  safe and predictable; they do not know this server exists by name ·
  _status_: `assumed` · _criticality_: secondary
  - Open questions: how should consent for motion-active (tier-3) tools
    propagate from the chat UI back to the operator? Out of scope for v1.
- **Reachy Mini hardware (safety boundary)** — _category_: indirect ·
  _surface_: the physical consequences of tool calls (motor moves, motor
  enable/disable, lifecycle transitions) · _expects_: pose-range validation
  against `control-surface`, safe-torque wrapping around motor toggles,
  audit trail per invocation · _status_: `assumed` · _criticality_: primary
  - This is the load-bearing safety audience: it is not a person, but its
    needs gate every tier-2/3 tool.
  - Open questions: should hardware-emergency-stop integration be exposed
    as its own tier-3 tool, or stay implicit in the daemon's behaviour?

## Open questions (cross-cutting)

- Platform coverage: which of Wireless / Lite / Simulation has actually been
  validated end-to-end with this server? The canonical spec demands a
  per-platform tool-availability matrix; until that's exercised, the
  per-platform audience-need assumptions stay open.
- Spec-drift mechanism: there is no formal mechanism today that prevents
  this implementation from silently diverging from
  `spec/reachy-mini/mcp-server/`. Until a spec-drift audit job runs in CI,
  contributor / maintainer expectations rest on review discipline.
- Remote-mode policy: if anyone opens the server on `0.0.0.0`, the audience
  landscape shifts (auth, multi-user). Spec marks this as out of scope v1;
  the audience list should be re-run via the `revisit` operation before
  enabling any non-localhost default.

## Revisit triggers

- A non-localhost default or `0.0.0.0` bind is enabled — adds multi-user,
  remote-network, and auth-governance audiences.
- A new MCP frontend is officially supported with client-specific behaviour
  — direct-consumer surface diversifies.
- The Pollen daemon ships a breaking REST change — governing-party
  expectations and operator migration paths shift.
- Hugging-Face publishing, cloud deployment, or any non-local distribution
  enters scope.
- Additional hardware targets (e.g. Reachy 2) become supported — hardware
  safety-boundary audience splits per platform.
- A maintainer policy file (`MAINTAINERS.md`, `CODEOWNERS`) is introduced —
  contributor audience needs explicit listing.
