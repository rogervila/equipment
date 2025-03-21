import os
from glob import glob

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import ThreadSafeSingleton as Singleton, Configuration
from dotenv import load_dotenv
from cachetools import cached

from equipment.Database.SQLAlchemyFactory import SQLAlchemyFactory
from equipment.Log.LoggerFactory import LoggerFactory
from equipment.Queue.QueueFactory import QueueFactory
from equipment.Storage.StorageFactory import StorageFactory


def _load_environment(base_path: str) -> None:
    env_file = os.path.join(base_path, '.env')

    if os.path.isfile(env_file):
        load_dotenv(env_file)


def _config_files_list(base_path: str, extension: str) -> list[str]:
    return glob(
        os.path.join(
            base_path,
            'config',
            extension
        )
    )


class Equipment(DeclarativeContainer):
    # Ensure that no unexpected arguments are passed to the __new__ constructor.
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @classmethod
    @cached({})
    def make(cls, base_path: tuple[str, None] = None):
        base_path = base_path if base_path is not None else os.getcwd()
        _load_environment(base_path)
        instance = cls()

        for file in _config_files_list(base_path, '*.ini'):
            instance.config.from_ini(file)

        for file in _config_files_list(base_path, '*.yaml'):
            instance.config.from_yaml(file)

        for file in _config_files_list(base_path, '*.json'):
            instance.config.from_json(file)

        instance.config.base_path.from_value(base_path)

        assert instance.config.base_path() == base_path

        return instance

    config = Configuration()

    log = Singleton(
        LoggerFactory, config.app.name, config.base_path, config.log
    )

    queue = Singleton(
        QueueFactory, config.queue, log
    )

    storage = Singleton(
        StorageFactory, config.storage, config.base_path, log
    )

    database = Singleton(
        SQLAlchemyFactory, config.database, config.base_path, log
    )


def equipment(base_path: tuple[str, None] = None) -> Equipment:
    return Equipment.make(base_path)


def cli() -> None:
    from equipment.Command import main as _cli
    _cli()
