import unittest
from unittest.mock import MagicMock
from redis import Redis
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from equipment.framework.tests.TestCase import TestCase
from equipment.framework.Connection.RedisConnection import RedisConnection


class RedisConnectionTest(TestCase):
    def setUp(self):
        super().setUp()
        self.redis = RedisConnection(self.app.config(), self.app.log())

    def test_extends_from_abstract_Connection(self):
        self.assertTrue(
            isinstance(self.redis, AbstractConnection)
        )

    def test_returns_instance(self):
        self.assertTrue(
            isinstance(self.redis.factory(), Redis)
        )

    def test_connection_works(self):
        self.assertTrue(
            self.redis.connect()
        )

    def test_connection_fails(self):
        self.redis.log.debug = MagicMock(side_effect=Exception())

        self.assertFalse(
            self.redis.connect()
        )


if __name__ == '__main__':
    unittest.main()
