from importlib import import_module
from typing import Any, NoReturn
from sys import exit as _exit, modules as _modules
from pprint import pformat
from dependency_injector.containers import Container


def app(name: str = 'app.App.Container') -> Container:
    resolved_module = module(name)
    return resolved_module.Container


def module(name: str, print_exception: bool = False) -> Any:
    try:
        return import_module(name) if name not in _modules else _modules[name]
    except Exception as e:
        print_if(print_exception, e)
        return None


def print_if(condition: bool, *args, **kwargs) -> None:
    if condition:
        print(*args, **kwargs)


def print_unless(condition: bool, *args, **kwargs) -> None:
    if not condition:
        print(*args, **kwargs)


def dump(*args, **kwargs) -> None:
    pformat(*args, **kwargs)


def dd(*args, **kwargs) -> NoReturn:
    dump(*args, **kwargs)
    _exit()
