from click import confirm, echo, style
from equipment.console.Commands.AbstractCommand import AbstractCommand
from equipment.framework.helpers import module


class DatabaseSeedCommand(AbstractCommand):
    no_interaction: bool
    confirmation: bool

    def __init__(self, no_interaction: bool = False) -> None:
        self.no_interaction = no_interaction

    def run(self, *args, **kwargs) -> None:
        echo(style('Seeding...', fg='green'))
        self.confirmation = True if self.no_interaction else confirm('Do you want to run seeders?')  # nopep8

        if not self.confirmation:
            echo(style('Skip', fg='yellow'))
            return None

        seeder = module('database.seeders.Seeder')

        if not self.confirmation:
            echo(style('<database.seeders.Seeder> not found. Skip', fg='yellow'))
            return None

        seeder.Seeder.seed()
