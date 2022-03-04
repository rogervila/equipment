from click import echo
from equipment.console.Commands.AbstractCommand import AbstractCommand


class ExampleCommand(AbstractCommand):
    def __init__(self) -> None:
        pass # Constructor is not extended from AbstractCommand. You are free to pass any parameter to it

    def run(self, *args, **kwargs) -> None:
        echo('Running example command!')
