---
sidebar_position: 0
---

# Dependency Injection

## Overview

Dependency Injection (DI) is a core design pattern in Equipment used to manage object creation and lifecycle. It promotes loose coupling, improved modularity, and makes your application significantly easier to test.

Equipment uses the [`python-dependency-injector`](https://github.com/ets-labs/python-dependency-injector) library under the hood, specifically utilizing `ThreadSafeSingleton` for creating thread-safe, single-instance objects.

## The Equipment Architecture

Equipment separates dependencies into two layers:
1. **Library-level Singletons**: Core services provided by the Equipment framework (Log, Queue, Database, Storage).
2. **Application-level Singletons**: Custom services defined in your project's `App` class.

### Library-level Singletons

These are always available in any Equipment project. They are configured automatically based on your `config/` files.

- **Log**: `app.log()` - Centralized logging system.
- **Queue**: `app.queue()` - Background task management.
- **Database**: `app.database()` - SQLAlchemy engine and session management.
- **Storage**: `app.storage()` - Abstract filesystem interface.

### Application-level Singletons

You define your own services in the `App` class located in `app/__init__.py`.

```python
# app/__init__.py
from dependency_injector.providers import ThreadSafeSingleton as Singleton
from equipment import Equipment
from app.MyService import MyService

class App(Equipment):
    # Registering a custom service as a singleton
    myservice = Singleton(
        MyService,
        Equipment.log,  # Injecting a library-level singleton
        Equipment.config.app.my_setting # Injecting a configuration value
    )
```

## Usage Example

The `app()` function serves as a factory method to create and configure the main `App` instance.

```python
#!/usr/bin/env python
from app import app

# Create the application instance
app = app()

# Accessing library singletons
app.log().info("Hello World")
app.storage().write("test.txt", "data")

# Accessing your custom singletons
result = app.myservice().do_something()
```

## Advanced Injection

You can inject services into other services by passing them to the `Singleton` provider in your `App` class.

```python
class App(Equipment):
    repository = Singleton(UserRepository, Equipment.database)

    service = Singleton(
        UserService,
        repository,    # Injecting another singleton
        Equipment.log  # Injecting library singleton
    )
```

## Benefits

- **Modularity**: Dependencies are explicit and easy to swap.
- **Thread Safety**: `ThreadSafeSingleton` ensures a single instance even in multi-threaded environments (like web servers).
- **Testability**: You can easily override providers with mocks or stubs during testing.
- **Clean Code**: Reduces the need for global variables or complex factory functions.

## Best Practices

1. **Inject, Don't Fetch**: Pass dependencies to your service constructors instead of using the `app` instance inside the service.
2. **Keep services focused**: Each singleton should have a single, well-defined responsibility.
3. **Use the `App` class**: Always register your main business logic services in the `App` class for consistent lifecycle management.
