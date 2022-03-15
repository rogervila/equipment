import os
from typing import Any
from dotenv import load_dotenv
from equipment.framework.Environment.AbstractEnvironment import AbstractEnvironment
from equipment.framework.helpers import base_path


class LocalEnvironment(AbstractEnvironment):
    def __init__(self, relative_path: str = '.env'):
        self.path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            str(base_path(relative_path))
        )

        load_dotenv(dotenv_path=self.path)

    def get(self, key: str) -> Any:
        return os.environ.get(key)

    def set(self, key: str, value) -> None:
        os.environ[key] = value

    def all(self) -> list:
        return [{item: os.environ.get(item)} for item in os.environ]
