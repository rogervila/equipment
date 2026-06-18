---
sidebar_position: 6
---

# Storage

Equipment provides a storage abstraction with local filesystem and S3-compatible drivers. Application code can call the same methods regardless of the configured disk.

## Configuration

```yaml
storage:
  disk: ${FILESYSTEM_DISK:local}

  disks:
    local:
      path: storage/app

    s3:
      endpoint: ${S3_ENDPOINT}
      bucket: ${S3_BUCKET}
      access_key: ${S3_ACCESS_KEY}
      secret_key: ${S3_SECRET_KEY}
      region: ${S3_REGION:auto}
      prefix: ${S3_PREFIX:null}
```

The local driver uses `path`, for example `storage/app`.

## API

| Method | Behavior |
| --- | --- |
| `path(file)` | Return the local absolute path or S3 key. |
| `write(file, data)` | Write string data. Returns `True` or `False`. |
| `read(file)` | Read string data. Raises `FileNotFoundError` when missing. |
| `exists(file)` | Return whether the file exists. |
| `remove(file)` | Delete a file. Returns `True` or `False`. |
| `move(source, destination)` | Move or rename a file. Returns `True` or `False`. |
| `list(path)` | Return files directly under a directory/prefix. |

## Usage

```python
from app import app

application = app()
storage = application.storage()

storage.write("reports/today.txt", "ready")

if storage.exists("reports/today.txt"):
    content = storage.read("reports/today.txt")
    application.log().info(content)

storage.move("reports/today.txt", "reports/archive/today.txt")
storage.remove("reports/archive/today.txt")
```

## Local Driver

The local driver stores files under `base_path / config.storage.disks.local.path`. In the generated project, that is `storage/app`.

Use relative paths in calls to `app.storage()` so code stays portable across Unix, Windows, and S3.

## S3 Driver

The S3 driver uses `boto3`. It supports an optional `prefix` and treats `None`, `null`, and empty values as no prefix.

Use moto-backed tests for unit coverage and real bucket tests only in a controlled integration environment.

## Guidance

- Prefer `app.storage()` over direct `open()` calls for application-managed files.
- Keep user input sanitized before using it as a storage path.
- Avoid absolute paths in storage calls.
- Run both local and S3 storage tests before upgrading `boto3`, `botocore`, or `moto`.
