---
sidebar_position: 7
---

# Testing

Equipment projects use the Python standard library `unittest` runner. The repository also uses `coverage` for test coverage reporting.

The generated project includes a reusable `tests/TestCase.py` base class that creates Faker data and an application container for each test.

The test philosophy is simple: verify user workflows and service behavior, not just implementation details. Equipment-generated apps should be easy to refactor because tests describe what the app does.

## Generated TestCase

```python
import unittest
from faker import Faker
from app import app


class TestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.fake = Faker()
        self.app = app()
        self.app.config.app.env.from_value('testing')
```

    The base class gives each test:

    - `self.fake`: a Faker instance for realistic test values;
    - `self.app`: an Equipment application container;
    - `APP_ENV` forced to `testing` inside config.

    You can extend this base class with application-specific helpers, such as creating database rows, disabling logs, or setting local storage paths.

## Write A Test

```python
from tests.TestCase import TestCase


class StorageTest(TestCase):
    def test_write_and_read_file(self):
        filename = "example.txt"
        content = self.fake.sentence()

        self.assertTrue(self.app.storage().write(filename, content))
        self.assertEqual(content, self.app.storage().read(filename))
```

Prefer tests that follow a real workflow:

1. arrange input and config;
2. call an application service or entry point;
3. assert the observable result;
4. assert important side effects such as files, logs, database rows, or queued calls.

## Service Test Example

```python
from tests.TestCase import TestCase


class ReportsTest(TestCase):
    def test_report_writes_to_storage(self):
        path = self.app.reports().write_daily_report("Ready")

        self.assertTrue(self.app.storage().exists(path))
        self.assertEqual("Ready", self.app.storage().read(path))
```

## Mocking External Services

Use `unittest.mock` for external services that should not run in unit tests:

```python
from unittest.mock import Mock

from tests.TestCase import TestCase


class ReportsTest(TestCase):
    def test_report_uses_storage(self):
        storage = Mock()
        self.app.storage.override(storage)

        self.app.reports().write_daily_report("Ready")

        storage.write.assert_called_once()
```

Mock network calls, Redis calls, S3 calls, email providers, and payment providers unless the test is explicitly an integration test.

## Run Generated Project Tests

```bash
python -m unittest discover -s tests
```

With coverage:

```bash
python -m pip install .[dev]
python -m coverage run -m unittest discover -s tests
python -m coverage report
```

Run a single test module:

```bash
python -m unittest tests.app.test_Inspire
```

Run one test class or method:

```bash
python -m unittest tests.app.test_Inspire.TestInspire
python -m unittest tests.app.test_Inspire.TestInspire.test_quote
```

## Run Repository Tests

From the Equipment repository root:

```bash
python -m pip install -r requirements.txt
python -m pip install coverage runtype faker
python -m coverage run -m unittest discover -s tests
python -m coverage report
```

## What To Cover Before Dependency Upgrades

- CLI dispatch for `equipment new` and `equipment compile`.
- Project scaffolding from the real template with network calls mocked.
- Template rendering and generated metadata.
- File creation, ignored directories, and compile output layout.
- Config loading from YAML and JSON.
- Local storage and S3 storage behavior.
- Database URL creation and session creation.
- Logging handler setup.
- Queue behavior for sync mode and Redis integration when Redis is available.

## Test Categories

Unit tests:

- service methods;
- configuration parsing;
- local storage behavior;
- database URL generation;
- queue sync behavior;
- scheduler registration helpers.

Integration tests:

- database sessions against SQLite;
- S3 behavior with moto;
- generated project install/import behavior;
- compile command output;
- CLI command behavior with mocked network calls.

External-service tests:

- Redis worker behavior;
- real S3 buckets;
- MySQL or PostgreSQL drivers;
- deployment-specific smoke tests.

Keep external-service tests opt-in unless CI provisions those services.

## Cross-platform Testing

Path handling, temporary directories, file cleanup, and compiled bytecode behavior can differ across Unix and Windows. When tests create temporary directories and call `os.chdir`, make sure cleanup changes back to the previous directory before deleting the temporary directory. Windows cannot delete the current working directory.

Prefer `pathlib.Path` for test file paths and avoid hardcoded `/` or `\\` separators.

## Coverage Guidance

Do not chase a number without context. Coverage is useful when it protects important workflows:

- project generation;
- generated metadata;
- config loading;
- local and S3 storage;
- database URL/session creation;
- logging handlers;
- queue behavior;
- scheduler loop behavior;
- compile command output.

If coverage reports include dependency internals or C-extension source paths, erase old coverage data and rerun the intended command:

```bash
python -m coverage erase
python -m coverage run -m unittest discover -s tests
python -m coverage report
```

## Current Practical Gaps

- Redis integration needs a running Redis service.
- S3 tests use moto for unit coverage and do not prove real cloud credentials.
- MySQL and PostgreSQL tests skip unless optional drivers are installed.
- Native Windows validation should still be run for batch scripts and path-sensitive changes.

## Guidance

- Prefer workflow tests over implementation-only assertions.
- Mock network access in `equipment new` tests.
- Use temporary directories for filesystem tests.
- Keep tests deterministic; use Faker for data variety, not for essential assertions.
- Keep tests importable with `python -m unittest discover -s tests`.
- Avoid sleeping tests; patch scheduler loops instead.
- Close files and log handlers before deleting temporary directories, especially on Windows.
