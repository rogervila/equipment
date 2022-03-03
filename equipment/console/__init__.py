#!/usr/bin/env python
import click
from equipment.console.Commands.NewCommand import NewCommand


@click.group()
@click.version_option()
def main() -> None:
    pass  # @click decorators handle the commands defined on this file


@main.command()
@click.argument('name')
def new(name):
    NewCommand(name).run()


if __name__ == '__main__':
    main()
