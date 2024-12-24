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
