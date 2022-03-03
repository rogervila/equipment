from os import getcwd, sep
from os.path import dirname, join, abspath, isdir, isfile
from click import confirm, echo, style
from equipment.console.Commands.AbstractCommand import AbstractCommand
from shutil import move, copyfile, copytree, ignore_patterns
from tempfile import gettempdir
from datetime import datetime
from codecs import open as _open
from pkg_resources import get_distribution


class NewCommand(AbstractCommand):
    name: str
    source: str
    destination: str
    already_exists: bool
    confirmation: bool

    def __init__(self, name: str) -> None:
        self.name = name

    def run(self, *args, **kwargs) -> None:
        self.source = abspath(join(dirname(__file__), '../../project'))
        self.destination = f'{getcwd()}{sep}{self.name}'
        self.already_exists = isdir(self.destination)
        self.confirmation = confirm(f'Directory "{self.destination}" already exists. Do you want to override it?') if self.already_exists else True  # nopep8

        if not self.confirmation:
            return None

        self._handle_existing_directory()
        self._copy_project_folder()
        self._generate_environment_file()
        self._replace_requirements_file()

        echo(style('Done!', fg='green'))
        echo(style(f'run "cd {self.destination} && pip install -r requirements.txt"', fg='green'))  # nopep8

    def _handle_existing_directory(self) -> None:
        if self.already_exists:
            temporal_destination = f'{gettempdir()}{sep}{datetime.now()}{self.name}'
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

        environment_file = f'{self.destination}{sep}.env'

        if isfile(environment_file):
            echo(style(f'WARNING: "{environment_file}" already exists. Skip...', fg='yellow'))  # nopep8
            return None

        copyfile(
            f'{self.destination}{sep}.env.example',
            environment_file
        )

    def _replace_requirements_file(self) -> None:
        requirements_file = f'{self.destination}{sep}requirements.txt'
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
