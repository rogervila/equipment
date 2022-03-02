from importlib import import_module
from typing import NoReturn
from sys import exit as _exit, modules
from pprint import pformat
from dependency_injector.containers import Container


def app(name: str = 'app.App.Container') -> Container:
    module = import_module(name) if name not in modules else modules[name]
    return module.Container


def dump(*args, **kwargs) -> None:
    pformat(*args, **kwargs)


def dd(*args, **kwargs) -> NoReturn:
    dump(*args, **kwargs)
    _exit()
