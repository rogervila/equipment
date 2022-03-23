import unittest
from datetime import datetime
from equipment.framework.Queue.AbstractQueue import AbstractQueue
from equipment.framework.tests.TestCase import TestCase


class AbstractQueueTest(TestCase):
    def test_abstract_methods(self):
        class TestQueue(AbstractQueue):
            pass

        def test_method():
            return True

        with self.assertRaises(NotImplementedError):
            TestQueue().push(test_method)

        with self.assertRaises(NotImplementedError):
            TestQueue().pushOn(datetime.now(), test_method)


if __name__ == '__main__':
    unittest.main()
