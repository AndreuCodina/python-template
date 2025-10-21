# 0.9.4-python3.14-bookworm-slim
FROM astral/uv@sha256:a9cceaa484b002f06f730b886f61172622589ccdf3ccfa801346aa0fb222fb39 AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-workspace --no-dev
COPY pyproject.toml uv.lock ./
COPY src src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# 3.14.0-slim-bookworm
FROM python@sha256:7ef4d5ec10b07d87c54d10941a3460c53b21c567b093e4f0bee56031f6e864f2 AS final

ENV PYTHON_APP_ENVIRONMENT=""

RUN adduser --system --group app
COPY --from=builder --chown=app /app /app
WORKDIR /app
EXPOSE 8000
USER app
CMD [".venv/bin/fastapi", "run", "src/python_template/api/main.py"]