# CLAUDE.md — Equipment Repository Guide

> This file gives LLM coding agents the context needed to work effectively in this repository. Read it fully before writing, editing, or reviewing code.

---

## What This Repository Is

**Equipment** is a Python project scaffolding framework published to PyPI as `equipment`.

Running `equipment new my-app` downloads the project template from GitHub and creates a ready-to-run Python application directory. The generated project includes configuration loading, dependency injection, logging, SQLAlchemy database access, queues, scheduling, local/S3 storage, unittest-based tests, and optional FastAPI serving.

- **Author**: Roger Vilà (`rogervila@me.com`)
- **License**: MIT
- **PyPI**: `pip install equipment`
- **Docs website**: <https://equipment-python.vercel.app>
- **LLM summary**: <https://equipment-python.vercel.app/llms.txt>
- **LLM full manual**: <https://equipment-python.vercel.app/llms-full.txt>
- **GitHub**: <https://github.com/rogervila/equipment>

---

## Repository Layout

```
equipment/                    ← Framework package (installable via pip)
  __init__.py                 ← Equipment container + equipment() + cli()
  __main__.py                 ← python -m equipment entry point
  Command/
    __init__.py               ← Click CLI group: "new" and "compile"
    AbstractCommand.py        ← Abstract base for CLI commands
    NewProjectCommand.py      ← "equipment new NAME" implementation
    CompileCommand.py         ← "equipment compile DIST" implementation
    _project/                 ← Temporary download cache (git-ignored)
  Database/
    SQLAlchemyFactory.py      ← SQLAlchemy engine + session + text() helper
  Log/
    AbstractLogger.py         ← Abstract logger interface
    LoggerFactory.py          ← Builds handlers from config/log.yaml
    NullLogger.py             ← Discards all log calls (use in tests)
  Queue/
    AbstractQueue.py          ← push() / push_at() interface
    QueueFactory.py           ← Selects SyncQueue or RedisQueue from config
    SyncQueue.py              ← Executes work immediately in current process
    RedisQueue.py             ← Enqueues work via RQ + Redis
  Scheduler/
    AbstractScheduler.py      ← Abstract scheduler interface
    Scheduler.py              ← schedule library loop with should_exit support
  Storage/
    AbstractStorage.py        ← path/write/read/exists/remove/move/list interface
    StorageFactory.py         ← Selects LocalStorage or S3Storage from config
    LocalStorage.py           ← Filesystem-backed storage driver
    S3Storage.py              ← boto3-backed S3-compatible storage driver

project/                      ← Generated project TEMPLATE (source of truth)
  app/
    __init__.py               ← App container: subclasses Equipment, adds services
    Inspire.py                ← Example service (random quote from config)
    Scheduler.py              ← Example Scheduler subclass with schedule jobs
  config/
    app.yaml                  ← APP_NAME, APP_ENV
    database.yaml             ← DB_CONNECTION, SQLite/MySQL/PostgreSQL settings
    inspiring.json            ← Example JSON data for Inspire service
    log.yaml                  ← LOG_CHANNEL, LOG_LEVEL, handlers, formatters
    queue.yaml                ← QUEUE_CONNECTION, Redis settings
    storage.yaml              ← FILESYSTEM_DISK, local path, S3 settings
    web.yaml                  ← WEB_HOST, PORT
  database/
    migrations/               ← Alembic migration environment + first migration
  storage/
    app/                      ← Local storage root
    logs/                     ← File log output directory
  tests/
    TestCase.py               ← Base class: app instance + Faker + testing env
    app/test_Inspire.py       ← Example test for the Inspire service
  .env.example                ← All environment variable defaults, copy to .env
  main.py                     ← Script entry point with feature usage examples
  queues.py                   ← RQ Worker entry point
  scheduler.py                ← Scheduler process entry point
  web.py                      ← FastAPI + Uvicorn entry point
  pyproject.toml              ← Generated project metadata (PROJECT_NAME placeholder)

tests/                        ← Framework test suite (run from repository root)
  test_Equipment.py           ← Equipment container and singleton provider tests
  test_ImportPerformance.py   ← Proves heavy deps are NOT imported at startup
  test_PackageMetadata.py     ← Asserts pyproject.toml classifiers and readmes
  Command/
    test_Cli.py               ← Click CLI dispatch tests
    test_NewProjectCommand.py ← Template scaffold tests (network mocked)
    test_CompileCommand.py    ← Compile output layout tests
  Database/
    test_SQLAlchemyFactory.py ← URL building and session tests
  Log/
    test_LoggerFactory.py     ← Handler creation + formatter + SQLite tests
  Queue/                      ← (empty __init__, no direct Queue unit tests yet)
  Scheduler/
    test_AbstractScheduler.py ← Abstract base raises NotImplementedError
    test_Scheduler.py         ← Scheduler loop with patched sleep/run_pending
  Storage/
    test_LocalStorage.py      ← LocalStorage filesystem operations
    test_S3Storage.py         ← S3Storage with moto mock

website/                      ← Docusaurus documentation site
  docs/
    intro.md                  ← Overview (read this first for broad context)
    getting-started/          ← Installation, structure, common workflows
    features/                 ← DI, config, database, log, queue, scheduler, storage, tests, compile
    reference/                ← CLI, environment variables, maintenance guide
    examples/                 ← FastAPI example
  docusaurus.config.js        ← Site config + docusaurus-plugin-llms root content
  package.json / package-lock.json ← npm dependencies (committed for Vercel)
  vercel.json                 ← Vercel routing + MIME type config

pyproject.toml                ← Framework package metadata (version = CURRENT_VERSION placeholder)
requirements.txt              ← Framework runtime + test dependencies
Makefile                      ← prepare / build / test targets
build.sh / build.bat          ← Local build scripts
.github/
  workflows/
    test.yml                  ← CI: 3×3 matrix (Ubuntu/Windows/macOS × 3.13/3.14/3.15)
    publish.yml               ← CD: PyPI publish on git tag push
  agents/
    equipment_developer_debugger.agent.md ← Specialist agent definition for this repo
.agents/skills/               ← Agent skill packs (git-ignored from end user projects)
.coveragerc                   ← Omits test files from coverage
.pylintrc                     ← Pylint config (many checks disabled for brevity)
.editorconfig                 ← utf-8, LF, 4-space indent, 2-space for YAML
```

---

## Architecture Deep Dive

### The Equipment Container

`equipment.Equipment` is a `dependency_injector.containers.DeclarativeContainer`. It is the composition root for both the framework and every generated project.

```python
class Equipment(DeclarativeContainer):
    config = Configuration()

    log      = ThreadSafeSingleton(LoggerFactory, config.app.name, config.base_path, config.log)
    queue    = ThreadSafeSingleton(QueueFactory, config.queue, log)
    storage  = ThreadSafeSingleton(StorageFactory, config.storage, config.base_path, log)
    database = ThreadSafeSingleton(SQLAlchemyFactory, config.database, config.base_path, log)
```

`Equipment.make(base_path)` is a `@cached({})` classmethod that:
1. Loads `.env` from `base_path` (if present) via `python-dotenv`.
2. Merges all `config/*.ini`, then `config/*.yaml`, then `config/*.json` into `config`.
3. Sets `config.base_path` to `base_path` (defaults to `os.getcwd()`).
4. Returns the configured container instance (cached per class, so a second call returns the same instance).

**Generated projects subclass Equipment:**

```python
# project/app/__init__.py
class App(Equipment):
    inspiring = Singleton(Inspire, Equipment.config.inspiring.quotes)
    scheduler = Singleton(Scheduler, Equipment.log, Equipment.queue, inspiring)

def app(base_path=None) -> App:
    return App.make(base_path)
```

This `App` class is the composition root for the application. All application services must be registered here as `ThreadSafeSingleton` providers.

### Lazy Import Pattern (Critical for Import Performance)

Heavy dependencies (`boto3`, `botocore`, `redis`, `rq`, `sqlalchemy`, `python_sqlite_log_handler`, `pythonjsonlogger`) are **NOT imported at module load time**. They are imported lazily inside `__init__` or factory methods:

```python
# Good — lazy import inside factory
class QueueFactory(AbstractQueue):
    def __init__(self, config, log):
        if config['connection'] == 'redis':
            from equipment.Queue.RedisQueue import RedisQueue  # lazy
            self.queue = RedisQueue(...)
```

`test_ImportPerformance.py` enforces this: importing `equipment` must not load any of these modules. **Do not add top-level imports of heavy optional modules.**

Similarly, `requests` (used by `NewProjectCommand` to download the template) is imported lazily inside `_download_project_template()`.

Light modules needed only on some code paths are listed in a module-level `__lazy_modules__` (PEP 810) placed before the imports. Python 3.15+ defers them until first use; 3.13/3.14 ignore the attribute and import eagerly:

| Module | `__lazy_modules__` | Needed only when |
|--------|--------------------|------------------|
| `equipment/__init__.py` | `dotenv` | `.env` exists in `base_path` |
| `equipment/Log/LoggerFactory.py` | `logging.handlers` | `daily` channel is used |
| `equipment/Command/NewProjectCommand.py` | `zipfile` | `equipment new` runs |
| `equipment/Command/CompileCommand.py` | `py_compile` | `equipment compile` runs |
| `equipment/Scheduler/Scheduler.py` | `schedule` | A `Scheduler` is instantiated |

`test_import_defers_lazy_modules` (3.15+ only) enforces this. Keep function-level imports for heavy dependencies: `__lazy_modules__` does nothing on 3.13/3.14. On 3.15, a lazy `from module import name` binding resolves at first use, so a `mock.patch` of `module.name` active at that moment is captured permanently. Do not list modules whose imported names tests patch, or modules whose import side effects must run at load time.

### Singleton Provider Lifecycle

- Providers use `ThreadSafeSingleton`. The first `.()` call creates and caches the instance.
- `hasattr(self, 'field_name')` guards prevent re-initialization on repeated calls.
- **Tests must override before first access** because singletons cache the first-created object.
- To silence logs in tests: `self.app.log.override(NullLogger())`
- To switch a driver in tests: `self.app.config.queue.connection.from_value('sync')`

### Configuration Loading Order

1. `.env` file (loaded with `python-dotenv`)
2. `config/*.ini` files
3. `config/*.yaml` files
4. `config/*.json` files
5. `config.base_path` set to the resolved base path

Config values from YAML/JSON support `${ENV_VAR:default}` interpolation. All loaded values are **strings**; cast at the call site when a library needs `int` or `bool`.

### CLI Commands

The `equipment` console script (defined in `pyproject.toml`) calls `equipment.cli()` → `equipment.Command.main`.

| Command | What It Does |
|---------|-------------|
| `equipment new NAME` | Downloads `main` branch ZIP from GitHub, extracts `project/` template, copies to `./NAME`, renames `PROJECT_NAME` in `pyproject.toml`, copies `.env.example` → `.env`. Requires network. |
| `equipment compile DIST` | Walks current directory, compiles `.py` → `.pyc` under `DIST/`, copies runtime assets (`config/`, `database/`, `storage/`, `.env`, `.env.example`, `.gitignore`, `pyproject.toml`, `README.md`, `.coveragerc`, `.editorconfig`). Excludes `tests/`, `equipment/`, `__pycache__/`, `dist/`, the output dir itself. |

### Storage Abstraction

`AbstractStorage` contract (all methods mirror each other across drivers):

| Method | Local Behavior | S3 Behavior |
|--------|---------------|-------------|
| `path(file)` | Returns absolute path under `storage/app/` | Returns S3 key (with prefix if set) |
| `write(file, data)` | Creates dirs, writes UTF-8 text | `put_object` |
| `read(file)` | Reads UTF-8 text, raises `FileNotFoundError` | `get_object`, raises `FileNotFoundError` |
| `exists(file)` | `os.path.isfile` | `head_object` |
| `remove(file)` | `os.remove` | `delete_object` |
| `move(src, dst)` | `os.rename` | copy then delete |
| `list(path)` | `os.listdir`, files only (not subdirs) | `list_objects_v2`, files only |

`write`, `remove`, `move` return `True`/`False`; exceptions are caught and logged.  
`read` and `list` raise exceptions when the target is missing.

### Queue Abstraction

| Driver | `push()` | `push_at()` |
|--------|----------|------------|
| `SyncQueue` | Calls `method(*args, **kwargs)` immediately | Ignores date, calls immediately |
| `RedisQueue` | `rq.Queue.enqueue(f=method, ...)` | `rq.Queue.enqueue_at(datetime=date, f=method, ...)` |

Both return `True`/`False`. Exceptions are caught, logged, and result in `False`.

**Critical rule for Redis queues**: callable must be a module-level importable function. No lambdas, nested functions, closures, or container providers as job payloads.

### Logging Subsystem

`LoggerFactory` builds Python standard library loggers from `config/log.yaml`:

| Channel | Handler Class |
|---------|--------------|
| `single` | `FileHandler` |
| `daily` | `TimedRotatingFileHandler` |
| `console` | `StreamHandler` |
| `sqlite` | `SQLiteLogHandler` (from `python_sqlite_log_handler`) |
| `null` / `None` | `NullHandler` |
| `stack` | Multiple handlers combined |

JSON formatting uses `pythonjsonlogger.JsonFormatter`. All methods set `stacklevel=2` so log records show the caller's file and line, not the `LoggerFactory` wrapper.

### Scheduler

`equipment.Scheduler.Scheduler` wraps the `schedule` library:
- Creates a `schedule.Scheduler()` instance as `self.schedule`.
- Loop: `run_pending()` → `sleep(1)` → check `should_exit`.
- Stops on `KeyboardInterrupt` or when `should_exit = True`.

Generated project `app/Scheduler.py` subclasses it, registers jobs, then calls `super().run()`.

### Database

`SQLAlchemyFactory` builds URLs and creates `engine` + `session_maker`:

| Driver | URL format |
|--------|-----------|
| `sqlite` | `sqlite:///BASE_PATH/path/to/file` or `sqlite://` for `:memory:` |
| `mysql` | `mysql+mysqlconnector://user:pass@host:port/db?charset=utf8mb4` |
| `postgresql` | `postgresql+psycopg2://user:pass@host:port/db` |

MySQL and PostgreSQL drivers are **optional** and must be installed separately. Tests skip with `self.skipTest(...)` when the driver is unavailable.

---

## Development Environment

### Python Support

- **Supported**: Python 3.13, 3.14, 3.15 (`requires-python = ">=3.13"`)
- **Platforms**: Ubuntu, Windows, macOS
- CI tests the full 3×3 matrix on every push

### Install For Development

```bash
python -m pip install -r requirements.txt
python -m pip install coverage runtype faker
```

### Run Framework Tests

```bash
# From repository root
python -m coverage run -m unittest discover -s tests
python -m coverage report
```

Run against a specific Python version:

```bash
python3.15 -m coverage run -m unittest discover -s tests
python3.14 -m coverage run -m unittest discover -s tests
python3.13 -m coverage run -m unittest discover -s tests
```

### Run Generated Project Tests

```bash
# From repository root — validates the template works end-to-end
cd project
python -m pip install .
python -m coverage run -m unittest
cp .env.example .env
python -m equipment compile dist
cd dist
python main.pyc
```

### Build The Website

```bash
cd website
npm ci
npm run build
```

The Docusaurus build generates `website/build/llms.txt` and `website/build/llms-full.txt` via `docusaurus-plugin-llms`. Do **not** hand-edit files under `website/build/`.

### Local Package Build

```bash
# Linux/macOS
bash build.sh

# Windows
build.bat
```

Both scripts temporarily set `version = 9.9.9` in `pyproject.toml`, build, install locally, then restore the placeholder.

---

## Key Conventions and Constraints

### Non-negotiable Rules

1. **Test runner is `unittest`, not pytest.** Never suggest pytest; CI runs `python -m unittest discover`.
2. **`requirements.txt` is both runtime and dev deps.** Do not add packages without explicit request.
3. **Lazy imports for heavy optional dependencies.** `boto3`, `redis`, `rq`, `sqlalchemy`, `pythonjsonlogger`, `python_sqlite_log_handler`, and `requests` must not be imported at module load time.
4. **Preserve all three Python versions.** Do not use syntax or features that break 3.13, 3.14, or 3.15.
5. **Cross-platform paths.** Use `pathlib.Path` or `os.path`. No hardcoded `/` or `\\` in Python logic.
6. **Do not edit `website/build/`.** Generated output; rebuild with `npm run build`.
7. **Do not mock network in NewProjectCommand unit tests with live calls.** Mock `_download_project_template` using `unittest.mock.patch`.
8. **`project/equipment/` is git-ignored and generated by `make prepare`.** Do not edit it directly; it is a copy of `equipment/`.
9. **Do not mix dependency upgrades with other changes.** Run the full suite before and after any dependency bump.
10. **Singleton services must not store per-request mutable state.** Safe to reuse between calls.

### Code Style

- **Indent**: 4 spaces for Python, 2 spaces for YAML.
- **Line endings**: LF (enforced by `.editorconfig`).
- **Encoding**: UTF-8 everywhere; always specify `encoding='utf-8'` in `open()`.
- **Abstract classes**: inherit `abc.ABC`, raise `NotImplementedError` directly (not `@abstractmethod`).
- **Type hints**: used in method signatures; `TYPE_CHECKING` guards avoid circular imports for type-only imports.
- **Pylint**: disabled rules include `broad-except`, `import-outside-toplevel`, `invalid-name`, `line-too-long`. See `.pylintrc`.

### Factory Pattern

All subsystems (Log, Queue, Storage, Database) use a factory class that:
- Accepts `config: dict` plus other dependencies.
- Guards initialization with `if not hasattr(self, 'field_name'):` to support singleton reuse.
- Delegates to concrete implementations (e.g., `SyncQueue`, `RedisQueue`).
- The factory itself implements the same interface as the concrete class (`LoggerFactory` is also an `AbstractLogger`).

### Testing Patterns

- **Framework tests** live in `tests/`, use bare `unittest.TestCase`, and set up their own config dicts.
- **Generated project tests** live in `project/tests/`, extend `project/tests/TestCase.py` which creates a real `App` container.
- **S3 tests**: use `moto.mock_aws()` context manager. Never make real S3 calls in unit tests.
- **File handler tests**: close handlers before `tearDown` deletes temp directories (required on Windows).
- **Scheduler tests**: patch `schedule.Scheduler.run_pending` and `time.sleep`, or set `scheduler.should_exit = True` to avoid sleeping.
- **CLI tests**: use `click.testing.CliRunner`; mock `NewProjectCommand`/`CompileCommand` for dispatch tests.
- **Template tests**: build a real in-memory ZIP from the `project/` directory and mock `_download_project_template` to return it.
- **`runtype.isa()`** is used in some tests for duck-type isinstance checks.
- **`faker.Faker()`** is used for test data (exposed as `self.fake` in generated `TestCase`).

### Windows-specific Concerns

- Windows cannot `os.rmdir`/`shutil.rmtree` the current working directory.
- Tests that call `os.chdir()` must call `os.chdir(previous_cwd)` **before** `rmtree`. Use `addCleanup` with LIFO order in mind.
- Open file handles block cleanup. Close log handlers explicitly in `tearDown`.
- Use `python -m pip install` rather than `pip install` for reliability in virtual environments.

---

## Configuration Reference

All environment variables with their defaults:

| Variable | Default | Config File |
|----------|---------|-------------|
| `APP_NAME` | `Equipment` | `config/app.yaml` |
| `APP_ENV` | `local` | `config/app.yaml` |
| `LOG_LEVEL` | `debug` | `config/log.yaml` |
| `LOG_CHANNEL` | `stack` | `config/log.yaml` |
| `DB_CONNECTION` | `sqlite` | `config/database.yaml` |
| `DB_HOST` | `127.0.0.1` | `config/database.yaml` |
| `DB_PORT` | `3306` / `5432` | `config/database.yaml` |
| `DB_DATABASE` | connection-specific | `config/database.yaml` |
| `DB_USERNAME` | connection-specific | `config/database.yaml` |
| `DB_PASSWORD` | connection-specific | `config/database.yaml` |
| `DB_CHARSET` | `utf8mb4` | `config/database.yaml` |
| `QUEUE_CONNECTION` | `sync` | `config/queue.yaml` |
| `REDIS_HOST` | `127.0.0.1` | `config/queue.yaml` |
| `REDIS_PORT` | `6379` | `config/queue.yaml` |
| `REDIS_DB` | `0` | `config/queue.yaml` |
| `REDIS_USERNAME` | `null` | `config/queue.yaml` |
| `REDIS_PASSWORD` | `null` | `config/queue.yaml` |
| `FILESYSTEM_DISK` | `local` | `config/storage.yaml` |
| `S3_ENDPOINT` | (none) | `config/storage.yaml` |
| `S3_BUCKET` | (none) | `config/storage.yaml` |
| `S3_ACCESS_KEY` | (none) | `config/storage.yaml` |
| `S3_SECRET_KEY` | (none) | `config/storage.yaml` |
| `S3_REGION` | `auto` | `config/storage.yaml` |
| `S3_PREFIX` | `null` | `config/storage.yaml` |
| `WEB_HOST` | `0.0.0.0` | `config/web.yaml` |
| `PORT` | `8000` | `config/web.yaml` |

---

## CI/CD Pipeline

### test.yml (runs on every push)

Matrix: `{ubuntu-latest, windows-latest, macos-latest}` × `{3.13, 3.14, 3.15}`

Steps:
1. Install `requirements.txt` dependencies.
2. Install `coverage runtype faker`.
3. Run `python -m coverage run -m unittest discover -s tests`.
4. (Ubuntu only) Build the package as 9.9.9, install it, then run the full generated project workflow: install, test, compile, run compiled main.

### publish.yml (runs on tag push)

1. Replaces `CURRENT_VERSION` placeholder in `pyproject.toml` with the git tag version.
2. Also patches `project/pyproject.toml` to uncomment the equipment dependency line.
3. Builds with `python -m build`.
4. Uploads to PyPI via `twine` using `PYPI_TOKEN` secret.

---

## Package Build Details

`pyproject.toml` uses `version = "CURRENT_VERSION"` as a placeholder. The CI pipeline and local build scripts use `sed` (Linux/macOS) or PowerShell string replacement (Windows) to substitute the real version before building.

`[tool.setuptools.dynamic]` reads dependencies from `requirements.txt` at build time.

`[tool.setuptools.packages.find]` includes only `equipment*` packages from the repository root.

All non-Python files needed at runtime (`.yaml`, `.json`, `.md`, `.gitignore`, `.example`, `.toml`, etc.) are declared in `[tool.setuptools.package-data]`.

---

## Website and LLM Documentation

The Docusaurus site under `website/` is deployed to Vercel.

- `website/package-lock.json` **must be committed** for deterministic Vercel builds.
- `website/vercel.json` configures routing for `.md` file paths and MIME types.
- `docusaurus-plugin-llms` generates `build/llms.txt` and `build/llms-full.txt` from `website/docs/`.
- The root LLM content is defined inside `website/docusaurus.config.js`.
- To update LLM-facing content, edit `website/docs/*.md` source files and rebuild. Never hand-edit `website/build/`.

---

## Dependency Highlights

| Dependency | Version | Role |
|-----------|---------|------|
| `dependency-injector` | `>=4.49.1,<5` | Container, `DeclarativeContainer`, `ThreadSafeSingleton`, `Configuration` |
| `click` | `>=8.4.2,<9` | CLI framework |
| `python-dotenv` | `>=1.2.2,<2` | `.env` file loading |
| `PyYAML` | `>=6.0.3,<7` | YAML config loading |
| `cachetools` | `>=7.1.4,<8` | `@cached({})` on `Equipment.make()` |
| `parent-import` | `==0.0.1` | Utility (imported in package) |
| `sqlalchemy` | `>=2.0.51,<3` | Database engine, sessions, text() |
| `boto3` + stubs | `>=1.43.37,<2` | S3 storage driver |
| `moto[s3]` | `>=5.2.2,<6` | S3 mock for tests |
| `redis` | `>=8.0.1,<9` | Redis connection for queue |
| `rq` | `>=2.10.0,<3` | Redis Queue (worker framework) |
| `schedule` | `>=1.2.2,<2` | Scheduler loop |
| `requests` | `>=2.34.2,<3` | Template download in `equipment new` |
| `python-json-logger` | `>=4.1.0,<5` | JSON log formatter |
| `python_sqlite_log_handler` | `>=1.1.0,<2` | SQLite log handler |

Dev-only (install separately, not in `requirements.txt`):

| Package | Purpose |
|---------|---------|
| `coverage` | Test coverage |
| `runtype` | `isa()` duck-type assertions |
| `faker` | Test data generation |

---

## Common Mistakes to Avoid

1. **Saying Equipment uses pytest.** It uses `unittest`. The command is `python -m unittest discover -s tests`.
2. **Editing `project/equipment/`** — it is a git-ignored copy generated by `make prepare`. Edit `equipment/` instead.
3. **Top-level imports of `boto3`, `redis`, `sqlalchemy`, etc.** — these must be lazy. A test enforces this.
4. **Passing lambdas to Redis queues.** RQ cannot serialize them. Use module-level functions.
5. **Storing per-request data on singleton services.** Singletons are shared across calls.
6. **Deleting temp directories before `os.chdir()` back.** Windows blocks this.
7. **Not closing file handlers before `tearDown` deletes temp files.** Windows blocks open handles.
8. **Making live GitHub/S3/Redis calls in unit tests.** Mock all of them.
9. **Forgetting to update `project/pyproject.toml` classifiers** when adding a Python version. Both `pyproject.toml` files must stay in sync.
10. **Hand-editing `website/build/`.** Content is generated; changes are lost on next build.
11. **Using `sed` or UNIX-only shell commands in generated project code or docs.** Must work on Windows.
12. **Mixing dependency upgrades with other work.** Keep them in dedicated commits.
13. **Interpreting `equipment compile` as dependency bundling.** It only compiles `.py` → `.pyc` and copies assets; dependencies must be installed separately at the target.
14. **Using `run_pending()` in scheduler tests without patching sleep.** Tests that sleep are fragile; patch `time.sleep` and `schedule.Scheduler.run_pending`.

---

## Task Playbooks

### Fix a Test Failure

1. Identify the exact failing test, OS, and Python version from the CI log.
2. Read the test file and the source it covers.
3. Reproduce with: `python -m coverage run -m unittest tests.path.to.module`.
4. Make the smallest change that fixes the root cause.
5. Re-run the failing test, then the full suite.
6. If the failure is Windows-specific, look for `os.chdir`, open file handles, or path separator assumptions.

### Change a Framework Service (Log/Queue/Storage/Database/Scheduler)

1. Edit the implementation under `equipment/<Service>/`.
2. Update or add tests under `tests/<Service>/`.
3. If the config shape changes, update `project/config/<service>.yaml` and relevant docs.
4. Run: `python -m coverage run -m unittest discover -s tests`.
5. If the generated project is affected: `cd project && python -m pip install . && python -m coverage run -m unittest`.

### Add or Modify a CLI Command

Relevant files:
- `equipment/Command/__init__.py` (Click registration)
- `equipment/Command/NewProjectCommand.py` or `CompileCommand.py`
- `tests/Command/test_Cli.py`, `test_NewProjectCommand.py`, `test_CompileCommand.py`
- `website/docs/reference/cli.md`

Validation:
```bash
python -m coverage run -m unittest tests.Command.test_Cli tests.Command.test_NewProjectCommand tests.Command.test_CompileCommand
```

### Change the Generated Project Template

Relevant files:
- All files under `project/`
- `tests/Command/test_NewProjectCommand.py` (scaffold tests)
- `tests/test_PackageMetadata.py` (metadata sync)
- `website/docs/` (any docs describing structure, workflows, or config)

After changes:
1. Run `python -m coverage run -m unittest discover -s tests`.
2. Run the generated project validation workflow from `project/`.
3. Update docs if file names, config keys, entry points, or workflows changed.

### Change Configuration Behavior

- Keep `.env` loading before config file loading.
- Keep `config.base_path` set after all other config.
- Environment values are always strings; cast at use sites.
- Keep `.env.example` in sync with documented variables.
- Update `website/docs/features/config.md` and `website/docs/reference/environment-variables.md`.

### Update the Website or LLM Docs

1. Edit `.md` files under `website/docs/`.
2. To change root LLM content, edit `website/docusaurus.config.js`.
3. Rebuild: `cd website && npm ci && npm run build`.
4. Verify: `test -f website/build/llms.txt && test -f website/build/llms-full.txt`.
5. Commit source changes only; `website/build/` is regenerated by Vercel.

### Upgrade a Dependency

1. Run `python -m coverage run -m unittest discover -s tests` on the current code (baseline).
2. Bump the version range in `requirements.txt`.
3. Run `python -m pip install -r requirements.txt` to install the new version.
4. Run the full test suite again.
5. Run the generated project validation.
6. High-risk dependencies: `dependency-injector`, `SQLAlchemy`, `boto3`/`botocore`/`moto`, `redis`/`rq`, `python-json-logger`, `python_sqlite_log_handler`, `click`, `schedule`.

---

## Validation Command Reference

```bash
# Framework tests (run from repository root)
python -m pip install -r requirements.txt
python -m pip install coverage runtype faker
python -m coverage run -m unittest discover -s tests
python -m coverage report

# Single test module
python -m coverage run -m unittest tests.Log.test_LoggerFactory

# Generated project end-to-end
cd project
python -m pip install .
python -m coverage run -m unittest
cp .env.example .env
python -m equipment compile dist
cd dist && python main.pyc

# Website
cd website
npm ci
npm run build
test -f build/llms.txt
test -f build/llms-full.txt

# Python 3.15 specifically
python3.15 -m coverage run -m unittest discover -s tests

# Python 3.14 specifically
python3.14 -m coverage run -m unittest discover -s tests

# Python 3.13 specifically
python3.13 -m coverage run -m unittest discover -s tests
```

---

## Documentation Map

| Topic | Source File |
|-------|-------------|
| Project overview | `website/docs/intro.md` |
| Installation | `website/docs/getting-started/installation.md` |
| Generated directory structure | `website/docs/getting-started/directory-structure.md` |
| Common workflows | `website/docs/getting-started/common-workflows.md` |
| Dependency injection | `website/docs/features/dependency-injection.md` |
| Configuration | `website/docs/features/config.md` |
| Database | `website/docs/features/database.md` |
| Logging | `website/docs/features/log.md` |
| Queue | `website/docs/features/queue.md` |
| Scheduler | `website/docs/features/scheduler.md` |
| Storage | `website/docs/features/storage.md` |
| Testing | `website/docs/features/tests.md` |
| Compilation | `website/docs/features/compilation.md` |
| FastAPI example | `website/docs/examples/fastapi.md` |
| CLI reference | `website/docs/reference/cli.md` |
| Environment variables | `website/docs/reference/environment-variables.md` |
| Maintenance guide | `website/docs/reference/maintenance.md` |

---

## Known Gaps and External Service Constraints

- **Redis** integration requires a running Redis service. Unit tests use `sync` driver; Redis integration requires Redis available in CI or locally.
- **S3** tests use `moto` mock. Real S3-compatible bucket tests must be done separately.
- **MySQL** and **PostgreSQL** require optional drivers (`mysql-connector-python` or `psycopg2-binary`) and running database services.
- **Native Windows** validation should be run when changing path handling, file cleanup, batch scripts, or shell commands.
- **Vercel** deployment behavior for routing and MIME types may differ from local dev servers; validate `vercel.json` routing separately.
- **Bytecode compatibility**: `.pyc` files built on one Python version or OS may not run on another. Build with the target interpreter when possible.
