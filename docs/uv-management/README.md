# uv - Fast Python Package Manager

`uv` is an extremely fast Python package manager written in Rust, providing a unified interface for managing Python projects, command-line tools, single-file scripts, and even Python itself.

## Installation

You can install `uv` using `pip` or via the official installation script.

### Option 1: Install via pip
If you already have Python and pip installed:
```bash
pip install uv
```

### Option 2: Install via script
This installs `uv` and sets up Python for you:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Commands Overview

### 1. Creating and Managing Projects

- **Initialize a new Python project**:
    ```bash
    uv init
    ```

- **Add dependencies to your project**:
    ```bash
    uv add "package_name>=version"
    ```
    Example:
    ```bash
    uv add "fastapi>=0.112"
    ```

- **Run commands in the project environment** (without needing to activate the virtual environment manually):
    ```bash
    uv run "command"
    ```
    Example:
    ```bash
    uv run uvicorn main:app --reload
    ```

- **Generate and sync lockfile for dependencies**:
    ```bash
    uv lock
    uv sync
    ```

### 2. Managing Command-Line Tools

- **Install command-line tools in isolated environments**:
    ```bash
    uv tool install tool_name
    ```
    Example:
    ```bash
    uv tool install ruff
    ```

- **Run one-off commands without explicit installation**:
    ```bash
    uvx tool_name
    ```
    Example:
    ```bash
    uvx ruff check
    ```

- **List installed tools**:
    ```bash
    uv tool list
    ```

- **Upgrade all installed tools**:
    ```bash
    uv tool upgrade --all
    ```

### 3. Python Installation and Management

- **Install a specific version of Python**:
    ```bash
    uv python install 3.12
    ```

- **Automatically manage Python versions as needed** (e.g., on `uv run`):
    ```bash
    uv run script.py
    ```

### 4. Single-File Python Scripts

You can manage standalone Python scripts with embedded dependencies directly inside the script.

- **Add dependencies to a script**:
    ```bash
    uv add --script script.py "package_name<version"
    ```
    Example:
    ```bash
    uv add --script main.py "requests<3" "rich"
    ```

- **Run a single-file script**:
    ```bash
    uv run script.py
    ```

- **Run a script with additional dependencies**:
    ```bash
    uv run --with "package_name" script.py
    ```

### 5. Workspaces

Manage multiple packages in the same repository using workspaces.

- **Define workspace members** in your `pyproject.toml`:
    ```toml
    [tool.uv.workspace]
    members = ["libraries/*"]
    ```

- **Run a command in a specific workspace member**:
    ```bash
    uv run --package package_name
    ```

## Documentation

For full documentation, visit the [official uv documentation](https://docs.astral.sh/uv/).
