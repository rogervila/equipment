---
sidebar_position: 2
---

# Environment Variables

Equipment projects use `.env` and process environment variables to specialize configuration. The generated config files use `${VARIABLE:default}` syntax.

Keep `.env.example` as documentation. Keep real secrets in `.env`, CI secrets, a container orchestrator, or a deployment platform secret store.

## Application Variables

| Variable | Default | Description |
| --- | --- | --- |
| `APP_NAME` | `Equipment` | Human-readable app name used in logs and examples. |
| `APP_ENV` | `local` | Environment name. Common values: `local`, `testing`, `staging`, `production`. |

Example:

```env
APP_NAME=Billing API
APP_ENV=local
```

## Logging Variables

| Variable | Default | Description |
| --- | --- | --- |
| `LOG_CHANNEL` | `stack` | Active logging channel. |
| `LOG_LEVEL` | `debug` | Python log level. |

Common values:

```env
LOG_CHANNEL=stack
LOG_LEVEL=debug
```

Production platform example:

```env
LOG_CHANNEL=console
LOG_LEVEL=info
```

Quiet test example:

```env
LOG_CHANNEL=null
LOG_LEVEL=critical
```

## Database Variables

| Variable | Default | Description |
| --- | --- | --- |
| `DB_CONNECTION` | `sqlite` | Active connection key. |
| `DB_HOST` | `127.0.0.1` | MySQL/PostgreSQL host. |
| `DB_PORT` | `3306` or `5432` | MySQL/PostgreSQL port. |
| `DB_DATABASE` | connection-specific | SQLite file path or database name. |
| `DB_USERNAME` | connection-specific | MySQL/PostgreSQL username. |
| `DB_PASSWORD` | connection-specific | MySQL/PostgreSQL password. |
| `DB_CHARSET` | `utf8mb4` | MySQL charset. |

SQLite local example:

```env
DB_CONNECTION=sqlite
DB_DATABASE=database/database.sqlite
```

MySQL example:

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=equipment
DB_USERNAME=equipment
DB_PASSWORD=equipment
DB_CHARSET=utf8mb4
```

PostgreSQL example:

```env
DB_CONNECTION=postgresql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=equipment
DB_USERNAME=equipment
DB_PASSWORD=equipment
```

## Queue Variables

| Variable | Default | Description |
| --- | --- | --- |
| `QUEUE_CONNECTION` | `sync` | Active queue driver. |
| `REDIS_HOST` | `127.0.0.1` | Redis host. |
| `REDIS_PORT` | `6379` | Redis port. |
| `REDIS_DB` | `0` | Redis database number. |
| `REDIS_USERNAME` | `null` | Redis username when required. |
| `REDIS_PASSWORD` | `null` | Redis password when required. |

Local/test example:

```env
QUEUE_CONNECTION=sync
```

Worker example:

```env
QUEUE_CONNECTION=redis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
```

## Storage Variables

| Variable | Default | Description |
| --- | --- | --- |
| `FILESYSTEM_DISK` | `local` | Active storage disk. |
| `S3_ENDPOINT` | none | S3-compatible endpoint. |
| `S3_BUCKET` | none | Bucket name. |
| `S3_ACCESS_KEY` | none | Access key. |
| `S3_SECRET_KEY` | none | Secret key. |
| `S3_REGION` | `auto` | S3 region. |
| `S3_PREFIX` | `null` | Optional object key prefix. |

Local example:

```env
FILESYSTEM_DISK=local
```

S3 example:

```env
FILESYSTEM_DISK=s3
S3_ENDPOINT=https://s3.example.com
S3_BUCKET=my-app-files
S3_ACCESS_KEY=...
S3_SECRET_KEY=...
S3_REGION=eu-west-1
S3_PREFIX=production
```

## Web Variables

| Variable | Default | Description |
| --- | --- | --- |
| `WEB_HOST` | `0.0.0.0` | Host passed to Uvicorn. |
| `PORT` | `8000` | Port passed to Uvicorn. |

Local example:

```env
WEB_HOST=127.0.0.1
PORT=8000
```

Container/PaaS example:

```env
WEB_HOST=0.0.0.0
PORT=8000
```

## Recommended `.env` Profiles

Local script or web development:

```env
APP_ENV=local
LOG_CHANNEL=stack
LOG_LEVEL=debug
DB_CONNECTION=sqlite
QUEUE_CONNECTION=sync
FILESYSTEM_DISK=local
WEB_HOST=127.0.0.1
PORT=8000
```

Production web process:

```env
APP_ENV=production
LOG_CHANNEL=console
LOG_LEVEL=info
DB_CONNECTION=postgresql
QUEUE_CONNECTION=redis
FILESYSTEM_DISK=s3
WEB_HOST=0.0.0.0
PORT=8000
```

Production worker process:

```env
APP_ENV=production
LOG_CHANNEL=console
LOG_LEVEL=info
DB_CONNECTION=postgresql
QUEUE_CONNECTION=redis
FILESYSTEM_DISK=s3
```

## Type Conversion

Environment variables are text. Convert values before passing them to libraries that need numbers or booleans:

```python
port = int(application.config.web.port())
enabled = str(application.config.feature.enabled()).lower() == "true"
```

## Secret Handling

Never commit real secrets to Git. Do not add secrets to `config/*.yaml`, `README.md`, tests, logs, or LLM docs. Keep `.env.example` realistic but fake.

## Troubleshooting

Variable appears ignored:

Confirm `.env` is in the project base path and the process starts from that directory. Also check whether the variable is already set in the shell or deployment platform.

Variable has wrong type:

Cast explicitly at the call site.

Production uses local settings:

Check deployment environment variables. `.env` files are often not present in production unless explicitly copied.
