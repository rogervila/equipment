from typing import TYPE_CHECKING
from datetime import datetime
from redis import Redis
from rq import Queue
from equipment.Queue.AbstractQueue import AbstractQueue

if TYPE_CHECKING:
    from equipment.Log.AbstractLogger import AbstractLogger


class RedisQueue(AbstractQueue):
    _queue: Queue

    def __init__(self, config: dict, log: 'AbstractLogger'):
        self.log = log
        self.config = config

        if not hasattr(self, '_queue'):
            redis = Redis(
                host=config['host'],
                port=int(config['port']),
                db=int(config['db']),
                # TODO: add more configurable properties
            )

            self._queue = Queue(connection=redis)

    def push(self, method, *args, **kwargs) -> bool:
        try:
            self._queue.enqueue(
                f=method,
                args=args,
                kwargs=kwargs
            )

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def push_at(self, date: 'datetime', method, *args, **kwargs) -> bool:
        try:
            self._queue.enqueue_at(
                datetime=date,
                f=method,
                args=args,
                kwargs=kwargs
            )

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False
