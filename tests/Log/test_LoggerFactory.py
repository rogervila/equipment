from tempfile import gettempdir
import unittest
from random import randint
from logging import StreamHandler, FileHandler, NullHandler, DEBUG
from logging.handlers import TimedRotatingFileHandler
from equipment.Log.LoggerFactory import LoggerFactory
from pythonjsonlogger.jsonlogger import JsonFormatter
from os import sep


class LoggerFactoryTest(unittest.TestCase):
    def test_logger_level_normalization(self):
        config = {'channel': None, 'level': ' dEbUg '}
        factory = LoggerFactory('', gettempdir(), config)
        self.assertEqual(DEBUG, factory.logger.getEffectiveLevel())

    def test_get_handlers_list_null(self):
        config = {'channel': None, 'level': 'debug'}
        factory = LoggerFactory('', gettempdir(), config)
        handlers = factory._get_handlers_list()
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
        handlers = factory._get_handlers_list()
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
        handlers = factory._get_handlers_list()
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
        handlers = factory._get_handlers_list()
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
        handlers = factory._get_handlers_list()
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
        handlers = factory._get_handlers_list()
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0].formatter, JsonFormatter)
        self.assertEqual(indent, handlers[0].formatter.json_indent)
        handlers[0].close()
