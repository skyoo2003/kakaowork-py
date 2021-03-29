.PHONY: all setup install test test-watch lint typecheck build clean update-changelog

all: install test lint typecheck

setup:
	poetry run pre-commit install

install:
	poetry check
	poetry install

test:
	poetry run pytest -v -s $(filter-out $@, $(MAKECMDGOALS))

lint:
	poetry run flake8 kakaowork tests

typecheck:
	poetry run mypy kakaowork

build:
	poetry build

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf dist/ *.egg-info

update-changelog:
	poetry run towncrier --yes
