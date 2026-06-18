<p align="center"><img src="https://rogervila.es/static/img/equipment-logo.png" alt="Equipment: Python Project Scaffolding Framework" height="200" /></p>

[![PyPI version](https://badge.fury.io/py/equipment.svg)](https://badge.fury.io/py/equipment)
![PyPI - Downloads](https://img.shields.io/pypi/dm/equipment)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://equipment-python.vercel.app)

# Equipment: Python Project Scaffolding Framework

Equipment is a scaffolding framework for starting Python applications with a ready-to-use project layout. It creates a project that already has configuration loading, dependency injection, logging, storage, SQLAlchemy database access, queues, scheduling, tests, and optional FastAPI entry points.

Use Equipment when you want a practical application skeleton instead of a blank directory. It is most useful for scripts that may grow, backend services, queue workers, scheduled jobs, internal tools, and web APIs that need consistent structure from day one.

## Requirements

- Python 3.12, 3.13, or 3.14.
- Windows, macOS, or Linux.
- `pip` for installation.
- Optional external services depending on features: Redis for the Redis queue driver, S3-compatible storage for the S3 driver, and database drivers for MySQL or PostgreSQL.

## Install

```bash
python -m pip install equipment
```

For an isolated command-line install, `pipx install equipment` also works when `pipx` is available.

## Create A Project

```bash
equipment new my-app
cd my-app
python -m pip install .
python main.py
```

On Windows, the Python launcher is also supported:

```bat
py -3.14 -m pip install equipment
equipment new my-app
cd my-app
py -3.14 -m pip install .
py -3.14 main.py
```

## Generated Project Structure

```text
my-app/
├── app/                  # Application services and scheduler definitions
│   ├── __init__.py       # App container and custom service registration
│   ├── Inspire.py        # Example service
│   └── Scheduler.py      # Example scheduled tasks
├── config/               # YAML and JSON configuration files
│   ├── app.yaml
│   ├── database.yaml
│   ├── inspiring.json
│   ├── log.yaml
│   ├── queue.yaml
│   ├── storage.yaml
│   └── web.yaml
├── database/             # SQLite file location and Alembic migrations
├── storage/              # Local storage and log directories
├── tests/                # unittest base class and example tests
├── .env.example          # Environment variable template
├── main.py               # Script entry point and feature examples
├── queues.py             # Redis queue worker entry point
├── scheduler.py          # Scheduler process entry point
├── web.py                # FastAPI entry point
├── pyproject.toml        # Generated project metadata and dependencies
└── README.md             # Generated project guide
```

## Common Workflows

Run the generated script:

```bash
python main.py
```

Run the generated tests:

```bash
python -m unittest discover -s tests
```

Run the scheduler:

```bash
python scheduler.py
```

Run the Redis worker after setting `QUEUE_CONNECTION=redis` and starting Redis:

```bash
python queues.py
```

Run the FastAPI example:

```bash
python web.py
```

Compile a project into bytecode and runtime assets:

```bash
equipment compile dist
cd dist
python main.pyc
```

## Configuration Model

Equipment loads `.env` from the project root, then reads `config/*.ini`, `config/*.yaml`, and `config/*.json`. Configuration values can use `${NAME:default}` interpolation.

Important generated settings:

| File | Purpose |
| --- | --- |
| `config/app.yaml` | Application name and environment. |
| `config/database.yaml` | SQLAlchemy connection selection and database options. |
| `config/log.yaml` | Log level, channel, handlers, and JSON formatter. |
| `config/queue.yaml` | `sync` or `redis` queue driver. |
| `config/storage.yaml` | `local` or `s3` storage driver. |
| `config/web.yaml` | FastAPI host and port. |
| `config/inspiring.json` | Example data consumed by the generated `Inspire` service. |

## Development And Maintenance

Install the repository dependencies and run tests:

```bash
python -m pip install -r requirements.txt
python -m pip install coverage runtype faker
python -m coverage run -m unittest discover -s tests
python -m coverage report
```

Build the documentation site:

```bash
cd website
pnpm install
pnpm build
```

Windows helper scripts use the `PYTHON` environment variable when set, otherwise `python`:

```bat
set PYTHON=py -3.14
test.bat
```

## Cross-Platform Notes

- Prefer `python -m ...` commands because they work consistently in virtual environments.
- On Windows, use `py -3.14` or `python` depending on how Python is installed.
- Do not rely on Unix-only commands such as `rm`, `cp`, or `sed` inside generated projects.
- Path handling in the current CLI uses `pathlib` so generated and compiled paths follow the active operating system.

## Limitations And Assumptions

- `equipment new` downloads the template from the `main` branch of the Equipment GitHub repository, so project creation needs network access.
- Redis queue processing requires a running Redis service.
- S3 storage requires compatible credentials and bucket configuration.
- MySQL and PostgreSQL require optional database driver dependencies in the generated project.
- Local validation in this repository depends on the Python interpreters installed on the machine; CI is configured for Python 3.12, 3.13, and 3.14 on Ubuntu, Windows, and macOS.

## Documentation

- Website: <https://equipment-python.vercel.app>
- LLM summary: <https://equipment-python.vercel.app/llms.txt>
- Full LLM manual: <https://equipment-python.vercel.app/llms-full.txt>

## License

This project is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).

Equipment icons created by <a href="https://www.flaticon.com/free-icons/toolbox">Freepik - Flaticon</a>.

## Author

[Roger Vilà](https://github.com/rogervila)
