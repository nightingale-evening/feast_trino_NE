
.PHONY: build

ROOT_DIR 	:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

format:
	# Sort
	cd ${ROOT_DIR}; python -m isort feast_trino/ tests/

	# Format
	cd ${ROOT_DIR}; python -m black --target-version py37 feast_trino tests

lint:
	cd ${ROOT_DIR}; python -m mypy feast_trino/ tests/
	cd ${ROOT_DIR}; python -m isort feast_trino/ tests/ --check-only
	cd ${ROOT_DIR}; python -m flake8 feast_trino/ tests/
	cd ${ROOT_DIR}; python -m black --target-version py37 --check feast_trino  tests

test:
	cd ${ROOT_DIR}; python -m pytest tests/

build:
	rm -rf dist/*
	python setup.py sdist bdist_wheel

install-ci-dependencies:
	pip install -e ".[ci]"

start-local-cluster:
	docker run --detach --rm -p 8080:8080 --name trino -v ${ROOT_DIR}/config/catalog/:/etc/catalog/:ro trinodb/trino:364
	sleep 15

kill-local-cluster:
	docker stop trino