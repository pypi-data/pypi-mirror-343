# pypi2aur

**pypi2aur** is a command-line tool that helps you convert Python packages from PyPI into Arch Linux AUR PKGBUILD templates. It streamlines the process of packaging Python projects for the Arch User Repository, automating metadata extraction and template generation.

## Requirements
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for project management
- [requests](https://pypi.org/project/requests/) for HTTP requests
- [click](https://pypi.org/project/click/) for CLI

## Installation

1. Create a python virtual environment:

```bash
uv venv --python 3.13 # if you use uv
python -m venv .venv
```

2. Activate the Python Virtual Environment:
```bash
source .venv/bin/activate.fish
```
3. Install dependencies using uv:
```bash
uv sync
```

## Usage

After installing the dependencies and activating your virtual environment, you can use the `pypi2aur` CLI to generate and manage PKGBUILD files for Python packages from PyPI.

### Commands

- **create [PKG]**
  
  Generates a new PKGBUILD file for the specified PyPI package.
  
  **Usage:**
  ```bash
  pypi2aur create <package-name>
  ```
  
  - `<package-name>`: The name of the PyPI package to generate the PKGBUILD for.

- **update**
  
  Updates the existing PKGBUILD file in the current directory to match the latest version of the package on PyPI. The package name is read from the `pkgname` field in the PKGBUILD file.
  
  **Usage:**
  ```bash
  pypi2aur update
  ```

- **showdeps [PKG]**
  
  Displays the dependencies of the specified PyPI package as listed on PyPI.
  
  **Usage:**
  ```bash
  pypi2aur showdeps <package-name>
  ```
  
  - `<package-name>`: The name of the PyPI package to inspect.

### Example

```bash
# Create a PKGBUILD for the 'requests' package
pypi2aur create requests

# Update the PKGBUILD to the latest version
pypi2aur update

# Show dependencies for the 'requests' package
pypi2aur showdeps requests
```

All commands provide colorful output and helpful error messages. For more details, run any command with `--help`.

## Development

- All code uses static type hints and follows PEP8.
- Variable and function names use camelCase.
- Use `uv` for dependency management and virtual environments.

### Running Tests

```bash
uv pip install -r requirements-dev.txt
pytest
```

## Contributing

Contributions are welcome! Please open issues or pull requests. Follow the code style and naming conventions described above.

## License

MIT License. See [LICENSE](LICENSE) for details.
