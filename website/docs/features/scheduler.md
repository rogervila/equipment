---
sidebar_position: 5
---

# Scheduler

Equipment uses the `schedule` library for recurring tasks. The generated `scheduler.py` entry point creates the app and calls `app.scheduler().run()`.

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

## Common Patterns

```python
def cleanup() -> None:
    pass


class Scheduler(Equipment):
    def run(self) -> None:
        self.schedule.every(10).minutes.do(cleanup)
        self.schedule.every().day.at("03:00").do(cleanup)
        self.schedule.every().monday.do(cleanup)

        super().run()
```

## Queue Integration

Long-running scheduled work should be pushed to the queue so the scheduler loop stays responsive:

```python
self.schedule.every().hour.do(self.queue.push, rebuild_report, report_id)
```

With `QUEUE_CONNECTION=sync`, this still runs immediately. With `QUEUE_CONNECTION=redis`, the work is handled by `queues.py`.

## Guidance

- Always call `super().run()` after registering scheduled jobs.
- Keep scheduler jobs short or delegate to the queue.
- Handle exceptions inside task functions so one failure does not stop recurring work.
- The `schedule` library uses the machine's local time; account for that in deployments.
- Use focused tests with patched sleep/run-pending behavior for scheduler loops.
