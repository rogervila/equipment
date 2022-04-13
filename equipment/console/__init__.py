#!/usr/bin/env python

# pylint: disable=redefined-outer-name

import sys
from inspect import getmembers
from os import getcwd
import click
from click.core import Context
from equipment.console.Commands.DatabaseMigrateCommand import DatabaseMigrateCommand
from equipment.console.Commands.DatabaseSeedCommand import DatabaseSeedCommand
from equipment.console.Commands.MakeJobCommand import MakeJobCommand
from equipment.console.Commands.NewCommand import NewCommand
from equipment.framework.helpers import module


@click.group()
@click.version_option()
def main() -> None:
    pass  # @click decorators handle the commands defined on this file


@main.command()
@click.argument('name')
def new(name: str) -> None:
    NewCommand(name).run()


@main.group()
def make() -> None:
    pass  # @click decorators handle the commands defined on this file


@make.command()
@click.argument('name')
def job(name: str) -> None:
    MakeJobCommand(name).run()


@main.group()
def database() -> None:
    pass  # @click decorators handle the commands defined on this file


@database.command()
@click.pass_context
@click.option('--seed', flag_value=True, default=False)
@click.option('--fresh', flag_value=True, default=False)
@click.option('--no-interaction', flag_value=True, default=False)
def migrate(ctx: Context, seed: bool, fresh: bool, no_interaction: bool) -> None:
    DatabaseMigrateCommand(ctx, seed, fresh, no_interaction).run()


@database.command()
@click.option('--no-interaction', flag_value=True, default=False)
def seed(no_interaction: bool) -> None:
    DatabaseSeedCommand(no_interaction).run()


def _load_additional_commands() -> None:
    '''Add project commands if available'''

    sys.path.append(getcwd())
    project_commands_module = module(
        'app.Commands.commands',
        print_exception=False
    )

    if project_commands_module is None:
        return

    for member in getmembers(project_commands_module):
        if not isinstance(member[1], click.Command):
            continue

        try:
            main.add_command(getattr(project_commands_module, member[0]))
        except Exception:
            pass  # Error messages here do not provide any value and break the console developer experience


_load_additional_commands()

if __name__ == '__main__':
    main()
