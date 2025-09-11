# Overview

Python archetype + uv + Vertical Slice Architecture

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
