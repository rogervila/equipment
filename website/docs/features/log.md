---
sidebar_position: 1
---

# Logging System

## Overview

Equipment logging system provides a robust and flexible way to track and record events, errors, and important information throughout the application lifecycle.

## Configuration

Logging is configured through the `log.yaml` configuration file, which offers extensive customization options.

### Global Configuration

```yaml
log:
  level: ${LOG_LEVEL:debug}  # Default log level, can be overridden by environment variable
  channel: ${LOG_CHANNEL:stack}  # Default logging channel
```

### Log Levels

Supported log levels:
- `debug`: Most verbose, detailed diagnostic information
- `info`: General application events
- `warning`: Potential issues
- `error`: Serious problems
- `critical`: Highest severity failures

### Log Channels

Channels define how and where logs are output. Multiple channels can be combined.

#### Available Channels

1. **stack**: Combines multiple channels
   ```yaml
   stack:
     channels:
       - single  # Log to a single file
       - console  # Log to console
       # - etc
   ```

2. **single**: Single file logging
   ```yaml
   single:
     formatter: json  # "null" or "json"
     filename: 'storage/logs/app.log'  # Log file path
   ```

3. **daily**: Rotating daily log files
   ```yaml
   daily:
     formatter: json # "null" or "json"
     filename: 'storage/logs/app.log'
     when: 'midnight'  # Rotate at midnight
     interval: 1       # Rotate daily
     backupCount: 7    # Keep 7 days of logs
   ```

4. **console**: Console logging
   ```yaml
   console:
     formatter: null  # "null" or "json"
     stream: null     # Standard output
   ```

5. **sqlite**: Database logging
   ```yaml
   sqlite:
     filename: 'storage/logs/app.sqlite'  # SQLite database for logs
     table_name: logs  # Table to store logs
   ```

### Formatters

Customize log message formatting:

```yaml
formatters:
  json:
    format: '%(message)s %(asctime)s %(levelname)s %(levelno)d %(pathname)s %(lineno)d'
    indent: null  # JSON indentation
```

## Basic Usage

```py
# Initialize the application
from app import app

app = app()

# Log messages at different levels
app.log().debug('Detailed diagnostic information')
app.log().info('Application started successfully')
app.log().warning('Potential configuration issue detected')
app.log().error('Failed to connect to database')
app.log().critical('Critical system failure')
```

## Environment Configuration

Log configuration can be dynamically set using environment variables:
- `LOG_LEVEL`: Set the default log level
- `LOG_CHANNEL`: Specify the default logging channel

## Best Practices

- Use appropriate log levels
- Avoid logging sensitive information
- Configure log rotation to manage disk space
- Use environment-specific logging configurations

## Troubleshooting

1. Verify log file permissions
2. Check disk space for log files
3. Validate YAML configuration syntax
4. Use console logging for immediate debugging

## Performance Considerations

- Minimize debug logs in production
- Use asynchronous logging for high-performance applications
- Monitor log file sizes and rotation
