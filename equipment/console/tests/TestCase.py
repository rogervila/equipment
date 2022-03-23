import unittest
import os
from faker import Faker


class TestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        # Global faker instance
        self.faker = Faker()

        # Access tests base path
        self.tests_path = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    unittest.main()
