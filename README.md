# Overview

Python monorepo + uv + Vertical Slice Architecture

# Projects
`api` and `transcriber`.

# Execute project

```bash
docker compose --file docker-compose-dev.yaml up --detach
```

```bash
uv run -- fastapi dev api/src/api/main.py
```

```bash
docker compose --file docker-compose-dev.yaml down --volumes
```
