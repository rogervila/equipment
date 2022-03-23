import unittest
from datetime import datetime
from equipment.framework.Queue.AbstractQueue import AbstractQueue
from equipment.framework.Queue.SyncQueue import SyncQueue
from equipment.framework.tests.TestCase import TestCase


class SyncQueueTest(TestCase):
    def setUp(self):
        super().setUp()
        self.queue = SyncQueue(
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
            def pass_test():
                return True

            def fail_test():
                raise Exception

            self.assertTrue(
                self.queue.push(pass_test)
            )

            self.assertFalse(
                self.queue.push(fail_test)
            )

            self.assertTrue(
                self.queue.pushOn(datetime.now(), pass_test)
            )

            self.assertFalse(
                self.queue.pushOn(datetime.now(), fail_test)
            )


if __name__ == '__main__':
    unittest.main()
