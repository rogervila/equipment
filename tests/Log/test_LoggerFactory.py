from tempfile import gettempdir
from os import sep
from codecs import open  # pylint: disable=W0622
import unittest
from sqlite3 import connect
from logging import StreamHandler, FileHandler, NullHandler, DEBUG
from logging.handlers import TimedRotatingFileHandler
from random import randint
from pythonjsonlogger.jsonlogger import JsonFormatter
from python_sqlite_log_handler import SQLiteLogHandler
from equipment.Log.LoggerFactory import LoggerFactory


class LoggerFactoryTest(unittest.TestCase):
    def test_logger_level_normalization(self):
        config = {'channel': None, 'level': ' dEbUg '}
        factory = LoggerFactory('', gettempdir(), config)
        self.assertEqual(DEBUG, factory.logger.getEffectiveLevel())

    def test_get_handlers_list_null(self):
        config = {'channel': None, 'level': 'debug'}
        factory = LoggerFactory('', gettempdir(), config)
        handlers = factory._get_handlers_list() # pylint: disable=W0212
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], NullHandler)
        self.assertIsNone(handlers[0].formatter)
        handlers[0].close()

    def test_get_handlers_list_single_file(self):
        filename = f'{str(randint(9, 99999))}.log'
        config = {
            'level': 'debug',
            'channel': 'single',
            'channels': {
                'single': {'filename': filename}
            }
        }
        factory = LoggerFactory(gettempdir(), gettempdir(), config)
        handlers = factory._get_handlers_list() # pylint: disable=W0212
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], FileHandler)
        self.assertEqual(
            f'{gettempdir()}{sep}{filename}',
            handlers[0].baseFilename
        )
        self.assertIsNone(handlers[0].formatter)
        handlers[0].close()

    def test_get_handlers_list_daily_file(self):
        filename = f'{str(randint(9, 99999))}.log'
        config = {
            'level': 'debug',
            'channel': 'daily',
            'channels': {
                'daily': {'filename': filename, 'when': 'D', 'interval': 1, 'backupCount': 7}
            }
        }
        factory = LoggerFactory(gettempdir(), gettempdir(), config)
        handlers = factory._get_handlers_list() # pylint: disable=W0212
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], TimedRotatingFileHandler)
        self.assertEqual(
            f'{gettempdir()}{sep}{filename}',
            handlers[0].baseFilename
        )
        self.assertEqual('D', handlers[0].when)
        self.assertEqual(60 * 60 * 24, handlers[0].interval)  # when == 'D'
        self.assertEqual(7, handlers[0].backupCount)
        self.assertIsNone(handlers[0].formatter)
        handlers[0].close()

    def test_get_handlers_list_console(self):
        config = {
            'level': 'debug',
            'channel': 'console',
            'channels': {
                'console': {'stream': None}  # 'ext://sys.stdout'
            }
        }
        factory = LoggerFactory('', gettempdir(), config)
        handlers = factory._get_handlers_list() # pylint: disable=W0212
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], StreamHandler)
        self.assertIsNone(handlers[0].formatter)
        handlers[0].close()

    def test_get_handlers_list_stack(self):
        config = {
            'level': 'debug',
            'channel': 'stack',
            'channels': {
                'stack': {
                    'channels': ['single', 'daily'],
                },
                'single': {'filename': f'{str(randint(9, 99999))}.log'},
                'daily': {'filename': f'{str(randint(9, 99999))}.log', 'when': 'D', 'interval': 1, 'backupCount': 7},
            }
        }
        factory = LoggerFactory(gettempdir(), gettempdir(), config)
        handlers = factory._get_handlers_list() # pylint: disable=W0212
        self.assertEqual(2, len(handlers))
        self.assertIsInstance(handlers[0], FileHandler)
        self.assertIsNone(handlers[0].formatter)
        self.assertIsInstance(handlers[1], TimedRotatingFileHandler)
        self.assertIsNone(handlers[1].formatter)
        handlers[0].close()
        handlers[1].close()

    def test_get_handlers_list_json_formatter(self):
        indent = randint(2, 8)
        config = {
            'level': 'debug',
            'channel': 'console',
            'channels': {
                'console': {'stream': None, 'formatter': 'json'}
            },
            'formatters': {
                'json': {
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'indent': indent
                }
            }
        }
        factory = LoggerFactory(gettempdir(), gettempdir(), config)
        handlers = factory._get_handlers_list() # pylint: disable=W0212
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0].formatter, JsonFormatter)
        self.assertEqual(indent, handlers[0].formatter.json_indent)
        handlers[0].close()

    def test_sqlite_channel(self):
        filename = f'{str(randint(9, 99999))}.sqlite'
        config = {
            'level': 'debug',
            'channel': 'sqlite',
            'channels': {
                'sqlite': {'filename': filename}
            }
        }
        factory = LoggerFactory(gettempdir(), gettempdir(), config)
        handlers = factory._get_handlers_list() # pylint: disable=W0212
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], SQLiteLogHandler)


        self.assertEqual(
            f'{gettempdir()}{sep}{filename}',
            handlers[0].db_path
        )
        self.assertIsNone(handlers[0].formatter)


        msg = f'test msg {str(randint(9, 99999))}'
        factory.debug(msg)
        handlers[0].close()

        conn = connect(handlers[0].db_path)
        cursor = conn.cursor()

        '''
        # TODO: Cannot perform this select query because the file is locked by another thread.
        cursor.execute(f'SELECT COUNT(*) FROM logs WHERE message = "{msg}"')
        count = cursor.fetchone()[0]
        self.assertEqual(1, count)
        '''

        cursor.execute("PRAGMA journal_mode")
        self.assertEqual("wal", cursor.fetchone()[0].lower())

        cursor.execute("PRAGMA synchronous")
        self.assertEqual(2, int(cursor.fetchone()[0]))

        cursor.close()

        conn.close()

    def test_keeps_module(self):
        filename = f'{str(randint(9, 99999))}.log'
        config = {
            'level': 'debug',
            'channel': 'single',
            'channels': {
                'single': {'filename': filename, 'formatter': 'json'}
            },
            'formatters': {
                'json': {
                    'format': '%(pathname)s %(lineno)s %(message)s',
                    'indent': None
                }
            }
        }
        factory = LoggerFactory(gettempdir(), gettempdir(), config)

        message = f'test message {str(randint(9, 99999))}'
        factory.debug(message)

        with open(f'{gettempdir()}{sep}{filename}', 'r') as file:
            lines = file.readlines()
            self.assertEqual(1, len(lines))
            self.assertTrue(message in lines[0])
            self.assertTrue('test_LoggerFactory.py' in lines[0])
