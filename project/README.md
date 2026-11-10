# Equipment Project

This project was generated with Equipment. It includes configuration loading, dependency injection, logging, storage, database access, queues, scheduling, tests, and optional FastAPI and MCP server entry points.

## Requirements

- Python 3.13, 3.14, or 3.15.
- Windows, macOS, or Linux.
- Optional services depending on configuration: Redis, S3-compatible storage, MySQL, or PostgreSQL.

## Install

```bash
python -m pip install .
```

For development dependencies:

```bash
python -m pip install .[dev]
```

## Run

```bash
python main.py
```

Optional entry points:

```bash
python scheduler.py
python queues.py
python web.py
python mcpserver.py
```

`queues.py` requires Redis. `web.py` uses the FastAPI and Uvicorn dependencies declared in `pyproject.toml`. `mcpserver.py` uses [FastMCP](https://gofastmcp.com) to expose tools, resources, and prompts to MCP clients such as Claude Code, Claude Desktop, Cursor, or VS Code.

## Try The MCP Server

The FastMCP CLI talks to `mcpserver.py` without any MCP client:

```bash
fastmcp list mcpserver.py --resources --prompts
fastmcp call mcpserver.py inspire
```

## Connect An MCP Client

By default, `mcpserver.py` uses the `stdio` transport: the MCP client starts the process itself, from the project root, with the Python interpreter where the project is installed. For example, with Claude Code running in the project root:

```bash
claude mcp add my-app -- python mcpserver.py
```

To serve MCP over HTTP instead, set `MCP_TRANSPORT=http` in `.env`, run `python mcpserver.py`, and connect the client to `http://127.0.0.1:8001/mcp`:

```bash
claude mcp add --transport http my-app http://127.0.0.1:8001/mcp
```

With the `stdio` transport, never write to stdout (for example with `print()`): stdout carries the MCP protocol. Use `app.log()` instead.

## Test

```bash
python -m unittest discover -s tests
```

With coverage installed:

```bash
python -m coverage run -m unittest discover -s tests
python -m coverage report
```

## Configure

- Copy `.env.example` to `.env` for local overrides.
- Edit `config/app.yaml` for application name and environment.
- Edit `config/database.yaml` for SQLAlchemy connection settings.
- Edit `config/log.yaml` for log handlers and JSON formatting.
- Edit `config/queue.yaml` to switch between `sync` and `redis` queues.
- Edit `config/storage.yaml` to switch between `local` and `s3` storage.
- Edit `config/web.yaml` for FastAPI host and port.
- Edit `config/mcp.yaml` for the MCP server transport, host, port, and path.

Use `pathlib` for application file paths and prefer `python -m ...` commands for cross-platform behavior.
