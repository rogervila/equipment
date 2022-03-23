import unittest
from equipment.framework.tests.TestCase import TestCase
from equipment.framework.helpers import module


class ModuleHelperTest(TestCase):
    def test_module_helper_returns_module(self):
        result = module('equipment.framework.tests.TestCase')
        self.assertIsNotNone(result)

    def test_module_helper_returns_none_when_module_not_found(self):
        result = module('this_module_does_not_exist')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
