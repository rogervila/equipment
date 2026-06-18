---
sidebar_position: 5
---

# Task Scheduling

Equipment provides a powerful task scheduler build on top of the popular [`schedule`](https://schedule.readthedocs.io) library. It allows you to define recurring tasks at specific intervals or times using a human-readable syntax.

## Scheduling Tasks

All your scheduled tasks should be defined in the `run()` method of your `app/Scheduler.py` class.

### Common Scheduling Patterns

```python
class Scheduler(Equipment):
    def run(self) -> None:
        # Run every minute
        self.schedule.every(1).minutes.do(self.my_task)

        # Run every hour at 30 minutes past the hour
        self.schedule.every().hour.at(":30").do(self.my_task)

        # Run daily at a specific time
        self.schedule.every().day.at("10:30").do(self.my_task)

        # Run every Monday
        self.schedule.every().monday.do(self.my_task)

        # Run every 5 to 10 minutes (random range)
        self.schedule.every(5).to(10).minutes.do(self.my_task)

        # Important: call super().run() to start the execution loop
        super().run()
```

## Scheduler & Queue Integration

A powerful pattern in Equipment is using the scheduler to push tasks into a background queue. This prevents the scheduler from blocking on long-running tasks.

```python
def process_data():
    # Long-running task
    pass

class Scheduler(Equipment):
    def run(self) -> None:
        # Instead of calling process_data directly, we push it to the queue
        self.schedule.every().hour.do(self.queue.push, process_data)

        super().run()
```

## Running the Scheduler

The scheduler runs in a separate process that stays alive indefinitely.

```bash
# Start the scheduler
python scheduler.py
```

## Best Practices

1. **Keep tasks lightweight**: If a task takes more than a few seconds, push it to a queue instead of running it directly in the scheduler.
2. **Use Centralized Logging**: Always use `self.log` within your scheduler tasks to track execution and errors.
3. **Handle Exceptions**: The scheduler loop can stop if a task raises an unhandled exception. Wrap your task logic in `try...except` blocks.
4. **Timezones**: Be aware that the `schedule` library uses the system's local time by default.
