# 0.10.7-python3.14-trixie
FROM astral/uv@sha256:e91eb38ed4bdf7e897bc87a2167c299d4fad062115b6a69d86af5f1c439a43c4 AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 UV_NO_DEV=1
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-workspace
COPY src src
RUN uv sync --locked

# 3.14.3-slim-bookworm
FROM python@sha256:f0540d0436a220db0a576ccfe75631ab072391e43a24b88972ef9833f699095f AS final
RUN adduser --system --group app
COPY --from=builder --chown=app /app /app
WORKDIR /app
EXPOSE 8000
USER app
CMD [".venv/bin/fastapi", "run", "src/python_template/api/main.py"]