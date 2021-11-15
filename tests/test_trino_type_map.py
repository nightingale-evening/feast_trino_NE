import pyarrow as pa
import pytest

from feast_trino.trino_type_map import pa_to_trino_value_type, trino_to_pa_value_type


@pytest.mark.parametrize(
    "input_value,expected",
    [
        (pa.field("test", pa.null()), "null"),
        (pa.field("test", pa.bool_()), "boolean"),
        (pa.field("test", pa.date32()), "date"),
        (pa.field("test", pa.timestamp("us")), "timestamp"),
        (pa.field("test", pa.timestamp("us", tz="utc")), "timestamp with time zone"),
        (pa.field("test", pa.float32()), "decimal"),
        (pa.field("test", pa.float64()), "double"),
        (pa.field("test", pa.list_(pa.null())), "array['null']"),
        (pa.field("test", pa.list_(pa.bool_())), "array['boolean']"),
        (pa.field("test", pa.list_(pa.date32())), "array['date']"),
        (pa.field("test", pa.list_(pa.timestamp("us"))), "array['timestamp']"),
        (
            pa.field("test", pa.list_(pa.timestamp("us", tz="utc"))),
            "array['timestamp with time zone']",
        ),
        (pa.field("test", pa.list_(pa.float32())), "array['decimal']"),
        (pa.field("test", pa.list_(pa.float64())), "array['double']"),
    ],
)
def test_pa_to_trino_value_type(input_value, expected):
    assert pa_to_trino_value_type(str(input_value.type)) == expected


@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("Decimal(20, 0)", pa.float32()),
        ("Decimal(38, 0)", pa.float64()),
        ("Decimal(20,0)", pa.float32()),
        ("Decimal(38,0)", pa.float64()),
        ("timestamp", pa.timestamp("us")),
        ("timestamp with timezone", pa.timestamp("us")),
    ],
)
def test_trino_to_pa_value_type(input_value, expected):
    assert trino_to_pa_value_type(input_value) == expected
