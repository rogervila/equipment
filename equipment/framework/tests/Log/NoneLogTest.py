import unittest
from uuid import uuid4
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Log.NoneLog import NoneLog
from equipment.framework.tests.TestCase import TestCase


class NoneLogTest(TestCase):
    def setUp(self):
        super().setUp()
        self.log = NoneLog(self.app.config())

    def test_extends_from_abstract_log(self):
        with self.app.log.override(self.log):
            self.assertTrue(
                isinstance(self.app.log(), AbstractLog)
            )

    def test_returns_none(self):
        with self.app.log.override(self.log):
            message = str(uuid4())

            self.assertIsNone(
                self.app.log().debug(message)
            )

            self.assertIsNone(
                self.app.log().info(message)
            )

            self.assertIsNone(
                self.app.log().warning(message)
            )

            self.assertIsNone(
                self.app.log().error(message)
            )

            self.assertIsNone(
                self.app.log().critical(message)
            )


if __name__ == '__main__':
    unittest.main()
