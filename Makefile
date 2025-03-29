# Makefile for line-dog-bot 🐶

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=. pytest

format:
	black .

lint:
	ruff check .

all: install format lint test
