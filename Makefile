SHELL := /bin/bash

.PHONY: test lint build type-check

test: build
	pytest

type-check: build
	mypy --strict --package mini

lint: build
	pylint --source-roots . $(shell git ls-files '*.py')

build:
	pip install -r requirements.txt
	pip install -e .
