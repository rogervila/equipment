from tempfile import gettempdir
import unittest
from random import randint
from logging import StreamHandler, FileHandler, NullHandler, DEBUG
from logging.handlers import TimedRotatingFileHandler
from equipment.Log.LoggerFactory import LoggerFactory
from os import sep

class LoggerFactoryTest(unittest.TestCase):
    def test_logger_level_normalization(self):
        factory = LoggerFactory('', gettempdir(), {'channel': None, 'level': ' dEbUg '})
        self.assertEqual(DEBUG, factory.logger.getEffectiveLevel())

    def test_get_handlers_list_null(self):
        config = {'channel': None, 'level': 'debug'}
        factory = LoggerFactory('', gettempdir(), config)
        handlers = factory._get_handlers_list(config)
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], NullHandler)
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
        handlers = factory._get_handlers_list(config)
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], FileHandler)
        self.assertEqual(f'{gettempdir()}{sep}{filename}', handlers[0].baseFilename)
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
        handlers = factory._get_handlers_list(config)
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], TimedRotatingFileHandler)
        self.assertEqual(f'{gettempdir()}{sep}{filename}', handlers[0].baseFilename)
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
        handlers = factory._get_handlers_list(config)
        self.assertEqual(1, len(handlers))
        self.assertIsInstance(handlers[0], StreamHandler)
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
        handlers = factory._get_handlers_list(config)
        self.assertEqual(2, len(handlers))
        self.assertIsInstance(handlers[0], FileHandler)
        self.assertIsInstance(handlers[1], TimedRotatingFileHandler)
        handlers[0].close()
        handlers[1].close()
