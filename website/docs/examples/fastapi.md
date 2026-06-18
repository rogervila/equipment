---
sidebar_position: 1
---

# FastAPI Example

Generated Equipment projects include `web.py`, a small FastAPI entry point that reads host and port from `config/web.yaml` and uses the generated application container.

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

## Run

```bash
python web.py
```

Then open the configured host and port, usually `http://127.0.0.1:8000` for local development.

## Extend

Add routers or services in `app/`, then inject framework services through the generated `App` container. Keep route functions thin and move business logic into testable services.

## Guidance

- Keep web configuration in `config/web.yaml` or environment variables.
- Do not hardcode secrets or deployment hostnames in `web.py`.
- Use FastAPI's normal testing tools for HTTP behavior and Equipment's `TestCase` for service-level behavior.
