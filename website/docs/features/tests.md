---
sidebar_position: 7
---

# Testing Framework

Equipment provides a robust and developer-friendly testing framework designed to simplify and enhance the testing experience. It uses `pytest` under the hood and provides a specialized `TestCase` base class that handles boilerplate setup.

## The `TestCase` Base Class

Every project generated with Equipment includes a `tests/__init__.py` file defining a `TestCase` class. By inheriting from this class, you get several features out of the box:

1. **Automatic Application Context**: A fresh `App` instance is created for every test method, ensuring isolation.
2. **Faker Integration**: A pre-configured `Faker` instance is available as `self.fake` for easy test data generation.
3. **Environment Management**: The application is automatically switched to the `testing` environment, preventing accidental changes to production data.

## Writing Tests

### Unit Tests

Unit tests focus on individual components or functions in isolation.

```python
from tests import TestCase

class MyServiceTest(TestCase):
    def test_logic(self):
        # Access the app instance
        app = self.app

        # Use Faker for random data
        name = self.fake.name()

        # Assertions
        self.assertEqual(app.config.app.name(), "Equipment")
        self.assertTrue(app.storage().exists(".gitignore"))
```

### Integration Tests

Integration tests verify that different parts of the system work together correctly (e.g., Database + Storage).

```python
from tests import TestCase

class DatabaseStorageTest(TestCase):
    def test_save_to_db_and_file(self):
        # Perform operations using library services
        self.app.database().execute("INSERT INTO logs (msg) VALUES ('test')")
        self.app.storage().write("log.txt", "test")

        # Verify
        self.assertTrue(self.app.storage().exists("log.txt"))
```

## Running Tests

You can run your tests using the standard `pytest` command.

```bash
# Run all tests
pytest

# Run tests in a specific file
pytest tests/test_example.py

# Run a specific test class
pytest tests/test_example.py::TestExample
```

## Best Practices

1. **Inherit from `TestCase`**: Always use the provided base class to ensure a clean testing environment.
2. **Use `self.fake`**: Avoid hardcoding test data. Use Faker to generate diverse and realistic data.
3. **Mock External APIs**: For services that call external APIs, use libraries like `unittest.mock` or `responses` to avoid making real network requests.
4. **Keep Tests Independent**: Ensure that tests do not depend on the order in which they are run.
