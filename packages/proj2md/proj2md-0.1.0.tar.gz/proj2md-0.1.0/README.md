# proj2md

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/proj2md.svg)](https://pypi.org/project/proj2md)
[![Python Versions](https://img.shields.io/pypi/pyversions/proj2md.svg)](https://pypi.org/project/proj2md)

proj2md is a command-line tool that generates a comprehensive Markdown document
for any project directory. It traverses files, extracts structure and contents,
and outputs a self-descriptive `.md` file ideal for LLM ingestion or static documentation.

## Features

- Recursive directory traversal with extension filtering
- Optional ASCII tree view of the project structure
- Automatic table of contents with anchors
- YAML front-matter with project metadata (name, version, author, date)
- Modes:
  - `light`: only tree + existing README
  - `full`: complete extraction of all files
- List of dependencies from `pyproject.toml` or `poetry`
- Customizable snippet length (`--max-snippet-lines`)
- Exclusion patterns for files/folders (`--exclude`)
- Easy installation via `pip` and entry-point `proj2md`

## Installation

Requires Python 3.13 or higher.

Install from PyPI:

```bash
pip install proj2md
```

Or install locally from source:

```bash
git clone https://github.com/yourusername/proj2md.git
cd proj2md
pip install .
```

## Usage

Basic usage (note that the actual file will be prefixed with `generated_`):

Note: regardless of the name provided via `--output-file`, the output
file will be prefixed with `generated_` to avoid self-inclusion.
  
Basic usage:

```bash
proj2md --input-dir ./my_project --output-file ./project.md
```

Available options:

```bash
--input-dir, -i PATH        Root directory (default: .)
--output-file, -o FILE      Output Markdown file (default: project.md)
--with-tree / --no-tree     Include project tree (default: with-tree)
--with-deps / --no-deps     Include dependencies list (default: with-deps)
--extensions, -e EXT1,EXT2  Comma-separated extensions (default: .py,.md,.yaml,.json)
--mode [light|full]         Extraction mode (default: full)
--max-snippet-lines N       Limit lines per file snippet
--exclude, -x PAT1,PAT2     Comma-separated ignore patterns
```

## Examples

Full extraction with tree and dependencies:

```bash
proj2md -i ./src -o docs/project_full.md --with-tree --with-deps --mode full
```

Light mode (only tree + README):

```bash
proj2md -i ./src -o docs/project_light.md --no-deps --no-tree --mode light
```

## Development

A `Taskfile.yaml` is provided to simplify common development workflows.
Install the [Task runner](https://taskfile.dev/) (`task` command), then run:

```bash
# Setup development environment (venv, dependencies, pre-commit)
task setup-dev

# Run the test suite
task run-tests

# Run code formatting and linting
task linter

# Clean build artifacts and cache
task clean
```

To list all available tasks:

```bash
task --list
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing.

## Code of Conduct

This project adheres to the [Contributor Covenant](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
