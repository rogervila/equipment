---
sidebar_position: 99
---

# Project Compilation

## Compile Command

The `equipment compile <path>` command is used to compile the entire project into a `<path>` directory. This process involves:

- Converting all Python (`.py`) files to compiled Python (`.pyc`) files
- Preserving all non-Python files in their original structure
- Creating a complete, ready-to-distribute version of the project

### Usage

```bash
# compile into the ./dist directory
equipment compile dist
```

### Compilation Details

- **Python Files**: Converted to bytecode (`.pyc`) for faster execution
- **Non-Python Files**: Copied as-is to maintain project structure
- **Output Directory**: All compiled files are placed in the `<path>` folder

This command is useful for:
- Creating a distributable version of your project
- Improving initial load times by pre-compiling Python files
- Preparing the project for deployment or sharing
