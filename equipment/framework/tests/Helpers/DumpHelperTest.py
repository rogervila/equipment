import unittest
from unittest.mock import patch
from equipment.framework.tests.TestCase import TestCase
from equipment.framework.helpers import dump


class DumpHelperTest(TestCase):
    @patch('pprint.pformat')
    # pylint: disable=unused-argument
    def test_dump(self, mock_pformat):
        self.assertIsNone(dump('foo'))


if __name__ == '__main__':
    unittest.main()
