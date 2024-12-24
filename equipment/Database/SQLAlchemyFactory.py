import os
from typing import TYPE_CHECKING
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from sqlalchemy import Engine, TextClause
    from sqlalchemy.orm.session import Session
    from equipment.Log.AbstractLogger import AbstractLogger


def _create_sqlite_url(config: dict, base_path: str) -> str:
    schema = config['schema']
    database = '' if config['database'] == ':memory:' else os.path.join(
        base_path,
        config['database']
    )

    return f"{schema}://" if database == '' else f"{schema}:///{database}"


def _create_mysql_url(config: dict) -> str:
    return f"{config['schema']}://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset={config['charset']}"


def _create_postgresql_url(config: dict) -> str:
    return f"{config['schema']}://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"


class SQLAlchemyFactory:
    url: str
    session_maker: sessionmaker
    engine: 'Engine'

    def __init__(self, config: dict, base_path: str, log: 'AbstractLogger'):
        if not hasattr(self, 'session_maker'):
            if config['connection'] == 'sqlite':
                self.url = _create_sqlite_url(config['connections']['sqlite'], base_path)
            elif config['connection'] == 'mysql':
                self.url = _create_mysql_url(config['connections']['mysql'])
            elif config['connection'] == 'postgresql':
                self.url = _create_postgresql_url(config['connections']['postgresql'])
            else:
                raise ValueError(f'Unknown queue connection type: {config["connection"]}')

            self.engine = create_engine(self.url)
            self.session_maker = sessionmaker(bind=self.engine)

    def session(self) -> 'Session':
        return self.session_maker()

    @staticmethod
    def text(query: str) -> 'TextClause':
        return text(query)
