import os
from logging import Handler, FileHandler, Logger, NullHandler, StreamHandler, getLogger, getLevelNamesMapping
from logging.handlers import TimedRotatingFileHandler
from equipment.Log.AbstractLogger import AbstractLogger
from pythonjsonlogger.jsonlogger import JsonFormatter


class LoggerFactory(AbstractLogger):
    logger: Logger
    base_path: str

    def __init__(self, name: str, base_path: str, config: dict):
        self.base_path = base_path

        if not hasattr(self, 'logger'):
            logger = getLogger(name)
            _clear_logger(logger)

            logger.setLevel(
                getLevelNamesMapping()[str(config['level']).upper().strip()]
            )

            handlers = self._get_handlers_list(config)

            for handler in handlers:
                if 'formatter' in config and str(config['formatter']).lower() == 'json':
                    handler.setFormatter(JsonFormatter(config['formatters']['json']['format'], json_indent=None))

                logger.addHandler(handler)

            self.logger = logger

    def debug(self, *args, **kwargs) -> None:
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs) -> None:
        self.logger.critical(*args, **kwargs)

    def _get_handlers_list(self, config: dict) -> list[Handler]:
        channel = config['channel']

        if channel is None or channel == 'None' or channel == 'null':
            return [NullHandler()]

        if channel == 'stack':
            handlers = []
            channels = list(config['channels']['stack']['channels'])

            for channel in channels:
                handlers.append(self._get_channel_handler(channel, config['channels'][channel]))
            return handlers

        return [self._get_channel_handler(channel, config['channels'][channel])]

    def _get_channel_handler(self, channel: str, config: dict) -> Handler:
        if channel == 'single':
            handler = FileHandler(os.path.join(
                self.base_path,
                str(config['filename'])
            ))
        elif channel == 'daily':
            handler = TimedRotatingFileHandler(
                filename=os.path.join(
                    self.base_path,
                    str(config['filename'])
                ),
                when=str(config['when']),
                interval=int(config['interval']),
                backupCount=int(config['backupCount'])
            )
        elif channel == 'console':
            handler = StreamHandler(config['stream'])
        else:
            raise ValueError(f'Invalid channel name: {channel}')

        return handler


def _clear_logger(logger: Logger) -> None:
    handlers = logger.handlers
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)
