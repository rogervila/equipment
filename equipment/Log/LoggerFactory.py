import os
from logging import Handler, FileHandler, Logger, NullHandler, StreamHandler, getLogger, getLevelNamesMapping
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger.jsonlogger import JsonFormatter
from python_sqlite_log_handler import SQLiteLogHandler
from equipment.Log.AbstractLogger import AbstractLogger


class LoggerFactory(AbstractLogger):
    logger: Logger
    base_path: str
    config: dict

    def __init__(self, name: str, base_path: str, config: dict):
        self.base_path = base_path
        self.config = config

        if not hasattr(self, 'logger'):
            logger = getLogger(name)
            _clear_logger(logger)

            logger.setLevel(
                getLevelNamesMapping()[str(
                    self.config['level']).upper().strip()
                ]
            )

            handlers = self._get_handlers_list()

            for handler in handlers:
                logger.addHandler(handler)

            self.logger = logger

    def debug(self, *args, **kwargs) -> None:
        kwargs.setdefault('stacklevel', 2)
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        kwargs.setdefault('stacklevel', 2)
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        kwargs.setdefault('stacklevel', 2)
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        kwargs.setdefault('stacklevel', 2)
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs) -> None:
        kwargs.setdefault('stacklevel', 2)
        self.logger.critical(*args, **kwargs)

    def _get_handlers_list(self) -> list[Handler]:
        channel = self.config['channel']

        if channel is None or channel == 'None' or channel == 'null':
            return [NullHandler()]

        handlers = []
        channels = list(
            self.config['channels']['stack']['channels']
        ) if channel == 'stack' else [channel]

        for channel in channels:
            handlers.append(
                self._get_channel_handler(
                    channel,
                    self.config['channels'][channel]
                )
            )

        return handlers

    def _get_channel_handler(self, channel: str, channel_config: dict) -> Handler:
        if channel == 'single':
            handler = FileHandler(os.path.join(
                self.base_path,
                str(channel_config['filename'])
            ))
        elif channel == 'daily':
            handler = TimedRotatingFileHandler(
                filename=os.path.join(
                    self.base_path,
                    str(channel_config['filename'])
                ),
                when=str(channel_config['when']),
                interval=int(channel_config['interval']),
                backupCount=int(channel_config['backupCount'])
            )
        elif channel == 'console':
            handler = StreamHandler(channel_config['stream'])
        elif channel == 'sqlite':
            handler = SQLiteLogHandler(
                db_path=os.path.join(
                    self.base_path,
                    str(channel_config['filename'])
                ),
                table_name=channel_config['table_name'] if 'table_name' in channel_config else 'logs'
            )
        else:
            raise ValueError(f'Invalid channel name: {channel}')

        if 'formatter' in channel_config and str(channel_config['formatter']).strip().lower() == 'json':
            handler.setFormatter(
                JsonFormatter(
                    self.config['formatters']['json']['format'],
                    json_indent=self.config['formatters']['json']['indent']
                )
            )

        return handler


def _clear_logger(logger: Logger) -> None:
    handlers = logger.handlers
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)
