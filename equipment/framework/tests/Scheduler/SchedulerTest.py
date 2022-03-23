import time
import unittest
from unittest.mock import patch
import schedule
from equipment.framework.Scheduler.AbstractScheduler import AbstractScheduler
from equipment.framework.Scheduler.Scheduler import Scheduler
from equipment.framework.tests.TestCase import TestCase


class SchedulerTest(TestCase):
    def setUp(self):
        super().setUp()

        self.scheduler = Scheduler(
            config=self.app.config(),
            log=self.app.log()
        )
        self.scheduler.should_exit = True

    def test_returns_none(self):
        with patch.object(schedule.Scheduler, 'run_pending', return_value=None):
            with patch.object(time, 'sleep', return_value=None):
                self.assertIsNone(self.scheduler.run())


if __name__ == '__main__':
    unittest.main()
