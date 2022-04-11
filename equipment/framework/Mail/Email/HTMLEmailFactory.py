from os import sep
from typing import Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja_markdown import MarkdownExtension
from premailer import transform
from html2text import html2text
from equipment.framework.helpers import base_path
from equipment.framework.Mail.Email.Email import Email
from equipment.framework.Mail.Email.EmailFactory import EmailFactory


class HTMLEmailFactory(EmailFactory):
    text = None  # type: str
    html = None  # type: str
    jinja = None  # type: Environment

    def load(self) -> None:
        if self.jinja is None:
            self.reload()

    def reload(self) -> None:
        self.jinja = Environment(
            loader=FileSystemLoader(
                str(base_path(f'resources{sep}views{sep}emails'))
            ),
            autoescape=select_autoescape()
        )

        self.jinja.add_extension(MarkdownExtension)

    def render(self, template: str, parameters: Optional[dict] = None) -> None:
        self.load()

        self.html = transform(
            (self.jinja.get_template(template)).render(
                parameters if parameters is not None else {}
            )
        )

        self.text = html2text(self.html)

    def make(self) -> Email:
        if self.html is None:
            raise ValueError('"html" cannot be None')

        return super().make()
