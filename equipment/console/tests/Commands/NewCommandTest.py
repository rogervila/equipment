import unittest
from equipment.console.Commands.NewCommand import NewCommand


class test_WelcomeMail(unittest.TestCase):
    def test_command_returns_none(self):
        self.assertIsNone(NewCommand('foo').run())


if __name__ == '__main__':
    unittest.main()
