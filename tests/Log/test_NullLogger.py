import unittest
from logging import Logger, getLogger
from equipment.Log.AbstractLogger import AbstractLogger
from equipment.Log.NullLogger import NullLogger


class AbstractLoggerTest(unittest.TestCase):
    def test_get_logger_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            AbstractLogger().get_logger()


class NullLoggerTest(unittest.TestCase):
    def test_log_methods_discard_records(self):
        log = NullLogger()

        self.assertIsNone(log.debug('debug'))
        self.assertIsNone(log.info('info'))
        self.assertIsNone(log.warning('warning'))
        self.assertIsNone(log.error('error'))
        self.assertIsNone(log.critical('critical'))

    def test_get_logger_returns_disabled_standalone_logger(self):
        log = NullLogger()
        logger = log.get_logger()

        self.assertIsInstance(logger, Logger)
        self.assertTrue(logger.disabled)
        self.assertIs(logger, log.get_logger())
        self.assertIsNot(getLogger(logger.name), logger)

        with self.assertNoLogs(logger):
            logger.critical('critical')


if __name__ == '__main__':
    unittest.main()
