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

## Best Practices
- Always handle potential exceptions when performing file operations
- Use relative paths to maintain portability
- Implement proper error handling for file not found scenarios

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
