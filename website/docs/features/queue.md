---
sidebar_position: 4
---

# Queue

Equipment provides a queue abstraction with two drivers: `sync` and `redis`.

The `sync` driver runs work immediately in the current process. The `redis` driver sends jobs to Redis through RQ so a worker process can execute them.

## Configuration

```yaml
queue:
  connection: ${QUEUE_CONNECTION:sync}

  connections:
    sync:

    redis:
      host: ${REDIS_HOST:127.0.0.1}
      port: ${REDIS_PORT:6379}
      db: ${REDIS_DB:0}
      username: ${REDIS_USERNAME:null}
      password: ${REDIS_PASSWORD:null}
```

## Sync Driver

Use `sync` for local development, tests, and simple scripts:

```python
from app import app

application = app()

def send_email(address: str) -> None:
    application.log().info("Sending email", extra={"address": address})

application.queue().push(send_email, "user@example.com")
```

With the sync driver, `send_email` runs before `push` returns.

## Redis Driver

Set `QUEUE_CONNECTION=redis`, start Redis, then run the worker:

```bash
python queues.py
```

Push jobs from your application:

```python
application.queue().push(send_email, "user@example.com")
```

Schedule a job for later:

```python
from datetime import datetime, timedelta

run_at = datetime.now() + timedelta(minutes=10)
application.queue().push_at(run_at, send_email, "user@example.com")
```

## Guidance

- Keep queued callables importable and stable.
- Prefer small serializable arguments such as IDs instead of large objects.
- Use idempotent task logic so retries are safe.
- Use `sync` in tests unless the test specifically validates Redis integration.
- Run Redis-backed tests only when CI or local development provides Redis.
