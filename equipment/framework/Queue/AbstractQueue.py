import abc
from datetime import datetime


class AbstractQueue(abc.ABC):
    def push(self, method, *args, **kwargs) -> bool:
        raise NotImplementedError

    def pushOn(self, date: datetime, method, *args, **kwargs) -> bool:
        raise NotImplementedError
