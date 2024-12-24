import os
import click
from equipment.Command.NewProjectCommand import NewProjectCommand


@click.group()
@click.version_option()
def main() -> None:
    pass  # @click decorators handle the commands defined on this file


@main.command()
@click.argument('name')
def new(name):
    NewProjectCommand().run(
        name=name,
        path=os.getcwd(),
    )


if __name__ == '__main__':
    main()
