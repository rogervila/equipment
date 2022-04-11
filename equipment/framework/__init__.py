from equipment.framework.helpers import app
from equipment.framework.App.Container import Container


def equipment(name: str = 'app.App.Container', autodiscover: bool = True) -> 'Container':
    return app(name, autodiscover)
