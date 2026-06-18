---
sidebar_position: 9
---

# Compilation

The `equipment compile` command prepares a generated project for bytecode-based distribution. It compiles Python files to `.pyc` and copies runtime assets into an output directory.

Compilation is optional. Use it when you want a deployment directory that contains Python bytecode and runtime assets but excludes tests and source `.py` files.

## Command

```bash
equipment compile dist
```

Run it from the generated project root.

## What It Does

- Walks the current directory.
- Ignores `__pycache__`, `dist`, `tests`, `equipment`, and the selected output directory.
- Compiles `.py` files into `.pyc` files under the output directory.
- Copies runtime assets: `config`, `database`, `storage`, `.coveragerc`, `.editorconfig`, `.env`, `.env.example`, `.gitignore`, `pyproject.toml`, and `README.md`.

The command is designed for generated projects. Run it from the generated project root, not from inside the `equipment` package repository unless you are intentionally testing the command.

## Example

```bash
equipment compile dist
cd dist
python main.pyc
```

On Windows:

```bat
equipment compile dist
cd dist
py -3.14 main.pyc
```

## Output Shape

```text
dist/
├── app/
│   └── ... .pyc files
├── config/
├── database/
├── storage/
├── main.pyc
├── queues.pyc
├── scheduler.pyc
├── web.pyc
├── README.md
└── pyproject.toml
```

Tests and the vendored `equipment` package directory are intentionally excluded.

## Included And Excluded Content

Included by default:

- compiled `.pyc` files for application Python files;
- `config/`;
- `database/`;
- `storage/`;
- `.coveragerc`;
- `.editorconfig`;
- `.env`;
- `.env.example`;
- `.gitignore`;
- `pyproject.toml`;
- `README.md`.

Excluded by default:

- `tests/`;
- `equipment/` when present inside the generated project;
- `__pycache__/`;
- `dist/`;
- the selected output directory;
- source `.py` files.

## Deployment Checklist

After compiling:

1. `cd` into the output directory.
2. Run `python main.pyc`.
3. Run any deployment smoke script you maintain.
4. Confirm config files and `.env` values are appropriate for the target environment.
5. Confirm optional services such as Redis, database, and S3 are reachable.

If the target environment differs from your build environment, build with the Python version and operating system you intend to run where possible.

## Cross-platform Notes

- Use `python main.pyc` on Unix and Windows when `python` is on PATH.
- Use `py -3.14 main.pyc` on Windows when selecting a specific interpreter.
- Do not rely on executable file permissions in compiled output.
- Keep paths inside application code platform-safe with `pathlib` or `os.path`.

## Limitations

- Bytecode is not a security boundary. Treat `.pyc` files as packaging convenience, not source protection.
- Compiled output should be tested before deployment.
- Platform-specific bytecode should be built with the Python version and operating system you plan to run.
- The command does not bundle third-party dependencies into the output directory.
- The command does not replace proper packaging, containerization, or deployment automation.

## Troubleshooting

`ModuleNotFoundError` in compiled output:

Install project dependencies in the runtime environment. The compile command copies your project runtime assets, not every dependency from the environment.

Config file missing:

Confirm the file is in one of the included runtime asset paths or copy it as part of your deployment process.

Compiled output includes stale files:

Delete the output directory before compiling again.

Compiled output runs locally but not on another machine:

Check Python version, operating system, architecture, installed dependencies, and environment variables.

## Guidance

- Compile into a clean output directory such as `dist` or `build/output`.
- Do not compile into the source root.
- Run `python main.pyc` from inside the output directory to verify imports and runtime assets.
- Use `pathlib` in project code so compiled projects behave consistently on Windows and Unix.
- Keep compile validation in CI if bytecode deployment is part of your release process.
