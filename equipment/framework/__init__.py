from dependency_injector.containers import Container
from equipment.framework.helpers import app


def equipment(name: str = 'app.App.Container', autodiscover: bool = True) -> Container:
    return app(name, autodiscover)
