---
sidebar_position: 3
---

# Project Directory Structure

## Overview

Equipment provides a meticulously designed, modular project structure that promotes clean code organization, maintainability, and scalability. Each directory and file has a specific responsibility within the application architecture.

## Visual Directory Tree

```text
my-app/
├── app/                  # Application-specific logic
│   ├── __init__.py       # Service definitions and App class
│   ├── Inspire.py        # Example service
│   └── Scheduler.py      # Custom task scheduling
├── config/               # Configuration files (YAML, JSON, INI)
│   ├── app.yaml          # Core application settings
│   ├── database.yaml     # Database connections
│   ├── log.yaml          # Logging configuration
│   ├── queue.yaml        # Queue settings
│   └── storage.yaml      # Storage configuration
├── database/             # Database persistence
│   ├── migrations/       # Alembic migration scripts
│   └── database.sqlite   # Default SQLite database (if used)
├── storage/              # Filesystem API storage
│   ├── app/              # Default local storage directory
│   ├── logs/             # Application log files
│   └── .gitignore        # Keep directory structure
├── tests/                # Test suite
│   ├── __init__.py       # Test configuration and base class
│   └── test_example.py   # Example test cases
├── .env.example          # Template for environment variables
├── .env                  # Local environment variables (git-ignored)
├── main.py               # Main application entry point
├── queues.py             # Queue worker entry point
├── scheduler.py          # Scheduler entry point
├── web.py                # Web server entry point
└── pyproject.toml        # Project metadata and dependencies
```

## Detailed Directory breakdown

### `app/`
**Purpose**: Core Application Logic.
- **`__init__.py`**: Defines the `App` class which inherits from `Equipment`. This is where you register your custom services as singletons.
- **`Inspire.py`**: A sample service demonstrating how to implement business logic.
- **`Scheduler.py`**: Customizes the scheduling logic for your application.

### `config/`
**Purpose**: Configuration Management.
- Supports YAML, JSON, and INI formats.
- Manages settings for all core components (Database, Log, Queue, Storage).
- Supports environment variable interpolation (e.g., `${DB_PASSWORD}`).

### `database/`
**Purpose**: Database Persistence and Migrations.
- **`migrations/`**: Contains Alembic versions and configuration for database schema evolution.

### `storage/`
**Purpose**: Flexible Filesystem API.
- **`app/`**: The base directory for the `Local` storage driver.
- **`logs/`**: Where log files are stored when using the `single` or `daily` log channels.

### `tests/`
**Purpose**: Quality Assurance.
- Uses `pytest` by default.
- Provides a `TestCase` base class that initializes a fresh application context for every test.

## Key Entry Points

### `main.py`
The primary entry point for your application logic. Use this for one-off scripts, batch processing, or demonstrating functionality.

### `scheduler.py`
Starts the background task scheduler. It runs indefinitely, executing tasks defined in `app/Scheduler.py`.

### `queues.py`
Starts a Redis queue worker (using `rq`). Required only if you are using the `redis` queue driver.

### `web.py`
The entry point for a FastAPI web server. Defines your routes and handles HTTP requests.

## Best Practices

- **Keep `app/` clean**: Organize complex logic into subdirectories within `app/`.
- **Use `.env`**: Always use environment variables for sensitive or environment-specific configuration.
- **Test everything**: Place your tests in the `tests/` directory and inherit from the provided `TestCase`.
