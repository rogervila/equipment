import unittest
from equipment.framework.Jobs.AbstractJob import AbstractJob
from equipment.framework.tests.BaseTest import BaseTest
from equipment.framework.helpers import app


class test_AbstractJob(BaseTest):
    def test_dispatch(self):
        class TestJob(AbstractJob):
            pass

        self.assertIsNone(TestJob().dispatchWithContainer(app('equipment.framework.App.Container'), 1, 2, 3))  # nopep8


if __name__ == '__main__':
    unittest.main()
