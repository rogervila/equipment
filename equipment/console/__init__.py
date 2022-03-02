#!/usr/bin/env python
import click
from equipment.console.Commands.NewCommand import NewCommand


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument('name')
def new(name):
    NewCommand(name).run()


if __name__ == '__main__':
    main()
