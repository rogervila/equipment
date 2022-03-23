import unittest
from unittest.mock import patch
import mail1
from equipment.framework.Mail.Email.HTMLEmailFactory import HTMLEmailFactory
from equipment.framework.Mail.AbstractMail import AbstractMail
from equipment.framework.Mail.SMTPMail import SMTPMail
from equipment.framework.tests.TestCase import TestCase


class SMTPMailTest(TestCase):
    def setUp(self):
        super().setUp()
        self.mail = SMTPMail(
            config=self.app.config(),
            log=self.app.log(),
        )

    def test_extends_from_abstract_Mail(self):
        with self.app.mail.override(self.mail):
            self.assertTrue(
                isinstance(self.app.mail(), AbstractMail)
            )

    def test_email_success(self):
        with self.app.mail.override(self.mail):
            with patch.object(mail1, 'send', return_value=None):
                class MyEmail(HTMLEmailFactory):
                    subject = 'My Email Subject'
                    text = 'My Email Text'
                    html = '<p>My Email <b>HTML</b></p>'
                    sender = 'sender@example.com'
                    recipients = ['test@test.com']
                    cc = ['cc@example.com']
                    bcc = ['bcc@example.com']
                    attachments = {}

                self.assertTrue(
                    self.app.mail().send(MyEmail())
                )

    def test_email_failure(self):
        with self.app.mail.override(self.mail):
            with patch.object(mail1, 'send', side_effect=Exception()):
                class MyEmail(HTMLEmailFactory):
                    subject = 'My Email Subject'
                    text = 'My Email Text'
                    html = '<p>My Email <b>HTML</b></p>'
                    sender = 'sender@example.com'
                    recipients = ['test@test.com']
                    cc = ['cc@example.com']
                    bcc = ['bcc@example.com']
                    attachments = {}

                self.assertFalse(
                    self.app.mail().send(MyEmail())
                )


if __name__ == '__main__':
    unittest.main()
