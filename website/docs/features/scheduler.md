---
sidebar_position: 5
---

# Scheduler

Equipment uses the `schedule` library for recurring tasks. The generated `scheduler.py` entry point creates the app and calls `app.scheduler().run()`.

Use the scheduler for periodic application-level work: reports, cleanup, polling, cache refreshes, and enqueueing background jobs. The scheduler is a long-running process and should be started separately from `main.py`, `web.py`, and `queues.py`.

## Generated Scheduler

Scheduled work is defined in `app/Scheduler.py`:

```python
from equipment.Scheduler.Scheduler import Scheduler as Equipment


class Scheduler(Equipment):
    def run(self) -> None:
        self.schedule.every(1).seconds.do(
            lambda: self.log.debug(self.inspiring.quote())
        )

        self.schedule.every(5).seconds.do(
            self.queue.push,
            _inspire,
            self.log,
            self.inspiring,
        )

        super().run()
```

Run it with:

```bash
python scheduler.py
```

Real applications should choose intervals that match the work being done.

## Common Patterns

```python
def cleanup() -> None:
    pass


class Scheduler(Equipment):
    def run(self) -> None:
        self.schedule.every(10).minutes.do(cleanup)
        self.schedule.every().day.at("03:00").do(cleanup)
        self.schedule.every().monday.do(cleanup)
        self.schedule.every().hour.do(cleanup)
        self.schedule.every(5).to(10).minutes.do(cleanup)

        super().run()
```

Always call `super().run()` after registering jobs.

## Queue Integration

Long-running scheduled work should be pushed to the queue:

```python
self.schedule.every().hour.do(self.queue.push, rebuild_report, report_id)
```

With `QUEUE_CONNECTION=sync`, this still runs immediately. With `QUEUE_CONNECTION=redis`, the work is handled by `queues.py`.

## Process Model

The scheduler loop:

1. logs startup;
2. calls `self.schedule.run_pending()`;
3. sleeps briefly;
4. repeats until interrupted or `should_exit` is set.

Run one scheduler process when a job must happen once globally. If multiple scheduler replicas are active, each replica may run or enqueue the same job.

## Scheduler-safe Jobs

Good scheduler jobs are:

- short;
- idempotent;
- logged;
- exception-safe;
- independent of terminal state;
- safe to run again after a restart.

For slow work, enqueue a task:

```python
def enqueue_report_rebuild(queue, report_id: int) -> None:
    queue.push(rebuild_report, report_id)
```

## Environment-specific Scheduling

```python
class Scheduler(Equipment):
    def run(self) -> None:
        if self.config.app.env() != "production":
            self.log.info("Skipping production-only jobs")
            super().run()
            return

        self.schedule.every().day.at("03:00").do(self.queue.push, rebuild_report, 123)
        super().run()
```

If scheduling behavior grows, add `config/scheduler.yaml` and inject those values into the scheduler.

## Testing Scheduler Code

Avoid tests that sleep. Patch `schedule.Scheduler.run_pending` or set `scheduler.should_exit = True` after one loop.

Test the task function separately from schedule registration.

## Deployment Checklist

- Decide whether the scheduler should run as one process or many.
- Use Redis queues for long tasks.
- Log job start and completion with stable IDs.
- Document timezone assumptions.
- Monitor the scheduler process like any other worker.
- Avoid schedules that run more often than the task can complete.

## Troubleshooting

Scheduled task never runs:

Confirm `python scheduler.py` is running, the job is registered before `super().run()`, and the system clock/timezone matches the schedule.

Scheduler blocks:

A job is probably doing long-running work inline. Push that work to the queue.

Task runs multiple times:

Multiple scheduler processes may be active, or the schedule interval may be too frequent.

## Guidance

- Keep scheduler jobs short or delegate to the queue.
- Handle exceptions inside task functions.
- Account for local machine time and timezone.
- Use focused tests with patched sleep/run-pending behavior.
- Avoid multiple scheduler replicas unless jobs are idempotent or externally locked.
