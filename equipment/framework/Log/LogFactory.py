from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Log.GELFLog import GELFLog
from equipment.framework.Log.LocalLog import LocalLog
from equipment.framework.Log.ConsoleLog import ConsoleLog
from equipment.framework.Log.NoneLog import NoneLog
from icecream import ic


class LogFactory(AbstractLog):
    def __init__(self, config: AbstractConfig):
        driver_name = config.get('LOG', 'driver')

        if driver_name == 'local':
            self.driver = LocalLog(config)
        elif driver_name == 'console':
            self.driver = ConsoleLog(config)
        elif driver_name == 'gelf':
            self.driver = GELFLog(config)
        elif driver_name == 'none':
            self.driver = NoneLog(config)
        else:
            error = f'Log driver "{driver_name}" is not supported'
            ic.configureOutput(prefix='')
            ic(error)
            raise NotImplementedError(error)

    def debug(self, *args, **kwargs) -> None:
        self.driver.debug(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        self.driver.info(*args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        self.driver.warning(*args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        self.driver.error(*args, **kwargs)

    def critical(self, *args, **kwargs) -> None:
        self.driver.critical(*args, **kwargs)

    def get_handlers(self) -> list:
        return self.driver.get_handlers()

    def get_level(self) -> int:
        return self.driver.get_level()

    def get_name(self) -> str:
        return self.driver.get_name()
