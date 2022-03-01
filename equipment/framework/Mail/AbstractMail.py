import abc
from typing import Union
from equipment.framework.Mail.Email.Email import Email
from equipment.framework.Mail.Email.EmailFactory import EmailFactory


class AbstractMail(abc.ABC):
    def send(self, email: Union[Email, EmailFactory]) -> bool:
        raise NotImplementedError
