---
sidebar_position: 1
---

# FastAPI Example

Generated Equipment projects include `web.py`, a small FastAPI entry point that reads host and port from `config/web.yaml` and uses the generated application container.

The example is intentionally minimal. It shows how to combine FastAPI with the generated `app()` container, not how to structure every production API.

## Dependencies

The generated `pyproject.toml` includes:

```toml
dependencies = [
    "equipment>=1.0.0",
    "fastapi[standard]>=0.100.0,<1",
    "uvicorn[standard]>=0.30,<1",
]
```

Install the generated project before running the web example:

```bash
python -m pip install .
```

## Configuration

`config/web.yaml`:

```yaml
web:
  host: ${WEB_HOST:0.0.0.0}
  port: ${PORT:8000}
```

Set `WEB_HOST` or `PORT` in `.env` or the process environment to change runtime behavior.

## Generated `web.py`

```python
from app import app
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from uvicorn import Server, Config

app = app()
name = app.config.app.name()
web = FastAPI(title=name)


@web.get("/", response_class=HTMLResponse)
async def landing() -> str:
    return f'''
        <h1>{name}</h1>
        <hr />
        <p>{app.inspiring().quote()}</p>
    '''


if __name__ == '__main__':
    server = Server(Config(
        app='web:web',
        host=str(app.config.web.host()),
        port=int(app.config.web.port()),
    ))
    server.run()
```

The generated file creates the application container once at module import time. For many small apps, that is enough. For larger apps, keep the container creation in one module and import routers that depend on services.

## Run

```bash
python web.py
```

Then open the configured host and port, usually `http://127.0.0.1:8000` for local development.

If `WEB_HOST=0.0.0.0`, the server listens on all interfaces. Browsers on the same machine should still use `127.0.0.1` or `localhost`.

## Extend

Add routers or services in `app/`, then inject framework services through the generated `App` container. Keep route functions thin and move business logic into testable services.

## Add A Router

Create a router module:

```python
# app/routes/health.py
from fastapi import APIRouter
from app import app

router = APIRouter()
application = app()


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "app": application.config.app.name(),
    }
```

Include it in `web.py`:

```python
from app.routes.health import router as health_router

web.include_router(health_router)
```

## Use Services In Routes

Keep route handlers thin:

```python
@web.post("/reports/{report_id}/rebuild")
def rebuild_report(report_id: int) -> dict[str, str]:
    app.queue().push(rebuild_report_job, report_id)
    return {"status": "queued"}
```

Put business behavior in services registered in `app/__init__.py`, then call those services from routes or queued jobs.

## Configuration Per Environment

Local `.env` example:

```env
APP_ENV=local
WEB_HOST=127.0.0.1
PORT=8000
LOG_CHANNEL=stack
QUEUE_CONNECTION=sync
```

Container or PaaS example:

```env
APP_ENV=production
WEB_HOST=0.0.0.0
PORT=8000
LOG_CHANNEL=console
QUEUE_CONNECTION=redis
```

## Testing FastAPI Routes

Use FastAPI's test client for HTTP behavior and Equipment's `TestCase` for service behavior:

```python
from fastapi.testclient import TestClient
from web import web


class WebTest(TestCase):
    def test_health(self):
        client = TestClient(web)
        response = client.get("/health")

        self.assertEqual(200, response.status_code)
        self.assertEqual("ok", response.json()["status"])
```

For service-level tests, call the service directly without HTTP. This keeps most tests fast and focused.

## Deployment Notes

- The generated `web.py` runs Uvicorn directly for convenience.
- Production deployments may use a process manager, container command, or platform-specific start command.
- Keep secrets in environment variables, not in route modules.
- Use `LOG_CHANNEL=console` in platforms that collect stdout.
- Use `QUEUE_CONNECTION=redis` and a separate worker process for slow work.

## Troubleshooting

Server starts but route cannot import `app`:

Run from the generated project root or install the project with `python -m pip install .`.

Port is already in use:

Change `PORT` in `.env` or stop the process using the port.

Queued route blocks instead of returning quickly:

`QUEUE_CONNECTION` is probably `sync`. Use Redis for true background processing.

## Guidance

- Keep web configuration in `config/web.yaml` or environment variables.
- Do not hardcode secrets or deployment hostnames in `web.py`.
- Use FastAPI's normal testing tools for HTTP behavior and Equipment's `TestCase` for service-level behavior.
- Keep route handlers small and move business logic into services.
- Use queues for slow work triggered by HTTP requests.
