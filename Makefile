# Makefile for line-dog-bot 🐶

install:
	pip install -r requirements-dev.txt

test:
	PYTHONPATH=. pytest

format:
	black .

lint:
	ruff check . --fix

all: install format lint test
