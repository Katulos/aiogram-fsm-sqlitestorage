.DEFAULT_GOAL := help
.PHONY: deps help test

tests_dir := tests
examples_dir := examples
code_dir := $(package_dir) $(tests_dir) $(examples_dir)
reports_dir := htmlcov

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: clean
clean: # Clean up
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -name .pytest_cache`
	rm -rf *.egg-info
	rm -f report.html
	rm -f .coverage
	rm -rf {build,dist,site,.cache,.mypy_cache,.ruff_cache,reports}

.PHONY: deps
deps: clean # Install dependencies
	pip install -e ."[dev,test]" -U --upgrade-strategy=eager
	pre-commit install

.PHONY: test
test:  # Run tests
	pytest --cov=sqlitestorage --cov-config .coveragerc tests/

.PHONY: test-coverage
test-coverage:  # Run tests with coverage
	mkdir -p $(reports_dir)/tests/
	pytest --cov=aiogram --cov-config .coveragerc --html=$(reports_dir)/tests/index.html tests/
	coverage html -d $(reports_dir)/coverage
	coverage html -d $(reports_dir)/coverage


.PHONY: build
build: clean # Build package
	poetry build
