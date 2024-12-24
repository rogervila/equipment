from typing import TYPE_CHECKING
from equipment.Storage.AbstractStorage import AbstractStorage
from equipment.Storage.LocalStorage import LocalStorage

if TYPE_CHECKING:
    from equipment.Log.AbstractLogger import AbstractLogger


class StorageFactory(AbstractStorage):
    storage: AbstractStorage

    def __init__(self, config: dict, base_path: str, log: 'AbstractLogger'):
        if not hasattr(self, 'storage'):
            if config['disk'] == 'local':
                self.storage = LocalStorage(config['disks']['local'], base_path, log)
                return

            # TODO: S3Storage, FTPStorage, etc.

            raise ValueError(f'Unknown storage type type: {config["disk"]}')

    def path(self, file: str) -> str:
        return self.storage.path(file)

    def write(self, file: str, data: str) -> bool:
        return self.storage.write(file, data)

    def read(self, file: str) -> str:
        return self.storage.read(file)

    def exists(self, file: str) -> bool:
        return self.storage.exists(file)

    def remove(self, file: str) -> bool:
        return self.storage.remove(file)

    def move(self, source: str, destination: str) -> bool:
        return self.storage.move(source, destination)

    def list(self, path: str) -> list:
        return self.storage.list(path)
