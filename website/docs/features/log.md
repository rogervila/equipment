---
sidebar_position: 3
---

# Logging

Equipment builds logging on top of the Python standard library. `LoggerFactory` reads `config/log.yaml`, creates handlers, and exposes familiar methods such as `debug`, `info`, `warning`, `error`, and `critical`.

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
```

## Channels

- `stack`: sends each log record to multiple configured channels.
- `single`: writes to one file.
- `daily`: writes to a rotating timed file handler.
- `console`: writes to standard output or the configured stream.
- `sqlite`: writes to a SQLite log table.

Set `LOG_CHANNEL=null` to use a null handler in contexts where no logs should be emitted.

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

## JSON Formatting

The generated config uses `python-json-logger` when a channel has `formatter: json`.

```yaml
formatters:
  json:
    format: '%(message)s %(asctime)s %(levelname)s %(levelno)d %(pathname)s %(lineno)d'
    indent: null
```

## Guidance

- Do not log secrets, credentials, tokens, or personally identifiable information.
- Use `stack` locally when you want both console and file output.
- Use JSON in production when logs are collected by another system.
- Ensure directories such as `storage/logs` exist before file logging.
- Run logging handler tests before upgrading `python-json-logger` or `python_sqlite_log_handler`.
