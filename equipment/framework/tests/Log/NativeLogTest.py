import unittest
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Log.NativeLog import NativeLog
from equipment.framework.tests.TestCase import TestCase


class NativeLogTest(TestCase):
    def test_extends_from_abstract_log(self):
        with self.app.log.override(NativeLog(config=self.app.config())):
            self.assertTrue(
                isinstance(self.app.log(), AbstractLog)
            )

    def test_properties_are_not_implemented(self):
        with self.app.log.override(NativeLog(config=self.app.config())):
            with self.assertRaises(NotImplementedError):
                self.app.log().get_handlers()

            with self.assertRaises(NotImplementedError):
                self.app.log().get_level()

            with self.assertRaises(NotImplementedError):
                self.app.log().get_name()


if __name__ == '__main__':
    unittest.main()
