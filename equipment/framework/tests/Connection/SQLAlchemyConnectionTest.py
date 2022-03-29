import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm.session import Session
from equipment.framework.Connection.SQLAlchemyConnection import SQLAlchemyConnection
from equipment.framework.tests.TestCase import TestCase


class SQLAlchemyConnectionTest(TestCase):
    def setUp(self):
        super().setUp()
        self.sql = SQLAlchemyConnection(
            config=self.app.config(),
            log=self.app.log()
        )

    def test_abstract_methods(self):
        with self.assertRaises(NotImplementedError):
            self.sql.connect()

    def test_url_method(self):
        self.sql.engine = MagicMock()
        self.sql.connection = 'foo'

        self.assertEqual(
            self.sql.url(),
            'foo'
        )

    def test_session_method(self):
        self.sql.engine = MagicMock()
        self.sql.connection = 'foo'

        self.assertIsInstance(self.sql.session(), Session)


if __name__ == '__main__':
    unittest.main()
