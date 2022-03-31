from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Storage.AbstractStorage import AbstractStorage
from equipment.framework.Storage.LocalStorage import LocalStorage
from equipment.framework.Storage.S3Storage import S3Storage


class StorageFactory(AbstractStorage):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        driver_name = config.get('STORAGE', 'driver')

        if driver_name == 'local':
            self.driver = LocalStorage(config, log)
        elif driver_name == 's3':
            self.driver = S3Storage(config, log)
        else:
            error = f'Storage driver "{driver_name}" is not supported'
            log.error(error)
            raise NotImplementedError(error)

    def path(self, file: str) -> str:
        return self.driver.path(file)

    def write(self, file: str, data: str) -> bool:
        return self.driver.write(file, data)

    def read(self, file: str) -> str:
        return self.driver.read(file)

    def exists(self, file: str) -> bool:
        return self.driver.exists(file)

    def remove(self, file: str) -> bool:
        return self.driver.remove(file)

    def move(self, source: str, destination: str) -> bool:
        return self.driver.move(source, destination)

    def list(self, path: str) -> bool:
        return self.driver.list(path)
