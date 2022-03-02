from redis import Redis
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from equipment.framework.Log.AbstractLog import AbstractLog


class RedisConnection(AbstractConnection):
    def __init__(self, config: AbstractConfig, log: AbstractLog, name: str = 'CONNECTION_REDIS'):
        self.config = config
        self.log = log
        self.redis = None
        self.name = name

    def load(self) -> None:
        if self.redis is None:
            self.reload()

    def reload(self) -> None:
        self.connect()

    def connect(self) -> bool:
        try:
            self.redis = Redis(
                host=self.config.get(self.name, 'host'),
                port=self.config.get(self.name, 'port'),
                db=self.config.get(self.name, 'db'),
            )

            self.log.debug(self.redis)

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def factory(self) -> Redis:
        self.load()

        return self.redis
