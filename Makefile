SHELL := /bin/bash

.PHONY: test lint build

test: build
	pytest

lint: build
	pylint $(shell git ls-files '*.py')

build:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .
