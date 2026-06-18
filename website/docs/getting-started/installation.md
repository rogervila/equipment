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
