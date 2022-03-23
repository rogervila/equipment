import unittest
from unittest.mock import MagicMock, patch
import sqlalchemy
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from equipment.framework.Connection.SQLiteConnection import SQLiteConnection
from equipment.framework.tests.TestCase import TestCase


class SQLiteConnectionTest(TestCase):
    def setUp(self):
        super().setUp()
        config = self.app.config()
        config.set('CONNECTION_SQLITE', 'path', ':memory:')

        self.sql = SQLiteConnection(
            config=config,
            log=self.app.log()
        )

    def test_extends_from_abstract_Connection(self):
        self.assertTrue(
            isinstance(self.sql, AbstractConnection)
        )

    def test_returns_instance(self):
        self.assertTrue(
            isinstance(
                self.sql.factory(),
                sqlalchemy.engine.base.Engine
            )
        )

    def test_connection_works(self):
        with patch.object(sqlalchemy, 'create_engine', return_value={}):
            self.assertTrue(
                self.sql.connect()
            )

    def test_connection_fails(self):
        with patch.object(sqlalchemy, 'create_engine', return_value={}):
            self.sql.log.debug = MagicMock(side_effect=Exception())

            self.assertFalse(
                self.sql.connect()
            )


if __name__ == '__main__':
    unittest.main()
