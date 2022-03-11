import unittest
from equipment.framework.tests.BaseTest import BaseTest
from equipment.framework.helpers import raise_if


class test_raise_if(BaseTest):
    def test_true(self):
        with self.assertRaises(ImportError):
            raise_if(True, ImportError('foo'))

    def test_false(self):
        self.assertIsNone(raise_if(False, ImportError('foo')))


if __name__ == '__main__':
    unittest.main()
