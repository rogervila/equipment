import fnmatch
import os
from typing import Any, Optional
from configparser import RawConfigParser
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.helpers import base_path
from equipment.framework.Environment.AbstractEnvironment import AbstractEnvironment


class LocalConfig(AbstractConfig):
    def __init__(self, env: AbstractEnvironment, relative_path: str = 'config'):
        self.env = env
        self.config = None  # type: Optional[RawConfigParser]
        self.pattern = '*.conf'
        self.env_prefix = 'env:'
        self.path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            str(base_path(relative_path))
        )

    def load(self) -> None:
        if self.config is None:
            self.reload()

    def reload(self) -> None:
        self.config = RawConfigParser()

        for file in os.listdir(self.path):
            file = os.path.join(self.path, file)

            if os.path.isfile(file) and fnmatch.fnmatch(file, self.pattern):
                self.config.read(file)

    def set(self, section: str, key: str, value) -> None:
        self.load()

        return self.config.set(section, key, value)

    def get(self, section: str, key: str) -> Any:
        self.load()

        value = self.config.get(section, key)

        real_value = self.env.get(
            value.lstrip(self.env_prefix)
        ) if value.startswith(self.env_prefix) else value

        try:
            return eval(real_value)
        except Exception:
            return real_value
