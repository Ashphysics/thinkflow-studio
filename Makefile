.PHONY: build run test audit clean

build:
	docker-compose build

run:
	docker-compose up

run-detached:
	docker-compose up -d

stop:
	docker-compose down

test:
	pytest tests/

audit:
	ruff check .
	mypy .
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
