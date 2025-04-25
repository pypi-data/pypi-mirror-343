# UV-Native Workflow

This document outlines the strict UV-native workflow for the RepoDex project. We **exclusively** use UV commands for all Python-related operations.

## Core Principles

1. **NEVER** use pip commands under any circumstances
2. **ALWAYS** use native UV commands
3. Zero tolerance for pip-based workflows

## Strict Rules

- **PROHIBITED**: Any command containing the string "pip" (e.g., `pip install`, `uv pip install`, etc.)
- **PROHIBITED**: Any reference to pip in documentation, comments, or code
- **PROHIBITED**: Any tools or libraries that internally use pip
- **REQUIRED**: All Python package operations must use native UV commands

## UV Command Reference

### Package Installation

```sh
# Install a package globally
uv install <package-name>

# Install a package as a development tool
uv tool install <package-name>

# Install packages from requirements.txt
uv sync
```

### Package Building and Publishing

```sh
# Build a package
uv build

# Publish a package to PyPI
uv publish --token "<your-token>"
```

### Virtual Environment Management

```sh
# Create and sync a virtual environment
uv sync

# Run a command in the virtual environment
.venv/bin/python script.py
```

## Publishing Workflow

The following is the **only** acceptable workflow for building and publishing the RepoDex package:

1. Update version in `repodex/__init__.py` and `pyproject.toml`
2. Build the package:
   ```sh
   uv build
   ```
3. Publish to PyPI:
   ```sh
   uv publish --token "<your-token>"
   ```
4. Verify installation:
   ```sh
   uv tool install repodex
   repodex --version
   ```

## Enforcement

These rules are non-negotiable and strictly enforced. Any pull request or contribution that violates these rules will be automatically rejected.

## Rationale

UV provides a modern, faster, and more reliable Python packaging experience. By standardizing on UV-native commands, we ensure consistent behavior across all development environments and eliminate the issues associated with pip-based workflows.
