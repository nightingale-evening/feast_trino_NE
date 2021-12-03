import pandas as pd

from feast_trino.connectors.upload import upload_pandas_dataframe_to_trino


def test_base_case(client, trino_schema):
    table_ref = f"{trino_schema}.ci.my_df"
    client.execute_query(f"CREATE SCHEMA IF NOT EXISTS {trino_schema}.ci")
    client.execute_query(f"DROP TABLE IF EXISTS {table_ref}")

    input_df = pd.DataFrame(
        data={"id": [1, 2, 3], "value": [4, 5, 6], "str": ["a", "b", "c"]}
    )

    upload_pandas_dataframe_to_trino(
        client=client,
        df=input_df,
        table_ref=table_ref,
        connector_args={"type": "memory"},
    )

    actual_results = client.execute_query(f"SELECT * FROM {table_ref}")
    actual_df = pd.DataFrame(
        data=actual_results.data, columns=actual_results.columns_names
    )
    pd.testing.assert_frame_equal(input_df, actual_df)
