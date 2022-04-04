from neo4j import GraphDatabase
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from equipment.framework.Log.AbstractLog import AbstractLog


class Neo4JConnection(AbstractConnection):
    def __init__(self, config: AbstractConfig, log: AbstractLog, name: str = 'CONNECTION_NEO4J'):
        self.config = config
        self.log = log
        self.driver = None
        self.name = name

    def load(self) -> None:
        if self.driver is None:
            self.reload()

    def reload(self) -> None:
        self.connect()

    def connect(self) -> bool:
        try:
            self.driver = GraphDatabase.driver(
                # pylint: disable=consider-using-f-string
                uri='''{schema}://{host}:{port}'''.format(
                    schema=self.config.get(self.name, 'schema'),
                    host=self.config.get(self.name, 'host'),
                    port=self.config.get(self.name, 'port'),
                ),
                auth=(
                    self.config.get(self.name, 'username'),
                    self.config.get(self.name, 'password'),
                ),
                encrypted=self.config.get(self.name, 'encrypted'),
            )

            self.log.debug(self.driver)

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def factory(self) -> GraphDatabase.driver:
        self.load()

        return self.driver
