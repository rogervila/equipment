from sys import exit as _exit
from time import sleep
import schedule
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Scheduler.AbstractScheduler import AbstractScheduler


class Scheduler(AbstractScheduler):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
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
