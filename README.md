# Mini

Max's INI (Mini) is a simple parser for the INI configuration format, implemented in Python.

# Installation

Create a Python virtual environment (venv)

```virtualenv .venv```

Activate venv

```source .venv/bin/activate```

Install mini in the virtual environment

```make build```

# Usage

The following command will convert a sample INI file to JSON

```mini --json tests/data/hello.ini```

For more information, run `mini --help`

# Development

Run pytest unit tests

```make test```
