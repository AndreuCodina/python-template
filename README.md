# Overview

Python monorepo + uv + Vertical Slice Architecture

# Projects

## API

RESTful API.

```bash
uv run -- fastapi dev api/src/api/main.py
```

```bash
docker build \
    --file api/src/api/Dockerfile \
    --tag python-monorepo:0.1.0 \
    --platform=linux/amd64 \
    .
```

```bash
docker run \
    --publish 8000:8000 \
    --env COMMON__ENVIRONMENT=Development \
    python-monorepo:0.1.0
```

# Transcriber

Audio transcriber reading from a queue.