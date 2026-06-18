import os
import unittest
from unittest.mock import patch

from click.testing import CliRunner

from equipment.Command import main


class CliTest(unittest.TestCase):
    def test_new_command_passes_project_name_and_current_directory(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            with patch('equipment.Command.NewProjectCommand') as command_class:
                result = runner.invoke(main, ['new', 'demo-app'])

                self.assertEqual(0, result.exit_code)
                command_class.return_value.run.assert_called_once_with(
                    name='demo-app',
                    path=os.getcwd(),
                )

    def test_compile_command_passes_dist_argument(self):
        runner = CliRunner()

        with patch('equipment.Command.CompileCommand') as command_class:
            result = runner.invoke(main, ['compile', 'release'])

            self.assertEqual(0, result.exit_code)
            command_class.return_value.run.assert_called_once_with(dist='release')


if __name__ == '__main__':
    unittest.main()
