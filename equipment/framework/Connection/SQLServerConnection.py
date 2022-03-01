from sqlalchemy import create_engine
from equipment.framework.Connection.SQLAlchemyConnection import SQLAlchemyConnection
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Log.AbstractLog import AbstractLog


class SQLServerConnection(SQLAlchemyConnection):
    def __init__(self, config: AbstractConfig, log: AbstractLog, name: str = 'CONNECTION_SQLSERVER'):
        super().__init__(config=config, log=log)
        self.name = name

    def connect(self) -> bool:
        try:
            self.connection = '''mssql+pyodbc://{username}:{password}@{host}:{port}/{db}?driver=ODBC+Driver+17+for+SQL+Server'''.format(
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
