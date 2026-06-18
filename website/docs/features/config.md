---
sidebar_position: 1
---

# Configuration

Equipment loads configuration from a project base path. It first loads `.env` when present, then merges files from `config/*.ini`, `config/*.yaml`, and `config/*.json`.

Generated projects use YAML for framework settings and JSON for the example quote data.

## Environment Interpolation

Configuration values can use `${VARIABLE:default}` syntax:

```yaml
app:
  name: ${APP_NAME:Equipment}
  env: ${APP_ENV:local}
```

Set values in `.env` for local development or in the real process environment for production.

## Generated Config Files

| File | Purpose |
| --- | --- |
| `config/app.yaml` | Application name and environment. |
| `config/database.yaml` | SQLAlchemy connection selection and database settings. |
| `config/log.yaml` | Log level, channel, handlers, and JSON formatter. |
| `config/queue.yaml` | `sync` or `redis` queue driver settings. |
| `config/storage.yaml` | `local` or `s3` storage disk settings. |
| `config/web.yaml` | FastAPI host and port. |
| `config/inspiring.json` | Example quote data used by `app/Inspire.py`. |

## App Settings

```yaml
app:
  name: ${APP_NAME:Equipment}
  env: ${APP_ENV:local}
```

## Database Settings

```yaml
database:
  connection: ${DB_CONNECTION:sqlite}
  connections:
    sqlite:
      schema: sqlite
      database: "${DB_DATABASE:database/database.sqlite}"
```

MySQL and PostgreSQL examples are present in the generated file. Uncomment or install the matching optional driver in the generated `pyproject.toml` before using them.

## Queue Settings

```yaml
queue:
  connection: ${QUEUE_CONNECTION:sync}
  connections:
    redis:
      host: ${REDIS_HOST:127.0.0.1}
      port: ${REDIS_PORT:6379}
      db: ${REDIS_DB:0}
```

Use `sync` for local development and simple scripts. Use `redis` when work should be processed by `queues.py`.

## Storage Settings

```yaml
storage:
  disk: ${FILESYSTEM_DISK:local}
  disks:
    local:
      path: storage/app
    s3:
      endpoint: ${S3_ENDPOINT}
      bucket: ${S3_BUCKET}
      access_key: ${S3_ACCESS_KEY}
      secret_key: ${S3_SECRET_KEY}
      region: ${S3_REGION:auto}
      prefix: ${S3_PREFIX:null}
```

The local storage key is `path`, not `root`.

## Add Custom Config

Add a new file under `config/`, for example `config/services.yaml`:

```yaml
services:
  api_base_url: ${API_BASE_URL:https://example.test}
```

Then access it through the loaded config:

```python
application = app()
base_url = application.config.services.api_base_url()
```

## Guidance

- Keep secrets out of committed config files.
- Prefer defaults that let local tests start without external services.
- Keep config file names stable; they become attributes on `application.config`.
- Use strings for environment-derived values and cast at the call site when a library needs `int` or `bool`.
