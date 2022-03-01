import unittest
from faker import Faker
from equipment.framework.Environment.LocalEnvironment import LocalEnvironment
from app.App.Container import Container


class BaseTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

        # Global faker instance
        self.faker = Faker()

        # Initialize app
        self.app = Container()

        # Override environment
        self.app.environment.override(LocalEnvironment('.env.test'))


if __name__ == '__main__':
    unittest.main()
