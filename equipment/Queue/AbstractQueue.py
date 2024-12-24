import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


class AbstractQueue(abc.ABC):
    def push(self, method, *args, **kwargs) -> bool:
        raise NotImplementedError

    def push_at(self, date: 'datetime', method, *args, **kwargs) -> bool:
        raise NotImplementedError
