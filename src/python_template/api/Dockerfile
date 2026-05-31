# 0.11-python3.14-trixie
FROM astral/uv@sha256:337df7a9d2254a1d8542bc77e16d10396b4028edd1cf7ba4358c6821b9da40c9 AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 UV_NO_DEV=1
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-workspace
COPY src src
RUN uv sync --locked

# python:3.14-slim-trixie
FROM python@sha256:c845af9399020c7e562969a13689e929074a10fd057acd1b1fad06a2fb068e97 AS final
WORKDIR /app
RUN adduser --system --group app
COPY --from=builder --chown=app /app .
USER app
EXPOSE 8080
CMD [".venv/bin/fastapi", "run", "--port", "8080", "src/python_template/api/main.py"]