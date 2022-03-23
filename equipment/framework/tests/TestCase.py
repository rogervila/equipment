import os
import unittest
from faker import Faker
from equipment.framework.helpers import app
from equipment.framework.Log.NoneLog import NoneLog
from equipment.framework.Config.LocalConfig import LocalConfig


class TestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        # Access tests base path
        self.tests_path = os.path.dirname(os.path.abspath(__file__))

        # Global faker instance
        self.faker = Faker()

        # Initialize app
        self.app = app('equipment.framework.App.Container')

        # Override config
        self.app.config.override(LocalConfig(
            self.app.environment(),
            f'framework{os.sep}tests{os.sep}_stubs{os.sep}config'
        ))

        # Override logger
        self.app.log.override(NoneLog(config=self.app.config()))


if __name__ == '__main__':
    unittest.main()
