from typing import TYPE_CHECKING
from equipment.Scheduler.Scheduler import Scheduler as Equipment

if TYPE_CHECKING:
    from equipment.Log.AbstractLogger import AbstractLogger
    from equipment.Queue.AbstractQueue import AbstractQueue
    from app.Inspire import Inspire

def _inspire(log: 'AbstractLogger', inspiring: 'Inspire'):
    log.info(inspiring.quote())

class Scheduler(Equipment):
    """
    Schedule docs available in https://schedule.readthedocs.io/en/stable/
    """

    def __init__(self, log: 'AbstractLogger', queue: 'AbstractQueue', inspiring: 'Inspire'):
        super().__init__(log)
        self.queue = queue
        self.inspiring = inspiring

    def run(self) -> None:
        # Example without queues
        self.schedule.every(1).seconds.do(
            lambda: self.log.debug(self.inspiring.quote())
        )

        # Example with queues
        self.schedule.every(5).seconds.do(
            self.queue.push, _inspire, self.log, self.inspiring
        )

        super().run()
