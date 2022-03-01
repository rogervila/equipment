import logging
from logging import StreamHandler
from sys import stdout
from pygelf import GelfUdpHandler
from equipment.framework.Log.NativeLog import NativeLog


class GELFLog(NativeLog):
    def get_handlers(self) -> list:
        return [
            GelfUdpHandler(
                host=self.config.get('LOG_GELF', 'host'),
                port=self.config.get('LOG_GELF', 'port'),
                _app_name=self.config.get('APP', 'name')
            ),
            StreamHandler(stdout)
        ]

    def get_level(self) -> int:
        return getattr(logging, self.config.get('LOG_GELF', 'level'))

    def get_name(self) -> str:
        return self.config.get('LOG_GELF', 'name')
