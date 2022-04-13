import abc
from typing import Optional
from equipment.framework.App.Container import Container
from equipment.framework.helpers import app


class AbstractSeeder(abc.ABC):
    def __init__(self, container: Optional[Container] = None) -> None:
        self.app = container if container is not None else app()

    def seed(self) -> None:
        raise NotImplementedError
