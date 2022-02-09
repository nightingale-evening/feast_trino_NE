
.PHONY: build

ROOT_DIR               := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
FEAST_VERSION          ?= v0.16.1
TRINO_VERSION          ?= 364
PYPI_PASSWORD_SHOPIFY  ?= WRONG_PASSWORD
VERSION                := $(shell cat VERSION)
VERSION_TAG            := v${VERSION}
MOST_RECENT_TAG        := $(shell git describe --tags --abbrev=0)
DEFAULT_BRANCH         := main
GIT_BRANCH_NAME        := $(shell git rev-parse --abbrev-ref HEAD)

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
	cd ${ROOT_DIR}; rm -rf dist/*
	cd ${ROOT_DIR}; python setup.py sdist bdist_wheel

release:
	cd ${ROOT_DIR}; git tag -m "Release ${VERSION_TAG}" ${VERSION_TAG}
	cd ${ROOT_DIR}; git push --tags origin

unset-release:
	cd ${ROOT_DIR}; git tag -d ${VERSION_TAG} || true
	cd ${ROOT_DIR}; git push --delete origin ${VERSION_TAG} || true

publish:
ifndef PYPI_PASSWORD_SHOPIFY
	@echo "PYPI_PASSWORD_SHOPIFY environment variable missing"
	exit 1
endif
ifeq (${PYPI_PASSWORD_SHOPIFY}, WRONG_PASSWORD)
	@echo "Ask your lead to get access to PYPI_PASSWORD_SHOPIFY"
	exit 1
endif
ifneq (${GIT_BRANCH_NAME}, ${DEFAULT_BRANCH})
	@echo "You can only publish a new package if you are on the ${DEFAULT_BRANCH} branch"
	exit 1
endif
ifneq (${VERSION_TAG}, ${MOST_RECENT_TAG})
	@echo "The version present in VERSION is different than the most recent version tag"
	exit 1
endif

	cd ${ROOT_DIR}; git checkout tags/${VERSION_TAG}
	make build
	cd ${ROOT_DIR}; twine upload -u shopify -p ${PYPI_PASSWORD_SHOPIFY} dist/* || true
	cd ${ROOT_DIR}; git checkout main

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