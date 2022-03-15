import os
from codecs import open as _open
from os.path import abspath, dirname, isfile, join
from pathlib import Path
from click import confirm, echo, style
from equipment.console.Commands.AbstractCommand import AbstractCommand


class MakeJobCommand(AbstractCommand):
    name: str
    replacement: str
    jobs_path: str
    destination: str
    source: str
    confirmation: bool

    def __init__(self, name: str, replacement: str = '_REPLACEME_') -> None:
        self.name = name
        self.replacement = replacement

    def run(self, *args, **kwargs) -> None:
        echo(style(f'Creating {self.name} job...', fg='green'))

        self.jobs_path = f'{os.getcwd()}{os.sep}app{os.sep}Jobs'
        self.source = abspath(join(dirname(__file__), f'..{os.sep}stubs{os.sep}Job.py'))  # nopep8
        self.destination = f'{self.jobs_path}{os.sep}{self.name}.py'
        self.confirmation = confirm(f'Directory "{self.destination}" already exists. Do you want to override it?') if isfile(self.destination) else True  # nopep8

        if not self.confirmation:
            echo(style('Skip', fg='yellow'))
            return None

        self._ensureJobsDirectory()
        self._createFile()

        echo(style('Done!', fg='green'))

    def _ensureJobsDirectory(self) -> None:
        Path(self.jobs_path).mkdir(parents=True, exist_ok=True)

        init_file = f'{self.jobs_path}{os.sep}__init__.py'

        if not isfile(init_file):
            with _open(init_file, 'w') as f:
                f.write('')

    def _createFile(self) -> None:
        content = ''

        with _open(self.source, 'r') as source:
            content = source.read()

        with _open(self.destination, 'w') as destination:
            destination.write(content.replace(self.replacement, self.name))
