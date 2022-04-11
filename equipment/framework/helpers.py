from importlib import import_module
from inspect import getfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn, Optional
from sys import exit as _exit, modules as _modules
from pprint import pformat
from equipment.framework.Exceptions.ContainerModuleNotFound import ContainerModuleNotFound

if TYPE_CHECKING:
    from equipment.framework.App.Container import Container


def app(name: str = 'app.App.Container', autodiscover: bool = True) -> 'Container':
    framework_container = module('equipment.framework.App.Container')
    resolved_module = module(name)

    # Fallback framework module
    if autodiscover and resolved_module is None:
        resolved_module = framework_container

    raise_unless(isinstance(resolved_module, framework_container.__class__), ContainerModuleNotFound(name))  # nopep8

    return resolved_module.Container


def base_path(join: Optional[str] = None, container: Optional['Container'] = None, rootfile: str = '.equipment') -> Path:
    if container is None:
        container = app()

    path = Path(getfile(container))

    while not path.joinpath(rootfile).exists():
        path = path.parent

    return path.absolute().joinpath(
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
