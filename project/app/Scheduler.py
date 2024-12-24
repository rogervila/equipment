from typing import TYPE_CHECKING
from equipment.Scheduler.Scheduler import Scheduler as Equipment

if TYPE_CHECKING:
    from equipment.Log.AbstractLogger import AbstractLogger
    from equipment.Queue.AbstractQueue import AbstractQueue
    from app.Inspire import Inspire


# Schedule setup (https://schedule.readthedocs.io/en/stable/)


def _inspire(log: 'AbstractLogger', inspiring: 'Inspire'):
    log.info(inspiring.quote())


class Scheduler(Equipment):
    def __init__(self, log: 'AbstractLogger', queue: 'AbstractQueue', inspiring: 'Inspire'):
        super().__init__(log)
        self.queue = queue
        self.inspiring = inspiring

    def run(self) -> None:
        # Example without queues
        self.schedule.every(5).seconds.do(
            _inspire, self.log, self.inspiring
        )

        # Example with queues
        self.schedule.every(5).seconds.do(
            self.queue.push, _inspire, self.log, self.inspiring
        )

        super().run()
