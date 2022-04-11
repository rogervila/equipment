import unittest
from pathlib import Path
from equipment.framework.tests.TestCase import TestCase
from equipment.framework.helpers import base_path


class BasePathHelperTest(TestCase):
    def test_base_path_returns_path_instance(self):
        result = base_path('foo', self.app)

        self.assertIsInstance(result, Path)
        self.assertTrue(str(result).endswith('foo'))

    def test_base_path_returns_expected_path(self):
        result = base_path('', self.app)

        self.assertIsInstance(result, Path)
        self.assertTrue(result.joinpath('.equipment').is_file())


if __name__ == '__main__':
    unittest.main()
