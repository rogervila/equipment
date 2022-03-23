import click
from app.Commands.ExampleCommand import ExampleCommand


@click.command()
def example():
    ExampleCommand().run()
