# 0.7.3-python3.12-bookworm-slim
FROM ghcr.io/astral-sh/uv@sha256:0178a92d156b6f6dbe60e3b52b33b421021f46d634aa9f81f42b91445bb81cdf AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY api api
COPY domain domain
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 3.12.10-slim-bookworm
FROM python@sha256:31a416db24bd8ade7dac5fd5999ba6c234d7fa79d4add8781e95f41b187f4c9a AS final

ENV COMMON__ENVIRONMENT=""

RUN adduser --system --no-create-home nonroot
COPY --from=builder --chown=nonroot /app /app
WORKDIR /app
EXPOSE 8000
USER nonroot
CMD [".venv/bin/poe", "start-api-pro"]

