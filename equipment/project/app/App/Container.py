from dependency_injector.providers import Singleton
from app.Scheduler.Scheduler import Scheduler
from equipment.framework.App.Container import Container as E
from equipment.framework.Connection.SQLiteConnection import SQLiteConnection


class Container(E):
    scheduler = Singleton(Scheduler, E.config, E.log)  # nopep8

    # Available SQL connections: SQLServerConnection, MySQLConnection, PostgreSQLConnection
    sql = Singleton(SQLiteConnection, E.config, E.log)

    # Other Connections are also available:
    # mongo = Singleton(MongoDBConnection, E.config, E.log)
    # neo4j = Singleton(Neo4JConnection, E.config, E.log)
    # redis = Singleton(RedisConnection, E.config, E.log)

    # CUSTOMIZE CONNECTIONS:
    #
    # You can create your own connection variant by specifying the config
    # section where the connection parameters should be read from
    #
    # $ my_sqlite = Singleton(SQLiteConnection, config, log, 'CONFIG_SECTION')

    # APPEND CUSTOM SINGLETONS
    #
    # Custom classes and functions can be provided by the container
    #
    # $ myservice = Singleton(MyService, config, log)
    #
    # Now you can call app.myservice() to get the singleton instance
