import unittest
from equipment.Scheduler.AbstractScheduler import AbstractScheduler


class AbstractSchedulerTest(unittest.TestCase):
    def test_abstract_methods(self):
        class TestScheduler(AbstractScheduler):
            pass

        with self.assertRaises(NotImplementedError):
            TestScheduler().run()


if __name__ == '__main__':
    unittest.main()
