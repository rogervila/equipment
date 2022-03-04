import unittest
from unittest.mock import patch
from equipment.framework.tests.BaseTest import BaseTest
from equipment.framework.helpers import dump


class test_dump(BaseTest):
    @patch('pprint.pformat')
    # pylint: disable=unused-argument
    def test_dump(self, mock_pformat):
        self.assertIsNone(dump('foo'))


if __name__ == '__main__':
    unittest.main()
