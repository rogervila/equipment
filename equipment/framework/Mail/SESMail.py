from typing import Union
from boto3 import client
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Mail.AbstractMail import AbstractMail
from equipment.framework.Mail.Email.Email import Email
from equipment.framework.Mail.Email.EmailFactory import EmailFactory


class SESMail(AbstractMail):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
        self.log = log
        self.log.debug('aws_endpoint:')
        self.log.debug(self.config.get('MAIL_SES', 'aws_endpoint'))
        self.client = None

    def load(self) -> None:
        if self.client is None:
            self.reload()

    def reload(self) -> None:
        self.client = client(
            service_name='ses',
            endpoint_url=self.config.get('MAIL_SES', 'aws_endpoint'),
            region_name=self.config.get('MAIL_SES', 'aws_region'),
            aws_access_key_id=self.config.get(
                'MAIL_SES', 'aws_access_key_id'),
            aws_secret_access_key=self.config.get(
                'MAIL_SES', 'aws_secret_access_key'),
        )

    def send(self, email: Union[Email, EmailFactory]) -> bool:
        if isinstance(email, EmailFactory):
            email = email.make()

        return self._send_without_attachments(email) if len(email.attachments.keys()) == 0 else self._send_with_attachments(email)

    def _send_with_attachments(self, email: Email) -> bool:
        raise NotImplementedError

    def _send_without_attachments(self, email: Email) -> bool:
        try:
            self.load()

            response = self.client.send_email(
                Source=email.sender,
                Destination={
                    'ToAddresses': email.recipients,
                    'CcAddresses': email.cc,
                    'BccAddresses': email.bcc
                },
                Message={
                    'Subject': {
                        'Data': email.subject,
                        'Charset': email.encoding
                    },
                    'Body': {
                        'Text': {
                            'Data': email.text,
                            'Charset': email.encoding
                        },
                        'Html': {
                            'Data': email.html,
                            'Charset': email.encoding
                        }
                    }
                },
            )

            # for adding attachments support -> https://www.learnaws.org/2020/12/18/aws-ses-boto3-guide/#how-to-send-an-email-with-attachments-using-ses

            self.log.debug('Email sent! Message ID:')
            self.log.debug(response['MessageId'])

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False
