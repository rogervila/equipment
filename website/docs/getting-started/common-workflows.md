---
sidebar_position: 4
---

# Common Workflows

This page collects practical workflows for building an application with Equipment after the project has been generated.

## Create A New Application Service

1. Add a service class under `app/`.
2. Register it in `app/__init__.py` if it needs framework services or shared lifecycle management.
3. Add tests under `tests/`.
4. Call the service from `main.py`, `web.py`, a queue job, or a scheduled task.

Example service:

```python
# app/Reports.py
from equipment.Storage.AbstractStorage import AbstractStorage
from equipment.Log.AbstractLogger import AbstractLogger


class Reports:
    def __init__(self, storage: AbstractStorage, log: AbstractLogger):
        self.storage = storage
        self.log = log

    def write_daily_report(self, content: str) -> str:
        path = "reports/daily.txt"
        self.storage.write(path, content)
        self.log.info("Daily report written", extra={"path": path})
        return path
```

Register it:

```python
# app/__init__.py
from dependency_injector.providers import ThreadSafeSingleton as Singleton
from equipment import Equipment
from app.Reports import Reports


class App(Equipment):
    reports = Singleton(Reports, Equipment.storage, Equipment.log)
```

Use it:

```python
from app import app

application = app()
application.reports().write_daily_report("Ready")
```

## Add Configuration For A Service

Create `config/reports.yaml`:

```yaml
reports:
  output_path: ${REPORTS_OUTPUT_PATH:reports/daily.txt}
  enabled: ${REPORTS_ENABLED:true}
```

Inject the config value:

```python
class App(Equipment):
    reports = Singleton(
        Reports,
        Equipment.storage,
        Equipment.log,
        Equipment.config.reports.output_path,
    )
```

Use environment variables in `.env` for machine-specific values:

```env
REPORTS_OUTPUT_PATH=reports/local-daily.txt
```

## Add A Database-backed Feature

1. Define SQLAlchemy models in your application code.
2. Add or update Alembic migration metadata.
3. Create a migration under `database/migrations`.
4. Run the migration locally.
5. Add repository/service tests.

Typical commands:

```bash
cd database/migrations
alembic revision --autogenerate -m "create invoices table"
alembic upgrade head
```

Use sessions carefully:

```python
session = application.database().session()
try:
    session.add(invoice)
    session.commit()
except Exception:
    session.rollback()
    raise
finally:
    session.close()
```

## Add A Queued Task

Put queued functions at module scope so Redis/RQ can import them:

```python
# app/jobs.py
from app import app


def rebuild_report(report_id: int) -> None:
    application = app()
    application.log().info("Rebuilding report", extra={"report_id": report_id})
```

Queue it from a script or route:

```python
from app import app
from app.jobs import rebuild_report

application = app()
application.queue().push(rebuild_report, 123)
```

Local development can keep `QUEUE_CONNECTION=sync`. Production worker mode usually sets `QUEUE_CONNECTION=redis` and runs:

```bash
python queues.py
```

## Add A Scheduled Task

Add scheduled work in `app/Scheduler.py`:

```python
from app.jobs import rebuild_report


class Scheduler(Equipment):
    def run(self) -> None:
        self.schedule.every().day.at("03:00").do(
            self.queue.push,
            rebuild_report,
            123,
        )
        super().run()
```

Run it with:

```bash
python scheduler.py
```

Use the queue for slow work so the scheduler loop stays responsive.

## Add A FastAPI Route

Add routes in `web.py` for small apps, or move them into a router module for larger apps.

```python
from fastapi import APIRouter
from app import app

router = APIRouter()
application = app()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": application.config.app.name()}
```

Then include the router from `web.py`:

```python
from app.routes import router

web.include_router(router)
```

Keep route functions thin. Put business logic in services registered on the `App` container.

## Add Tests For A Workflow

Use the generated `TestCase` when a test needs an application container:

```python
from tests.TestCase import TestCase


class ReportsTest(TestCase):
    def test_report_is_written_to_storage(self):
        path = self.app.reports().write_daily_report("Ready")

        self.assertTrue(self.app.storage().exists(path))
        self.assertEqual("Ready", self.app.storage().read(path))
```

Use `unittest.mock` for external systems that should not run in unit tests:

```python
from unittest.mock import Mock

self.app.storage.override(Mock())
```

## Prepare For Deployment

Before deployment, decide these values explicitly:

- `APP_ENV`: environment name such as `production`, `staging`, or `local`.
- `LOG_CHANNEL`: `console`, `stack`, `single`, `daily`, `sqlite`, or `null`.
- `DB_CONNECTION`: `sqlite`, `mysql`, or `postgresql`.
- `QUEUE_CONNECTION`: `sync` or `redis`.
- `FILESYSTEM_DISK`: `local` or `s3`.
- `WEB_HOST` and `PORT`: web server binding values.

Run a deployment-style smoke test:

```bash
python -m pip install .
python -m unittest discover -s tests
python main.py
```

If you compile the project, smoke test the compiled output too:

```bash
equipment compile dist
cd dist
python main.pyc
```

## Upgrade Dependencies Safely

Dependency upgrades should be their own change. Before upgrading, run the current tests to establish a baseline. After upgrading, run:

```bash
python -m coverage run -m unittest discover -s tests
python -m coverage report
cd project
python -m pip install .
python -m unittest discover -s tests
```

Pay close attention to SQLAlchemy, boto3/botocore/moto, redis/rq, python-json-logger, dependency-injector, and FastAPI/Uvicorn upgrades because Equipment integrates directly with those packages.
