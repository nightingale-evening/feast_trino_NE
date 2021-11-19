# Feast Trino Support

Trino is not included in current [Feast](https://github.com/feast-dev/feast) roadmap, this project intends to add Trino support for Offline Store.  

## Todo List
- [DONE, none] ~~Create the open source repo~~
- [Done, none] First stab at the Trino plugin
- [Done, none] Add the ability to upload a pandas dataframe
- [Done, none] Pass all integration tests and release a first version of Trino
- [TODO, none] Add another connector like Hive
- [TODO, v0.1.0-beta] Publish a beta release in Pypi

## Version compatibilities
Here is how the current feast-trino plugin has been tested

| Feast-trino | Python | Feast  | Trino |
|-------------|--------|--------|-------|
| Beta        | 3.7    | 0.15.1 | 364   |

## Quickstart

#### Install feast-trino

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

set `offline_store` type to be `feast_trino.TrinoOfflineStore`

```yaml
project: ...
registry: ...
provider: local
offline_store:
    type: feast_trino.TrinoOfflineStore
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
git clone https://github.com/shopify/feast-trino.git
cd feast-trino
# creating virtual env ...
python -v venv venv/
source venv/bin/activate

make build

# before commit
make format
make lint
```

#### Testing unit test

```shell
make start-local-cluster
make test
make kill-local-cluster
```

__Note: You can visit http://localhost:8080/ui/ to access the Web UI of Trino. This makes it easy to look for queries.__

#### Testing against Feast universal suite

```shell
make install-feast-submodule
make start-local-cluster
make test-python-universal
make kill-local-cluster
```

#### Using different versions of Feast or Trino
The [makefile](./Makefile) contains the following default values:
- FEAST_VERSION: v0.15.1
- TRINO_VERSION: 364

Thus, `make install-feast-submodule` will automatically compile Feast `v0.15.1`. If you want to try another version like `v0.14.1`, you just need to run `make install-feast-submodule FEAST_VERSION=v0.14.1`

Same applies for TRINO_VERSION when you start the local cluster `make start-local-cluster TRINO_VERSION=XXX`