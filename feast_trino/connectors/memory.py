import pandas as pd

from feast_trino.connectors.utils import (
    CREATE_SCHEMA_QUERY_TEMPLATE,
    INSERT_ROWS_QUERY_TEMPLATE,
    format_pandas_row,
    get_trino_table_schema_from_dataframe,
    pandas_dataframe_fix_batches,
)
from feast_trino.trino_utils import Trino


def upload_pandas_dataframe_to_trino(
    client: Trino, df: pd.DataFrame, table_ref: str
) -> None:
    client.execute_query(
        CREATE_SCHEMA_QUERY_TEMPLATE.format(
            table_ref=table_ref, schema=get_trino_table_schema_from_dataframe(df=df)
        )
    )

    # Upload batchs of 1M rows at a time
    for batch_df in pandas_dataframe_fix_batches(df=df, batch_size=1000000):
        client.execute_query(
            INSERT_ROWS_QUERY_TEMPLATE.format(
                table_ref=table_ref,
                columns=",".join(batch_df.columns),
                values=format_pandas_row(batch_df),
            )
        )
