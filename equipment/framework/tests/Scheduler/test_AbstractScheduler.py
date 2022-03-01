import unittest
from equipment.framework.Scheduler.AbstractScheduler import AbstractScheduler
from tests.BaseTest import BaseTest


class test_AbstractScheduler(BaseTest):
    def test_abstract_methods(self):
        class TestScheduler(AbstractScheduler):
            pass

        with self.assertRaises(NotImplementedError):
            TestScheduler().run()


if __name__ == '__main__':
    unittest.main()
