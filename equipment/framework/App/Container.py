from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from equipment.framework.Config.ConfigFactory import ConfigFactory
from equipment.framework.Environment.EnvironmentFactory import EnvironmentFactory
from equipment.framework.Log.LogFactory import LogFactory
from equipment.framework.Mail.MailFactory import MailFactory
from equipment.framework.Queue.QueueFactory import QueueFactory
from equipment.framework.Storage.StorageFactory import StorageFactory


class Container(DeclarativeContainer):
    environment = Singleton(EnvironmentFactory)
    config = Singleton(ConfigFactory, environment)
    log = Singleton(LogFactory, config)
    queue = Singleton(QueueFactory, config, log)
    storage = Singleton(StorageFactory, config, log)
    mail = Singleton(MailFactory, config, log)
