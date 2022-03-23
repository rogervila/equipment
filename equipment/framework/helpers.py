from importlib import import_module
from inspect import getfile
from pathlib import Path
from typing import Any, NoReturn, Optional
from sys import exit as _exit, modules as _modules
from pprint import pformat
from dependency_injector.containers import Container
from equipment.framework.Exceptions.ContainerModuleNotFound import ContainerModuleNotFound


def app(name: str = 'app.App.Container', autodiscover: bool = True) -> Container:
    resolved_module = module(name)
    
    # Fallback framework module
    if autodiscover and resolved_module is None:
        resolved_module = module('equipment.framework.App.Container')

    raise_if(resolved_module is None, ContainerModuleNotFound(name))

    return resolved_module.Container


def base_path(join: Optional[str] = None, container: Optional[Container] = None) -> Path:
    if container is None:
        container = app()

    # We assume containers always leave under ./app/App/Container
    return Path(getfile(container)).parent.parent.parent.absolute().joinpath(
        join if join is not None else ''
    )


def module(name: str, print_exception: bool = False) -> Any:
    try:
        return import_module(name) if name not in _modules else _modules[name]
    except Exception as e:
        print_if(print_exception, e)
        return None


def raise_if(condition: bool, exception: Exception) -> None:
    if condition:
        raise exception


def raise_unless(condition: bool, exception: Exception) -> None:
    if not condition:
        raise exception


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
