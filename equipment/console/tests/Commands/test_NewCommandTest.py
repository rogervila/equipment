import unittest
from shutil import move, rmtree
from os import getcwd, sep
from os.path import isdir, isfile
from tempfile import gettempdir
from datetime import datetime
from codecs import open as _open
from equipment.console.Commands.NewCommand import NewCommand


class test_NewCommandTest(unittest.TestCase):
    def test_command(self):
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
