---
sidebar_position: 3
---

# Maintenance Guide

This page describes how to keep Equipment and generated projects healthy over time.

## Supported Runtime Contract

Equipment currently supports:

- Python 3.12
- Python 3.13
- Python 3.14
- Windows
- macOS
- Linux

When changing code, config, templates, or docs, preserve all supported Python versions unless there is a deliberate compatibility decision documented in the change.

## Repository Validation

From the repository root:

```bash
python -m pip install -r requirements.txt
python -m pip install coverage runtype faker
python -m coverage run -m unittest discover -s tests
```

For Python 3.14 specifically:

```bash
python3.14 -m coverage run -m unittest discover -s tests
```

For Python 3.13 specifically:

```bash
python3.13 -m coverage run -m unittest discover -s tests
```

## Generated Project Validation

After changing the template under `project/`, validate that the generated project still installs, tests, compiles, and runs:

```bash
cd project
python -m pip install .
python -m coverage run -m unittest
cp .env.example .env
python -m equipment compile dist
cd dist
python main.pyc
```

On Windows, use the Python launcher if needed:

```powershell
py -3.14 -m pip install .
py -3.14 -m coverage run -m unittest
copy .env.example .env
py -3.14 -m equipment compile dist
cd dist
py -3.14 main.pyc
```

## Website Validation

The website is deployed on Vercel and uses npm:

```bash
cd website
npm ci
npm run build
```

Keep `website/package-lock.json` committed when website dependencies change. Vercel uses the lockfile for deterministic installs.

The hosted LLM files are generated during the Docusaurus build by `docusaurus-plugin-llms`:

- `https://equipment-python.vercel.app/llms.txt`
- `https://equipment-python.vercel.app/llms-full.txt`

Do not hand-edit generated files in `website/build/`. Update `website/docs/` content and the plugin root content in `website/docusaurus.config.js` instead.

## Dependency Upgrade Policy

Do not mix dependency upgrades with unrelated compatibility, docs, or test changes. Upgrade dependencies in a dedicated change so failures are easy to diagnose.

Before upgrading:

1. Run the current test suite.
2. Note skipped tests and warnings.
3. Upgrade one dependency group at a time.
4. Run repository tests.
5. Run generated project validation.
6. Run website validation if website dependencies changed.
7. Update docs only when behavior, commands, or constraints changed.

High-risk dependencies:

- `dependency-injector`: affects container configuration and singleton providers.
- `SQLAlchemy`: affects database URLs, engines, sessions, and ORM examples.
- `boto3`, `botocore`, `moto`: affect S3 storage tests and behavior.
- `redis`, `rq`: affect queue and worker behavior.
- `python-json-logger`, `python_sqlite_log_handler`: affect logging handlers.
- `click`: affects CLI behavior.
- `schedule`: affects scheduler behavior.
- Docusaurus packages: affect website builds and Vercel deployment.

## Template Change Checklist

When editing `project/`:

- Update generated tests if behavior changes.
- Update website docs if commands, files, or config change.
- Update website docs and the `docusaurus-plugin-llms` root content in `website/docusaurus.config.js` if architecture or constraints change.
- Validate generated project install and tests.
- Validate compile output if entry points or runtime assets change.
- Keep Unix and Windows behavior in mind.

## Python Version Change Checklist

When adding or removing Python support:

- Update root `pyproject.toml` classifiers.
- Update generated `project/pyproject.toml` classifiers and `requires-python` if needed.
- Update GitHub Actions matrix.
- Run tests on each supported interpreter available locally.
- Update README, website docs, and the `docusaurus-plugin-llms` root content in `website/docusaurus.config.js`.
- Document any dependency blocker instead of silently upgrading requirements.

## Cross-platform Checklist

- Use `pathlib` or `os.path` for paths.
- Avoid hardcoded `/` and `\\` in Python logic.
- Avoid shell-specific generated project commands unless alternatives are documented.
- Remember Windows cannot delete the current working directory.
- Close files, log handlers, and database connections before cleanup.
- Prefer `python -m ...` commands in docs.
- Do not assume executable bits behave the same on Windows and Unix.

## Documentation Checklist

When docs change:

- Keep README, website docs, [llms.txt](https://equipment-python.vercel.app/llms.txt), and [llms-full.txt](https://equipment-python.vercel.app/llms-full.txt) consistent. The LLM files are generated from docs during `npm run build`.
- Prefer copyable commands.
- Include Windows notes when commands differ.
- Mention required external services such as Redis, S3, MySQL, or PostgreSQL.
- Avoid claiming pytest is the default; Equipment uses `unittest`.
- Keep examples aligned with actual generated files.
- Run `cd website && npm ci && npm run build`.

## Release Notes To Watch

When preparing releases, watch for:

- setuptools warnings about project metadata;
- Python deprecations that become removals;
- Docusaurus and Webpack compatibility changes;
- dependency security advisories;
- GitHub Actions image changes;
- Vercel Node/npm changes;
- Windows path and cleanup behavior.

## Known Practical Gaps

- Redis integration requires a real Redis service for full validation.
- S3 tests use moto; real S3-compatible services should be validated separately.
- MySQL and PostgreSQL examples need optional drivers and database services.
- Native Windows validation should be run for path, cleanup, shell, and batch changes.
- Bytecode compile validation does not replace packaging or deployment tests.
