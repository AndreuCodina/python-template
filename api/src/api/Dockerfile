# 0.8.11-python3.12-bookworm-slim
FROM astral/uv@sha256:8101ad825250a114e7bef89eefaa73c31e34e10ffbe5aff01562740bac97553c AS builder

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
FROM python@sha256:42cf2422587a3dac0e0a3674a4d86f01570d5d7260588f3845f51e6176d8134b AS final

ENV COMMON__ENVIRONMENT=""

RUN adduser --system --no-create-home nonroot
COPY --from=builder --chown=nonroot /app /app
WORKDIR /app
EXPOSE 8000
USER nonroot
CMD [".venv/bin/poe", "start-api-pro"]