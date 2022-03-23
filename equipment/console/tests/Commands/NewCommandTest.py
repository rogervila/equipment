import unittest
import os
from shutil import move, rmtree
from os.path import isdir, isfile
from tempfile import gettempdir
from datetime import datetime
from codecs import open as _open
from unittest.mock import patch
from click.testing import CliRunner
from equipment.console.Commands.NewCommand import NewCommand
from equipment.console import new
from equipment.console.tests.TestCase import TestCase


class NewCommandTest(TestCase):
    def test_command_invoke(self):
        project = '__pycache__'  # ensure it is always ignored
        print(f'{self.tests_path}{os.sep}{project}')

        with patch.object(os, 'getcwd', return_value=self.tests_path):
            runner = CliRunner()
            result = runner.invoke(new, [project])
            self.assertTrue(result.exit_code == 0)

        rmtree(f'{self.tests_path}{os.sep}{project}', ignore_errors=False)

    def test_command_class(self):
        project = '__pycache__'  # ensure it is always ignored
        full_path = f'{self.tests_path}{os.sep}{project}'

        if isdir(full_path):
            move(full_path, f'{gettempdir()}{os.sep}{datetime.now()}{os.sep}{project}')  # nopep8

        self.assertFalse(isdir(full_path))

        with patch.object(os, 'getcwd', return_value=self.tests_path):
            self.assertIsNone(NewCommand(project).run())

        self.assertTrue(isdir(full_path))

        self.assertTrue(isfile(f'{full_path}{os.sep}.env'))

        requirements_file = f'{full_path}{os.sep}requirements.txt'

        self.assertTrue(isfile(requirements_file))

        with _open(requirements_file, 'r') as f:
            self.assertTrue('equipment==' in f.read())

        rmtree(full_path, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
