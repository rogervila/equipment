import unittest
import boto3
from moto import mock_ses
from equipment.framework.Mail.Email.HTMLEmailFactory import HTMLEmailFactory
from equipment.framework.Mail.AbstractMail import AbstractMail
from equipment.framework.Mail.SESMail import SESMail
from equipment.framework.tests.TestCase import TestCase


class SESMailTest(TestCase):
    def setUp(self):
        super().setUp()
        self.mail = SESMail(
            config=self.app.config(),
            log=self.app.log(),
        )

    def test_extends_from_abstract_Mail(self):
        with self.app.mail.override(self.mail):
            self.assertTrue(
                isinstance(self.app.mail(), AbstractMail)
            )

    @mock_ses
    def test_send_email_without_attachments(self):
        with self.app.mail.override(self.mail):
            self.app.mail().client = boto3.client('ses', region_name='us-east-1')
            self.app.mail().client.verify_email_address(EmailAddress='sender@example.com')

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

    '''
    @mock_ses
    def test_send_email_with_attachments(self):
        with self.app.mail.override(self.mail):
            self.app.mail().client = boto3.client('ses')
            self.app.mail().client.verify_email_address(EmailAddress='sender@example.com')

            class MyEmail(HTMLEmailFactory):
                subject = 'My Email Subject'
                text = 'My Email Text'
                html = '<p>My Email <b>HTML</b></p>'
                sender = 'sender@example.com'
                recipients = ['test@test.com']
                cc = ['cc@example.com']
                bcc = ['bcc@example.com']
                attachments = {
                    TODO: SESEmail attachments support
                }

            self.assertTrue(
                self.app.mail().send(MyEmail())
            )
    '''


if __name__ == '__main__':
    unittest.main()
