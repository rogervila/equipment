---
sidebar_position: 4
---

# Queue

Equipment provides a queue abstraction with two drivers: `sync` and `redis`.

Use queues when work should happen outside the current request, script, or scheduler loop. Common examples include sending emails, generating reports, importing files, processing uploads, retrying webhooks, rebuilding caches, and running expensive cleanup tasks.

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

## Drivers

| Driver | Behavior | Use Case |
| --- | --- | --- |
| `sync` | Runs work immediately in the current process. | Local development, deterministic tests, simple scripts. |
| `redis` | Enqueues jobs into Redis through RQ. | Background workers, web requests that should return quickly, scheduled jobs. |

## Sync Driver

```python
from app import app

application = app()

def send_email(address: str) -> None:
    application.log().info("Sending email", extra={"address": address})

application.queue().push(send_email, "user@example.com")
```

With the sync driver, `send_email` runs before `push` returns. This makes tests easy to reason about, but it is not real background processing.

## Redis Driver

Set `QUEUE_CONNECTION=redis`, start Redis, and run a worker:

```bash
python queues.py
```

On Windows PowerShell:

```powershell
$env:QUEUE_CONNECTION = "redis"
python queues.py
```

Push jobs from application code:

```python
application.queue().push(send_email, "user@example.com")
```

Schedule a job for later:

```python
from datetime import datetime, timedelta

run_at = datetime.now() + timedelta(minutes=10)
application.queue().push_at(run_at, send_email, "user@example.com")
```

## Task Function Design

RQ workers must be able to import queued functions. Prefer module-level functions:

```python
# app/jobs/reports.py
from app import app


def rebuild_report(report_id: int) -> None:
    application = app()
    application.reports().rebuild(report_id)
```

Queue it by passing the function object:

```python
from app.jobs.reports import rebuild_report

application.queue().push(rebuild_report, 123)
```

Avoid lambdas, nested functions, open file handles, active database sessions, request objects, container instances, and large in-memory objects as queued arguments. Pass stable identifiers and load fresh data inside the worker.

## Idempotency

Queued tasks may run more than once after retries, worker crashes, deployment restarts, or network interruptions. Design tasks so a repeat run is safe.

Useful patterns:

- check whether a record has already been processed;
- use database uniqueness constraints;
- write output to deterministic paths;
- use idempotency keys for external APIs that support them;
- log task start and finish with stable IDs.

## Error Handling

`push()` returns `True` or `False` for enqueueing/execution at the queue layer.

In sync mode, exceptions raised by the function are caught, logged, and result in `False`.

In Redis mode, enqueueing errors are caught, but task failures happen in worker processes and are managed by RQ. Check worker logs for task exceptions.

## Queue From FastAPI

```python
@web.post("/reports/{report_id}/rebuild")
def rebuild(report_id: int) -> dict[str, str]:
    application.queue().push(rebuild_report, report_id)
    return {"status": "queued"}
```

With `sync`, this executes immediately. With `redis`, the response can return after enqueueing.

## Queue From Scheduler

```python
self.schedule.every().hour.do(self.queue.push, rebuild_report, 123)
```

Schedulers should enqueue slow work instead of running it inline.

## Deployment Checklist

- Redis is reachable from both producer processes and worker processes.
- `QUEUE_CONNECTION=redis` is set where background behavior is expected.
- Worker processes run `python queues.py`.
- Task functions are importable from module scope.
- Task arguments are serializable and small.
- Logs include task IDs or domain IDs for debugging.

## Testing Queued Work

Test business logic directly where possible. Test queue integration separately.

```python
called = []

def job(value):
    called.append(value)

self.assertTrue(self.app.queue().push(job, 42))
self.assertEqual([42], called)
```

Use `sync` in most tests. Run Redis-backed tests only when Redis is available in CI or local development.

## Troubleshooting

Task runs immediately instead of in the background:

`QUEUE_CONNECTION` is probably `sync`.

Task never runs:

Check Redis connectivity, worker process logs, and whether the function can be imported by the worker.

Task works in sync mode but not Redis mode:

Check serialization and importability. Pass IDs rather than objects.

Delayed tasks do not run when expected:

Confirm worker support for scheduled jobs and check server time assumptions.

## Guidance

- Keep queued callables importable and stable.
- Prefer small serializable arguments such as IDs.
- Use idempotent task logic so retries are safe.
- Use `sync` in tests unless specifically testing Redis integration.
- Do not pass active database sessions, file handles, request objects, or dependency-injector providers as job payloads.
