import unittest
from equipment.framework.Jobs.AbstractJob import AbstractJob
from app.Jobs.ExampleJob import ExampleJob
from equipment.framework.tests.BaseTest import BaseTest


class test_ExampleJob(BaseTest):
    def test_extends_from_abstract_job(self):
        self.assertTrue(
            isinstance(ExampleJob(), AbstractJob)
        )


if __name__ == '__main__':
    unittest.main()
