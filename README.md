# Overview

Project template for Python projects + uv + Vertical Slice Architecture

# Execute project

**Initialize environment:**

```bash
docker compose --file compose-dev.yaml up --detach
```

**Run project:**

> Visual Studio Code -> Run and Debug -> api

(or `uv run -- fastapi dev src/python_template/api/main.py`)

**Destroy environment:**

```bash
docker compose --file compose-dev.yaml down --volumes
```
