---
sidebar_position: 1
---

# Installation Guide

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.12+ (latest stable recommended)
- **Package Manager**: pip (version 21.0+)

## Installation Methods

### 1. Install via pip (Recommended)

For most users, installing Equipment globally or in a specialized tool environment (like `pipx`) is the easiest way to access the `equipment` command.

```bash
# Install Equipment globally
pip install equipment
```

#### Using a Virtual Environment

It is highly recommended to use a virtual environment for your projects to manage dependencies cleanly.

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS and Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install Equipment in the virtual environment
pip install equipment
```

### 2. Create a New Project

Once Equipment is installed, you can use the CLI to scaffold a new project.

```bash
# Generate a new Equipment project
equipment new my-app

# Navigate to the project directory
cd my-app

# Install project dependencies in editable mode
# This installs the dependencies defined in pyproject.toml
pip install .
```

### 3. Verify Installation

After installation and project creation, verify that everything is working as expected.

```bash
# Check the Equipment CLI version
equipment --version

# Run the main entry point of your newly created project
python main.py
```

## Advanced Dependency Management

### Using `pipenv`

If you prefer `pipenv` for dependency management:

```bash
# Install pipenv
pip install pipenv

# Create a new project with pipenv
pipenv --python 3.12
pipenv install equipment

# Activate the virtual environment
pipenv shell
```

### Using `poetry`

Equipment is also compatible with `poetry`:

```bash
# Initialize a poetry project
poetry init
poetry add equipment

# Enter the virtual environment
poetry shell
```

## Troubleshooting

### Common Installation Issues

1. **Python Version Compatibility**
   - **Issue**: `equipment` requires Python 3.12+.
   - **Solution**: Check your Python version: `python --version`. If it's lower than 3.12, upgrade your Python installation.

2. **Command Not Found**
   - **Issue**: After installing with `pip`, the `equipment` command is not recognized.
   - **Solution**: Ensure that your Python scripts directory is in your system's `PATH`. This is common when installing without a virtual environment.

3. **pip Installation Problems**
   - **Solution**: Upgrade pip to the latest version:
     ```bash
     python -m pip install --upgrade pip
     ```

## Support

- **GitHub Issues**: [Report a problem](https://github.com/rogervila/equipment/issues)
- **Community Support**: [Discussions](https://github.com/rogervila/equipment/discussions)
