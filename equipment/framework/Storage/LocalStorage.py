import codecs
import os
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Storage.AbstractStorage import AbstractStorage


class LocalStorage(AbstractStorage):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
        self.log = log

    def base_path(self) -> str:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../../',
            self.config.get('STORAGE_LOCAL', 'path')
        )

    def path(self, file: str) -> str:
        return os.path.join(
            self.base_path(),
            file
        )

    def write(self, file: str, data: str) -> bool:
        try:
            file = self.path(file)

            self.log.debug('LocalStorage@write file: ' + str(file))

            os.makedirs(
                os.path.dirname(file),
                exist_ok=True
            )

            with codecs.open(file, 'w') as filepath:
                filepath.write(data)

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def read(self, file: str) -> str:
        file = self.path(file)
        self.log.debug('file: ' + file)

        with codecs.open(file, 'r') as filepath:
            return filepath.read()

    def exists(self, file: str) -> bool:
        return os.path.isfile(self.path(file))

    def remove(self, file: str) -> bool:
        try:
            os.remove(self.path(file))
            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def move(self, source: str, destination: str) -> bool:
        try:
            os.rename(
                self.path(source),
                self.path(destination)
            )
            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def list(self, path: str) -> list:
        path = os.path.join(self.base_path(), path)

        if not os.path.isdir(path):
            raise NotADirectoryError(f'{path} is not a directory')

        return [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]  # nopep8
