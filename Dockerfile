# syntax=docker/dockerfile:1.7

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    VIRTUAL_ENV=/app/.venv

WORKDIR /app

COPY requirements.txt ./
RUN uv venv /app/.venv \
 && uv pip install --python /app/.venv/bin/python -r requirements.txt

COPY pyproject.toml README.md ./
COPY src ./src
RUN uv pip install --python /app/.venv/bin/python --no-deps .


FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    XDG_CACHE_HOME=/home/mcp/.cache

RUN groupadd --gid 10001 mcp \
 && useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin mcp \
 && mkdir -p /home/mcp/.cache/reachy-mini-mcp \
 && chown -R mcp:mcp /home/mcp/.cache

WORKDIR /app
COPY --from=builder --chown=mcp:mcp /app/.venv /app/.venv
COPY --chown=mcp:mcp src /app/src

USER mcp

ENTRYPOINT ["python", "-m", "reachy_mini_mcp"]
