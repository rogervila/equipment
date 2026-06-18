---
sidebar_position: 9
---

# Project Compilation

Equipment provides a built-in `compile` command that prepares your project for distribution by converting Python files into bytecode (`.pyc`) and packaging all necessary assets into a single directory.

## Why Compile?

1. **Performance**: Bytecode files skip the compilation step when executed, leading to faster startup times.
2. **Obfuscation**: While not a security measure, bytecode is harder to read than source code, providing a basic level of protection for your logic.
3. **Clean Distribution**: Compiling creates a dedicated `dist` folder containing only what's needed to run the application, making deployment simpler.

## Usage

Run the `compile` command followed by the target directory name.

```bash
# Compile the project into the 'dist' folder
equipment compile dist
```

## How it Works

When you run the `compile` command, Equipment performs the following steps:

1. **Scans the Project**: It identifies all files in your current directory while respecting a set of default ignore patterns (like `.git`, `venv`, `__pycache__`, etc.).
2. **Converts Python Files**: Every `.py` file is compiled into a `.pyc` file using the `py_compile` module. The original `.py` files are **not** included in the output.
3. **Preserves Assets**: All non-Python files (YAML, JSON, INI, SQL, TXT, etc.) are copied exactly as they are to the target directory.
4. **Maintains Structure**: The directory hierarchy is perfectly preserved in the output directory.

## Deployment

After compilation, the `dist` folder is ready to be deployed.

```bash
# Navigate to the compiled project
cd dist

# Run the application (no .py files needed!)
python main.pyc
```

## Best Practices

1. **Compile before Release**: Always use the `compile` command before packaging your application for production.
2. **Verify the Output**: After compiling, run your tests or the main entry point within the `dist` folder to ensure everything was copied correctly.
3. **Keep it Clean**: Avoid compiling directly into your main project directory. Always use a dedicated output folder like `dist` or `build`.
