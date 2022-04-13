from click import confirm, echo, style
from alembic import command
from alembic.config import Config
from equipment.console.Commands.AbstractCommand import AbstractCommand
from equipment.framework.helpers import base_path


class DatabaseMigrateCommand(AbstractCommand):
    seed: bool
    no_interaction: bool
    confirmation: bool

    def __init__(self, seed: bool = False, no_interaction: bool = False) -> None:
        self.seed = seed
        self.no_interaction = no_interaction

    def run(self, *args, **kwargs) -> None:
        echo(style('Running migrations...', fg='green'))
        self.confirmation = True if self.no_interaction else confirm('Do you want to run migrations?')  # nopep8

        if not self.confirmation:
            echo(style('Skip', fg='yellow'))
            return None

        config = Config(str(base_path('database/migrations/alembic.ini')))
        config.set_main_option('script_location', str(base_path('database/migrations')))  # nopep8

        command.upgrade(config, 'head')
