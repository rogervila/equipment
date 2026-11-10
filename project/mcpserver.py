#!/usr/bin/env python

from app import app
from fastmcp import FastMCP

app = app()

name = app.config.app.name()
transport = str(app.config.mcp.transport())
host = str(app.config.mcp.host())
port = int(app.config.mcp.port())
path = str(app.config.mcp.path())

app.log().info(
    f'''
    Welcome to {name}

    This file runs an MCP server defined in ./config/mcp.yaml
    transport: {transport}
    {'MCP clients start this file and talk to it through stdin/stdout' if transport == 'stdio' else f'url: http://{host}:{port}{path}'}
    '''
)

# mask_error_details: clients only see messages from fastmcp.exceptions.ToolError, never other exception details
mcp = FastMCP(name, instructions=f'Tools, resources and prompts exposed by {name}.', mask_error_details=True)


@mcp.tool
def inspire() -> str:
    """Return a random inspiring quote."""
    return app.inspiring().quote()


@mcp.resource('quotes://all', mime_type='application/json')
def quotes() -> list[str]:
    """Every quote defined in ./config/inspiring.json."""
    return app.config.inspiring.quotes()


@mcp.prompt
def motivate(topic: str) -> str:
    """Ask for a short motivational message about a topic."""
    return f'Write a short motivational message about {topic}. Take inspiration from this quote: {app.inspiring().quote()}'


if __name__ == '__main__':
    try:
        if transport == 'stdio':
            mcp.run('stdio', show_banner=False)
        else:
            mcp.run(transport, host=host, port=port, path=path, show_banner=False, host_origin_protection='auto')
    except KeyboardInterrupt:
        app.log().info('Exiting MCP server...')
        exit()
