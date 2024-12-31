import os
import click
from .NewProjectCommand import NewProjectCommand


@click.group()
@click.version_option()
def main() -> None:
    pass  # @click decorators handle the commands defined on this file


@main.command()
@click.argument('name')
def new(name: str) -> None:
    NewProjectCommand().run(
        name=name,
        path=os.getcwd(),
    )
