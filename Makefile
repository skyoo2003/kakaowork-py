.PHONY: all setup install test lint typecheck build clean docs update-changelog

all: install test lint typecheck

setup:
	poetry run pre-commit install

install:
	poetry check
	poetry install -E cli

test:
	poetry run pytest -v -s $(filter-out $@, $(MAKECMDGOALS))

lint:
	poetry run flake8 kakaowork tests
	poetry run pydocstyle kakaowork

typecheck:
	poetry run mypy kakaowork

build:
	poetry build

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf dist *.egg-info .mypy_cache .pytest_cache .report .tox .coverage

docs:
	poetry run make clean html -C docs

update-changelog:
	poetry run towncrier --yes
