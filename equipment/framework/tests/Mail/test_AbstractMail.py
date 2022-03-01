import unittest
from equipment.framework.Mail.AbstractEmail import AbstractEmail
from equipment.framework.Mail.AbstractMail import AbstractMail
from tests.BaseTest import BaseTest


class test_AbstractMail(BaseTest):
    def test_abstract_methods(self):
        class TestMail(AbstractMail):
            pass

        with self.assertRaises(NotImplementedError):
            class MyEmail(AbstractEmail):
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
