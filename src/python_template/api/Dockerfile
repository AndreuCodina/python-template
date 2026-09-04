# 0.12-python3.14-trixie
FROM astral/uv@sha256:0d7d613acc4bdc9dae1fabd67d30b94887aeab61e215d4a286ce1304a5b90ecf AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 UV_NO_DEV=1
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-workspace
COPY src src
RUN uv sync --locked

# python:3.14-slim-trixie
FROM python@sha256:8edbf9e42c7fb168b9c523718ed907117e6d2e60f5889c0c499bbda3a787da53 AS final
WORKDIR /app
RUN adduser --system --group app
COPY --from=builder --chown=app /app .
USER app
EXPOSE 8080
CMD [".venv/bin/fastapi", "run", "--port", "8080", "src/python_template/api/main.py"]