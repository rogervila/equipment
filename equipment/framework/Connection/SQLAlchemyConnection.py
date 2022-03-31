from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from equipment.framework.Log.AbstractLog import AbstractLog


class SQLAlchemyConnection(AbstractConnection):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
        self.log = log
        self.engine = None
        self.connection = None

    def load(self) -> None:
        if self.engine is None:
            self.reload()

    def reload(self) -> None:
        self.connect()

    # Connections are handled on specific implementations like SQLiteConnection, etc.
    def connect(self) -> bool:
        raise NotImplementedError

    def url(self) -> str:
        self.load()
        return self.connection

    def factory(self) -> engine.base.Engine:
        self.load()
        return self.engine

    def session(self) -> Session:
        self.load()
        _session = sessionmaker(bind=self.engine)
        return _session()
