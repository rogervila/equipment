---
sidebar_position: 1
---

# Equipment Overview

Equipment is a scaffolding framework for creating Python application projects. It gives a new project a working structure for configuration, dependency injection, logging, storage, database access, queues, scheduling, tests, and optional FastAPI serving.

The goal is to remove the repetitive setup that appears at the beginning of many Python applications while keeping the generated project simple enough to modify. Equipment is not a web framework and it does not force one application architecture. It creates a practical starting point that can support scripts, workers, scheduled jobs, APIs, and internal tools.

## Who Should Use It

Use Equipment when you want:

- a Python project scaffold with common application services already wired;
- a consistent layout for scripts, web entry points, queue workers, and schedulers;
- configuration files that can be driven by environment variables;
- a small dependency injection container for framework and application services;
- a template that works on Windows, macOS, and Linux.

Equipment is less useful when you only need a single-file script, when you already have a strong framework-specific project generator, or when project creation must work offline without a local copy of the template.

## Supported Platforms

- Python 3.12, 3.13, and 3.14.
- Windows, macOS, and Linux.
- CI is configured to test all supported Python versions on all three operating systems.

## Quick Start

```bash
python -m pip install equipment
equipment new my-app
cd my-app
python -m pip install .
python main.py
```

Windows users can use the Python launcher:

```bat
py -3.14 -m pip install equipment
equipment new my-app
cd my-app
py -3.14 -m pip install .
py -3.14 main.py
```

## What Gets Generated

An Equipment project includes:

- `app/` for custom services and scheduler definitions;
- `config/` for YAML and JSON configuration;
- `database/` for SQLite and Alembic migrations;
- `storage/` for local files and logs;
- `tests/` with a `unittest.TestCase` base class and Faker support;
- `main.py`, `queues.py`, `scheduler.py`, and `web.py` entry points;
- `pyproject.toml`, `.env.example`, and `README.md`.

## Core Concepts

- Configuration is loaded from `.env` and `config/*` files.
- The `Equipment` container exposes framework services: `log`, `queue`, `storage`, and `database`.
- The generated `App` class registers application services with `dependency-injector` singletons.
- Queue and storage drivers can be switched through configuration.
- Tests use standard `unittest` discovery, so they run with the Python standard library test runner.

## Maintenance Contract

The repository avoids dependency upgrades inside compatibility or documentation work. Dependency updates should be done as their own change with the full test suite and generated-project workflow validated afterwards.
