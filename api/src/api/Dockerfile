# 0.8.11-python3.12-bookworm-slim
FROM astral/uv@sha256:165703e3c12d7fca3dfa15b2012b98d6e03c261a516d4bd7ca3a956c57c7abce AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-workspace --no-dev
COPY pyproject.toml uv.lock ./
COPY common common
COPY domain domain
COPY api api
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 3.12.11-slim-bookworm
FROM python@sha256:3b2f1b9c9948e9dc96e1a2f4668ba9870ff43ab834f91155697476142b3bc299 AS final

ENV COMMON__ENVIRONMENT=""

RUN adduser --system --no-create-home nonroot
COPY --from=builder --chown=nonroot /app /app
WORKDIR /app
EXPOSE 8000
USER nonroot
CMD [".venv/bin/poe", "start-api-pro"]