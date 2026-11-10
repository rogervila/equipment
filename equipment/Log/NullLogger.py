from logging import Logger
from equipment.Log.AbstractLogger import AbstractLogger


class NullLogger(AbstractLogger):
    def debug(self, *args, **kwargs) -> None:
        pass

    def info(self, *args, **kwargs) -> None:
        pass

    def warning(self, *args, **kwargs) -> None:
        pass

    def error(self, *args, **kwargs) -> None:
        pass

    def critical(self, *args, **kwargs) -> None:
        pass

    def get_logger(self) -> Logger:
        if not hasattr(self, 'logger'):
            # Standalone logger, not registered in logging's global registry, that discards every record
            self.logger = Logger(self.__class__.__name__)
            self.logger.disabled = True

        return self.logger
