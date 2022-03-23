import unittest
from equipment.framework.tests.TestCase import TestCase
from equipment.framework.helpers import raise_if


class RaseIfHelperTest(TestCase):
    def test_true(self):
        with self.assertRaises(ImportError):
            raise_if(True, ImportError('foo'))

    def test_false(self):
        self.assertIsNone(raise_if(False, ImportError('foo')))


if __name__ == '__main__':
    unittest.main()
