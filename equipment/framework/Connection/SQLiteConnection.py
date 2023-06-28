import os
from sqlalchemy import create_engine
from equipment.framework.Connection.SQLAlchemyConnection import SQLAlchemyConnection
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Log.AbstractLog import AbstractLog


class SQLiteConnection(SQLAlchemyConnection):
    def __init__(self, config: AbstractConfig, log: AbstractLog, name: str = 'CONNECTION_SQLITE'):
        super().__init__(config=config, log=log)
        self.memory = ':memory:'
        self.name = name

    def connect(self) -> bool:
        try:
            schema = self.config.get(self.name, 'schema')
            path = self.config.get(self.name, 'path')
            base_path = os.path.join(os.getcwd(), '../') if os.path.isfile(os.path.join(os.getcwd(), 'alembic.ini')) else os.getcwd()

            db = path if path == self.memory else os.path.join(
                base_path,
                path
            )

            if db != self.memory and not os.path.isfile(db):
                raise FileNotFoundError(db)

            self.connection = f'{schema}:///{db}'
            self.engine = create_engine(self.connection)

            self.log.debug(self.engine)

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False
