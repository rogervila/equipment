import unittest
from equipment.framework.Storage.AbstractStorage import AbstractStorage
from equipment.framework.tests.TestCase import TestCase


class AbstractStorageTest(TestCase):
    def test_abstract_methods(self):
        class TestStorage(AbstractStorage):
            pass

        with self.assertRaises(NotImplementedError):
            TestStorage().write('a', 'b')

        with self.assertRaises(NotImplementedError):
            TestStorage().read('a')

        with self.assertRaises(NotImplementedError):
            TestStorage().exists('a')

        with self.assertRaises(NotImplementedError):
            TestStorage().remove('a')


if __name__ == '__main__':
    unittest.main()
