# 0.7.19-python3.12-bookworm-slim
FROM astral/uv@sha256:5778d479c0fd7995fedd44614570f38a9d849256851f2786c451c220d7bd8ccd AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY api api
COPY domain domain
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 3.12.11-slim-bookworm
FROM python@sha256:4600f71648e110b005bf7bca92dbb335e549e6b27f2e83fceee5e11b3e1a4d01 AS final

ENV COMMON__ENVIRONMENT=""

RUN adduser --system --no-create-home nonroot
COPY --from=builder --chown=nonroot /app /app
WORKDIR /app
EXPOSE 8000
USER nonroot
CMD [".venv/bin/poe", "start-api-pro"]

