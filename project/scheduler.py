#!/usr/bin/env python

from app import app

app = app()
app.log().info(
    f'''
    Welcome to {app.config.app.name()}

    This file runs a task scheduler that executes the tasks defined in app/Scheduler.py.
    '''
)

app.scheduler().run()
