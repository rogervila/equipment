---
sidebar_position: 1
---

# Installation Guide

## System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.12+
- **Package Manager**: pip (version 21.0+)

## Installation Methods

### 1. Install via pip (Recommended)

```bash
# Install Equipment globally
pip install equipment

# Alternatively, install in a virtual environment
python -m venv equipment-env
source equipment-env/bin/activate  # On Windows: equipment-env\Scripts\activate
pip install equipment
```

### 2. Create a New Project

```bash
# Generate a new Equipment project
equipment new my-app

# Navigate to the project directory
cd my-app

# Install project dependencies
pip install .
```

### 3. Verify Installation

```bash
# Run the main application
python main.py

# Check Equipment version
equipment --version
```

## Troubleshooting

### Common Installation Issues

1. **Python Version Compatibility**
   - Ensure you're using Python 3.12+
   - Check your Python version: `python --version`

2. **pip Installation Problems**
   ```bash
   # Upgrade pip to the latest version
   python -m pip install --upgrade pip
   ```
<!--
### Dependency Management

We recommend using `pipenv` for advanced dependency management:

```bash
# Install pipenv
pip install pipenv

# Create a new project with pipenv
pipenv --python 3.12
pipenv install equipment

# Activate the virtual environment
pipenv shell
```
-->

## Support

- **GitHub Issues**: [Report a problem](https://github.com/rogervila/equipment/issues)
- **Community Support**: [Discussions](https://github.com/rogervila/equipment/discussions)
