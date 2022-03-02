import abc
from typing import Any


class AbstractEnvironment(abc.ABC):
    def get(self, key: str) -> Any:
        raise NotImplementedError

    def set(self, key: str, value) -> None:
        raise NotImplementedError

    def all(self) -> list:
        raise NotImplementedError
