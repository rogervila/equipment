import unittest
from unittest.mock import MagicMock
from redis import Redis
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from tests.BaseTest import BaseTest


class test_RedisConnection(BaseTest):
    def test_extends_from_abstract_Connection(self):
        self.assertTrue(
            isinstance(self.app.redis(), AbstractConnection)
        )

    def test_returns_instance(self):
        self.assertTrue(
            isinstance(self.app.redis().factory(), Redis)
        )

    def test_connection_works(self):
        self.assertTrue(
            self.app.redis().connect()
        )

    def test_connection_fails(self):
        self.app.redis().log.debug = MagicMock(side_effect=Exception())

        self.assertFalse(
            self.app.redis().connect()
        )


if __name__ == '__main__':
    unittest.main()
