import unittest
import os
from unittest.mock import patch
from shutil import rmtree
from os.path import isfile
from click.testing import CliRunner
from equipment.console.Commands.MakeJobCommand import MakeJobCommand
from equipment.console import job
from equipment.console.tests.TestCase import TestCase


class MakeJobCommandTest(TestCase):
    def _cleanup(self) -> None:
        rmtree(f'{self.tests_path}{os.sep}app', ignore_errors=True)

    def setUp(self) -> None:
        super().setUp()
        self._cleanup()

    def tearDown(self) -> None:
        super().tearDown()
        self._cleanup()

    def test_command_invoke(self):
        name = '__pycache__'  # ensure it is always ignored

        with patch.object(os, 'getcwd', return_value=self.tests_path):
            runner = CliRunner()
            result = runner.invoke(job, [name])
            self.assertTrue(result.exit_code == 0)

    def test_command_class(self):
        name = '__pycache__'  # ensure it is always ignored
        full_path = f'{self.tests_path}{os.sep}app{os.sep}Jobs{os.sep}{name}.py'

        self.assertFalse(isfile(full_path))

        with patch.object(os, 'getcwd', return_value=self.tests_path):
            self.assertIsNone(MakeJobCommand(name).run())

        self.assertTrue(isfile(full_path))


if __name__ == '__main__':
    unittest.main()
