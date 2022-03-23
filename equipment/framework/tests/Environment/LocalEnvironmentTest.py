import unittest
from equipment.framework.Environment.AbstractEnvironment import AbstractEnvironment
from equipment.framework.Environment.LocalEnvironment import LocalEnvironment
from equipment.framework.tests.TestCase import TestCase


class LocalEnvironmentTest(TestCase):
    def setUp(self):
        super().setUp()
        self.env = LocalEnvironment()

    def test_extends_from_abstract_environment(self):
        with self.app.environment.override(self.env):
            self.assertTrue(
                isinstance(self.app.environment(), AbstractEnvironment)
            )

    def test_returns_list_with_env_variables(self):
        with self.app.environment.override(self.env):
            result = self.app.environment().all()

            self.assertEqual(
                type(result),
                type([])
            )

            if len(result) > 0:
                self.assertEqual(
                    type(result[0]),
                    type({})
                )


if __name__ == '__main__':
    unittest.main()
