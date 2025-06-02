# 0.7.8-python3.12-bookworm-slim
FROM ghcr.io/astral-sh/uv@sha256:a37c15d1474625eb986ba6b31623a2caae1da3075290bcbbafe22ff51b21de01 AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY api api
COPY domain domain
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 3.12.10-slim-bookworm
FROM python@sha256:0bc836167214f98aca9c9bca7b4c6dc2c2a77f4a29d5029e6561a14706335102 AS final

ENV COMMON__ENVIRONMENT=""

RUN adduser --system --no-create-home nonroot
COPY --from=builder --chown=nonroot /app /app
WORKDIR /app
EXPOSE 8000
USER nonroot
CMD [".venv/bin/poe", "start-api-pro"]

