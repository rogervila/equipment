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

## Mental Model

An Equipment application has two layers:

1. The framework layer, provided by the `equipment` package.
2. The application layer, generated into your project and owned by you.

The framework layer is intentionally small. It knows how to load configuration, create loggers, create queue drivers, create storage drivers, and create a SQLAlchemy database factory. The application layer decides what the app does with those services.

The generated project is not meant to be a black box. You should edit it. Add services under `app/`, add configuration under `config/`, and add tests under `tests/`. The generated files are a starting contract, not a code generator that needs to own the project forever.

## Request And Process Flow

Most Equipment entry points follow the same flow:

1. Import `app` from `app/__init__.py`.
2. Call `app()` to create or retrieve an application container for the current base path.
3. Read config values from `application.config`.
4. Use framework services such as `application.log()`, `application.storage()`, `application.database()`, or `application.queue()`.
5. Delegate business logic to application services registered on the generated `App` class.

For example, `main.py`, `web.py`, `scheduler.py`, and `queues.py` all start by creating an application context. That keeps scripts, web routes, scheduled jobs, and workers aligned around the same configuration and dependency graph.

## What Equipment Owns

Equipment owns these reusable concerns:

- loading `.env` and `config/` files;
- wiring framework services into a dependency injection container;
- creating log handlers from config;
- selecting sync or Redis queue behavior;
- selecting local or S3 storage behavior;
- creating SQLAlchemy engines and sessions;
- compiling project files for bytecode distribution;
- scaffolding a new project from the maintained template.

Your application owns these concerns:

- domain models and business services;
- database schema design and migrations;
- HTTP routes and request validation;
- queued task functions;
- scheduler definitions;
- deployment-specific environment variables;
- tests for your own behavior.

## What Equipment Does Not Do

Equipment does not replace FastAPI, SQLAlchemy, Alembic, Redis, boto3, or `unittest`. It provides a structure for using those tools consistently. When you need advanced behavior, use the underlying library directly inside your own service layer.

Equipment also does not provide a built-in authentication system, object-relational model base, API router generator, Docker deployment contract, secret manager, production process supervisor, or cloud deployment platform. Those choices stay with the application.

## Good First Changes

After generating a project, common first edits are:

- rename the project in `.env` by changing `APP_NAME`;
- set `APP_ENV=local` for local development;
- replace `app/Inspire.py` with your first domain service;
- register that service in `app/__init__.py`;
- add tests under `tests/`;
- choose whether `web.py`, `queues.py`, or `scheduler.py` are needed;
- remove optional generated dependencies from `pyproject.toml` if a feature will not be used.

## Reading Order

New users should read these pages in order:

1. Installation.
2. Generated Directory Structure.
3. Common Workflows.
4. Configuration.
5. Dependency Injection.
6. The feature pages for the services they plan to use.

LLM coding agents should also read [llms.txt](https://equipment-python.vercel.app/llms.txt) and [llms-full.txt](https://equipment-python.vercel.app/llms-full.txt) before making broad changes, because those hosted files summarize project constraints and common mistakes.

## Maintenance Contract

The repository avoids dependency upgrades inside compatibility or documentation work. Dependency updates should be done as their own change with the full test suite and generated-project workflow validated afterwards.
