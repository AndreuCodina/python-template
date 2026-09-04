# 0.12-python3.14-trixie
FROM astral/uv@sha256:8b940d3a9d65bed080436972241af2e21c84b5e8c9193f7014ed71479ee795ff AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 UV_NO_DEV=1
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-workspace
COPY src src
RUN uv sync --locked

# python:3.14-slim-trixie
FROM python@sha256:a7fb1e634c4a578f9e0bd6327f11a3cde11b7a9395f48e24360c0988bcc5c2bc AS final
WORKDIR /app
RUN adduser --system --group app
COPY --from=builder --chown=app /app .
USER app
EXPOSE 8080
CMD [".venv/bin/fastapi", "run", "--port", "8080", "src/python_template/api/main.py"]