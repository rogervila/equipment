---
sidebar_position: 1
---

# Scheduler

## Overview

Equipment uses the [schedule](https://schedule.readthedocs.io) library to manage and execute scheduled tasks. The scheduler provides a flexible and powerful way to run periodic tasks within the application.

## Key Components

### `app/Scheduler.py`
This file defines the core scheduling logic for the application. It extends the base `Equipment.Scheduler` class and provides:
- Integration with the application's logging system
- Support for background task queuing
- Ability to schedule and run periodic tasks

### `scheduler.py`
The main entry point for running scheduled tasks. It:
- Initializes the application context
- Starts the scheduler to run defined tasks

## Dependencies and Initialization

The scheduler is initialized in `app/__init__.py` using dependency injection:
- Integrated with the application's logging system
- Connected to the task queue
- Optionally linked with additional services (e.g., `Inspire` for generating quotes)

## Task Scheduling

Tasks are defined directly in `app/Scheduler.py`. The implementation leverages the `schedule` library, allowing for:
- Interval-based scheduling (every X minutes/hours/days)
- Specific time-based scheduling
- Recurring tasks
- One-time tasks

### Example Task
```python
class Scheduler(Equipment):
    # ...

    def run(self) -> None:
        self.schedule.every(5).seconds.do(
            lambda: self.log.debug('Scheduled message')
        )
```

## Running the Scheduler

To start the scheduler, simply run:
```bash
python scheduler.py
```

This will:
1. Initialize the application
2. Set up all scheduled tasks
3. Begin executing tasks according to their defined schedules

## Features
- Thread-safe task scheduling
- Integrated logging
- Background task processing
- Flexible task definition

## Best Practices
- Keep scheduled tasks lightweight
- Use logging to track task execution
- Handle potential exceptions within scheduled tasks
