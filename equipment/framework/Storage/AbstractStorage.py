import abc


class AbstractStorage(abc.ABC):
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
