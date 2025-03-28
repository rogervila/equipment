---
sidebar_position: 1
---

# FastAPI Example

Equipment provides a robust, modular approach to building web applications using FastAPI. This example demonstrates key features and best practices.

## Project Structure Overview

Before diving into the code, let's understand the project structure:

```
project/
│
├── app/                # Core application logic
│   └── __init__.py     # Equipment initialization
│   └── ...             # Application services
├── config/             # Configuration management
│   └── web.yaml        # Web server configuration
│   └── ...             # Other configuration files
└── web.py              # FastAPI server
```

## Basic Setup and Configuration

```python
#!/usr/bin/env python

# Import the core application framework
from app import app

# Import FastAPI and related dependencies
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from uvicorn import Server, Config

# Initialize the Equipment application
# This provides centralized configuration, logging, and core services
app = app()

# Logging configuration - demonstrates Equipment's integrated logging
app.log().info(
    f'''
    Welcome to {app.config.app.name()}

    This file runs a FastAPI server defined in ./config/web.yaml
    host: {app.config.web.host()}
    port: {app.config.web.port()}
    '''
)

# Create FastAPI application with dynamic naming from configuration
name = app.config.app.name()
web = FastAPI(title=name)
```

### Key Concepts
- `app()` initializes Equipment, providing:
  - Centralized configuration management
  - Integrated logging
  - Access to application-wide services
- Configuration is dynamically loaded from YAML files, placed in `config/`
- Logging is pre-configured and easily accessible, and is configurable in `config/log.yaml`

## Route Definition

Equipment comes with a utility to fetch inspiring quotes, which is used in this example.

```python
@web.get("/", response_class=HTMLResponse)
async def landing() -> str:
    # This example uses the Inspire service for dynamic content
    return f'''
        <h1>{name}</h1>
        <hr />
        <p>{app.inspiring().quote()}</p>
    '''
```

### Route Features
- Uses standard FastAPI route decorators
- Demonstrates Equipment's `inspiring()` utility for dynamic content
- Type hints and response class for improved type safety

## Server Initialization

```python
if __name__ == '__main__':
    try:
        # Server configuration from config/web.yaml
        server = Server(Config(
            app='web:web',
            host=str(app.config.web.host()),
            port=int(app.config.web.port()),
        ))
        server.run()
    except KeyboardInterrupt:
        # Graceful shutdown with logging
        app.log().info('Exiting webserver...')
```

### Server Management
- Dynamic host and port configuration
- Graceful shutdown handling
- Integrated logging for server events

## Configuration Example

```yaml
# config/web.yaml
web:
  host: 0.0.0.0
  port: 8000

app:
  name: Equipment Demo
```

### Best Practices
1. Separate configuration from code
2. Use environment-specific settings
3. Centralize application parameters

## Running the Application

```bash
python web.py
```

## Additional Equipment Features
- Automatic dependency injection
- Comprehensive logging and monitoring

**Pro Tip**: Leverage Equipment's modular design to easily extend and customize your web application.
