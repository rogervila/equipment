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

The generated `App` class is the application composition root. A composition root is the place where concrete services are assembled. Keeping service registration in one file makes the dependency graph easy to inspect and easy for LLMs to reason about.

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

## Constructor Injection Pattern

Prefer this pattern:

```python
class InvoiceService:
    def __init__(self, database, log):
        self.database = database
        self.log = log

    def create_invoice(self, customer_id: int) -> int:
        self.log.info("Creating invoice", extra={"customer_id": customer_id})
        # Use self.database here.
        return 1
```

Register it once:

```python
class App(Equipment):
    invoices = Singleton(InvoiceService, Equipment.database, Equipment.log)
```

Then use it from entry points:

```python
from app import app

application = app()
invoice_id = application.invoices().create_invoice(customer_id=42)
```

Avoid this pattern inside business services:

```python
class InvoiceService:
    def create_invoice(self, customer_id: int) -> int:
        from app import app
        application = app()
        application.log().info("Creating invoice")
        return 1
```

The second version hides dependencies, makes tests more difficult, and can create surprising container instances when called from workers or scripts.

## Provider Lifecycle

Generated services use `ThreadSafeSingleton`. The first call creates the service, and later calls reuse it. This is useful for services that hold references to framework factories such as logging, database, storage, or queue providers.

Use singleton services for:

- stateless business services;
- repositories that use shared framework factories;
- adapters around external systems;
- scheduler classes;
- services that are safe to reuse between calls.

Avoid storing request-specific mutable state on singleton services. In web apps, request data should live in function parameters, local variables, database rows, or dedicated request-scoped objects that you create manually.

## Passing Configuration Into Services

You can inject config values directly:

```python
class Reports:
    def __init__(self, storage, output_path: str):
        self.storage = storage
        self.output_path = output_path


class App(Equipment):
    reports = Singleton(
        Reports,
        Equipment.storage,
        Equipment.config.reports.output_path,
    )
```

The injected config provider is evaluated when the service is created. If tests need a different value, override the config before calling the service for the first time:

```python
self.app.config.reports.output_path.from_value("test-report.txt")
report = self.app.reports()
```

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

When overriding providers, keep the override local to the test. `unittest` creates a new `TestCase` instance for each method, but singleton providers can still hold created objects. For tests that override core providers, reset the provider or create a fresh app base path if the test needs strict isolation.

## Designing Services For Workers And Schedulers

Queue workers and schedulers run in separate processes. Services should therefore be importable from module scope and should not depend on local state created only in `main.py`.

Good worker-friendly pattern:

```python
# app/jobs.py
from app import app


def send_invoice(invoice_id: int) -> None:
    application = app()
    application.invoices().send(invoice_id)
```

The queued function creates its own application container in the worker process and delegates to a service. That keeps the queued function small and lets tests target `InvoiceService` directly.

## Naming Conventions

- Use lowercase provider names such as `reports`, `invoices`, or `mailer`.
- Use class names for service classes such as `Reports`, `InvoiceService`, or `Mailer`.
- Keep provider names stable because entry points and tests may call them directly.
- Group related providers together in `app/__init__.py` when the application grows.

## Troubleshooting

`AttributeError` when accessing a service:

The service is not registered on the generated `App` class, or the entry point imported the wrong `app` object.

Configuration value is missing:

Confirm the config file exists under `config/`, the top-level key matches the filename, and the application is running from the project root or an explicit base path.

Service uses stale config in a test:

The singleton may have already been created. Override config before first access, or reset the provider before creating the service again.

## Guidance

- Register long-lived services as `ThreadSafeSingleton` providers.
- Keep application registrations in `app/__init__.py` so the container stays discoverable.
- Pass framework services into constructors instead of importing a global app object inside business logic.
- Reset or override providers in tests when a dependency touches the filesystem, network, database, or queue.
- Keep singleton services stateless with respect to per-request data.
- Put process entry-point logic in `main.py`, `web.py`, `queues.py`, or `scheduler.py`, and reusable behavior in registered services.
