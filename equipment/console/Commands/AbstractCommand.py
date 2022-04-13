import abc
from typing import Any, Optional
from equipment.framework.helpers import module


class AbstractCommand(abc.ABC):
    def run(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def console(self, method_name: Optional[str] = None) -> Any:
        _console = module('equipment.console')

        if method_name is None:
            return _console

        return getattr(_console, method_name)
