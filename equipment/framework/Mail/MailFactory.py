from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Mail.AbstractMail import AbstractMail
from equipment.framework.Mail.SMTPMail import SMTPMail
from equipment.framework.Mail.SESMail import SESMail
from equipment.framework.Mail.LogMail import LogMail
from typing import Union
from equipment.framework.Mail.Email.Email import Email
from equipment.framework.Mail.Email.EmailFactory import EmailFactory


class MailFactory(AbstractMail):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        driver_name = config.get('MAIL', 'driver')

        if driver_name == 'smtp':
            self.driver = SMTPMail(config, log)
        elif driver_name == 's3':
            self.driver = SESMail(config, log)
        elif driver_name == 'log':
            self.driver = LogMail(config, log)
        else:
            error = f'Mail driver "{driver_name}" is not supported'
            log.error(error)
            raise NotImplementedError(error)

    def send(self, email: Union[Email, EmailFactory]) -> bool:
        return self.driver.send(email)
