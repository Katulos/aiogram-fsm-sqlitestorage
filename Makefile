.DEFAULT_GOAL := help
.PHONY: deps help test

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build
	rm -fr dist
	rm -fr .eggs
	rm -fr .ruff_cache
	rm -fr .mypy_cache
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache

deps:  ## Install dependencies
	python -m pip install -r requirements-test.txt

test:  ## Run tests
	pytest
