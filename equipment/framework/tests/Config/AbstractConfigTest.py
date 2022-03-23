import unittest
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.tests.TestCase import TestCase


class AbstractConfigTest(TestCase):
    def test_abstract_methods(self):
        class TestConfig(AbstractConfig):
            pass

        with self.assertRaises(NotImplementedError):
            TestConfig().reload()

        with self.assertRaises(NotImplementedError):
            TestConfig().set('foo', 'bar', 'xyz')

        with self.assertRaises(NotImplementedError):
            TestConfig().get('foo', 'bar')


if __name__ == '__main__':
    unittest.main()
