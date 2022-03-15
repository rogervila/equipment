import os
from codecs import open as _open
from datetime import datetime
from os.path import abspath, dirname, isdir, isfile, join
from shutil import copyfile, copytree, ignore_patterns, move
from tempfile import gettempdir
from click import confirm, echo, style
from pkg_resources import get_distribution
from equipment.console.Commands.AbstractCommand import AbstractCommand


class NewCommand(AbstractCommand):
    name: str
    source: str
    destination: str
    already_exists: bool
    confirmation: bool

    def __init__(self, name: str) -> None:
        self.name = name

    def run(self, *args, **kwargs) -> None:
        self.source = abspath(join(dirname(__file__), f'..{os.sep}..{os.sep}project'))  # nopep8
        self.destination = f'{os.getcwd()}{os.sep}{self.name}'
        self.already_exists = isdir(self.destination)
        self.confirmation = confirm(f'Directory "{self.destination}" already exists. Do you want to override it?') if self.already_exists else True  # nopep8

        if not self.confirmation:
            echo(style('Skip', fg='yellow'))
            return None

        self._handle_existing_directory()
        self._copy_project_folder()
        self._generate_environment_file()
        self._replace_requirements_file()

        echo(style('Done!', fg='green'))
        echo(style(f'run "cd {self.destination} && pip install -r requirements.txt"', fg='green'))  # nopep8

    def _handle_existing_directory(self) -> None:
        if self.already_exists:
            temporal_destination = f'{gettempdir()}{os.sep}{datetime.now()}{self.name}'
            move(self.destination, temporal_destination)

    def _copy_project_folder(self) -> None:
        echo(style('Creating folder project...', fg='green'))

        copytree(
            self.source,
            self.destination,
            ignore=ignore_patterns('*.pyc', 'tmp*', '*__pycache__*', '*.env', '*.coverage')  # nopep8
        )

    def _generate_environment_file(self) -> None:
        echo(style('Generating environment file...', fg='green'))

        environment_file = f'{self.destination}{os.sep}.env'

        if isfile(environment_file):
            echo(style(f'WARNING: "{environment_file}" already exists. Skip...', fg='yellow'))  # nopep8
            return None

        copyfile(
            f'{self.destination}{os.sep}.env.example',
            environment_file
        )

    def _replace_requirements_file(self) -> None:
        requirements_file = f'{self.destination}{os.sep}requirements.txt'
        data = ''

        with _open(requirements_file, 'r') as f:
            data = f.read()

        try:
            replaced = f'equipment=={get_distribution("equipment").version}'
        except Exception as e:
            echo(style(f'WARNING: could not get equipment version. Error: "{str(e)}"', fg='yellow'))  # nopep8
            replaced = 'equipment'

        data = data.replace('-e ../../', replaced)

        with _open(requirements_file, 'w') as f:
            f.write(data)
