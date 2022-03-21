from equipment.framework.Mail.Email.Email import Email
from equipment.framework.Mail.Email.HTMLEmailFactory import HTMLEmailFactory


class WelcomeEmail(HTMLEmailFactory):
    user_name = None  # type: str
    registration_link = 'https://example.com'

    def make(self) -> Email:
        self.render('welcome.html', {
            'user_name': self.user_name,
            'registration_link': self.registration_link,
        })

        self.subject = f'Welcome, {self.user_name}!'

        return super().make()
