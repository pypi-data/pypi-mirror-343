# Legislative Converter

![UV](https://img.shields.io/badge/package%20manager-uv-purple)
![Ruff](https://img.shields.io/badge/code%20style-ruff-black)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![Mypy](https://img.shields.io/badge/types-mypy-blue)

A tool for converting New Zealand legislative documents from PDF to Markdown format. This isn't working yet we're just setting up the bones.

> [!NOTE]
> Keep this readme brief for now as we're in development - all details are to be kept in the `memory-bank/`, not here

## Overview

This project provides a tool for converting New Zealand legislative documents from PDF to Markdown format. It uses a LangGraph-based agent architecture to extract the structure and content of the documents, format them according to Markdown rules, and assemble the final Markdown document.

## Features

- Extract document structure from PDF files
- Extract content based on the structure map
- Format content according to Markdown rules
- Assemble the final Markdown document
- Preserve the hierarchical structure of the original document
- Handle special elements consistently

## Requirements

- Python 3.12
- UV for package management

## Installation

1. Clone the repository:

```sh
git clone https://github.com/shaneholloman/legislative-converter.git
cd legislative-converter
```

1. Set up the environment:

```sh
./scripts/setup-env.sh
```

1. Activate the environment:

```sh
source .venv/bin/activate
```

## Usage

```sh
python -m legislative_converter.main input.pdf -o output.md
```

### Options

- `-o, --output`: Path to the output Markdown file (default: input file with .md extension)
- `-v, --verbose`: Enable verbose output

## Development

### Running Tests

```sh
pytest
```

### Code Style

This project uses:

- Ruff for linting and formatting
- Mypy for static type checking

All code must have proper type annotations.

## License

MIT
