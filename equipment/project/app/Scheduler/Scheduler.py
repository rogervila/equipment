from app.Jobs.ExampleJob import ExampleJob
from equipment.framework.Scheduler.Scheduler import Scheduler as BScheduler

# Schedule setup (https://schedule.readthedocs.io/en/stable/)


class Scheduler(BScheduler):
    def run(self) -> None:
        self.schedule.every(1).seconds.do(
            self.log.info, 'Logging from scheduler'
        )

        self.schedule.every(1).seconds.do(
            ExampleJob.dispatchSync, 'not enqueued message'
        )

        self.schedule.every(1).seconds.do(
            ExampleJob.dispatch, 'enqueued message'
        )

        super().run()
