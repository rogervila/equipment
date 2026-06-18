---
sidebar_position: 3
---

# Generated Directory Structure

`equipment new my-app` creates an application scaffold with runtime code, configuration, tests, and project metadata. The structure is intentionally small so it can be understood before it is customized.

```text
my-app/
├── app/
│   ├── __init__.py
│   ├── Inspire.py
│   └── Scheduler.py
├── config/
│   ├── app.yaml
│   ├── database.yaml
│   ├── inspiring.json
│   ├── log.yaml
│   ├── queue.yaml
│   ├── storage.yaml
│   └── web.yaml
├── database/
│   ├── .gitignore
│   └── migrations/
├── storage/
│   ├── app/
│   └── logs/
├── tests/
│   ├── TestCase.py
│   └── app/test_Inspire.py
├── .coveragerc
├── .editorconfig
├── .env.example
├── .gitignore
├── README.md
├── main.py
├── pyproject.toml
├── queues.py
├── scheduler.py
└── web.py
```

## Application Code

`app/__init__.py` defines the generated `App` container. It inherits from `equipment.Equipment` and registers application services with `dependency-injector` singletons.

`app/Inspire.py` is a small example service that reads quote data from `config/inspiring.json`.

`app/Scheduler.py` defines scheduled tasks for `scheduler.py`.

## File-by-file Reference

| Path | Owned By | Purpose |
| --- | --- | --- |
| `app/__init__.py` | You | Defines the application container and service registrations. |
| `app/Inspire.py` | You | Example service; replace or remove when your own services exist. |
| `app/Scheduler.py` | You | Defines recurring jobs for the scheduler process. |
| `config/app.yaml` | You | App name and environment defaults. |
| `config/database.yaml` | You | SQLAlchemy connection configuration. |
| `config/inspiring.json` | You | Example data for `Inspire`; safe to remove with the example service. |
| `config/log.yaml` | You | Log channels, handlers, levels, and formatters. |
| `config/queue.yaml` | You | Queue driver selection and Redis connection values. |
| `config/storage.yaml` | You | Local/S3 storage driver settings. |
| `config/web.yaml` | You | Host and port used by `web.py`. |
| `database/migrations/` | You | Alembic migration environment and migration versions. |
| `storage/app/` | Runtime | Local storage root for application-managed files. |
| `storage/logs/` | Runtime | Log output directory for file-based handlers. |
| `tests/TestCase.py` | You | Shared test setup with Faker and an application container. |
| `main.py` | You | Script entry point and examples. |
| `queues.py` | You | Redis worker entry point. |
| `scheduler.py` | You | Scheduler process entry point. |
| `web.py` | You | FastAPI entry point. |
| `.env.example` | You | Documented environment variable template. |
| `.env` | Local runtime | Local overrides copied from `.env.example`; keep secrets out of Git. |
| `pyproject.toml` | You | Generated project metadata and dependencies. |
| `README.md` | You | Project-specific instructions for maintainers and users. |

## Configuration

The `config/` directory is loaded by filename and extension. Equipment supports `.ini`, `.yaml`, and `.json` files. The generated project uses YAML for application services and JSON for the example quote list.

Use `${ENV_NAME:default}` syntax to let `.env` or system environment variables override defaults.

## Entry Points

- `main.py`: script entry point and examples for storage, queue, database, and logging.
- `scheduler.py`: starts the schedule loop defined in `app/Scheduler.py`.
- `queues.py`: starts an RQ worker for Redis-backed queues.
- `web.py`: starts the FastAPI example using `config/web.yaml`.

## When To Remove Generated Files

The scaffold includes several optional capabilities. You can remove them when a project does not use them:

- Remove `web.py` and FastAPI/Uvicorn dependencies if the project is not a web app.
- Remove `queues.py` and Redis configuration if the project never uses async workers.
- Remove `scheduler.py` and `app/Scheduler.py` if there are no recurring jobs.
- Remove Alembic dependencies and `database/migrations/` if the project does not own a relational schema.
- Remove `app/Inspire.py` and `config/inspiring.json` after replacing the example service.

When removing a feature, remove its tests, config references, and documentation together. That keeps the project understandable for future humans and LLMs.

## Where To Put New Code

Use `app/` for application code. For a small project, flat files are fine:

```text
app/
├── __init__.py
├── Billing.py
├── Reports.py
└── Scheduler.py
```

For a larger project, organize by domain or responsibility:

```text
app/
├── billing/
│   ├── __init__.py
│   ├── models.py
│   ├── repository.py
│   └── service.py
├── notifications/
│   ├── __init__.py
│   └── service.py
└── Scheduler.py
```

Register only the services that need container-managed dependencies in `app/__init__.py`. Plain helper functions and data models do not need DI registrations.

## Tests

The generated `tests/TestCase.py` is based on `unittest.TestCase`. It creates an app instance, sets `APP_ENV` to `testing`, and exposes `self.fake` from Faker.

Run generated tests with:

```bash
python -m unittest discover -s tests
```

## Files Created During Development

The scaffold intentionally ignores local runtime files such as `.env`, compiled Python files, coverage output, SQLite files, logs, and virtual environments. This keeps generated projects portable across Unix and Windows.

Common generated or local-only files include:

- `.env`: local secrets and environment overrides;
- `.coverage`: coverage data;
- `htmlcov/`: HTML coverage reports;
- `*.pyc` and `__pycache__/`: Python bytecode cache;
- `database/*.sqlite*`: local SQLite database files;
- `storage/logs/*.log`: file log output;
- `dist/` and `build/`: compile or packaging outputs;
- `.venv/` or `venv/`: virtual environments.

Do not rely on these files being present in production. They should be recreated by deployment or runtime setup.

## Safe Customization

- Add business logic under `app/`.
- Add configuration files under `config/`.
- Keep secrets in `.env` or real environment variables.
- Keep tests under `tests/` and prefer workflow tests around public entry points.
- Use `pathlib` for custom file handling so code works on Windows and Unix.
