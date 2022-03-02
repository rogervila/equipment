import unittest
from equipment.framework.Environment.AbstractEnvironment import AbstractEnvironment
from equipment.framework.tests.BaseTest import BaseTest


class test_LocalEnvironment(BaseTest):
    def test_abstract_methods(self):
        class TestEnvironment(AbstractEnvironment):
            pass

        with self.assertRaises(NotImplementedError):
            TestEnvironment().all()

        with self.assertRaises(NotImplementedError):
            TestEnvironment().set('foo', 'xyz')

        with self.assertRaises(NotImplementedError):
            TestEnvironment().get('foo')


if __name__ == '__main__':
    unittest.main()
