import pytest

from feast_trino.trino_utils import Trino

HOST = "localhost"
PORT = "8080"
TEST_SCHEMA = "memory"


@pytest.fixture
def trino_schema():
    return TEST_SCHEMA


@pytest.fixture
def client():
    return Trino(user="user", catalog=TEST_SCHEMA, host=HOST, port=PORT)
