import abc
from equipment.framework.helpers import app


class AbstractJob(abc.ABC):
    @classmethod
    def dispatchSync(cls, *args, **kwargs) -> None:
        cls.app = app()
        cls.handle(*args, **kwargs)

    @classmethod
    def dispatch(cls, *args, **kwargs) -> None:
        app().queue().push(cls.dispatchSync, *args, **kwargs)

    @classmethod
    def handle(cls, *args, **kwargs) -> None:
        raise NotImplementedError
