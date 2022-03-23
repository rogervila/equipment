import unittest
from equipment.framework.Scheduler.AbstractScheduler import AbstractScheduler
from equipment.framework.tests.TestCase import TestCase


class AbstractSchedulerTest(TestCase):
    def test_abstract_methods(self):
        class TestScheduler(AbstractScheduler):
            pass

        with self.assertRaises(NotImplementedError):
            TestScheduler().run()


if __name__ == '__main__':
    unittest.main()
