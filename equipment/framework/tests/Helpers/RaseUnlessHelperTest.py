import unittest
from equipment.framework.tests.TestCase import TestCase
from equipment.framework.helpers import raise_unless


class RaseUnlessHelperTest(TestCase):
    def test_true(self):
        with self.assertRaises(ImportError):
            raise_unless(False, ImportError('foo'))

    def test_false(self):
        self.assertIsNone(raise_unless(True, ImportError('foo')))


if __name__ == '__main__':
    unittest.main()
