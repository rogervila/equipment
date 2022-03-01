import abc


class AbstractScheduler(abc.ABC):
    def run(self) -> None:
        raise NotImplementedError
