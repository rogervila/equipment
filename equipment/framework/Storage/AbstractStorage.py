import abc


class AbstractStorage(abc.ABC):
    def base_path(self) -> str:
        raise NotImplementedError

    def path(self, file: str) -> str:
        raise NotImplementedError

    def write(self, file: str, data: str) -> bool:
        raise NotImplementedError

    def read(self, file: str) -> str:
        raise NotImplementedError

    def exists(self, file: str) -> bool:
        raise NotImplementedError

    def remove(self, file: str) -> bool:
        raise NotImplementedError

    def move(self, source: str, destination: str) -> bool:
        raise NotImplementedError

    def list(self, path: str) -> list:
        raise NotImplementedError
