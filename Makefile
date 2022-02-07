
.PHONY: build

ROOT_DIR 	:= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
FEAST_VERSION ?= v0.16.1
TRINO_VERSION ?= 364
VERSION 	:=$(shell cat VERSION)

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

test-python-universal:
	-mv ${ROOT_DIR}/tests ${ROOT_DIR}/tests_old
	-cd ${ROOT_DIR}; FULL_REPO_CONFIGS_MODULE=feast_trino.feast_tests FEAST_USAGE=False IS_TEST=True python -m pytest --integration --universal ${ROOT_DIR}/feast/sdk/python/tests/
	-mv ${ROOT_DIR}/tests_old ${ROOT_DIR}/tests

test-python-universal-ci:
	mv ${ROOT_DIR}/tests ${ROOT_DIR}/tests_old
	cd ${ROOT_DIR}; FULL_REPO_CONFIGS_MODULE=feast_trino.feast_tests FEAST_USAGE=False IS_TEST=True python -m pytest --integration --universal ${ROOT_DIR}/feast/sdk/python/tests
	mv ${ROOT_DIR}/tests_old ${ROOT_DIR}/tests

build:
	rm -rf dist/*
	python setup.py sdist bdist_wheel

release:
	git tag -m "Release v${VERSION}" v${VERSION}

install-feast-submodule:
	cd ${ROOT_DIR}; git submodule add --force https://github.com/feast-dev/feast.git feast
	cd ${ROOT_DIR}/feast; git fetch --all --tags
	cd ${ROOT_DIR}/feast; git reset --hard tags/${FEAST_VERSION}
	cd ${ROOT_DIR}/feast; pip install -e "sdk/python[ci]"
	-cd ${ROOT_DIR}; git rm --cached -f feast/ .gitmodules

install-ci-dependencies:
	pip install -e ".[ci]"

start-local-cluster:
	docker run --detach --rm -p 8080:8080 --name trino -v ${ROOT_DIR}/config/catalog/:/etc/catalog/:ro trinodb/trino:${TRINO_VERSION}
	sleep 15

kill-local-cluster:
	docker stop trino