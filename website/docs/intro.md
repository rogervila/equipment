---
sidebar_position: 1
---

# Prologue

## What is Equipment?

Equipment is a comprehensive scaffolding framework designed to simplify and streamline Python project development. It provides a robust, flexible foundation that adapts to projects of any scale - from simple scripts to complex enterprise applications.

By providing a pre-configured architecture and a set of core services, Equipment allows you to focus on your business logic rather than boilerplate code and project setup.

## Why Equipment?

- **Zero Configuration**: Get up and running in minutes with a standardized project structure.
- **Batteries Included**: Built-in support for Dependency Injection, SQLite/MySQL/PostgreSQL, Logging, Queues, Scheduling, and Storage.
- **Flexible & Non-opinionated**: Use what you need, ignore what you don't. It fits any development strategy.
- **Scalable**: Start small and grow your project into a large-scale application without changing your fundamental architecture.
- **Modern Tech Stack**: Leverages industry-standard libraries like SQLAlchemy, Alembic, and Redis.

## Key Design Principles

1. **Developer Experience**: Minimize boilerplate code and configuration overhead.
2. **Flexibility**: Support various project types and development strategies.
3. **Scalability**: Grow from small scripts to large applications seamlessly.
4. **Modularity**: Easy integration with other Python tools and frameworks.

## Core Features

### 🔧 Dependency Injection
- Intuitive dependency management using `python-dependency-injector`.
- Support for class-based and function-based dependencies.
- Simplifies object lifecycle management and improves testability.

### 🏗️ Project Initialization
- One-command project creation: `equipment new my-app`.
- Consistent setup across different project types.
- Pre-configured `pyproject.toml`, `.env`, and directory structure.

### 📝 Advanced Logging
- Configurable logging system with multiple channels (console, file, daily, sqlite).
- Support for JSON formatters.
- Environment-specific logging levels.

### ⏰ Task Scheduling
- Built-in task scheduler powered by the `schedule` library.
- Support for periodic and recurring tasks.
- Integrates seamlessly with the queue system.

### 📦 Queue Management
- Support for `sync` (synchronous) and `redis` (asynchronous) queues.
- Asynchronous task processing using `rq`.
- Easy enqueuing of any Python callable.

### 💾 Database Integration
- SQLAlchemy ORM integration with support for multiple providers.
- Automated migrations powered by Alembic.
- Easy-to-use session management.

### 💽 Storage Management
- Filesystem abstraction layer (Local and S3 support).
- Consistent API for file operations.
- Easily extensible for custom storage drivers.

## Getting Started

To start a new project with Equipment:

```bash
# 1. Install Equipment CLI
pip install equipment

# 2. Create a new project directory
equipment new my-app

# 3. Enter the project and install it as an editable package
cd my-app
pip install .

# 4. Run the main entry point
python main.py
```

## 🤝 Community and Support

We're passionate about making Python development easier and more enjoyable. Join our community:
- [GitHub Discussions](https://github.com/rogervila/equipment/discussions)
- [Issue Tracker](https://github.com/rogervila/equipment/issues)
- [Contributing Guidelines](https://github.com/rogervila/equipment/blob/main/CONTRIBUTING.md)

## 📄 License

This project is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).

Equipment icons created by <a href="https://www.flaticon.com/free-icons/toolbox">Freepik - Flaticon</a>
