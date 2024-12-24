from typing import TYPE_CHECKING
from equipment.Queue.AbstractQueue import AbstractQueue
from equipment.Queue.SyncQueue import SyncQueue
from equipment.Queue.RedisQueue import RedisQueue

if TYPE_CHECKING:
    from datetime import datetime
    from equipment.Log.AbstractLogger import AbstractLogger


class QueueFactory(AbstractQueue):
    queue: AbstractQueue

    def __init__(self, config: dict, log: 'AbstractLogger'):
        if not hasattr(self, 'queue'):
            if config['connection'] == 'sync':
                self.queue = SyncQueue(log)
                return

            if config['connection'] == 'redis':
                self.queue = RedisQueue(config['connections']['redis'], log)
                return

            raise ValueError(f'Unknown queue connection type: {config["connection"]}')

    def push(self, method, *args, **kwargs) -> bool:
        return self.queue.push(method, *args, **kwargs)

    def push_at(self, date: 'datetime', method, *args, **kwargs) -> bool:
        return self.queue.push_at(date, method, *args, **kwargs)
