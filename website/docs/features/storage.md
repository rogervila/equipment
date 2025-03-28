---
sidebar_position: 1
---

# Storage
The Storage API provides a robust and intuitive interface for filesystem operations. It abstracts away complex file handling, offering simple methods for common file-related tasks.

## Core Methods

| Method | Description | Example |
|--------|-------------|---------|
| `write(path, content)` | Write content to a file | `app.storage().write('reports/daily.txt', 'Sales report data')` |
| `read(path)` | Read file contents | `report_content = app.storage().read('reports/daily.txt')` |
| `exists(path)` | Check file existence | `if app.storage().exists('reports/daily.txt'):` |
| `list(directory)` | List files in a directory | `files = app.storage().list('reports/')` |
| `move(source, destination)` | Move a file | `app.storage().move('reports/daily.txt', 'archives/daily.txt')` |
| `remove(path)` | Delete a file | `app.storage().remove('archives/old_report.txt')` |

## Disk Configurations

The Storage API supports multiple disk types for flexible file storage:

### Local Disk
The local disk stores files on the server's filesystem. It's ideal for development and small-scale applications.

- **Path**: Configurable local directory (default: `storage/app`)
- **Use Case**: Local development, testing, and small file storage needs

### S3 Disk
The S3 disk provides cloud-based storage using Amazon S3 or compatible object storage services.

- **Configuration**:
  - `endpoint`: S3-compatible storage service URL
  - `bucket`: S3 bucket name
  - `access_key`: Authentication credentials
  - `secret_key`: Authentication credentials
  - `region`: Optional AWS region (defaults to 'auto')
  - `prefix`: Optional path prefix within the bucket

- **Note**: S3 works with any S3 compatible provider, like Cloudflare R2, MinIO, etc.

### Switching Disk Configuration

You can easily switch between disk types using environment variables or configuration files:

```yaml
storage:
  disk: ${FILESYSTEM_DISK:local}  # Defaults to 'local', can be set to 's3'
```

This flexibility allows you to:
- Use local storage during development
- Seamlessly migrate to cloud storage in production
- Support multiple storage backends without code changes

## Advanced Usage Example
```python
report = {
    'title': 'Daily Sales Report',
    'data': {
        'total_sales': 123456,
        'total_profit': 123456
    }
}

# Write report
if not app.storage().write('report.json', json.dumps(report)):
    raise Exception('Failed to write report')

# ...

# Read report
if app.storage().exists('report.json'):
    loaded_report = json.loads(app.storage().read('report.json'))

    # Let's assume we have a Reports service with a validate method
    app.reports().validate(loaded_report)
```

## Best Practices
- Always handle potential exceptions when performing file operations
- Use relative paths to maintain portability
- Implement proper error handling for file not found scenarios
