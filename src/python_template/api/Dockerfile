# 0.10.2-python3.14-trixie
FROM astral/uv@sha256:a1307beb5bcfc9d4766cf53a20fc1598ccb6da4554419a57060ed6b31a97f265 AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 UV_NO_DEV=1

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-workspace
COPY src src
RUN uv sync --locked

# 3.14.3-slim-bookworm
FROM python@sha256:f0540d0436a220db0a576ccfe75631ab072391e43a24b88972ef9833f699095f AS final

ENV PYTHON_APP_ENVIRONMENT=""

RUN adduser --system --group app
COPY --from=builder --chown=app /app /app
WORKDIR /app
EXPOSE 8000
USER app
CMD [".venv/bin/fastapi", "run", "src/python_template/api/main.py"]