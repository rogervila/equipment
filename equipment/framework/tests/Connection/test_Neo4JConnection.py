import unittest
from unittest.mock import patch
import neo4j
from equipment.framework.Connection.AbstractConnection import AbstractConnection
from tests.BaseTest import BaseTest


class test_Neo4JConnection(BaseTest):
    def test_extends_from_abstract_Connection(self):
        self.assertTrue(
            isinstance(self.app.neo4j(), AbstractConnection)
        )

    def test_returns_instance(self):
        with patch.object(neo4j.GraphDatabase, 'driver', return_value={}):
            self.assertTrue(
                isinstance(
                    self.app.neo4j().factory(),
                    type({})
                )
            )

    def test_connection_works(self):
        with patch.object(neo4j.GraphDatabase, 'driver', return_value={}):
            self.assertTrue(
                self.app.neo4j().connect()
            )

    def test_connection_fails(self):
        with patch.object(neo4j.GraphDatabase, 'driver', side_effect=Exception()):
            self.assertFalse(
                self.app.neo4j().connect()
            )


if __name__ == '__main__':
    unittest.main()
