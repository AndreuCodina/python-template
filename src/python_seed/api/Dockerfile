# 0.8.16-python3.12-bookworm-slim
FROM astral/uv@sha256:190d69899a7a73b22460b2779f85d2d65fddf9bcb05037d4463beaf52310a919 AS builder

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

# 3.12.11-slim-bookworm
FROM python@sha256:3ad2a947749a3eb74acd9e00636ffa0def5aae0bbbd9fa4fff6253e404e2fe15 AS final

ENV COMMON__ENVIRONMENT=""

RUN adduser --system --group app
COPY --from=builder --chown=app /app /app
WORKDIR /app
EXPOSE 8000
USER app
CMD [".venv/bin/poe", "start-api-pro"]