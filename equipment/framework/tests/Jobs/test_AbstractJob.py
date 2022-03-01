import unittest
from equipment.framework.Jobs.AbstractJob import AbstractJob
from tests.BaseTest import BaseTest


class test_AbstractJob(BaseTest):
    def test_abstract_methods(self):
        class TestJob(AbstractJob):
            pass

        with self.assertRaises(NotImplementedError):
            TestJob().run(1, 2, 3)


if __name__ == '__main__':
    unittest.main()
