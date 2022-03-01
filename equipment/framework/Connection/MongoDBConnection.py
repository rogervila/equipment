from pymongo import MongoClient, database
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from equipment.framework.Log.AbstractLog import AbstractLog


class MongoDBConnection(AbstractConnection):
    def __init__(self, config: AbstractConfig, log: AbstractLog, name: str = 'CONNECTION_MONGODB'):
        self.config = config
        self.log = log
        self.client = None
        self.name = name

    def load(self) -> None:
        if self.client is None:
            self.reload()

    def reload(self) -> None:
        self.connect()

    def connect(self) -> bool:
        try:
            self.client = MongoClient(
                host=self.config.get(self.name, 'host'),
                port=self.config.get(self.name, 'port'),
                username=self.config.get(self.name, 'username'),
                password=self.config.get(self.name, 'password'),
                authSource=self.config.get(self.name, 'auth_source'),
                authMechanism=self.config.get(self.name, 'auth_mechanism'),
            )

            self.log.debug(self.client)

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def factory(self, connection_name=None) -> database.Database:
        self.load()

        return self.client[self.config.get(self.name, 'db') if connection_name is None else connection_name]
