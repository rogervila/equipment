#!/usr/bin/env python

import sys
from inspect import getmembers
from os import getcwd
import click
from equipment.framework.helpers import module
from equipment.console.Commands.NewCommand import NewCommand


@click.group()
@click.version_option()
def main() -> None:
    pass  # @click decorators handle the commands defined on this file


@main.command()
@click.argument('name')
def new(name):
    NewCommand(name).run()


# Add project commands if available
sys.path.append(getcwd())
project_commands_module = module('app.Commands', print_exception=True)

if project_commands_module is not None:
    for member in getmembers(project_commands_module):
        if isinstance(member[1], click.Command):
            try:
                main.add_command(getattr(project_commands_module, member[0]))
            except Exception:
                pass

if __name__ == '__main__':
    main()
