from sqlalchemy import create_engine
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Connection.SQLAlchemyConnection import SQLAlchemyConnection
from equipment.framework.Log.AbstractLog import AbstractLog


class PostgreSQLConnection(SQLAlchemyConnection):
    def __init__(self, config: AbstractConfig, log: AbstractLog, name: str = 'CONNECTION_POSTGRESQL'):
        super().__init__(config=config, log=log)
        self.name = name

    def connect(self) -> bool:
        try:
            # pylint: disable=consider-using-f-string
            self.connection = '''{schema}://{username}:{password}@{host}:{port}/{db}'''.format(
                schema=self.config.get(self.name, 'schema'),
                username=self.config.get(self.name, 'username'),
                password=self.config.get(self.name, 'password'),
                host=self.config.get(self.name, 'host'),
                port=self.config.get(self.name, 'port'),
                db=self.config.get(self.name, 'db'),
            )

            self.engine = create_engine(self.connection)

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False
