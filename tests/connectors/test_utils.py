import pandas as pd
import pytest

from feast_trino.connectors.utils import (
    format_datetime,
    format_pandas_row,
    pandas_dataframe_fix_batches,
    pyarrow_schema_from_dataframe,
    trino_table_schema_from_dataframe,
)


@pytest.fixture
def input_df():
    return pd.DataFrame(
        data={
            "id": [1, 2, 3],
            "str_value": ["a", "b", "c"],
            "int_value": [4, 5, 6],
            "float_value": [7.0, 8.0, 9.0],
            "datetime_value": pd.to_datetime(
                ["2021-01-01", "2021-01-02", "2021-01-03"]
            ),
        }
    )


def test_pyarrow_schema_from_dataframe(input_df):
    assert pyarrow_schema_from_dataframe(df=input_df) == {
        "id": "bigint",
        "str_value": "varchar",
        "int_value": "bigint",
        "float_value": "double",
        "datetime_value": "timestamp",
    }


def test_trino_table_schema_from_dataframe(input_df):
    assert (
        trino_table_schema_from_dataframe(df=input_df)
        == "id bigint,str_value varchar,int_value bigint,float_value double,datetime_value timestamp"
    )


def test_pandas_dataframe_fix_batches(input_df):
    input_df = input_df.append([input_df] * 50, ignore_index=True)

    assert len(input_df) == 153
    for i, _ in enumerate(pandas_dataframe_fix_batches(df=input_df, batch_size=100)):
        pass
    assert i == 1


def test_format_pandas_row(input_df):
    assert (
        format_pandas_row(df=input_df[:1])
        == "(1,'a',4,7.0,TIMESTAMP '2021-01-01 00:00:00.000000')"
    )


def test_format_datetime():
    assert format_datetime(pd.to_datetime("2021-01-01")) == "2021-01-01 00:00:00.000000"
    assert (
        format_datetime(pd.to_datetime("2021-01-01").tz_localize("EST"))
        == "2021-01-01 05:00:00.000000"
    )
