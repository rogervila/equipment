#!/usr/bin/env python

from app.Jobs.ExampleJob import ExampleJob

print('''

Instead of loading the equipment
you can may Jobs that already
load the framework

''')

ExampleJob.dispatchSync('Running job')

ExampleJob.dispatch('Running job on queue')
