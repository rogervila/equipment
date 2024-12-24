import abc


class AbstractLogger(abc.ABC):
    def debug(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def info(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def warning(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def error(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def critical(self, *args, **kwargs) -> None:
        raise NotImplementedError
