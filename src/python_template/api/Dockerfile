# 0.9.16-python3.14-bookworm-slim
FROM astral/uv@sha256:95b472508fed5e3c78db1d6b69022a4fb5c4c443c0478943dc78946ae200990a AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0 UV_NO_DEV=1

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-workspace
COPY pyproject.toml uv.lock ./
COPY src src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# 3.14.2-slim-bookworm
FROM python@sha256:1f3bc1dcbdc23f54cf2e9a5a8428db4a5f28c53636dec4964c7ae35eb1ebd192 AS final

ENV PYTHON_APP_ENVIRONMENT=""

RUN adduser --system --group app
COPY --from=builder --chown=app /app /app
WORKDIR /app
EXPOSE 8000
USER app
CMD [".venv/bin/fastapi", "run", "src/python_template/api/main.py"]