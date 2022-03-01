from importlib import import_module
from typing import NoReturn
from sys import exit as _exit
from pprint import pformat
from dependency_injector.containers import Container


def app() -> Container:
    module = import_module('app.App.Container')
    return module.Container


def dump(*args, **kwargs) -> None:
    pformat(*args, **kwargs)


def dd(*args, **kwargs) -> NoReturn:
    dump(*args, **kwargs)
    _exit()
