from equipment.framework.Jobs.AbstractJob import AbstractJob


class _REPLACEME_(AbstractJob):
    @classmethod
    def handle(cls, *args, **kwargs) -> None:
        app = cls.app

        app.log().debug(args)
        app.log().debug(kwargs)
