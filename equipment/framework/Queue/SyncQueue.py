from datetime import datetime
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Queue.AbstractQueue import AbstractQueue


class SyncQueue(AbstractQueue):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
        self.log = log

    def push(self, method, *args, **kwargs) -> bool:
        try:
            method(*args, **kwargs)
            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def pushOn(self, date: datetime, method, *args, **kwargs) -> bool:
        # SyncQueue ignores specific dates
        return self.push(method, *args, **kwargs)
