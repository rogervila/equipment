---
sidebar_position: 2
---

# MCP Server Example

Generated Equipment projects include `mcpserver.py`, a small [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server built with [FastMCP](https://gofastmcp.com). It exposes application services as MCP tools, resources, and prompts. MCP clients like Claude Code, Claude Desktop, Cursor, or VS Code can then use them.

It follows the same strategy as the [FastAPI example](./fastapi.md). One entry point file reads its settings from `config/mcp.yaml` and uses the generated `app()` container. Tools can use every Equipment service: configuration, logs, queues, storage, database, and your own services.

:::info Why `mcpserver.py` and not `mcp.py`
Python puts the project root first on the import path. FastMCP is built on the MCP Python SDK, whose package is named `mcp`. A project file named `mcp.py` would replace that package for every `import mcp`, including the imports inside FastMCP. `python mcp.py` and the test suite would then fail with a misleading error: `ImportError: FastMCP server support is not installed`. For the same reason, the queue worker is `queues.py` and not `queue.py`, which would shadow the standard library `queue` module.
:::

## Quick Start

This walkthrough connects a new project to Claude Code with the default `stdio` transport. Other clients follow the same idea (see [Connect A Client](#connect-a-client)).

1. Create the project, and install it in a virtual environment:

   ```bash
   equipment new my-app
   cd my-app
   python -m venv .venv
   ```

   Activate the virtual environment: `source .venv/bin/activate` on Linux and macOS, or `.venv\Scripts\activate` on Windows. Then install the project:

   ```bash
   python -m pip install .
   ```

2. Check that the MCP server works, without any client:

   ```bash
   python -m unittest tests.test_mcpserver
   fastmcp call mcpserver.py inspire
   ```

3. Register the server in Claude Code. Run the command from the project root, with the virtual environment interpreter:

   ```bash
   # Linux and macOS
   claude mcp add my-app -- .venv/bin/python mcpserver.py

   # Windows
   claude mcp add my-app -- .venv\Scripts\python.exe mcpserver.py
   ```

   You do not start the server yourself. Claude Code starts `mcpserver.py` from the project root when a session begins, and stops it at the end.

4. Start `claude` in the project root, and check the connection with `/mcp`. The server `my-app` must show as connected, with the `inspire` tool.

5. Use it:

   - **Tools**: ask "Give me an inspiring quote from my-app". The model calls the `inspire` tool, which runs `app.inspiring().quote()`.
   - **Resources**: type `@my-app:quotes://all` in a message to attach the quote list.
   - **Prompts**: run `/mcp__my-app__motivate` and enter a topic.

6. Add your own tools in `mcpserver.py` (see [Add A Tool](#add-a-tool)). Then reconnect the server from `/mcp`, or restart `claude`, so the client loads the new tool list.

Logs go to `storage/logs/app.log`. With the `stack` log channel they also go to stderr, which Claude Code keeps in its MCP logs.

To run the server as a long-lived HTTP service instead, see [Run](#run).

## Library

The example uses [FastMCP](https://gofastmcp.com) (`fastmcp` on PyPI), the most widely used framework for building MCP servers in Python.

- It is built on the official MCP Python SDK, and adds what a server needs beyond the protocol: an in-memory client for tests, a CLI to run, list, and call servers, middleware, server composition, and authentication providers.
- Tools, resources, and prompts are plain Python functions. Type hints become the JSON schema, and docstrings become descriptions.
- It speaks both MCP protocol eras: the handshake era (`2025-11-25` and earlier), which most clients use today, and the modern `2026-07-28` protocol.

## Dependencies

The generated `pyproject.toml` includes:

```toml
dependencies = [
    "equipment>=1.0.0",
    "fastmcp>=4.1.7,<5", # Remove if mcpserver.py will not be used.
]
```

Install the generated project before running the MCP server:

```bash
python -m pip install .
```

FastMCP may ship breaking changes in minor versions. For production deployments, pin the exact version you tested, for example `"fastmcp==4.1.7"`.

If the project does not need an MCP server, delete `mcpserver.py`, `config/mcp.yaml`, `tests/test_mcpserver.py`, and the `fastmcp` dependency.

## Configuration

`config/mcp.yaml`:

```yaml
mcp:
  transport: ${MCP_TRANSPORT:stdio}
  host: ${MCP_HOST:127.0.0.1}
  port: ${MCP_PORT:8001}
  path: ${MCP_PATH:/mcp}
```

| Key | Default | Description |
|-----|---------|-------------|
| `transport` | `stdio` | `stdio`: the MCP client starts `mcpserver.py` and talks to it through stdin/stdout. `http`: `mcpserver.py` serves MCP over Streamable HTTP. |
| `host` | `127.0.0.1` | HTTP bind host. Only used by `http`. |
| `port` | `8001` | HTTP port. Only used by `http`. The default does not collide with `web.py` (`8000`). |
| `path` | `/mcp` | HTTP endpoint path. Only used by `http`. |

Set `MCP_TRANSPORT`, `MCP_HOST`, `MCP_PORT`, or `MCP_PATH` in `.env` or in the process environment to change runtime behavior. Values that the MCP client passes as environment variables take precedence over `.env`.

FastMCP also reads its own `FASTMCP_*` settings from the environment and from `.env`, for example `FASTMCP_LOG_LEVEL=WARNING` to hide its startup messages. See the [FastMCP settings reference](https://gofastmcp.com/docs/more/settings).

## Generated `mcpserver.py`

```python
from app import app
from fastmcp import FastMCP

app = app()

name = app.config.app.name()
transport = str(app.config.mcp.transport())
host = str(app.config.mcp.host())
port = int(app.config.mcp.port())
path = str(app.config.mcp.path())

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
```

The generated file also logs a welcome message with the active transport (omitted above).

The example shows the three MCP primitives:

- **Tools** (`@mcp.tool`) are functions the model can call. The function name, type hints, and docstring become the tool name, input schema, and description.
- **Resources** (`@mcp.resource(uri)`) are read-only data the client can load into context.
- **Prompts** (`@mcp.prompt`) are reusable prompt templates the user can pick in the client.

Three options differ from the FastMCP defaults:

- `mask_error_details=True` keeps internal error details away from clients (see [Errors](#errors)).
- `show_banner=False` replaces the FastMCP startup banner with the Equipment welcome log. The banner also checks PyPI for FastMCP updates on startup.
- `host_origin_protection='auto'` enables DNS rebinding protection for HTTP requests that reach the server through a loopback address (see [Deployment Notes](#deployment-notes)).

## Run

With the default `stdio` transport, you do not start the server yourself. The MCP client starts `python mcpserver.py` from the project root when it needs it.

To serve MCP over HTTP, set the transport in `.env`:

```env
MCP_TRANSPORT=http
```

Then start the server:

```bash
python mcpserver.py
```

The server listens on `http://127.0.0.1:8001/mcp`. Stop it with `CTRL+C`.

The FastMCP CLI can also run the server: `fastmcp run mcpserver.py --transport http --port 8001`. The CLI ignores the `if __name__ == '__main__':` block, so it takes the transport, host, port, and path from its own flags instead of `config/mcp.yaml`.

## Try It From The Terminal

The FastMCP CLI loads `mcpserver.py` and talks to it over stdio, without any MCP client. Run these commands from the project root:

```bash
# List tools, resources, and prompts
fastmcp list mcpserver.py --resources --prompts

# Call a tool, read a resource, and render a prompt
fastmcp call mcpserver.py inspire
fastmcp call mcpserver.py quotes://all
fastmcp call mcpserver.py motivate --prompt topic=testing

# Summary of the server and its components
fastmcp inspect mcpserver.py
```

Tool arguments use the `key=value` form, for example `fastmcp call mcpserver.py save_note filename=a.txt content=hi`.

## Connect A Client

### Claude Code

`stdio`: run this command from the project root. Claude Code starts the server from that directory.

```bash
claude mcp add my-app -- python mcpserver.py
```

`http`: start `python mcpserver.py` first, then add the URL:

```bash
claude mcp add --transport http my-app http://127.0.0.1:8001/mcp
```

Use the Python interpreter where the project is installed, for example `.venv/bin/python` on Linux and macOS, or `.venv\Scripts\python.exe` on Windows.

FastMCP also has a `fastmcp install claude-code` command. It runs the server through `uv` in an isolated environment, so it does not use your project virtual environment. For Equipment projects, `claude mcp add` with the project interpreter is simpler.

### JSON Configuration

Most MCP clients (Claude Desktop, Cursor, VS Code, Windsurf) use a JSON file with a similar shape. The server must start from the project root, so that `config/` and `.env` are found. Some clients accept a `cwd` key for that. Check your client documentation for the file location and the supported keys.

```json
{
  "mcpServers": {
    "my-app": {
      "command": "/absolute/path/to/project/.venv/bin/python",
      "args": ["mcpserver.py"],
      "cwd": "/absolute/path/to/project",
      "env": {
        "APP_ENV": "local"
      }
    }
  }
}
```

### MCP Inspector

The [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) is a browser UI for calling tools, reading resources, and rendering prompts by hand. It requires Node.js:

```bash
npx @modelcontextprotocol/inspector python mcpserver.py
```

## Never Write To Stdout With `stdio`

With the `stdio` transport, stdout carries the MCP protocol messages. Anything else written to stdout corrupts the stream, and the client disconnects.

- Do not call `print()` in tools or in the services they use.
- Log with `app.log()`. The default `console` channel writes to stderr, and the `single` channel writes to `storage/logs/app.log`. Both are safe.
- If you configure a custom stream for the `console` log channel, do not point it to `sys.stdout`.

FastMCP writes its own logs to stderr through the `fastmcp` logger. It does not change the root logger, so Equipment log lines are not duplicated.

The HTTP transport does not have this restriction.

## Add A Tool

Tools are plain functions. Keep them thin, and move business behavior into services registered in `app/__init__.py`:

```python
@mcp.tool
def save_note(filename: str, content: str) -> bool:
    """Save a note in the application storage."""
    app.log().info(f'Saving note {filename}')
    return app.storage().write(f'notes/{filename}', content)


@mcp.tool
def rebuild_report(report_id: int) -> str:
    """Queue a report rebuild and return immediately."""
    app.queue().push(rebuild_report_job, report_id)
    return 'queued'
```

Type hints define the input schema that the client sends to the model. Return values become structured output too:

- `dict`, Pydantic models, and dataclasses always produce structured output.
- Primitives and collections (`str`, `int`, `list[str]`) produce structured output when the function has a return type annotation.

### Sync And Async Tools

- `def` tools run in a thread pool. Use them for the usual blocking Equipment calls: database sessions, storage, queues, and HTTP clients like `requests`. Equipment providers are `ThreadSafeSingleton`s, so they are safe to share between threads.
- `async def` tools run on the event loop. Use them only when every call inside is non-blocking.

### Inject Services With `Depends`

FastMCP can inject Equipment providers into tools with `Depends`. Injected parameters are hidden from the tool schema, and container overrides still apply:

```python
from fastmcp.dependencies import Depends
from app.Inspire import Inspire


@mcp.tool
def inspire(inspiring: Inspire = Depends(app.inspiring)) -> str:
    """Return a random inspiring quote."""
    return inspiring.quote()
```

The typed parameter gives your editor autocompletion on the service. Calling `app.inspiring()` inside the tool, like the generated example does, is equivalent.

### Errors

Raise an exception inside a tool to report a failure. FastMCP sends it back to the client as a tool error (`is_error=True`), and the server keeps running.

The generated server sets `mask_error_details=True`. For a regular exception, the client only sees `Error calling tool '<name>'`, so details like file paths or database URLs do not reach the model. The full traceback still goes to stderr and to the client MCP logs.

Raise `ToolError` when the model should see the reason:

```python
from fastmcp.exceptions import ToolError


@mcp.tool
def get_report(report_id: int) -> str:
    """Return a report."""
    if not app.storage().exists(f'reports/{report_id}.txt'):
        raise ToolError(f'Report {report_id} does not exist')

    return app.storage().read(f'reports/{report_id}.txt')
```

## Split Tools Into Modules

For larger servers, group tools by domain and register them in `mcpserver.py`:

```python
# app/tools/notes.py
from fastmcp import FastMCP
from app import app


def register(mcp: FastMCP) -> None:
    @mcp.tool
    def save_note(filename: str, content: str) -> bool:
        """Save a note in the application storage."""
        return app().storage().write(f'notes/{filename}', content)
```

```python
# mcpserver.py
from app.tools import notes

notes.register(mcp)
```

`app()` always returns the same cached container, so modules can call it directly.

## Serve MCP From `web.py`

To serve MCP and the FastAPI routes from one process and one port, mount the FastMCP app in `web.py`. FastAPI must use the MCP app lifespan, which starts the MCP session manager:

```python
from mcpserver import mcp

mcp_app = mcp.http_app(path='/', host_origin_protection='auto')
web = FastAPI(title=name, lifespan=mcp_app.lifespan)

# ... routes ...

web.mount('/mcp', mcp_app)
```

Clients connect to `http://127.0.0.1:8000/mcp/`. The URL without the trailing slash also works, through a `307` redirect.

If `web.py` already has its own lifespan, combine both with `combine_lifespans` from `fastmcp.utilities.lifespan`:

```python
web = FastAPI(title=name, lifespan=combine_lifespans(app_lifespan, mcp_app.lifespan))
```

## Testing MCP Tools

`tests/test_mcpserver.py` connects the FastMCP in-memory client to the server. The test needs no subprocess and no network, and runs with plain `unittest`:

```python
import asyncio
import unittest
from importlib.util import find_spec
from tests.TestCase import TestCase
from app.Inspire import Inspire


@unittest.skipUnless(find_spec('fastmcp'), 'fastmcp is not installed')
class TestMcpServer(TestCase):
    def mcp(self, request):
        from fastmcp import Client
        from mcpserver import mcp

        async def run():
            async with Client(mcp) as client:
                return await request(client)

        return asyncio.run(run())

    def test_inspire_tool(self):
        quote = self.fake.sentence()

        # Override any App service before calling the server, then restore it
        self.app.inspiring.override(Inspire([quote]))
        self.addCleanup(self.app.inspiring.reset_override)

        result = self.mcp(lambda client: client.call_tool('inspire', {}))

        self.assertFalse(result.is_error)
        self.assertEqual(quote, result.data)
```

The test and `mcpserver.py` share the same cached `App` container. Provider overrides in a test therefore apply to the tools. Always reset overrides with `addCleanup`, because the container lives for the whole test run.

`result.data` holds the tool return value as a Python object. Other client calls follow the same shape:

```python
tools = self.mcp(lambda client: client.list_tools())  # list of tools
contents = self.mcp(lambda client: client.read_resource('quotes://all'))  # contents[0].text
prompt = self.mcp(lambda client: client.get_prompt('motivate', {'topic': 'testing'}))  # prompt.messages
```

`call_tool` raises `fastmcp.exceptions.ToolError` when the tool fails. Pass `raise_on_error=False` to inspect `result.is_error` instead.

When several test files call MCP, move the `mcp()` helper into `tests/TestCase.py`.

For service-level behavior, test the service directly without MCP. This keeps most tests fast and focused.

## Deployment Notes

- Use `MCP_TRANSPORT=http` for remote servers. `stdio` only works for clients on the same machine.
- `host_origin_protection='auto'` validates the `Host` and `Origin` headers of requests that reach the server through a loopback address, such as `127.0.0.1`. This blocks DNS rebinding attacks against local servers. Requests that arrive through another network interface are not validated, so `MCP_HOST=0.0.0.0` in a container keeps working behind a public hostname.
- To validate every request against your public hostname, edit the `mcp.run(...)` call to pass `host_origin_protection=True, allowed_hosts=['mcp.example.com']`.
- A server without authentication exposes its tools to anyone who can reach the port. Keep remote servers behind a private network or a gateway, or use the FastMCP [authentication providers](https://gofastmcp.com/docs/servers/auth/authentication).
- For several workers behind a load balancer, set `FASTMCP_STATELESS_HTTP=true`, so requests do not depend on in-memory sessions.
- `equipment compile` compiles `mcpserver.py` like the other entry points. Run it with `python mcpserver.pyc` from the compiled directory.

## Troubleshooting

The client cannot connect, or shows `Connection closed`:

- Something wrote to stdout. Search for `print()` calls, and check the client MCP logs for the stderr output of the server.
- The server did not start from the project root, so `config/` was not found. Run the client from the project root, or set its working directory (`cwd`).
- The client uses a Python interpreter without the project dependencies. Point it at the virtual environment interpreter.

`ImportError: FastMCP server support is not installed`, although `fastmcp` is installed:

A file or directory named `mcp` in the project root shadows the MCP Python SDK. Rename it. The note at the top of this page explains why.

`ModuleNotFoundError: No module named 'mcp.server.fastmcp'`:

Code written for the FastMCP 1.0 API of MCP SDK version 1. Import `FastMCP` from `fastmcp` instead.

`ValueError: Unknown transport`:

`MCP_TRANSPORT` must be `stdio` or `http`. FastMCP also accepts `streamable-http` (same as `http`) and the legacy `sse` transport.

Port is already in use:

Change `MCP_PORT` in `.env`, or stop the process using the port.

## Guidance

- Keep MCP configuration in `config/mcp.yaml` or in environment variables.
- Write clear tool docstrings and type hints: the model reads them to decide when and how to call each tool.
- Keep tools small, and move business logic into services.
- Use queues for slow work triggered by tools.
- Raise `ToolError` for failures the model should understand.
- Test tools with the in-memory client, and test services directly.
