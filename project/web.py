#!/usr/bin/env python

from app import app
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from uvicorn import Server, Config

app = app()
app.log().info(
    f'''
    Welcome to {app.config.app.name()}

    This file runs a FastAPI server defined in ./config/web.yaml
    host: {app.config.web.host()}
    port: {app.config.web.port()}
    '''
)

name = app.config.app.name()
web = FastAPI(title=name)


@web.get("/", response_class=HTMLResponse)
async def landing() -> str:
    return f'''
        <h1>{name}</h1>
        <hr />
        <p>{app.inspiring().quote()}</p>
    '''

if __name__ == '__main__':
    try:
        server = Server(Config(
            app='web:web',
            host=str(app.config.web.host()),
            port=int(app.config.web.port()),
        ))
        server.run()
    except KeyboardInterrupt:
        app.log().info('Exiting webserver...')
        exit()
