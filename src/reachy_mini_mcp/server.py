"""Reachy Mini MCP server — minimal skeleton.

Tracks ``spec/reachy-mini/mcp-server/de.md`` in the ``claude-reachy-mini``
plugin repo. This skeleton exposes only the ``health-check`` tool so an MCP
client can confirm server wiring before any tier-2 write. Tier 1 / 2 / 3
tools land in follow-up commits.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

from reachy_mini_mcp import __version__

DEFAULT_DAEMON_URL = "http://127.0.0.1:8000"
HEALTH_CHECK_TIMEOUT_S = 2.0


def _daemon_url() -> str:
    return os.environ.get("REACHY_MINI_DAEMON_URL", DEFAULT_DAEMON_URL).rstrip("/")


def _audit_log_dir() -> Path:
    cache_home = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(cache_home) / "reachy-mini-mcp"


mcp = FastMCP("reachy-mini-mcp")


@mcp.tool()
def health_check() -> dict[str, Any]:
    """Probe Pollen-daemon reachability and local audit-log writability.

    First-contact probe for an MCP client per the spec's "Konsumenten und
    Boundary" section. Returns server version, daemon reachability, and the
    audit-log directory status in one call.
    """
    daemon_url = _daemon_url()
    daemon_status: dict[str, Any]
    try:
        response = httpx.get(
            f"{daemon_url}/api/daemon/status",
            timeout=HEALTH_CHECK_TIMEOUT_S,
        )
        response.raise_for_status()
        daemon_status = {"reachable": True, "status_code": response.status_code}
    except httpx.HTTPError as exc:
        daemon_status = {"reachable": False, "error": str(exc)}

    audit_dir = _audit_log_dir()
    try:
        audit_dir.mkdir(parents=True, exist_ok=True)
        probe = audit_dir / ".write-probe"
        probe.touch()
        probe.unlink()
        audit_status: dict[str, Any] = {"writable": True, "path": str(audit_dir)}
    except OSError as exc:
        audit_status = {"writable": False, "path": str(audit_dir), "error": str(exc)}

    return {
        "server_version": __version__,
        "daemon": {"url": daemon_url, **daemon_status},
        "audit_log": audit_status,
    }
