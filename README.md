# Overview

Python monorepo + uv + Vertical Slice Architecture

# Projects
`api` and `transcriber`.

# Execute project

```bash
docker compose --file docker-compose-dev.yaml up --detach
```

```bash
uv run -- poe start-api-dev
```

```bash
docker compose --file docker-compose-dev.yaml down --volumes
```
