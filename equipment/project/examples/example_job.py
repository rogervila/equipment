#!/usr/bin/env python

from app.Jobs.ExampleJob import ExampleJob

print('''
Instead of loading the app Container on main.py, you can use Jobs directly, since they already load the Container
''')

ExampleJob.dispatchSync('Running job')

ExampleJob.dispatch('Running job on queue')
