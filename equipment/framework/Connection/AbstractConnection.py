import abc


class AbstractConnection(abc.ABC):
    def connect(self) -> bool:
        raise NotImplementedError

    def load(self) -> None:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError
