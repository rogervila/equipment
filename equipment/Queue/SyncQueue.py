from typing import TYPE_CHECKING
from equipment.Queue.AbstractQueue import AbstractQueue

if TYPE_CHECKING:
    from datetime import datetime
    from equipment.Log.AbstractLogger import AbstractLogger


class SyncQueue(AbstractQueue):
    def __init__(self, log: 'AbstractLogger'):
        self.log = log

    def push(self, method, *args, **kwargs) -> bool:
        try:
            method(*args, **kwargs)
            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def push_at(self, date: 'datetime', method, *args, **kwargs) -> bool:
        # SyncQueue ignores specific dates
        return self.push(method, *args, **kwargs)
