import sys

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
]
