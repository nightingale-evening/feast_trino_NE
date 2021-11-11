from typing import Iterator

import pandas as pd
import pyarrow

from feast_trino.trino_type_map import pa_to_trino_value_type

CREATE_SCHEMA_QUERY_TEMPLATE = """
    CREATE TABLE IF NOT EXISTS {table_ref} (
    {schema}
)
"""

INSERT_ROWS_QUERY_TEMPLATE = """
    INSERT INTO {table_ref} ({columns})
    VALUES {values}
"""


def get_trino_table_schema_from_dataframe(df: pd.DataFrame) -> str:
    pyarrow_schema = pyarrow.Table.from_pandas(df).schema
    trino_schema = []
    for field in pyarrow_schema:
        try:
            trino_type = pa_to_trino_value_type(str(field.type))
        except KeyError:
            raise ValueError(
                f"Not supported type '{field.type}' in entity_df for '{field.name}'."
            )
        trino_schema.append((field.name, trino_type))

    return ",".join([f"{col_name} {col_type}" for col_name, col_type in trino_schema])


def pandas_dataframe_fix_batches(
    df: pd.DataFrame, batch_size: int
) -> Iterator[pd.DataFrame]:
    for pos in range(0, len(df), batch_size):
        yield df[pos : pos + batch_size]


def format_pandas_row(df: pd.DataFrame) -> str:
    def _format_value(value: str) -> str:
        if isinstance(value, str):
            return f"'{value}'"
        else:
            return f"{value}"

    results = []
    for row in df.values:
        results.append(f"({','.join([_format_value(v) for v in row])})")
    return ",".join(results)
