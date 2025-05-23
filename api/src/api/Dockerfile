# 0.7.3-python3.12-bookworm-slim
FROM ghcr.io/astral-sh/uv@sha256:83285c39ee68ed64708fca1495c2d0aad084e9ac02a8910f5180b8e36bcf803a AS builder

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

