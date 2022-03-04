import unittest
from shutil import move, rmtree
from os import getcwd, sep
from os.path import isdir, isfile
from tempfile import gettempdir
from datetime import datetime
from codecs import open as _open
from click.testing import CliRunner
from equipment.console.Commands.NewCommand import NewCommand
from equipment.console import new


class test_NewCommandTest(unittest.TestCase):
    def test_command_invoke(self):
        project = '__pycache__'  # ensure it is always ignored

        runner = CliRunner()
        result = runner.invoke(new, [project])
        self.assertTrue(result.exit_code == 0)

        rmtree(f'{getcwd()}{sep}{project}', ignore_errors=True)

    def test_command_class(self):
        project = '__pycache__'  # ensure it is always ignored
        full_path = f'{getcwd()}{sep}{project}'

        if isdir(full_path):
            move(full_path, f'{gettempdir()}{sep}{datetime.now()}{sep}{project}')  # nopep8

        self.assertFalse(isdir(full_path))

        self.assertIsNone(NewCommand(project).run())

        self.assertTrue(isdir(full_path))

        self.assertTrue(isfile(f'{full_path}{sep}.env'))

        requirements_file = f'{full_path}{sep}requirements.txt'

        self.assertTrue(isfile(requirements_file))

        with _open(requirements_file, 'r') as f:
            self.assertTrue('equipment==' in f.read())

        rmtree(full_path, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
