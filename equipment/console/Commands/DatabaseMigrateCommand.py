from click import confirm, echo, style
from click.core import Context
from alembic import command
from alembic.config import Config
from equipment.console.Commands.AbstractCommand import AbstractCommand
from equipment.framework.helpers import base_path


class DatabaseMigrateCommand(AbstractCommand):
    ctx: Context
    seed: bool
    no_interaction: bool
    fresh: bool
    confirmation: bool

    def __init__(self, ctx: Context, seed: bool = False, fresh: bool = False, no_interaction: bool = False) -> None:
        self.ctx = ctx
        self.seed = seed
        self.fresh = fresh
        self.no_interaction = no_interaction

    def run(self, *args, **kwargs) -> None:
        echo(style('Running migrations...', fg='green'))
        self.confirmation = True if self.no_interaction else confirm('Do you want to run migrations?')  # nopep8

        if not self.confirmation:
            echo(style('Skip', fg='yellow'))
            return None

        config = Config(str(base_path('database/migrations/alembic.ini')))
        config.set_main_option('script_location', str(base_path('database/migrations')))  # nopep8

        if self.fresh:
            # TODO: delete all tables instead of downgrade
            command.downgrade(config, 'base')

        command.upgrade(config, 'head')

        echo(style('Running migrations done!', fg='green'))

        if self.seed:
            self.ctx.invoke(self.console('seed'), no_interaction=self.no_interaction)  # nopep8
