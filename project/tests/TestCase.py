import unittest
from faker import Faker
from app import app
# from equipment.Log.NullLogger import NullLogger


class TestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        # Global faker instance
        self.fake = Faker()

        # Initialize app
        self.app = app()

        # Override environment
        self.app.config.app.env.from_value('testing')

        # (optional) Disable logs during tests
        # self.app.log.override(NullLogger())


if __name__ == '__main__':
    unittest.main()
