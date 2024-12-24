from typing import TYPE_CHECKING
from sys import exit as _exit
from time import sleep
import schedule
from equipment.Scheduler.AbstractScheduler import AbstractScheduler

if TYPE_CHECKING:
    from equipment.Log.AbstractLogger import AbstractLogger


class Scheduler(AbstractScheduler):
    def __init__(self, log: 'AbstractLogger'):
        self.log = log
        self.should_exit = False
        self.schedule = schedule.Scheduler()

    def run(self) -> None:
        self.log.info('Starting scheduler...')

        while True:
            try:
                self.schedule.run_pending()
                sleep(1)

                if self.should_exit:
                    break

            except KeyboardInterrupt:
                self.log.info('Stopping scheduler...')
                _exit()
