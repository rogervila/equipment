from os import sep
import unittest
from equipment.framework.App.Container import Container
from equipment.framework.Log.NoneLog import NoneLog
from equipment.framework.Config.LocalConfig import LocalConfig


class BaseTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

        # Initialize app
        self.app = Container()

        # Override config
        self.app.config.override(LocalConfig(
            self.app.environment(),
            f'tests{sep}_stubs{sep}config'
        ))

        # Override logger
        self.app.log.override(NoneLog(self.app.config))


if __name__ == '__main__':
    unittest.main()
