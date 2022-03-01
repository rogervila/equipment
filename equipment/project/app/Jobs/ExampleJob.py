from equipment.framework.Jobs.AbstractJob import AbstractJob
from app.App.Container import Container


class ExampleJob(AbstractJob):
    @classmethod
    def handle(cls, *args, **kwargs) -> None:
        app = cls.app  # type: Container

        app.log().debug(args)
        app.log().debug(kwargs)

        if len(args) > 0:
            app.log().info(f'Message from ExampleJob: {args[0]}')
