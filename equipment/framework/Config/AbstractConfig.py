import abc
from typing import Any


class AbstractConfig(abc.ABC):
    def load(self) -> None:
        raise NotImplementedError

    def reload(self) -> None:
        raise NotImplementedError

    def set(self, section: str, key: str, value) -> None:
        raise NotImplementedError

    def get(self, section: str, key: str) -> Any:
        raise NotImplementedError
