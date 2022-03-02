import abc
from equipment.framework.helpers import app


class AbstractJob(abc.ABC):
    @classmethod
    def dispatchSync(cls, *args, **kwargs) -> None:
        cls.app = app()  # nopep8
        cls.handle(*args, **kwargs)

    @classmethod
    def dispatch(cls, *args, **kwargs) -> None:
        app().queue().push(cls.dispatchSync, *args, **kwargs)  # nopep8

    @classmethod
    def dispatchWithContainer(cls, container, *args, **kwargs) -> None:
        print('????START')
        print(container)
        print('????END')
        container.queue().push(cls.dispatchSync, *args, **kwargs)  # nopep8

    @classmethod
    def handle(cls, *args, **kwargs) -> None:
        raise NotImplementedError
