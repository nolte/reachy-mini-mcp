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
READ_TIMEOUT_S = 2.0


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


@mcp.tool()
def get_motor_status() -> dict[str, Any]:
    """Read per-motor positions plus the global motor-control mode (Tier-1 read).

    Combines the daemon's ``/api/motors/status`` (global control mode) and
    ``/api/state/full`` (per-joint positions) into one inventory: up to six
    head joints (Stewart platform; daemon may report ``null`` while idle),
    one body-yaw motor, two antenna motors. Positions are in radians; the
    kinematic head pose is included as a Cartesian fallback.

    Per spec this is a Tier-1 read — no app-lock pre-check, no write-side
    gates. ``effort`` is not exposed by the daemon's REST surface and is
    therefore omitted.
    """
    daemon_url = _daemon_url()
    try:
        mode_response = httpx.get(
            f"{daemon_url}/api/motors/status", timeout=READ_TIMEOUT_S
        )
        mode_response.raise_for_status()
        state_response = httpx.get(
            f"{daemon_url}/api/state/full", timeout=READ_TIMEOUT_S
        )
        state_response.raise_for_status()
    except httpx.HTTPError as exc:
        raise RuntimeError(f"daemon unreachable at {daemon_url}: {exc}") from exc

    control_mode = mode_response.json().get("mode")
    state = state_response.json()

    motors: list[dict[str, Any]] = []
    head_joints = state.get("head_joints")
    if head_joints is not None:
        for index, position in enumerate(head_joints):
            motors.append(
                {"id": f"head_joint_{index}", "group": "head", "position_rad": position}
            )
    body_yaw = state.get("body_yaw")
    if body_yaw is not None:
        motors.append({"id": "body_yaw", "group": "body", "position_rad": body_yaw})
    antennas = state.get("antennas_position")
    if antennas is not None and len(antennas) == 2:
        motors.append(
            {"id": "antenna_left", "group": "antenna", "position_rad": antennas[0]}
        )
        motors.append(
            {"id": "antenna_right", "group": "antenna", "position_rad": antennas[1]}
        )

    return {
        "control_mode": control_mode,
        "motors": motors,
        "head_pose": state.get("head_pose"),
        "timestamp": state.get("timestamp"),
    }
