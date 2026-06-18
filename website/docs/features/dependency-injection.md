---
sidebar_position: 0
---

# Dependency Injection

Equipment uses `dependency-injector` to keep service creation explicit and reusable. The framework container provides shared services, and the generated project adds application-specific services on top.

## Runtime Container

The base `Equipment` container loads configuration and exposes these singleton providers:

- `log`: configured logger factory;
- `queue`: sync or Redis queue factory;
- `storage`: local or S3 storage factory;
- `database`: SQLAlchemy factory.

Generated projects subclass the base container in `app/__init__.py`:

```python
from dependency_injector.providers import ThreadSafeSingleton as Singleton
from equipment import Equipment
from app.Inspire import Inspire
from app.Scheduler import Scheduler


class App(Equipment):
    inspiring = Singleton(Inspire, Equipment.config.inspiring.quotes)

    scheduler = Singleton(
        Scheduler,
        Equipment.log,
        Equipment.queue,
        inspiring,
    )


def app(base_path: str | None = None) -> App:
    return App.make(base_path)
```

## Access Services

```python
from app import app

application = app()

application.log().info("Application started")
quote = application.inspiring().quote()
application.storage().write("quote.txt", quote)
```

## Add Your Own Service

Define a class in `app/` and register it in `App`:

```python
from dependency_injector.providers import ThreadSafeSingleton as Singleton
from equipment import Equipment
from app.Reports import Reports


class App(Equipment):
    reports = Singleton(
        Reports,
        Equipment.database,
        Equipment.storage,
        Equipment.log,
    )
```

Prefer constructor injection. It keeps dependencies visible, easier to test, and easier for LLMs to follow.

## Testing Overrides

Tests can override providers when a service should be replaced with a fake or mock:

```python
from unittest.mock import Mock

from tests.TestCase import TestCase


class ReportsTest(TestCase):
    def test_report_uses_storage(self):
        fake_storage = Mock()
        self.app.storage.override(fake_storage)

        self.app.reports().run()

        fake_storage.write.assert_called()
```

## Guidance

- Register long-lived services as `ThreadSafeSingleton` providers.
- Keep application registrations in `app/__init__.py` so the container stays discoverable.
- Pass framework services into constructors instead of importing a global app object inside business logic.
- Reset or override providers in tests when a dependency touches the filesystem, network, database, or queue.
