import sys


from .connectors.utils import (
    pyarrow_schema_from_dataframe,
    trino_table_schema_from_dataframe,
    pandas_dataframe_fix_batches,
    format_pandas_row,
    format_datetime,
)
from .connectors.upload import upload_pandas_dataframe_to_trino
from .trino import TrinoOfflineStore, TrinoOfflineStoreConfig
from .trino_source import TrinoOptions, TrinoSource

if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

__version__ = metadata.version("feast_trino")

__all__ = [
    "TrinoOptions",
    "TrinoSource",
    "TrinoOfflineStoreConfig",
    "TrinoOfflineStore",
    "pyarrow_schema_from_dataframe",
    "trino_table_schema_from_dataframe",
    "pandas_dataframe_fix_batches",
    "format_pandas_row",
    "format_datetime",
    "upload_pandas_dataframe_to_trino",
]
