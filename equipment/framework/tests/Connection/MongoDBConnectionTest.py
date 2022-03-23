import unittest
from unittest.mock import MagicMock, patch
import pymongo
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from equipment.framework.Connection.MongoDBConnection import MongoDBConnection
from equipment.framework.tests.TestCase import TestCase


class MongoDBConnectionTest(TestCase):
    def setUp(self):
        super().setUp()
        self.mongo = MongoDBConnection(self.app.config(), self.app.log())

    def test_extends_from_abstract_Connection(self):
        self.assertTrue(
            isinstance(self.mongo, AbstractConnection)
        )

    def test_connection_works(self):
        with patch.object(pymongo.MongoClient, '__init__', return_value=None):
            self.assertTrue(
                self.mongo.connect()
            )

    def test_connection_fails(self):
        self.mongo.client = MagicMock()
        self.mongo.log.debug = MagicMock(side_effect=Exception())

        self.assertFalse(
            self.mongo.connect()
        )


if __name__ == '__main__':
    unittest.main()
