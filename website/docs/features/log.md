---
sidebar_position: 3
---

# Logging

Equipment builds logging on top of the Python standard library. `LoggerFactory` reads `config/log.yaml`, creates handlers, and exposes familiar methods such as `debug`, `info`, `warning`, `error`, and `critical` through `application.log()`.

Use the logger from scripts, services, web routes, queue jobs, and scheduled tasks. Application code should not need to know whether logs go to stdout, a file, a rotating file, or SQLite. That is a configuration decision.

## Configuration

```yaml
log:
  level: ${LOG_LEVEL:debug}
  channel: ${LOG_CHANNEL:stack}

  channels:
    stack:
      channels:
        - single
        - console

    single:
      formatter: json
      filename: 'storage/logs/app.log'

    daily:
      formatter: json
      filename: 'storage/logs/app.log'
      when: 'midnight'
      interval: 1
      backupCount: 7

    console:
      formatter: null
      stream: null

    sqlite:
      filename: 'storage/logs/app.sqlite'
      table_name: logs

  formatters:
    json:
      format: '%(message)s %(asctime)s %(levelname)s %(levelno)d %(pathname)s %(lineno)d'
      indent: null
```

## Channels

| Channel | Behavior | Typical Use |
| --- | --- | --- |
| `stack` | Sends one log record to multiple configured channels. | Local development where console and file logs are both useful. |
| `single` | Writes to one file. | Small deployments or local debugging. |
| `daily` | Writes to a timed rotating file. | Single-server deployments where local files are retained briefly. |
| `console` | Writes to standard output or configured stream. | Containers, PaaS, CI, and production log collection. |
| `sqlite` | Writes to a SQLite table. | Local inspection or small internal tools. |
| `null` | Emits no visible logs. | Tests or intentionally quiet scripts. |

Set `LOG_CHANNEL=null` to use a null handler.

## Channel Selection

| Environment | Suggested Channel | Why |
| --- | --- | --- |
| Unit tests | `null` or `NullLogger` override | Avoid noisy output and file locks. |
| Local scripts | `stack` | See output immediately and retain a local log file. |
| Docker or PaaS | `console` | Let the platform collect logs. |
| One VM | `daily` | Keep rotating local files without extra infrastructure. |
| Debugging SQLite logging | `sqlite` | Query logs with SQL locally. |

## Usage

```python
from app import app

application = app()

application.log().info("Application started")
application.log().warning("Cache miss", extra={"key": "homepage"})

try:
    raise RuntimeError("example")
except RuntimeError:
    application.log().error("Operation failed", exc_info=True)
```

## Log Levels

- `debug`: detailed developer diagnostics.
- `info`: normal operational lifecycle events.
- `warning`: unexpected but recoverable situations.
- `error`: failed operation that needs attention.
- `critical`: severe failure that may require immediate intervention.

Avoid using `error` for expected validation failures. Reserve high-severity logs for conditions that operators should investigate.

## Structured Context

Use `extra` for stable, machine-readable context:

```python
application.log().info(
    "Invoice created",
    extra={"invoice_id": invoice_id, "customer_id": customer_id},
)
```

When a JSON formatter is active, extra fields can be included by log processors depending on formatter configuration. Do not log secrets, access tokens, passwords, private keys, or personally identifiable information.

## JSON Formatting

The generated formatter includes message, timestamp, level, path, and line number:

```yaml
formatters:
  json:
    format: '%(message)s %(asctime)s %(levelname)s %(levelno)d %(pathname)s %(lineno)d'
    indent: null
```

Useful `LogRecord` fields include `message`, `asctime`, `levelname`, `levelno`, `pathname`, `lineno`, `name`, `module`, `funcName`, `process`, and `threadName`.

## File Handlers

File-based handlers expect their parent directories to exist. The generated project includes `storage/logs/` for this reason.

```yaml
single:
  formatter: json
  filename: 'storage/logs/app.log'
```

If you change the log path, create the directory before the application starts.

## SQLite Logging

The `sqlite` channel writes records to a SQLite database file:

```yaml
sqlite:
  filename: 'storage/logs/app.sqlite'
  table_name: logs
```

SQLite logging is useful for local inspection but is not a high-volume production logging system. For production, prefer console JSON logs and let the platform collect them.

## Testing Logs

Tests can override logging with `NullLogger`:

```python
from equipment.Log.NullLogger import NullLogger

self.app.log.override(NullLogger())
```

Tests that assert file logs should close handlers before reading or deleting files. This matters on Windows because open file handles can block cleanup.

## Troubleshooting

No logs appear:

Check `LOG_CHANNEL`, `LOG_LEVEL`, and whether the app is running from the expected base path. `LOG_CHANNEL=null` intentionally disables output.

File log is not created:

Confirm the parent directory exists and the process has write permission.

Duplicate log lines appear:

Check whether custom code has added handlers to Python loggers. Equipment clears handlers when creating its logger, but direct logger modifications can still create duplicates.

JSON output is missing fields:

Update `formatters.json.format` to include the fields you need.

## Guidance

- Do not log secrets, credentials, tokens, or personally identifiable information.
- Use `stack` locally when you want both console and file output.
- Use JSON in production when logs are collected by another system.
- Ensure directories such as `storage/logs` exist before file logging.
- Use `extra` for IDs and stable attributes.
- Keep log volume reasonable in scheduled jobs and queues.
- Run logging handler tests before upgrading `python-json-logger` or `python_sqlite_log_handler`.
