import unittest
from faker import Faker
from equipment.framework.Environment.LocalEnvironment import LocalEnvironment
from equipment.framework.helpers import app


class TestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        # Global faker instance
        self.faker = Faker()

        # Initialize app
        self.app = app()

        # Override environment
        self.app.environment.override(LocalEnvironment('.env.test'))


if __name__ == '__main__':
    unittest.main()
