import unittest
from shutil import rmtree
from os import getcwd, sep
from os.path import isfile
from click.testing import CliRunner
from equipment.console.Commands.MakeJobCommand import MakeJobCommand
from equipment.console import job


class test_MakeJobCommand(unittest.TestCase):
    def _cleanup(self) -> None:
        rmtree(f'{getcwd()}{sep}app', ignore_errors=True)

    def setUp(self) -> None:
        super().setUp()
        self._cleanup()

    def tearDown(self) -> None:
        super().tearDown()
        self._cleanup()

    def test_command_invoke(self):
        name = '__pycache__'  # ensure it is always ignored

        runner = CliRunner()
        result = runner.invoke(job, [name])
        self.assertTrue(result.exit_code == 0)

    def test_command_class(self):
        name = '__pycache__'  # ensure it is always ignored
        full_path = f'{getcwd()}{sep}app{sep}Jobs{sep}{name}.py'

        self.assertFalse(isfile(full_path))

        self.assertIsNone(MakeJobCommand(name).run())

        self.assertTrue(isfile(full_path))


if __name__ == '__main__':
    unittest.main()
