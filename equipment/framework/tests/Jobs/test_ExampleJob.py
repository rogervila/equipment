import unittest
from equipment.framework.Jobs.AbstractJob import AbstractJob
from equipment.framework.Jobs.ExampleJob import ExampleJob
from tests.BaseTest import BaseTest


class test_ExampleJob(BaseTest):
    def test_extends_from_abstract_job(self):
        self.assertTrue(
            isinstance(ExampleJob(), AbstractJob)
        )

    def test_returns_none(self):
        self.assertIsNone(ExampleJob.run('test'))


if __name__ == '__main__':
    unittest.main()
