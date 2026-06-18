---
sidebar_position: 4
---

# Queue Management

Equipment provides a robust and flexible queue management system for handling asynchronous tasks efficiently. It supports multiple drivers, allowing you to switch between synchronous processing for development and distributed queuing for production.

## Configuration

Queues are configured in `config/queue.yaml`.

```yaml
queue:
  connection: ${QUEUE_CONNECTION:sync} # Options: sync, redis
  connections:
    redis:
      host: ${REDIS_HOST:127.0.0.1}
      port: ${REDIS_PORT:6379}
      db: ${REDIS_DB:0}
```

## Queue Drivers

### `sync` (Default)
- **Behavior**: Tasks are executed immediately in the current process.
- **Use Case**: Local development, debugging, or simple scripts where background processing is not required.
- **Note**: This driver does not require any additional services like Redis.

### `redis`
- **Behavior**: Tasks are pushed to a Redis instance and executed by background workers.
- **Use Case**: Production environments, long-running tasks, or when you need to offload work from a web request.
- **Requirement**: Requires a running Redis server and a worker process.

## Usage

### Enqueuing a Task

You can enqueue any Python callable (function or method).

```python
from app import app

app = app()

def send_email(to, subject, body):
    # Logic to send email
    print(f"Sending email to {to}")

# Push task to the queue
app.queue().push(send_email, "user@example.com", "Hello", "Welcome to Equipment!")
```

### Scheduling a Future Task

The `push_at` method allows you to schedule a task to be executed at a specific time.

```python
from datetime import datetime, timedelta

# Schedule a task to run 1 hour from now
run_at = datetime.now() + timedelta(hours=1)

app.queue().push_at(run_at, send_email, "user@example.com", "Reminder", "Don't forget!")
```

## Running the Worker

When using the `redis` driver, you must start a worker process to consume and execute the tasks.

```bash
# Start the queue worker
python queues.py
```

`queues.py` is a pre-configured entry point that initializes the application context and starts the `rq` worker.

## Best Practices

1. **Use async for long tasks**: Always offload tasks like email sending, image processing, or external API calls to a queue.
2. **Handle failures**: Ensure your queued functions are idempotent (safe to retry) and include proper error handling.
3. **Monitor your queues**: Use tools like `rq-dashboard` to monitor the status and performance of your Redis queues.
4. **Keep task arguments simple**: Prefer passing record IDs instead of full objects to avoid serialization issues and ensure data freshness.
