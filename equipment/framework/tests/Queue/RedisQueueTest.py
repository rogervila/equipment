import unittest
from unittest.mock import MagicMock
from equipment.framework.Queue.AbstractQueue import AbstractQueue
from equipment.framework.Queue.RedisQueue import RedisQueue
from equipment.framework.tests.TestCase import TestCase


class RedisQueueTest(TestCase):
    def setUp(self):
        super().setUp()
        self.queue = RedisQueue(
            config=self.app.config(),
            log=self.app.log(),
        )

    def test_extends_from_abstract_queue(self):
        with self.app.queue.override(self.queue):
            self.assertTrue(
                isinstance(self.app.queue(), AbstractQueue)
            )

    def test_enqueues_methods(self):
        with self.app.queue.override(self.queue):
            def method_test():
                return True

            self.queue.redis = MagicMock()
            self.queue.queue = MagicMock()

            self.assertTrue(
                self.queue.push(method_test)
            )

            self.queue.queue.enqueue = MagicMock(side_effect=Exception())

            self.assertFalse(
                self.queue.push(method_test)
            )


if __name__ == '__main__':
    unittest.main()
