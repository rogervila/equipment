import unittest
from pathlib import Path
from equipment.framework.tests.BaseTest import BaseTest
from equipment.framework.helpers import base_path


class test_base_path(BaseTest):
    def test_base_path_returns_path_instance(self):
        result = base_path('foo', self.app)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result).endswith('foo'))


if __name__ == '__main__':
    unittest.main()
