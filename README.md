# Feast Trino Support

Trino is not included in current [Feast](https://github.com/feast-dev/feast) roadmap, this project intends to add Trino support for Offline Store.  

## Todo List
- [DONE, none] ~~Create the open source repo~~
- [IN PROGRESS, none] First stab at the Trino plugin
- [TODO, none] Add the ability to upload a pandas dataframe
- [TODO, v0.1.0] Pass all integration tests and release a first version of Trino

## Quickstart

#### Install feast

```shell
pip install feast
```

#### Install feast-hive

- Install stable version

```shell
pip install feast-trino
```

- Install develop version (not stable):

```shell
pip install git+https://github.com/shopify/feast-trino.git 
```

#### Create a feature repository

```shell
feast init feature_repo
cd feature_repo
```

#### Edit `feature_store.yaml`

set `offline_store` type to be `feast_hive.TrinoOfflineStore`

```yaml
project: ...
registry: ...
provider: local
offline_store:
    type: feast_hive.TrinoOfflineStore
    host: localhost
    port: 8080
    user: feast
    catalog: default
online_store:
    type: sqlite
    path: .tmp/database.db
```

#### Create Trino Table
<!-- TODO -->

#### Edit `example.py`

```python
# This is an example feature definition file

from google.protobuf.duration_pb2 import Duration

from feast import Entity, Feature, FeatureView, ValueType
from feast_trino import TrinoSource

# Read data from Trino table
# Here we use a Query to reuse the original parquet data, 
# but you can replace to your own Table or Query.
driver_hourly_stats = TrinoSource(
    query = """
    SELECT Timestamp(cast(event_timestamp / 1000000 as bigint)) AS event_timestamp, 
           driver_id, conv_rate, acc_rate, avg_daily_trips, 
           Timestamp(cast(created / 1000000 as bigint)) AS created 
    FROM feast.driver_stats
    """,
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created",
)

# Define an entity for the driver.
driver = Entity(name="driver_id", value_type=ValueType.INT64, description="driver id", )

# Define FeatureView
driver_hourly_stats_view = FeatureView(
    name="driver_hourly_stats",
    entities=["driver_id"],
    ttl=Duration(seconds=86400 * 1),
    features=[
        Feature(name="conv_rate", dtype=ValueType.FLOAT),
        Feature(name="acc_rate", dtype=ValueType.FLOAT),
        Feature(name="avg_daily_trips", dtype=ValueType.INT64),
    ],
    online=True,
    input=driver_hourly_stats,
    tags={},
)
```

#### Apply the feature definitions

```shell
feast apply
```

#### Generating training data and so on

The rest are as same as [Feast Quickstart](https://docs.feast.dev/quickstart#generating-training-data)


## Developing and Testing

#### Developing

```shell
git clone https://github.com/baineng/feast-trino.git
cd feast-trino
# creating virtual env ...
pip install -e ".[dev]"

# before commit
make format
make lint
```

#### Testing

```shell
pip install -e ".[test]"
pytest -n 6 --host=localhost --port=8080 --user=feast --catalog=default
```
