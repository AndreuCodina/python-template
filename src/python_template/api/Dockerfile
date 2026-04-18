# 0.11.5-python3.14-trixie
FROM astral/uv@sha256:8459828f9db7128e6676cbe30aeb7a36aa2f5af3afc89276ecb2bf6cb8af12c0 AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 UV_NO_DEV=1
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-workspace
COPY src src
RUN uv sync --locked

# 3.14.4-slim-bookworm
FROM python@sha256:336220baf4dc02a9da56db1720ce6d248aa7c62a0445af0ea1876ae76cc99bed AS final
WORKDIR /app
RUN adduser --system --group app
COPY --from=builder --chown=app /app .
USER app
EXPOSE 8080
CMD [".venv/bin/fastapi", "run", "--port", "8080", "src/python_template/api/main.py"]