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

# Settings and .env files

The API must be deployed to several environments (development, staging, production...), but each company uses different environments (from one to any number), so the API is the only one that knows the number of environments and their names.
Then, each environment has its own settings (e.g., the logging level or URL of an external service may vary between environments).

So, we'll use this rules to store settings:
- A `.env` file for common settings.
- A `.env.{environment}` file for each environment.
- If a setting is in both `.env` and `.env.{environment}`, the one in `.env.{environment}` takes precedence.

Regarding the location of those files, the typical is to save `.env` files in the root of the project, but due to some popular tools and packages (Jupyter, FastAPI, Docker Compose...) load automatically and exclusively the file `.env`, ignoring the environments and the priority order defined by the API (e.g., `.env.{environment}` has priority over `.env` because it's the current environment), then we need to store the `.env` files in another location (in this case, in the `api` folder) and give the API the responsibility of loading them, taking into account the environment name.