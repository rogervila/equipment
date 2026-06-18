---
sidebar_position: 9
---

# Compilation

The `equipment compile` command prepares a generated project for bytecode-based distribution. It compiles Python files to `.pyc` and copies runtime assets into an output directory.

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

## Limitations

- Bytecode is not a security boundary. Treat `.pyc` files as packaging convenience, not source protection.
- Compiled output should be tested before deployment.
- Platform-specific bytecode should be built with the Python version and operating system you plan to run.

## Guidance

- Compile into a clean output directory such as `dist` or `build/output`.
- Do not compile into the source root.
- Run `python main.pyc` from inside the output directory to verify imports and runtime assets.
- Use `pathlib` in project code so compiled projects behave consistently on Windows and Unix.
