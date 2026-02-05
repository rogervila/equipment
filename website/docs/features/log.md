---
sidebar_position: 3
---

# Logging System

Equipment provides a robust and flexible logging system built on top of the standard Python `logging` module. It features multiple channels, custom formatters (including JSON), and environment-aware configuration.

## Configuration

Logging is configured in `config/log.yaml`.

```yaml
log:
  level: ${LOG_LEVEL:debug}
  channel: ${LOG_CHANNEL:stack}

  channels:
    stack:
      channels: [single, console]
    single:
      filename: storage/logs/app.log
      formatter: json
    daily:
      filename: storage/logs/daily.log
      formatter: json
      when: midnight
      interval: 1
      backupCount: 7
    console:
      stream: ext://sys.stdout
    sqlite:
      filename: database/logs.sqlite
      table_name: app_logs

  formatters:
    json:
      format: "%(asctime)s %(levelname)s %(name)s %(message)s"
      indent: null
```

## Logging Channels

### `stack`
Allows you to log to multiple channels simultaneously. Useful for logging to a file and the console at the same time.

### `single`
Logs all messages to a single file.

### `daily`
Automatically rotates the log file every day (or other configured interval), keeping a specified number of backups.

### `console`
Logs messages directly to the standard output (STDOUT).

### `sqlite`
Logs messages into a SQLite database table. This is very useful for building custom log viewers or searching logs with SQL.

## Log Levels

Standard Python log levels are supported:
- `app.log().debug()`
- `app.log().info()`
- `app.log().warning()`
- `app.log().error()`
- `app.log().critical()`

## JSON Formatters

Equipment makes it easy to output logs in JSON format, which is essential for modern log management systems like ELK or Datadog.

```yaml
# config/log.yaml
formatters:
  json:
    format: "%(asctime)s %(levelname)s %(name)s %(message)s"
    indent: null # Set to an integer for pretty-printing
```

## Usage Example

```python
from app import app

app = app()

# Simple logging
app.log().info("Application started")

# Logging with context (if using JSON formatter, these will be root fields)
app.log().error("Failed to connect to API", extra={"api_url": "https://api.example.com"})

# Logging exceptions
try:
    1 / 0
except Exception as e:
    app.log().error("Calculation error", exc_info=True)
```

## Best Practices

1. **Use appropriate levels**: Don't use `info` for debugging messages. Use `debug` instead.
2. **Don't log secrets**: Never log passwords, API keys, or personally identifiable information (PII).
3. **Use JSON for production**: Standardize your production logs with JSON for easier parsing and searching.
4. **Log Context**: Use the `extra` parameter to provide additional structured data with your logs.
