from click import echo
from equipment.console.Commands.AbstractCommand import AbstractCommand


class ExampleCommand(AbstractCommand):
    def __init__(self) -> None:
        pass

    def run(self, *args, **kwargs) -> None:
        echo('Running example command!')
