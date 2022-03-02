import logging
from logging import StreamHandler
from sys import stdout, stderr
from equipment.framework.Log.NativeLog import NativeLog


class ConsoleLog(NativeLog):
    def get_handlers(self) -> list:
        return [
            StreamHandler(stdout),
            StreamHandler(stderr)
        ]

    def get_level(self) -> int:
        level = self.config.get('LOG_CONSOLE', 'level')
        return getattr(logging, level if level is not None else 'DEBUG')

    def get_name(self) -> str:
        return self.config.get('LOG_CONSOLE', 'name')
