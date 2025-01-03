---
sidebar_position: 1
---

# Intro

Equipment is a scaffold project focused on the developer experience. Its goal is to avoid repeating basic application setups like handling configuration files or configuring database connections.

Equipment scales with your project. It does not force you to follow any specific development strategy, so it can be used with simple scripts and big applications.

Equipment is simple to extend and modify, which makes it very flexible to fit any project requirement. It can be easily integrated with other Python frameworks and tools.

Developers with any Python skills can work with Equipment. Do not hesitate to [reach us](https://github.com/rogervila/equipment/discussions) to provide feedback, raise issues, and collaborate with the project.

### Dependency Injection
- Easy dependency injection for building robust and maintainable applications
- Supports both class-based and function-based dependencies

### Project Initialization
- Easy project creation with a standardized template
- Quick setup for new Python projects by running a single command: `equipment new my-app`

### Logging Management
- Flexible logging configuration
- Multiple log channels and formatters
- Simple logging API for easy implementation

### Scheduling
- Built-in task scheduler
- Support for periodic and recurring tasks
- Seamless integration with queue systems

### Queue Management
- Supports both synchronous and Redis-based queues
- Asynchronous task processing
- Easy task enqueuing and scheduling

### Database migrations and ORM
- SQLAlchemy integration
- Multiple database driver support
- Built-in migration support via Alembic

### Storage Management, either Local or Cloud
- Filesystem abstraction layer
- Local storage driver
- Extensible storage configuration

## Quick Start

Equipment project includes a class that generates inspiring quotes as an example.
It uses the Singleton pattern to ensure that only one instance of the class exists, and a configuration file managed by Equipment.

### Installation
```bash
# Install Equipment
pip install equipment pipenv

# Generate a new project
equipment new my-app

# Install dependencies
cd my-app && pipenv install
```

### Usage

By default, equipment generates various entrypoints for the project.
- **main.py**: The main entrypoint for the application. It includes examples of how to use Equipment.
- **scheduler.py**: The entrypoint for the task scheduler.
- **queues.py**: The entrypoint for the queue system, using either Redis or synchronous queues.
- **web.py**: The entrypoint for the web server, based on FastAPI.

```bash
cd my-app

# Run the main script
py main.py

# Run the scheduler
py scheduler.py

# Enqueue tasks
py queues.py

# Run the web server
py web.py
```

## Under the hood

Equipment uses popular libraries and frameworks to avoid reinventing the wheel and provide a solid foundation for building robust and maintainable applications:

- [Dependency Injector](https://python-dependency-injector.ets-labs.org/) as container service
- [SQLAlchemy](https://www.sqlalchemy.org/) as ORM
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations
- [Redis](https://redis.io/) as queue driver
- [FastAPI](https://fastapi.tiangolo.com/) as web framework
- [Schedule](https://schedule.readthedocs.io/en/stable/) as task scheduler

## License

This project is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).

Equipment icons created by <a href="https://www.flaticon.com/free-icons/toolbox">Freepik - Flaticon</a>

## Author

[Roger Vilà](https://github.com/rogervila)
