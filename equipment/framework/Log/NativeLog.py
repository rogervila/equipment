import logging
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Log.AbstractLog import AbstractLog


class NativeLog(AbstractLog):
    def __init__(self, config: AbstractConfig):
        self.handlers = None
        self.format = None
        self.level = None
        self.name = None
        self.date_format = None
        self.logger = None
        self.config = config

    def load(self) -> None:
        if self.logger is None:
            self.reload()

    def reload(self) -> None:
        self.handlers = self.get_handlers()
        self.format = '[%(asctime)s] %(name)s.%(levelname)s %(message)s'
        self.level = self.get_level()
        self.name = self.get_name()
        self.date_format = '%Y-%m-%d %H:%M:%S'

        logging.basicConfig(
            format=self.format,
            level=self.level,
            datefmt=self.date_format,
            handlers=self.handlers
        )

        self.logger = logging.getLogger(self.name)

    def debug(self, *args, **kwargs) -> None:
        self.load()
        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        self.load()
        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        self.load()
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        self.load()
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs) -> None:
        self.load()
        self.logger.critical(*args, **kwargs)
