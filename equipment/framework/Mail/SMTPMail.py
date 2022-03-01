import mail1
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Mail.AbstractMail import AbstractMail
from typing import Union
from equipment.framework.Mail.Email.Email import Email
from equipment.framework.Mail.Email.EmailFactory import EmailFactory


class SMTPMail(AbstractMail):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
        self.log = log

    def send(self, email: Union[Email, EmailFactory]) -> bool:
        if isinstance(email, EmailFactory):
            email = email.make()

        try:
            mail1.send(
                subject=email.subject,
                text=email.text,
                text_html=email.html,
                sender=email.sender,
                recipients=email.recipients,
                cc=email.cc,
                bcc=email.bcc,
                attachments=email.attachments,
                smtp_host=self.config.get('MAIL_SMTP', 'host'),
                smtp_port=int(self.config.get('MAIL_SMTP', 'port')),
                username=self.config.get('MAIL_SMTP', 'user'),
                password=self.config.get('MAIL_SMTP', 'password')
            )

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False
