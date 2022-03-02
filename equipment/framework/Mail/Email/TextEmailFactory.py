from equipment.framework.Mail.Email.Email import Email
from equipment.framework.Mail.Email.HTMLEmailFactory import HTMLEmailFactory
from html2text import html2text


class TextEmailFactory(HTMLEmailFactory):
    text = None  # type: str
    html = None  # type: None

    # pylint: disable=dangerous-default-value
    def render(self, template: str, parameters: dict = {}) -> None:
        self.load()

        self.text = html2text(
            self.jinja.get_template(template).render(parameters)
        )

    def make(self) -> Email:
        if self.text is None:
            raise ValueError('"text" cannot be None')

        self.html = None

        return super().make()
