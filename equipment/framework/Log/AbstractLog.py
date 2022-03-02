import abc


class AbstractLog(abc.ABC):
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

    def get_handlers(self) -> list:
        raise NotImplementedError

    def get_level(self) -> int:
        raise NotImplementedError

    def get_name(self) -> str:
        raise NotImplementedError
