---
sidebar_position: 1
---

# CLI Reference

Equipment exposes a command-line interface through the `equipment` console script.

```bash
equipment --help
```

The current CLI has two commands:

- `equipment new NAME`
- `equipment compile DIST`

## `equipment new NAME`

Create a new project from the maintained Equipment template.

```bash
equipment new my-app
```

What it does:

1. Uses the current working directory as the parent path.
2. Downloads the Equipment GitHub archive from `https://github.com/rogervila/equipment/archive/refs/heads/main.zip`.
3. Extracts the `equipment-main/project` template.
4. Copies the template to `./NAME`.
5. Copies `.env.example` to `.env`.
6. Replaces `PROJECT_NAME` in the generated `pyproject.toml` with `NAME`.
7. Prompts before overwriting an existing directory.

Example:

```bash
equipment new billing-api
cd billing-api
python -m pip install .
python main.py
```

Windows example:

```powershell
equipment new billing-api
cd billing-api
py -3.14 -m pip install .
py -3.14 main.py
```

## `new` Command Constraints

- Network access to GitHub is required.
- The generated directory name is the name passed to the command.
- Existing directories are not overwritten without confirmation.
- The command creates a local `.env` file from `.env.example`.
- The command does not ask which features to include. Remove unused generated files after creation.

## `new` Command Testing Guidance

Tests should mock the GitHub download. Do not make unit tests depend on live network access.

Important behavior to test:

- project directory creation;
- `.env` creation from `.env.example`;
- `PROJECT_NAME` replacement in `pyproject.toml`;
- skip behavior when overwrite is declined;
- download failure behavior;
- ignored files such as logs, SQLite files, bytecode, caches, and virtual environments.

## `equipment compile DIST`

Compile a generated project into bytecode and runtime assets.

```bash
equipment compile dist
```

What it does:

1. Walks the current directory.
2. Ignores `__pycache__`, `dist`, `tests`, `equipment`, and the selected output directory.
3. Compiles `.py` files to `.pyc` files under `DIST`.
4. Copies runtime assets into `DIST`.

Runtime assets copied by default:

- `config/`
- `database/`
- `storage/`
- `.coveragerc`
- `.editorconfig`
- `.env`
- `.env.example`
- `.gitignore`
- `pyproject.toml`
- `README.md`

Example:

```bash
equipment compile dist
cd dist
python main.pyc
```

Windows example:

```powershell
equipment compile dist
cd dist
py -3.14 main.pyc
```

## `compile` Command Constraints

- Run from the generated project root.
- Compile into a clean output directory.
- Do not compile into the source root.
- The command does not bundle third-party dependencies.
- Bytecode is not a security boundary.
- Bytecode should be built with a compatible Python version for the target runtime.

## Exit And Error Behavior

The CLI prints human-readable status messages. Command implementations catch broad exceptions, print a red error message, and return. Tests should verify observable results rather than relying only on printed output.

## Cross-platform Notes

- Paths should be handled with `pathlib` or platform-safe APIs.
- Tests should avoid assuming `/` path separators.
- Windows cannot delete the current working directory, so tests that `chdir` into a temporary directory must change back before cleanup.
- Do not assume executable permissions behave the same on Unix and Windows.
