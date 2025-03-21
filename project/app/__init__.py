from dependency_injector.providers import ThreadSafeSingleton as Singleton
from equipment import Equipment
from app.Scheduler import Scheduler
from app.Inspire import Inspire


class App(Equipment):
    inspiring = Singleton(Inspire, Equipment.config.inspiring.quotes)

    scheduler = Singleton(
        Scheduler,
        Equipment.log,
        Equipment.queue,
        inspiring
    )


def app(base_path: tuple[str, None] = None) -> App:
    return App.make(base_path)
