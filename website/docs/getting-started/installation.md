---
sidebar_position: 1
---

# Installation

## Requirements

- Python 3.12, 3.13, or 3.14.
- Windows, macOS, or Linux.
- `pip` installed for the selected Python interpreter.
- Network access when running `equipment new`, because the command downloads the current project template from GitHub.

Check your interpreter:

```bash
python --version
```

On Windows, the Python launcher can select a version explicitly:

```bat
py -3.14 --version
```

## Install Equipment

Install the CLI into your active Python environment:

```bash
python -m pip install equipment
```

If you use `pipx` for command-line tools:

```bash
pipx install equipment
```

## Create A Virtual Environment

Unix shells:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install equipment
```

Windows PowerShell or Command Prompt:

```bat
py -3.14 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install equipment
```

## Create A Project

```bash
equipment new my-app
cd my-app
python -m pip install .
python main.py
```

The generated project has its own `pyproject.toml`. Install it from inside the generated directory so imports such as `from app import app` resolve correctly.

## What `equipment new` Does

The `new` command creates a project from the maintained template in this repository. At a high level it:

1. downloads the Equipment repository archive from GitHub;
2. extracts the `project/` template from that archive;
3. copies the template into the target directory;
4. creates `.env` from `.env.example`;
5. replaces `PROJECT_NAME` in the generated `pyproject.toml` with your project name;
6. prompts before overwriting an existing directory.

The command is intentionally simple: it does not ask a long list of questions or generate different project flavors. Start with the full template, then remove optional pieces you do not need.

## Project Names

Use project names that are valid package names after normalization. Short lowercase names with hyphens or underscores are easiest to work with:

```bash
equipment new billing-api
equipment new data_worker
```

Avoid names with spaces, shell metacharacters, or path separators. The command creates a directory with the name you pass and writes that name into generated metadata.

## Recommended Local Setup

For an application project, install Equipment globally with `pipx` or in a tooling environment, then create a separate virtual environment inside the generated project:

```bash
python -m pip install --user pipx
pipx install equipment
equipment new my-app
cd my-app
python -m venv .venv
source .venv/bin/activate
python -m pip install .[dev]
python -m unittest discover -s tests
```

On Windows PowerShell:

```powershell
py -3.14 -m pip install --user pipx
py -3.14 -m pipx ensurepath
pipx install equipment
equipment new my-app
cd my-app
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install .[dev]
python -m unittest discover -s tests
```

Using `python -m ...` commands helps ensure that packages install into the same interpreter that runs the application.

## Verify The Generated Project

Run the generated tests:

```bash
python -m unittest discover -s tests
```

Run optional entry points only when their dependencies are configured:

```bash
python scheduler.py
python queues.py
python web.py
```

`queues.py` expects Redis. `web.py` expects the FastAPI and Uvicorn dependencies from the generated `pyproject.toml`.

## Post-install Checklist

After the first successful run, check these files:

- `.env`: local environment values; do not commit secrets from this file.
- `config/app.yaml`: application name and environment defaults.
- `config/database.yaml`: default database connection and local SQLite path.
- `config/log.yaml`: log destination and format.
- `config/queue.yaml`: sync or Redis queue selection.
- `config/storage.yaml`: local or S3 storage selection.
- `pyproject.toml`: optional dependencies you may remove or uncomment.
- `tests/TestCase.py`: shared test setup for your app.

Then make one small application change and add a test for it. This verifies that the generated project is correctly installed and that imports resolve in your local environment.

## Offline And Restricted Networks

`equipment new` needs access to GitHub because it downloads the current template archive. In restricted environments, create the project on a machine with network access and copy the generated project into the restricted environment, or vendor the generated project template internally.

After a project exists, normal development does not require the `new` command. Your generated project can be installed from its own `pyproject.toml` like any other Python project.

## Dependency Managers

Equipment does not require a specific dependency manager. These are equivalent ways to use it:

```bash
python -m pip install equipment
```

```bash
pipenv --python 3.14
pipenv install equipment
pipenv run equipment new my-app
```

```bash
poetry add equipment
poetry run equipment new my-app
```

## Troubleshooting

Python version error:

Equipment requires Python 3.12 or newer and is tested on Python 3.12, 3.13, and 3.14. Check `python --version` or `py -0p` on Windows.

`equipment` command not found:

Use `python -m pip show equipment` to confirm where it is installed. If the scripts directory is not on `PATH`, use a virtual environment or `pipx`.

Project creation fails before files are copied:

Check network access to GitHub. The `new` command downloads `https://github.com/rogervila/equipment/archive/refs/heads/main.zip`.

Generated project install fails:

Run `python -m pip install .` from inside the generated project directory and confirm that `README.md` and `pyproject.toml` are present.

Imports fail with `ModuleNotFoundError: app`:

Run commands from the generated project root, or install the generated project into the active environment with `python -m pip install .`. The generated code expects the project root to be importable.

Redis worker fails to connect:

Keep `QUEUE_CONNECTION=sync` until Redis is installed and reachable. Then set `QUEUE_CONNECTION=redis`, configure `REDIS_HOST`, `REDIS_PORT`, and `REDIS_DB`, and run `python queues.py` in a separate process.

S3 storage fails:

Confirm `FILESYSTEM_DISK=s3` and all `S3_*` variables are present. For local development, prefer `FILESYSTEM_DISK=local` until the bucket and credentials are available.
