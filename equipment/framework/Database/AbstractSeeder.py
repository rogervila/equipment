import abc


class AbstractSeeder(abc.ABC):
    @staticmethod
    def seed() -> None:
        raise NotImplementedError
