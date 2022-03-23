import unittest
from equipment.framework.Jobs.AbstractJob import AbstractJob
from app.Jobs.ExampleJob import ExampleJob
from tests.TestCase import TestCase


class test_ExampleJob(TestCase):
    def test_extends_from_abstract_job(self):
        self.assertTrue(
            isinstance(ExampleJob(), AbstractJob)
        )


if __name__ == '__main__':
    unittest.main()
