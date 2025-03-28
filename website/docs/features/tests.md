---
sidebar_position: 1
---

# Testing

## Base TestCase Class

Equipment provides a custom base `TestCase` class that enhances the standard `unittest.TestCase` with several convenient features:

### Key Features

1. **Application Instance**:
   - Each test automatically receives an initialized application instance via `self.app`
   - Ensures a fresh application context for every test

2. **Faker Integration**:
   - Includes a pre-configured [Faker](https://faker.readthedocs.io) instance as `self.fake`
   - Simplifies generation of fake data for testing

3. **Environment Override**:
   - Automatically sets the application environment to `"testing"`
   - Ensures tests run in an isolated test environment
   - Prevents accidental interactions with production or development configurations

4. **Optional Logging Control**:
   - Provides the ability to disable logging during tests
   - Can be activated by uncommenting the `NullLogger()` override
   - Helps keep test output clean and focused

### Example Usage

```python
from tests import TestCase

class MyTest(TestCase):
    def test_something(self):
        # Access application instance
        app = self.app

        # Use Faker for test data
        username = self.fake.user_name()

        # Test your code...
```

### Best Practices

- Always inherit from `TestCase` for consistent test setup
- Utilize the `self.fake` instance for generating test data
- Leverage the automatic testing environment configuration
