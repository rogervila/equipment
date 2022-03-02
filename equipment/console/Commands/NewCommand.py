from equipment.console.Commands.AbstractCommand import AbstractCommand


class NewCommand(AbstractCommand):
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def run(self, *args, **kwargs) -> None:
        print(self.name)
