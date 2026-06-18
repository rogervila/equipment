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

## Configuration

The `config/` directory is loaded by filename and extension. Equipment supports `.ini`, `.yaml`, and `.json` files. The generated project uses YAML for application services and JSON for the example quote list.

Use `${ENV_NAME:default}` syntax to let `.env` or system environment variables override defaults.

## Entry Points

- `main.py`: script entry point and examples for storage, queue, database, and logging.
- `scheduler.py`: starts the schedule loop defined in `app/Scheduler.py`.
- `queues.py`: starts an RQ worker for Redis-backed queues.
- `web.py`: starts the FastAPI example using `config/web.yaml`.

## Tests

The generated `tests/TestCase.py` is based on `unittest.TestCase`. It creates an app instance, sets `APP_ENV` to `testing`, and exposes `self.fake` from Faker.

Run generated tests with:

```bash
python -m unittest discover -s tests
```

## Files Created During Development

The scaffold intentionally ignores local runtime files such as `.env`, compiled Python files, coverage output, SQLite files, logs, and virtual environments. This keeps generated projects portable across Unix and Windows.

## Safe Customization

- Add business logic under `app/`.
- Add configuration files under `config/`.
- Keep secrets in `.env` or real environment variables.
- Keep tests under `tests/` and prefer workflow tests around public entry points.
- Use `pathlib` for custom file handling so code works on Windows and Unix.
