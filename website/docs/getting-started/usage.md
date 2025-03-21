---
sidebar_position: 2
---

# 📚 Usage Guide

## Project Structure and Features

### Project Directory Overview

The project is organized into several key directories and files:

- `app/`: Contains the core application logic and components
- `config/`: Stores configuration files for different aspects of the application
- `database/`: Handles database-related operations and models
- `storage/`: Provides a flexible filesystem storage API
- `tests/`: Contains unit and integration tests
- `main.py`: Entry point of the application with helpful examples
- `scheduler.py`: Manages scheduled tasks
- `queues.py`: Handles task queuing
- `web.py`: Runs the web server

### Key Features

#### 1. Flexible Storage API
The project offers a simple and powerful filesystem storage API:
- Write files to storage
- Check file existence
- Read file contents
- List files
- Move and remove files

Example usage:
```python
# Write a file
app.storage().write('foo.txt', 'bar')

# Check if file exists
app.storage().exists('foo.txt')  # Returns True

# Read file contents
content = app.storage().read('foo.txt')  # Returns 'bar'
```

#### 2. Task Management
The project supports two primary task management methods:

##### Scheduled Tasks
Run scheduled tasks using:
```bash
$ py scheduler.py
```

##### Task Queuing
Enqueue and process background tasks:
```bash
$ py queues.py
```

#### 3. Web Server
Easily start a web server:
```bash
$ py web.py
```

### Getting Started
1. Install dependencies:
```bash
$ pipenv install
```

2. Explore the examples in `main.py` for more detailed usage instructions.

**Note**: Configuration details can be found in the respective YAML files within the `config/` directory.
