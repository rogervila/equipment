---
sidebar_position: 6
---

# Storage Management

Equipment provides a clean and unified Filesystem API through its Storage component. It allows you to perform common file operations using a consistent interface, regardless of whether you are using local disk or cloud storage like Amazon S3.

## Configuration

Configure your storage disks in `config/storage.yaml`.

```yaml
storage:
  disk: ${STORAGE_DISK:local} # Options: local, s3

  disks:
    local:
        root: storage/app
    s3:
        bucket: ${S3_BUCKET}
        region: ${S3_REGION}
        access_key: ${S3_ACCESS_KEY}
        secret_key: ${S3_SECRET_KEY}
```

## Core API Methods

All methods return a boolean indicating success, except for `read()` (returns content string), `path()` (returns absolute path), and `list()` (returns a list of files).

| Method | Description | Example |
|--------|-------------|---------|
| `write(path, data)` | Write data to a file | `app.storage().write('report.txt', '...')` |
| `read(path)` | Read the content of a file | `content = app.storage().read('report.txt')` |
| `exists(path)` | Check if a file exists | `if app.storage().exists('report.txt'):` |
| `remove(path)` | Delete a file | `app.storage().remove('temp.txt')` |
| `move(src, dest)` | Move/Rename a file | `app.storage().move('old.txt', 'new.txt')` |
| `list(directory)` | List files in a directory | `files = app.storage().list('images/')` |
| `path(file)` | Get the absolute path | `abs_path = app.storage().path('data.csv')` |

## Usage Examples

```python
from app import app

app = app()
storage = app.storage()

# Writing a JSON file
import json
data = {"status": "ok", "version": "1.0"}
storage.write("config.json", json.dumps(data))

# Checking existence and reading
if storage.exists("config.json"):
    config_data = json.loads(storage.read("config.json"))
    print(config_data["version"])

# Listing all files in the root of the disk
for file in storage.list(""):
    print(f"Found file: {file}")
```

## S3 Implementation

When using the `s3` driver, Equipment uses `boto3` under the hood. The API remains identical to the local driver, making it easy to migrate your application to the cloud.

> [!NOTE]
> Make sure to install the `boto3` package if you plan to use the S3 driver.

## Best Practices

1. **Use Relative Paths**: Always use relative paths from the root of your disk. Equipment handles the prefixing for you.
2. **Abstract Your Storage**: Don't use `os.path` or `open()` directly for application files. Use `app.storage()` to ensure your code is portable across different environments.
3. **Handle Errors**: While the methods return `False` on failure, they might also raise exceptions for critical errors (like permissions). Use `try...except` when necessary.
