from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Mail.AbstractMail import AbstractMail
from typing import Union
from equipment.framework.Mail.Email.Email import Email
from equipment.framework.Mail.Email.EmailFactory import EmailFactory
from pprint import pformat


class LogMail(AbstractMail):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
        self.log = log

    def send(self, email: Union[Email, EmailFactory]) -> bool:
        if isinstance(email, EmailFactory):
            email = email.make()

        self.log.info(pformat({
            'subject': email.subject,
            'text': email.text,
            'html': email.html,
            'sender': email.sender,
            'recipients': email.recipients,
            'cc': email.cc,
            'bcc': email.bcc,
            'attachments': email.attachments,
            'encoding': email.encoding,
        }, width=self.config.get('MAIL_LOG', 'width')))

        return True
