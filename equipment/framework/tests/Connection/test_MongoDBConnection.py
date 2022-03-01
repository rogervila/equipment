import unittest
from unittest.mock import MagicMock
import pymongo
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from tests.BaseTest import BaseTest


class test_MongoDBConnection(BaseTest):
    def test_extends_from_abstract_Connection(self):
        self.assertTrue(
            isinstance(self.app.mongo(), AbstractConnection)
        )

    def test_returns_instance(self):
        self.assertTrue(
            isinstance(self.app.mongo().factory(), pymongo.database.Database)
        )

    def test_connection_works(self):
        self.assertTrue(
            self.app.mongo().connect()
        )

    def test_connection_fails(self):
        self.app.mongo().log.debug = MagicMock(side_effect=Exception())

        self.assertFalse(
            self.app.mongo().connect()
        )


if __name__ == '__main__':
    unittest.main()
