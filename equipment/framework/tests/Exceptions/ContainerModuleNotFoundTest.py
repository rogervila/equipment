import unittest
from equipment.framework.tests.TestCase import TestCase
from equipment.framework.helpers import app
from equipment.framework.Exceptions.ContainerModuleNotFound import ContainerModuleNotFound


class ContainerModuleNotFoundTest(TestCase):
    def test_error_is_raised(self):
        with self.assertRaises(ContainerModuleNotFound):
            app('foo', autodiscover=False)


if __name__ == '__main__':
    unittest.main()
