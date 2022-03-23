import unittest
from equipment.framework.Mail.Email.HTMLEmailFactory import HTMLEmailFactory
from equipment.framework.Mail.AbstractMail import AbstractMail
from equipment.framework.tests.TestCase import TestCase


class AbstractMailTest(TestCase):
    def test_abstract_methods(self):
        class TestMail(AbstractMail):
            pass

        with self.assertRaises(NotImplementedError):
            class MyEmail(HTMLEmailFactory):
                subject = 'My Email Subject'
                text = 'My Email Text'
                html = '<p>My Email <b>HTML</b></p>'
                sender = 'sender@example.com'
                recipients = ['test@test.com']
                cc = ['cc@example.com']
                bcc = ['bcc@example.com']
                attachments = {}

            TestMail().send(MyEmail())


if __name__ == '__main__':
    unittest.main()
