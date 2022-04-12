from typing import Optional
from html2text import html2text
from equipment.framework.Mail.Email.Email import Email
from equipment.framework.Mail.Email.HTMLEmailFactory import HTMLEmailFactory


class TextEmailFactory(HTMLEmailFactory):
    text = None  # type: str
    html = None  # type: None

    def render(self, template: str, parameters: Optional[dict] = None) -> None:
        self.load()

        self.text = html2text(
            self.jinja.get_template(template).render(
                parameters if parameters is not None else {}
            )
        )

    def make(self) -> Email:
        if self.text is None:
            raise ValueError('"text" cannot be None')

        self.html = None

        return super().make()
