import unittest
from click.testing import CliRunner
from app.Commands.commands import example
from app.Commands.ExampleCommand import ExampleCommand
from tests.TestCase import TestCase

# Check: https://click.palletsprojects.com/en/8.0.x/testing/#testing-click-applications


class test_ExampleCommand(TestCase):
    def test_command_invoke(self):
        runner = CliRunner()
        result = runner.invoke(example)

        self.assertTrue(result.exit_code == 0)
        self.assertTrue(isinstance(result.output, str))

    def test_command_class(self):
        self.assertIsNone(
            ExampleCommand().run()
        )


if __name__ == '__main__':
    unittest.main()
