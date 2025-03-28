---
sidebar_position: 1
---

# Queue Management

## Overview
Equipment provides a flexible queue management system with two primary queue drivers: local (sync) and Redis. This allows for seamless handling of asynchronous tasks with different backend configurations.

## Queue Drivers
The queue driver is configured in `config/queue.yml` and can be set using the `QUEUE_CONNECTION` environment variable.

### 1. Sync Driver
- **Name**: `sync`
- **Behavior**: Tasks are processed immediately in the current process
- **Use Case**: Ideal for local development or simple task processing

### 2. Redis Driver
- **Name**: `redis`
- **Behavior**: Tasks are queued and processed by a separate worker
- **Configuration**:
  - `host`: Redis server host (default: 127.0.0.1)
  - `port`: Redis server port (default: 6379)
  - `db`: Redis database number (default: 0)
  - `username`: Optional Redis username
  - `password`: Optional Redis password

## Queue Methods

### `push(task)`
- Adds a task to the queue for immediate or deferred processing
- Works with both sync and Redis drivers

### `push_at(task, timestamp)`
- Schedules a task to be executed at a specific time
- Supports both sync and Redis drivers

## Usage Example

```python
# Initialize the application
from app import app

app = app()

# When using Sync driver, task is processed immediately

# When using Redis driver, task is queued for worker processing
# Start worker with: $ py queues.py

# Results in `app.log().debug(app.inspiring().quote())`
app.queue().push(
    app.log().debug,
    app.inspiring().quote()
)
```

## Running Queue Worker
For Redis driver, start the queue worker using:
```bash
$ py queues.py
```

## Configuration
Modify `config/queue.yml` to configure queue connection and Redis settings.
