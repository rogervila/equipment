from typing import Any
from equipment.framework.Config.LocalConfig import LocalConfig
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Environment.AbstractEnvironment import AbstractEnvironment


class ConfigFactory(AbstractConfig):
    def __init__(self, env: AbstractEnvironment):
        self.driver = LocalConfig(env)

    def load(self) -> None:
        self.driver.load()

    def reload(self) -> None:
        self.driver.reload()

    def set(self, section: str, key: str, value) -> None:
        self.driver.set(section, key, value)

    def get(self, section: str, key: str) -> Any:
        return self.driver.get(section, key)
