#!/usr/bin/env python

from app.App.Container import Container

app = Container()

app.log().info(
    f'''

    Welcome to {app.config().get('APP', 'name')}

    Do you need to run scheduled tasks?

    $ pip install -r requirements.txt
    $ py scheduler.py

    Do you need to enqueue tasks?

    $ pip install -r requirements.txt
    $ rq worker --with-scheduler --url redis://localhost:6379/0

    Do you need to run a web server?

    Linux:
    $ pip install -r requirements.txt
    $ waitress-serve --listen *:8000 web:app

    Windows:
    $ pip install -r .\\requirements.txt
    $ waitress-serve.exe --listen *:8000 web:app

    Check other examples on ./examples directory
    '''
)
