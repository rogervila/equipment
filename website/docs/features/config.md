---
sidebar_position: 1
---

# Configuration Management

Equipment features a robust and modular configuration system that supports **YAML**, **JSON**, and **INI** files. Each component has its own configuration file, promoting a clean separation of concerns and making it easy to manage complex application settings.

## Environment Variable Interpolation

One of the most powerful features of Equipment's configuration is automatic environment variable interpolation. This allows you to keep your configuration files generic while providing environment-specific values via `.env` files or system environment variables.

**Syntax**: `${VAR_NAME:default_value}`

```yaml
app:
  name: ${APP_NAME:My Application}
  debug: ${APP_DEBUG:true}
```

## Core Configuration Files

All configuration files are located in the `config/` directory.

### `app.yaml`
Manages core application settings:
- `name`: The name of your application.
- `env`: The current environment (e.g., `local`, `production`, `testing`).

### `database.yaml`
Handles database connection settings for various providers:

```yaml
database:
  connection: ${DB_CONNECTION:sqlite}

  connections:
    sqlite:
      schema: sqlite
      database: "${DB_DATABASE:database/database.sqlite}"
    mysql:
      schema: mysql+pymysql
      host: ${DB_HOST:localhost}
      port: ${DB_PORT:3306}
      database: ${DB_DATABASE:equipment}
      username: ${DB_USERNAME:root}
      password: ${DB_PASSWORD:root}
      charset: ${DB_CHARSET:utf8mb4}
```

### `log.yaml`
Configures the logging system, including channels and levels.

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
    console:
      stream: ext://sys.stdout
```

### `queue.yaml`
Defines settings for background task processing.

```yaml
queue:
  connection: ${QUEUE_CONNECTION:sync} # Options: sync, redis
  connections:
    redis:
      host: ${REDIS_HOST:127.0.0.1}
      port: ${REDIS_PORT:6379}
      db: ${REDIS_DB:0}
```

### `storage.yaml`
Configures the filesystem abstraction layer.

```yaml
storage:
  disk: ${STORAGE_DISK:local} # Options: local, s3
  disks:
    local:
      root: storage/app
    s3:
      bucket: ${S3_BUCKET}
      # ... s3 specific config
```

## Adding Custom Configuration

You can easily add your own configuration files (e.g., `services.yaml`) to the `config/` directory. Equipment will automatically load them, and you can access them via `app.config.services`.

## Best Practices

1. **Use `.env` for secrets**: Never commit sensitive data (passwords, API keys) to your `config/*.yaml` files. Use environment variables instead.
2. **Provide default values**: Always provide a sensible default in the interpolation syntax to ensure the app can start even if an environment variable is missing.
3. **Modularize**: If your configuration grows large, consider splitting it into smaller, logically grouped files.
