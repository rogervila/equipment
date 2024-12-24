#!/usr/bin/env python

from redis import Redis
from rq import Worker
from app import app


app = app()
app.log().info(
    f'''
    Welcome to {app.config.app.name()}

    This file runs a Redis worker that handles asynchronous queued requests.
    Check the queue example in main.py
    '''
)

config = app.config.queue.connections.redis()

redis = Redis(
    host=config['host'],
    port=int(config['port']),
    db=int(config['db']),
)

w = Worker(['default'], connection=redis)
w.work()
