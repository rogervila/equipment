#!/usr/bin/env python

from equipment.framework import equipment
from app.Mail.WelcomeEmail import WelcomeEmail

app = equipment()


app.log().info(
    f'''

    Welcome to {app.config().get('APP', 'name')}

    Do you to send an email?

    Go to the root folder and run:

    $ rm main.py && mv examples/example_email.py main.py
    $ py main.py
    '''
)

email = WelcomeEmail()
email.sender = 'example@example.com'
email.recipients = 'test@test.com'
email.user_name = 'John Doe'

app.mail().send(email)
