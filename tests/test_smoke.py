"""Smoke tests that keep the CI gate honest before real tier-1 tests land."""

from __future__ import annotations

import os
from unittest.mock import patch

from reachy_mini_mcp import __version__, server


def test_package_exposes_version() -> None:
    assert isinstance(__version__, str)
    assert __version__ != ""


def test_daemon_url_defaults_to_localhost() -> None:
    with patch.dict(os.environ, {}, clear=True):
        assert server._daemon_url() == "http://127.0.0.1:8000"


def test_daemon_url_honours_environment_override() -> None:
    with patch.dict(os.environ, {"REACHY_MINI_DAEMON_URL": "http://10.0.0.5:8000/"}):
        assert server._daemon_url() == "http://10.0.0.5:8000"


def test_audit_log_dir_uses_xdg_cache_home(tmp_path) -> None:
    with patch.dict(os.environ, {"XDG_CACHE_HOME": str(tmp_path)}):
        assert server._audit_log_dir() == tmp_path / "reachy-mini-mcp"
