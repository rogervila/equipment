import unittest
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from equipment.framework.tests.TestCase import TestCase


class AbstractConnectionTest(TestCase):
    def test_abstract_methods(self):
        class TestConnection(AbstractConnection):
            pass

        with self.assertRaises(NotImplementedError):
            TestConnection().connect()

        with self.assertRaises(NotImplementedError):
            TestConnection().load()

        with self.assertRaises(NotImplementedError):
            TestConnection().reload()


if __name__ == '__main__':
    unittest.main()
