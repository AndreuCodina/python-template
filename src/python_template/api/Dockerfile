# 0.8.22-python3.13-bookworm-slim
FROM astral/uv@sha256:c4a67221d74ad160ddf4e114804bda0f8dd2d2e1aa5c16e0817cf8530ff8f5f6 AS builder

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

# 3.13.7-slim-bookworm
FROM python@sha256:adafcc17694d715c905b4c7bebd96907a1fd5cf183395f0ebc4d3428bd22d92d AS final

ENV PYTHON_APP_ENVIRONMENT=""

RUN adduser --system --group app
COPY --from=builder --chown=app /app /app
WORKDIR /app
EXPOSE 8000
USER app
CMD [".venv/bin/fastapi", "run", "src/python_template/api/main.py"]