from redis import Redis
from rq import Queue
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Queue.AbstractQueue import AbstractQueue


class RedisQueue(AbstractQueue):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
        self.log = log
        self.redis = None
        self.queue = None

    def load(self) -> None:
        if self.queue is None:
            self.reload()

    def reload(self) -> None:
        self.redis = Redis(
            host=self.config.get('QUEUE_REDIS', 'host'),
            port=self.config.get('QUEUE_REDIS', 'port'),
            db=self.config.get('QUEUE_REDIS', 'db'),
        )

        self.queue = Queue(connection=self.redis)

    def push(self, method, *args, **kwargs) -> bool:
        try:
            self.load()

            self.log.debug('RedisQueue@push method:')
            self.log.debug(method)
            self.log.debug('RedisQueue@push args:')
            self.log.debug(args)
            self.log.debug('RedisQueue@push kwargs:')
            self.log.debug(kwargs)

            self.queue.enqueue(
                f=method,
                args=args,
                kwargs=kwargs
            )

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False
