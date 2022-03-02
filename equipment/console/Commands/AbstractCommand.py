import abc


class AbstractCommand(abc.ABC):
    def run(self, *args, **kwargs) -> None:
        raise NotImplementedError
