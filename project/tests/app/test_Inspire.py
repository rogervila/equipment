import unittest
from tests.TestCase import TestCase
from app.Inspire import Inspire


class TestInspire(TestCase):
    def test_quote(self):
        quotes = [self.fake.text(), self.fake.text(), self.fake.text()]
        inspire = Inspire(quotes)

        quote = inspire.quote()

        self.assertIn(quote, quotes)

    def test_app_quote(self):
        quote = self.app.inspiring().quote()

        self.assertIn(quote, self.app.config.inspiring.quotes())


if __name__ == '__main__':
    unittest.main()
