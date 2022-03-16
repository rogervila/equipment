#!/usr/bin/env python

from equipment.framework import equipment

app = equipment()

app.log().info(
    f"Welcome to {app.config().get('APP', 'name')}"
)

app.scheduler().run()
