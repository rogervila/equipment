---
sidebar_position: 1
---

# Configuration Management

The project uses a modular configuration system which supports YAML, JSON and INI files to manage different aspects of the application. Each configuration file is designed to handle a specific component or service, allowing for flexible and environment-aware configuration.

## Configuration Files

### `app.yaml`
Manages core application settings:
- `name`: Application name (defaults to "Equipment")
- `env`: Environment mode (defaults to "local"). This value may be used to determine the application mode (development, production, etc.)

Example:
```yaml
app:
  name: ${APP_NAME:Equipment}
  env: ${APP_ENV:local}
```

### `database.yaml`
Handles database connection configurations:
- Supports multiple database connection types
- Default connection is SQLite
- Configurable database path and connection parameters

Example:
```yaml
database:
  connection: ${DB_CONNECTION:sqlite}

  connections:
    sqlite:
      schema: sqlite
      database: "${DB_DATABASE:database/database.sqlite}"
```

### `log.yaml`
Configures logging settings for the application.

### `queue.yaml`
Manages background task queue configurations.

### `storage.yaml`
Defines file storage and filesystem API settings.

### `web.yaml`
Configures web server parameters.

### `inspiring.json`
Used by `app.inspiring()`

## Configuration Principles

1. **Environment Variables**: Configuration uses environment variable interpolation
2. **Modular Design**: Separate configuration files for different system components
3. **Default Values**: Sensible defaults provided for each configuration
4. **Flexibility**: Easy to override settings for different environments

## Best Practices

- Never commit sensitive information directly to configuration files
- Use environment variables for environment-specific settings
- Keep configuration files clean and well-documented
- Use `.env` files for local development configurations
