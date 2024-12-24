import unittest
from sqlalchemy import Engine
from sqlalchemy.orm.session import Session
from equipment.Log.NullLogger import NullLogger
from equipment.Database.SQLAlchemyFactory import SQLAlchemyFactory
from os import sep

class SQLAlchemyFactoryTest(unittest.TestCase):
    def test_sqlite_url(self):
        config = {
            'connection': 'sqlite',
            'connections': {
                'sqlite': {
                    'schema': 'sqlite',
                    'database': 'test.db'
                }
            }
        }
        base_path = '/tmp'
        factory = SQLAlchemyFactory(config, base_path, NullLogger())
        expected = f'sqlite:////tmp{sep}test.db'
        self.assertEqual(expected, factory.url)

    def test_sqlite_memory_url(self):
        config = {
            'connection': 'sqlite',
            'connections': {
                'sqlite': {
                    'schema': 'sqlite',
                    'database': ':memory:'
                }
            }
        }
        factory = SQLAlchemyFactory(config, '/path/not/used', NullLogger())
        expected = 'sqlite://'
        self.assertEqual(expected, factory.url)

    def test_mysql_url(self):
        try:
            import MySQLdb
            self.assertIsInstance(MySQLdb.version_info, tuple)
        except ImportError:
            self.skipTest('MySQLdb module not available')

        config = {
            'connection': 'mysql',
            'connections': {
                'mysql': {
                    'schema': 'mysql',
                    'username': 'user',
                    'password': 'pass',
                    'host': 'localhost',
                    'port': 3306,
                    'database': 'mydb',
                    'charset': 'utf8mb4'
                }
            }
        }
        factory = SQLAlchemyFactory(config, '', NullLogger())
        expected = 'mysql://user:pass@localhost:3306/mydb?charset=utf8mb4'
        self.assertEqual(expected, factory.url)

    def test_postgresql_url(self):
        try:
            import psycopg2
        except ImportError:
            self.skipTest('psycopg2 module not available')

        config = {
            'connection': 'postgresql',
            'connections': {
                'postgresql': {
                    'schema': 'postgresql',
                    'username': 'user',
                    'password': 'pass',
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'mydb'
                }
            }
        }
        factory = SQLAlchemyFactory(config, '', NullLogger())
        expected = 'postgresql://user:pass@localhost:5432/mydb'
        self.assertEqual(expected, factory.url)

    def test_unknown_connection(self):
        config = {'connection': 'unknown'}
        with self.assertRaises(ValueError):
            SQLAlchemyFactory(config, '', NullLogger())

    def test_create_engine(self):
        config = {
            'connection': 'sqlite',
            'connections': {
                'sqlite': {
                    'schema': 'sqlite',
                    'database': ':memory:'
                }
            }
        }
        factory = SQLAlchemyFactory(config, '', NullLogger())
        self.assertIsInstance(factory.engine, Engine)

    def test_create_session(self):
        config = {
            'connection': 'sqlite',
            'connections': {
                'sqlite': {
                    'schema': 'sqlite',
                    'database': ':memory:'
                }
            }
        }
        factory = SQLAlchemyFactory(config, '', NullLogger())
        session = factory.session()
        self.assertIsInstance(session, Session)
