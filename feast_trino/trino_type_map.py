from typing import Dict

import pyarrow as pa

from feast import ValueType


def trino_to_feast_value_type(trino_type_as_str: str) -> ValueType:
    type_map: Dict[str, ValueType] = {
        "tinyint": ValueType.INT32,
        "smallint": ValueType.INT32,
        "int": ValueType.INT32,
        "integer": ValueType.INT32,
        "bigint": ValueType.INT64,
        "double": ValueType.DOUBLE,
        "decimal": ValueType.FLOAT,
        "timestamp": ValueType.UNIX_TIMESTAMP,
        "char": ValueType.STRING,
        "varchar": ValueType.STRING,
        "boolean": ValueType.BOOL,
    }
    return type_map[trino_type_as_str.lower()]


def pa_to_trino_value_type(pa_type_as_str: str) -> str:
    # PyArrow types: https://arrow.apache.org/docs/python/api/datatypes.html
    # Trino type: https://trino.io/docs/current/language/types.html
    pa_type_as_str = pa_type_as_str.lower()

    if pa_type_as_str.startswith("date"):
        return "date"

    if pa_type_as_str.startswith("decimal"):
        return pa_type_as_str

    if pa_type_as_str.startswith("dictionary<values=string,"):
        return "string"

    type_map = {
        "null": "null",
        "bool": "boolean",
        "int8": "tinyint",
        "int16": "smallint",
        "int32": "int",
        "int64": "bigint",
        "uint8": "smallint",
        "uint16": "int",
        "uint32": "bigint",
        "uint64": "bigint",
        "float": "decimal",
        "double": "double",
        "binary": "binary",
        "string": "varchar",
        "timestamp": "timestamp",
    }
    return type_map[pa_type_as_str]


_TRINO_TO_PA_TYPE_MAP = {
    "null": pa.null(),
    "boolean": pa.bool_(),
    "timestamp": pa.timestamp("us"),
    "date": pa.date32(),
    "tinyint": pa.int8(),
    "smallint": pa.int16(),
    "int": pa.int32(),
    "bigint": pa.int64(),
    "decimal": pa.float32(),
    "double": pa.float64(),
    "binary": pa.binary(),
    "char": pa.string(),
    "varchar": pa.string(),
}


def trino_to_pa_value_type(trino_type_as_str: str) -> pa.DataType:
    trino_type_as_str = trino_type_as_str.lower()
    return _TRINO_TO_PA_TYPE_MAP[trino_type_as_str]
