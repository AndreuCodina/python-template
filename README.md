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

# Reasonings

## .env files

**Key points:**

- We store settings in .env files.
- There's a .env.{environment} file for each environment (Local, Development, Staging, Production).
- There's a .env file for common settings.
- If a setting is in both .env and .env.{environment}, the one in .env.{environment} takes precedence.

The typical is to save .env files in the root of the project, but due to some popular tools and libraries (Jupyter, FastAPI, Docker Compose...) load the file `.env` automatically (and an application has its own order, such as giving priority to the current environment, environment variables or a secret store), then we need to store them in another location (in this case, in the "api" folder) and give `ApplicationSettings` the path to the files.

Note: Renaming `.env` to `.env.Common` in the root isn't better because if your notebook isn't in the root, you have to specify the path in `ApplicationSettings` anyway, and `Common` can be confusing because it's not an environment.