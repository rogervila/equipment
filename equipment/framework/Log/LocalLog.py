import logging
from logging.handlers import TimedRotatingFileHandler
from equipment.framework.Log.NativeLog import NativeLog


class LocalLog(NativeLog):
    def get_handlers(self) -> list:
        return [
            TimedRotatingFileHandler(
                filename=self.config.get('LOG_LOCAL', 'path'),
                when='D',
                interval=1,
                delay=self.config.get('LOG_LOCAL', 'delay')
            )
        ]

    def get_level(self) -> int:
        level = self.config.get('LOG_LOCAL', 'level')
        return getattr(logging, level if level is not None else 'DEBUG')

    def get_name(self) -> str:
        return self.config.get('LOG_LOCAL', 'name')
