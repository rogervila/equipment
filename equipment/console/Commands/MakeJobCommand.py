from codecs import open as _open
from datetime import datetime
from os import getcwd, sep
from os.path import abspath, dirname, isdir, isfile, join
from shutil import copyfile, copytree, ignore_patterns, move
from tempfile import gettempdir
from click import confirm, echo, style
from equipment.console.Commands.AbstractCommand import AbstractCommand
from pathlib import Path


class MakeJobCommand(AbstractCommand):
    name: str
    replacement: str

    def __init__(self, name: str, replacement: str = '_REPLACEME_') -> None:
        self.name = name
        self.replacement = replacement

    def run(self, *args, **kwargs) -> None:
        echo(style(f'Creating {self.name} job...', fg='green'))

        jobs_path = f'{getcwd()}{sep}app{sep}Jobs'

        Path(jobs_path).mkdir(parents=True, exist_ok=True)

        destination = f'{jobs_path}{sep}{self.name}.py'

        confirmation = confirm(f'Directory "{destination}" already exists. Do you want to override it?') if isfile(destination) else True  # nopep8

        if not confirmation:
            echo(style('Skip', fg='yellow'))
            return None

        copyfile(
            abspath(join(dirname(__file__), f'..{sep}stubs{sep}Job.py')),
            destination
        )

        echo(style('Done!', fg='green'))
