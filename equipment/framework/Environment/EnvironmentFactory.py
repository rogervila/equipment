from typing import Any
from equipment.framework.Environment.AbstractEnvironment import AbstractEnvironment
from equipment.framework.Environment.LocalEnvironment import LocalEnvironment


class EnvironmentFactory(AbstractEnvironment):
    def __init__(self):
        self.driver = LocalEnvironment()

    def get(self, key: str) -> Any:
        return self.driver.get(key)

    def set(self, key: str, value) -> None:
        self.driver.set(key, value)

    def all(self) -> list:
        return self.driver.all()
