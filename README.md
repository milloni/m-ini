# Mini

Max's INI (Mini) is a simple parser for the INI configuration format, implemented in Python.

## Installation

Create a Python virtual environment (venv)

```bash
virtualenv .venv
```

Activate venv

```bash
source .venv/bin/activate
```

Install mini in the virtual environment

```bash
make build
```

## Usage

The following command will convert a sample INI file to JSON

```bash
mini --json tests/data/hello.ini
```

For more information, run

```bash
mini --help
```

## Development

Run pytest unit tests

```bash
make test
```
