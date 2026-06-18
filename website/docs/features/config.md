---
sidebar_position: 1
---

# Configuration

Equipment loads configuration from a project base path. It first loads `.env` when present, then merges files from `config/*.ini`, `config/*.yaml`, and `config/*.json`.

Generated projects use YAML for framework settings and JSON for the example quote data.

## Loading Order

The base path is the directory passed to `app(base_path)` or the current working directory when no base path is provided. Equipment then loads:

1. `.env` from the base path, if it exists.
2. `config/*.ini` files.
3. `config/*.yaml` files.
4. `config/*.json` files.
5. `config.base_path`, which is set to the resolved base path.

The generated app relies on this order so environment variables are available before YAML and JSON config values are read.

## Environment Interpolation

Configuration values can use `${VARIABLE:default}` syntax:

```yaml
app:
  name: ${APP_NAME:Equipment}
  env: ${APP_ENV:local}
```

Set values in `.env` for local development or in the real process environment for production.

The value before the colon is the environment variable name. The value after the colon is the default. If the variable is not set and no default is provided, the loaded value may be empty or unresolved depending on the underlying config loader.

Examples:

```yaml
app:
  env: ${APP_ENV:local}
database:
  connection: ${DB_CONNECTION:sqlite}
web:
  port: ${PORT:8000}
```

Environment values are loaded as strings. Convert them when a library expects another type:

```python
port = int(application.config.web.port())
debug = str(application.config.app.debug()).lower() == "true"
```

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

## Environment Variable Reference

| Variable | Default | Used By | Meaning |
| --- | --- | --- | --- |
| `APP_NAME` | `Equipment` | `config/app.yaml` | Human-readable application name. |
| `APP_ENV` | `local` | `config/app.yaml` | Environment name such as `local`, `testing`, `staging`, or `production`. |
| `LOG_LEVEL` | `debug` | `config/log.yaml` | Python logging level. |
| `LOG_CHANNEL` | `stack` | `config/log.yaml` | Active logging channel. |
| `DB_CONNECTION` | `sqlite` | `config/database.yaml` | Active database connection key. |
| `DB_HOST` | `127.0.0.1` | `config/database.yaml` | MySQL/PostgreSQL host. |
| `DB_PORT` | `3306` or `5432` | `config/database.yaml` | MySQL/PostgreSQL port. |
| `DB_DATABASE` | connection-specific | `config/database.yaml` | SQLite path or database name. |
| `DB_USERNAME` | connection-specific | `config/database.yaml` | MySQL/PostgreSQL username. |
| `DB_PASSWORD` | connection-specific | `config/database.yaml` | MySQL/PostgreSQL password. |
| `DB_CHARSET` | `utf8mb4` | `config/database.yaml` | MySQL charset. |
| `QUEUE_CONNECTION` | `sync` | `config/queue.yaml` | Active queue driver. |
| `REDIS_HOST` | `127.0.0.1` | `config/queue.yaml` | Redis host. |
| `REDIS_PORT` | `6379` | `config/queue.yaml` | Redis port. |
| `REDIS_DB` | `0` | `config/queue.yaml` | Redis database number. |
| `REDIS_USERNAME` | `null` | `config/queue.yaml` | Redis username when required. |
| `REDIS_PASSWORD` | `null` | `config/queue.yaml` | Redis password when required. |
| `FILESYSTEM_DISK` | `local` | `config/storage.yaml` | Active storage disk. |
| `S3_ENDPOINT` | none | `config/storage.yaml` | S3-compatible endpoint. |
| `S3_BUCKET` | none | `config/storage.yaml` | S3 bucket name. |
| `S3_ACCESS_KEY` | none | `config/storage.yaml` | S3 access key. |
| `S3_SECRET_KEY` | none | `config/storage.yaml` | S3 secret key. |
| `S3_REGION` | `auto` | `config/storage.yaml` | S3 region. |
| `S3_PREFIX` | `null` | `config/storage.yaml` | Optional object key prefix. |
| `WEB_HOST` | `0.0.0.0` | `config/web.yaml` | Host passed to Uvicorn. |
| `PORT` | `8000` | `config/web.yaml` | Port passed to Uvicorn. |

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

## Config File Shape

Use a top-level key that matches the filename. This makes the loaded config predictable:

```yaml
# config/billing.yaml
billing:
  currency: ${BILLING_CURRENCY:EUR}
  invoice_prefix: ${BILLING_INVOICE_PREFIX:INV}
```

Access it as:

```python
currency = application.config.billing.currency()
prefix = application.config.billing.invoice_prefix()
```

Nested structures are supported:

```yaml
notifications:
  email:
    enabled: ${EMAIL_ENABLED:false}
    sender: ${EMAIL_SENDER:no-reply@example.test}
```

Access nested values as chained attributes:

```python
sender = application.config.notifications.email.sender()
```

## Environment Profiles

The generated project uses a single config directory with environment interpolation rather than separate `config/local`, `config/production`, and `config/testing` directories. This keeps the project smaller and makes defaults obvious.

A typical local `.env` might be:

```env
APP_ENV=local
LOG_CHANNEL=stack
DB_CONNECTION=sqlite
QUEUE_CONNECTION=sync
FILESYSTEM_DISK=local
```

A production environment might set:

```env
APP_ENV=production
LOG_CHANNEL=console
DB_CONNECTION=postgresql
QUEUE_CONNECTION=redis
FILESYSTEM_DISK=s3
```

Do not commit production secrets. Keep `.env.example` as documentation and inject real values through your deployment platform.

## Testing Config

The generated `tests/TestCase.py` sets `self.app.config.app.env` to `testing`. Tests can also override any config value explicitly:

```python
self.app.config.queue.connection.from_value("sync")
self.app.config.storage.disk.from_value("local")
```

Override config before creating services that depend on those values, because singleton services may cache the first created instance.

## Troubleshooting

Config attribute does not exist:

Check the filename, extension, and top-level key. `config/reports.yaml` should usually define `reports:`.

Environment default is ignored:

Confirm `.env` is located at the app base path and that the process starts from the generated project root. You can also pass a base path explicitly with `app(base_path="/path/to/project")`.

Boolean or integer config behaves like a string:

Cast values before passing them to libraries. Environment variables are text.

## Guidance

- Keep secrets out of committed config files.
- Prefer defaults that let local tests start without external services.
- Keep config file names stable; they become attributes on `application.config`.
- Use strings for environment-derived values and cast at the call site when a library needs `int` or `bool`.
- Add new config files for new application services instead of overloading `app.yaml`.
- Keep `.env.example` synchronized with documented environment variables.
