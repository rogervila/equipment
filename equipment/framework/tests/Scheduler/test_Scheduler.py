import time
import unittest
from unittest.mock import patch
import schedule
from equipment.framework.Scheduler.AbstractScheduler import AbstractScheduler
from equipment.framework.Scheduler.Scheduler import Scheduler
from tests.BaseTest import BaseTest


class test_Scheduler(BaseTest):
    def setUp(self):
        super().setUp()

        self.scheduler = Scheduler(
            config=self.app.config(),
            log=self.app.log(),
            queue=self.app.queue()
        )
        self.scheduler.should_exit = True

    def test_extends_from_abstract_Scheduler(self):
        with self.app.scheduler.override(self.scheduler):
            self.assertTrue(
                isinstance(self.app.scheduler(), AbstractScheduler)
            )

    def test_returns_none(self):
        with self.app.scheduler.override(self.scheduler):
            with patch.object(schedule, 'run_pending', return_value=None):
                with patch.object(time, 'sleep', return_value=None):
                    self.assertIsNone(self.app.scheduler().run())


if __name__ == '__main__':
    unittest.main()
