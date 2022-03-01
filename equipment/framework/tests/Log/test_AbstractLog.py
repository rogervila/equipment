import unittest
from equipment.framework.Log.AbstractLog import AbstractLog
from tests.BaseTest import BaseTest


class test_AbstractLog(BaseTest):
    def test_abstract_methods(self):
        class TestLog(AbstractLog):
            pass

        with self.assertRaises(NotImplementedError):
            TestLog().debug()

        with self.assertRaises(NotImplementedError):
            TestLog().info()

        with self.assertRaises(NotImplementedError):
            TestLog().warning()

        with self.assertRaises(NotImplementedError):
            TestLog().error()

        with self.assertRaises(NotImplementedError):
            TestLog().critical()


if __name__ == '__main__':
    unittest.main()
