#!/usr/bin/env python

from app.App.Container import Container

app = Container()

app.log().info(
    f"Welcome to {app.config().get('APP', 'name')}"
)

app.scheduler().run()
