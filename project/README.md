# Equipment Project

This project was generated with Equipment. It includes configuration loading, dependency injection, logging, storage, database access, queues, scheduling, tests, and an optional FastAPI entry point.

## Requirements

- Python 3.12, 3.13, or 3.14.
- Windows, macOS, or Linux.
- Optional services depending on configuration: Redis, S3-compatible storage, MySQL, or PostgreSQL.

## Install

```bash
python -m pip install .
```

For development dependencies:

```bash
python -m pip install .[dev]
```

## Run

```bash
python main.py
```

Optional entry points:

```bash
python scheduler.py
python queues.py
python web.py
```

`queues.py` requires Redis. `web.py` uses the FastAPI and Uvicorn dependencies declared in `pyproject.toml`.

## Test

```bash
python -m unittest discover -s tests
```

With coverage installed:

```bash
python -m coverage run -m unittest discover -s tests
python -m coverage report
```

## Configure

- Copy `.env.example` to `.env` for local overrides.
- Edit `config/app.yaml` for application name and environment.
- Edit `config/database.yaml` for SQLAlchemy connection settings.
- Edit `config/log.yaml` for log handlers and JSON formatting.
- Edit `config/queue.yaml` to switch between `sync` and `redis` queues.
- Edit `config/storage.yaml` to switch between `local` and `s3` storage.
- Edit `config/web.yaml` for FastAPI host and port.

Use `pathlib` for application file paths and prefer `python -m ...` commands for cross-platform behavior.
