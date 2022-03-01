import abc
from typing import Optional, Union
from equipment.framework.Mail.Email.Email import Email


class EmailFactory(abc.ABC):
    subject = None  # type: str
    text = None  # type: Optional[str]
    html = None  # type: Optional[str]
    sender = None  # type: str
    recipients = None  # type: Union[list,str]
    cc = None  # type: list
    bcc = None  # type: list
    attachments = None  # type: dict
    encoding = None  # type: str

    # pylint: disable=dangerous-default-value
    def render(self, template: str, parameters: dict = {}) -> None:
        raise NotImplementedError

    def make(self) -> Email:
        data = {
            'subject': self.subject,
            'text': self.text,
            'html': self.html,
            'sender': self.sender,
            'recipients': self.recipients,
            'cc': self.cc,
            'bcc': self.bcc,
            'attachments': self.attachments,
            'encoding': self.encoding
        }

        if 'recipients' not in data:
            raise ValueError('''
            "recipients" should be a list or a str with email addresses
            ''')

        if isinstance(data['recipients'], str):
            data['recipients'] = [data['recipients']]

        if 'cc' not in data or data['cc'] is None:
            data['cc'] = []

        if 'bcc' not in data or data['bcc'] is None:
            data['bcc'] = []

        if 'attachments' not in data or data['attachments'] is None:
            data['attachments'] = {}

        if 'encoding' not in data or data['encoding'] is None:
            data['encoding'] = 'UTF-8'

        if ('html' not in data or data['html'] is None) and ('text' not in data or data['text'] is None):
            raise ValueError('''
            "html" and "text" fields cannot be None at the same time.
            At least one of both should contain the email content
            ''')

        return Email(data)
