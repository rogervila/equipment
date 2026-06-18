---
sidebar_position: 6
---

# Storage

Equipment provides a storage abstraction with local filesystem and S3-compatible drivers. Application code can call the same methods regardless of the configured disk.

Use storage for application-managed files: generated reports, uploads, exports, temporary artifacts, cache files, and files that may move from local disk to S3 later.

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
| `list(path)` | Return files directly under a directory or prefix. |

Pass relative paths. Avoid leading slashes, drive letters, and user-controlled `..` segments.

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

## Structured Data

Storage methods read and write strings. Serialize structured data explicitly:

```python
import json

payload = {"status": "ready", "count": 3}
application.storage().write("reports/status.json", json.dumps(payload))

loaded = json.loads(application.storage().read("reports/status.json"))
```

For binary files, encode data before writing or extend the storage abstraction in your application.

## Local Driver

The local driver stores files under `base_path / config.storage.disks.local.path`. In the generated project, that is `storage/app`.

Local storage is a good default for:

- local development;
- tests;
- single-machine scripts;
- generated files that do not need to be shared across servers.

Do not use local storage for horizontally scaled production apps unless every process sees the same shared filesystem.

## S3 Driver

The S3 driver uses `boto3`. It supports an optional `prefix` and treats `None`, `null`, and empty values as no prefix.

S3 storage is useful for:

- user uploads;
- generated exports;
- shared files across workers and web servers;
- environments without persistent local disks.

Example environment:

```env
FILESYSTEM_DISK=s3
S3_ENDPOINT=https://s3.example.com
S3_BUCKET=my-app-files
S3_ACCESS_KEY=...
S3_SECRET_KEY=...
S3_REGION=eu-west-1
S3_PREFIX=production
```

With `S3_PREFIX=production`, `write("reports/a.txt", "data")` writes to `production/reports/a.txt`.

## Path Safety

Do not pass untrusted raw user input directly as a storage path. Normalize it or generate your own filenames:

```python
safe_name = uploaded_filename.replace("/", "_").replace("\\", "_")
path = f"uploads/{user_id}/{safe_name}"
application.storage().write(path, content)
```

For stronger guarantees, generate filenames with UUIDs or database IDs.

## Error Handling

`write`, `remove`, and `move` return booleans. Check them when failure matters:

```python
if not application.storage().write(path, content):
    application.log().error("Could not write file", extra={"path": path})
    raise RuntimeError("Storage write failed")
```

`read` raises `FileNotFoundError` when a file is missing. Handle that separately when missing files are expected.

## Atomicity And Concurrency

The storage abstraction does not guarantee atomic writes, locks, version checks, or compare-and-swap behavior. If concurrent writes matter, add application-level coordination, database records, object versioning, or a queue.

For local storage, `move()` uses filesystem rename semantics. For S3, `move()` is implemented as copy then delete.

## Testing Storage

Use the local driver and a temporary base path for most tests. Use moto for S3 unit coverage. Keep real bucket tests separate from fast unit tests and protect them with explicit environment variables.

Test both success and failure paths:

- write then read;
- missing read;
- nested directory writes;
- move into a nested path;
- list files without listing subdirectories;
- S3 prefix handling.

## Troubleshooting

File is written to an unexpected directory:

Check `FILESYSTEM_DISK`, `config/storage.yaml`, and the application base path.

S3 key has an unexpected prefix:

Check `S3_PREFIX`. Values `None`, `null`, and empty string mean no prefix.

Local storage works but S3 does not:

Check endpoint, region, bucket, credentials, and network access. Then verify credentials with a small S3 integration test.

`FileNotFoundError` from `read()`:

Check the active disk, base path, and relative file path.

## Guidance

- Prefer `app.storage()` over direct `open()` calls for application-managed files.
- Keep user input sanitized before using it as a storage path.
- Avoid absolute paths in storage calls.
- Serialize non-string data explicitly.
- Design production storage around shared persistence when running multiple processes.
- Run both local and S3 storage tests before upgrading `boto3`, `botocore`, or `moto`.
