---
sidebar_position: 0
---

# Dependency Injection

## Overview

Dependency Injection (DI) is a design pattern used in Equipment to manage object creation and lifecycle, promoting loose coupling and improved modularity.

## Implementation Details

Equipment uses a [`library`](https://github.com/ets-labs/python-dependency-injector) to implement dependency injection, specifically utilizing `ThreadSafeSingleton` for creating thread-safe, single-instance objects.

### Key Components

#### Singleton Providers

Equipment defines singleton providers for key components:

1. **Inspiring Singleton**
   - Accessor: `app.inspiring()`
   - Creates a single instance of the `Inspire` class
   - Configured with quotes from the equipment configuration
   - Used as an example on how to implement application services

2. **Scheduler Singleton**
   - Accessor: `app.scheduler()`
   - Creates a single instance of the `Scheduler` class

Other components are also defined as singletons at the equipment library level:

1. **Log Singleton**
   - Accessor: `equipment.log()`
   - Creates a single instance of the `Log` class
   - Configured with log settings from the equipment configuration

2. **Queue Singleton**
   - Accessor: `equipment.queue()`
   - Creates a single instance of the `Queue` class
   - Configured with queue settings from the equipment configuration

3. **Database Singleton**
   - Accessor: `equipment.database()`
   - Creates a single instance of the `Database` class
   - Configured with database settings from the equipment configuration

4. **Storage Singleton**
   - Accessor: `equipment.storage()`
   - Creates a single instance of the `Storage` class
   - Configured with storage settings from the equipment configuration

### App Factory Method

The `app()` function serves as a factory method to create and configure the main `App` instance:

```python
#!/usr/bin/env python

from app import app

app = app()

# Accessing singleton providers
log = app.log()
queue = app.queue()
database = app.database()
storage = app.storage()
# etc...
```

## Benefits

- **Modularity**: Easy to manage and swap dependencies
- **Thread Safety**: Uses thread-safe singleton providers
- **Configuration Flexibility**: Dependencies can be easily configured
- **Reduced Coupling**: Components are loosely connected

## Best Practices

- Use singleton providers for shared, stateful components
- Inject dependencies through constructors
- Keep dependencies minimal and focused
