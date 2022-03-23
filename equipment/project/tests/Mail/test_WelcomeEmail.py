import unittest
from app.Mail.WelcomeEmail import WelcomeEmail
from tests.TestCase import TestCase


class test_WelcomeMail(TestCase):
    def test_welcome_email(self):
        user_name = self.faker.name()

        factory = WelcomeEmail()
        factory.subject = 'Welcome'
        factory.sender = self.faker.email()
        factory.recipients = self.faker.email()

        factory.user_name = user_name
        email = factory.make()

        self.assertIn(user_name, email.text)
        self.assertIn(user_name, email.html)


if __name__ == '__main__':
    unittest.main()
