import logging
from logging import NullHandler
from equipment.framework.Log.NativeLog import NativeLog


class NoneLog(NativeLog):
    def get_handlers(self) -> list:
        return [NullHandler()]

    def get_level(self) -> int:
        return logging.NOTSET

    def get_name(self) -> str:
        return self.config.get('LOG_NONE', 'name')
