---
sidebar_position: 7
---

# Testing

Equipment projects use the Python standard library `unittest` runner. The repository also uses `coverage` for test coverage reporting.

The generated project includes a reusable `tests/TestCase.py` base class that creates Faker data and an application container for each test.

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
