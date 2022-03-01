from typing import Optional
from py_dto import DTO


class Email(DTO):
    subject: str
    text: Optional[str]
    html: Optional[str]
    sender: str
    recipients: list
    cc: list
    bcc: list
    attachments: dict
    encoding: str
