from datetime import datetime
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Queue.AbstractQueue import AbstractQueue
from equipment.framework.Queue.SyncQueue import SyncQueue
from equipment.framework.Queue.RedisQueue import RedisQueue


class QueueFactory(AbstractQueue):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        driver_name = config.get('QUEUE', 'driver')

        if driver_name == 'sync':
            self.driver = SyncQueue(config, log)
        elif driver_name == 'redis':
            self.driver = RedisQueue(config, log)
        else:
            error = f'Queue driver "{driver_name}" is not supported'
            log.error(error)
            raise NotImplementedError(error)

    def push(self, method, *args, **kwargs) -> bool:
        return self.driver.push(method, *args, **kwargs)

    def pushOn(self, date: datetime, method, *args, **kwargs) -> bool:
        return self.driver.pushOn(date, method, *args, **kwargs)
